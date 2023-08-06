# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2020 ifm electronic gmbh
#
# THE PROGRAM IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND.
#
import logging
import numpy as np
import cv2
from scipy import optimize

logger = logging.getLogger(__name__)

def find_transformation(world, imgpoints, invIC, fixed_translation, binning, camRefToOpticalSystem, optMode):
    '''
    Estimates a rotation r, and translation t such that
        inverse_intrinsic_projection(R.T*(world - t)) approx. imgpoints

    :param world: 3xn points in world coordinates
    :param imgpoints: 2xn points in image coordinates corresponding to world
    :param invIC: inverse intrinsic calibration
    :param fixed_translation: either a vector containing the fixed camera position or None
    :param binning: whether binning should be applied to the calibration
    :param camRefToOpticalSystem: internal transformation between head reference and optical system
    :param optMode: must be either "lsq" (use scipy least square optimization) or "min" (use scipy minimization)
    :return: r=[rotX, rotY, rotZ], t=[transX, transY, transZ], MSE
    '''
    assert world.shape[0] == 3, 'world must be 3xn, but is {}'.format(world.shape)
    assert imgpoints.shape[0] == 2, 'imgpoints must be 2xn, but is {}'.format(imgpoints.shape)
    assert imgpoints.shape[1] == world.shape[1], 'imgpoints and world must have the same number of points'

    def cost(rt, fixed_translation, world, imgpoints, mode):
        if fixed_translation is None:
            r, t = rt[:3], rt[3:]
        else:
            r, t = rt, fixed_translation
        world2cam = project(world, r, t, inverse=True)
        # z must be positive
        if np.any(world2cam[2, :] <= 0):
            logger.warning("z <= 0")
            nz = world2cam[2, world2cam[2, :] <= 0]
            return np.sum(nz ** 2) * 1e10
        cam = inverse_intrinsic_projection(world2cam, invIC, binning, camRefToOpticalSystem)
        if mode == "lsq":
            return np.linalg.norm(cam - imgpoints, axis=0)
        elif mode == "min":
            return np.mean(np.linalg.norm(cam - imgpoints, axis=0)**2)
        elif mode == "minabs":
            return np.mean(np.abs(np.linalg.norm(cam - imgpoints, axis=0)))
        raise RuntimeError("unknown mode %s" % mode)

    # find starting value
    r, t = PnP(world, imgpoints, invIC, binning)
    r = np.array(r)
    t = np.array(t)
    logger.debug("PnP result: r=%s t=%s", r, t)
    # optimize brute force
    if fixed_translation is None:
        x0 = np.array([r, t]).flatten()
    else:
        x0 = np.array(r).flatten()
        
    if optMode == "lsq":
        opt = optimize.least_squares(cost, x0, args=(fixed_translation, world, imgpoints, optMode))
        r = opt.x[:3]
        t = opt.x[3:] if fixed_translation is None else fixed_translation
        rms = np.sqrt(np.mean(opt.fun**2))
        rms_unit = "rms"
    elif optMode in ["min", "minabs"]:
        opt = optimize.minimize(cost, x0, args=(fixed_translation, world, imgpoints, optMode))
        r = opt.x[:3]
        t = opt.x[3:] if fixed_translation is None else fixed_translation
        if optMode == "min":
            rms = np.sqrt(opt.fun)
            rms_unit = "rms"
        else:
            rms = opt.fun
            rms_unit = "mae"

    assert np.all(project(world, r, t, inverse=True)[2, :] > 0), 'z values must be positive'
    return r, t, rms, rms_unit


def PnP(world, image, invIC, binning):
    """
    Calls cv2.solvePnP with all invIC parameters translated to openCV. The result can be used as 
    an initial estimate of the calibration
    
    :param world: 3xN world coordinates of the inner corners
    :param image: 2xN image coordinates of the inner corners
    :param invIC: inverse intrinsic calibration
    :param binning: flag indicating whether the image coordinates are binned
    :return: r=[rotX, rotY, rotZ], t=[transX, transY, transZ]
    """
    fb = 0.5 if binning else 1.0

    assert invIC["modelID"] == 1
    fx, fy, mx, my, alpha, k1, k2, k3, k4, k5 = invIC["modelParameters"][:10]

    cameraMatrix = np.array([
        [fx * fb, 0, mx * fb],
        [0, fy * fb, my * fb],
        [0, 0, 1],
    ])

    # opencv uses different variable names:
    # https://docs.opencv.org/2.4/doc/tutorials/calib3d/camera_calibration/camera_calibration.html
    distCoeff = np.array([k1, k2, k3, k4, k5])

    retval, rvec, t = cv2.solvePnP(world.T, image.T, cameraMatrix, distCoeff)
    R, _ = cv2.Rodrigues(rvec)
    # algo expects cam -> world transformation
    r = rotMatReverse(R.T)
    t = -R.T.dot(t.squeeze())
    return r, t


def project(data, r, t, inverse=False):
    '''
    :return: R.dot(data) + t if inverse=False else R.T.dot(data - t)
    '''
    if inverse:
        return rotMat(*r).T.dot(data - np.array(t)[..., np.newaxis])
    else:
        return rotMat(*r).dot(data) + np.array(t)[..., np.newaxis]


def rotMat(*rot_xyz):
    '''
    :return: rotation matrix from rotX, rotY, rotZ
    '''
    R = np.eye(3)
    for i, alpha in enumerate(rot_xyz):
        lr = np.eye(3)
        lr[(i + 1) % 3, (i + 1) % 3] = np.cos(alpha)
        lr[(i + 2) % 3, (i + 2) % 3] = np.cos(alpha)
        lr[(i + 1) % 3, (i + 2) % 3] = -np.sin(alpha)
        lr[(i + 2) % 3, (i + 1) % 3] = np.sin(alpha)
        R = R.dot(lr)
    return R


def rotMatReverse(R):
    '''
    :return:rotX, rotY, rotZ from a rotation matrix R
    '''
    alpha = np.arctan2(R[1, 2], R[2, 2])
    c2 = np.sqrt(R[0, 0] ** 2 + R[0, 1] ** 2)
    beta = np.arctan2(-R[0, 2], c2)
    s1 = np.sin(alpha)
    c1 = np.cos(alpha)
    gamma = np.arctan2(s1 * R[2, 0] - c1 * R[1, 0], c1 * R[1, 1] - s1 * R[2, 1])
    rotX, rotY, rotZ = -alpha, -beta, -gamma
    if rotX < -np.pi / 2 or rotX > np.pi / 2:
        if rotX < 0:
            rotX += np.pi
        else:
            rotX -= np.pi
        rotY = np.pi - rotY
        if rotY < -np.pi:
            rotY += 2 * np.pi
        if rotY > np.pi:
            rotY -= 2 * np.pi
        rotZ = rotZ + np.pi
        if rotZ > np.pi:
            rotZ -= 2 * np.pi
    return rotX, rotY, rotZ


def inverse_intrinsic_projection(camXYZ, invIC, binning, camRefToOpticalSystem):
    '''
    3D points to pixel coordinates
    :param camXYZ: 3xn camera coordinates
    :param invIC: inverse intrinsic calibration
    :param internalTransRot: (forward) internal TransRot
    :return: 2xn pixel coordinates
    '''

    # reverse internalTransRot
    r = np.array(camRefToOpticalSystem["rot"])
    t = np.array(camRefToOpticalSystem["trans"])
    P = project(camXYZ, r, t, inverse=True)

    X = P[0, :]
    Y = P[1, :]
    Z = P[2, :]

    ixn = X / np.maximum(0.001, Z)
    iyn = Y / np.maximum(0.001, Z)

    # apply distortion
    fb = 0.5 if binning else 1.0
    assert invIC["modelID"] == 1
    fx, fy, mx, my, alpha, k1, k2, k3, k4, k5 = invIC["modelParameters"][:10]

    rd2 = ixn ** 2 + iyn ** 2
    radial = rd2 * (k1 + rd2 * (k2 + rd2 * k5)) + 1
    ixd = ixn * radial
    iyd = iyn * radial
    if k3 != 0 or k4 != 0:
        h = 2 * ixn * iyn
        tangx = k3 * h + k4 * (rd2 + 2 * ixn ** 2)
        tangy = k3 * (rd2 + 2 * iyn ** 2) + k4 * h
        ixd += tangx
        iyd += tangy

    # transform to imager
    ix = ((fx * fb * (ixd + alpha * iyd)) + mx * fb) - 0.5
    iy = ((fy * fb * (iyd)) + my * fb) - 0.5

    return np.vstack([ix, iy])

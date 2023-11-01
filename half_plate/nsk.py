import math
import numpy as np
from basic.earth_intersection import earth_intersection
from src import w_z

#находим центр и направляющие векторы НСК в ИСК,
def nsk(O1, K1, KSC, a0, b0, R):
    nsk_center_plate = KSC.transpose().dot([0, 0, 0]) + K1
    nsk_x_plate = KSC.transpose().dot([-b0, 0, 0]) + K1
    nsk_y_plate = KSC.transpose().dot([0, a0, 0]) + K1
    dir = O1 - nsk_center_plate
    dir = dir / np.linalg.norm(dir)
    tmp = min(earth_intersection(nsk_center_plate, dir, R)[0], earth_intersection(nsk_center_plate, dir, R)[1])
    nsk_center = nsk_center_plate + tmp * dir

    D_coeff = -np.dot(nsk_center, nsk_center)
    dir = O1 - nsk_x_plate
    dir = dir / np.linalg.norm(dir)
    tmp = -(np.dot(nsk_x_plate, nsk_center) + D_coeff) / (np.dot(dir, nsk_center))
    nsk_x = nsk_x_plate + tmp * dir

    dir = O1 - nsk_y_plate
    dir = dir / np.linalg.norm(dir)
    tmp = -(np.dot(nsk_y_plate, nsk_center) + D_coeff) / (np.dot(dir, nsk_center))
    nsk_y = nsk_y_plate + tmp * dir
    nsk_ox = []
    for i in range(3):
        nsk_ox.append(nsk_x[i] - nsk_center[i])
    nsk_ox = nsk_ox / np.linalg.norm(nsk_ox)
    nsk_oy = []
    for i in range(3):
        nsk_oy.append(nsk_y[i] - nsk_center[i])
    nsk_oy = nsk_oy / np.linalg.norm(nsk_oy)
    nsk_oz = []
    for i in range(3):
        nsk_oz.append(nsk_center[i])
    nsk_oz = nsk_oz / np.linalg.norm(nsk_oz)
    NSK = np.array([nsk_ox, nsk_oy, nsk_oz])
    norms = np.linalg.norm(NSK, axis=0)
    NSK = NSK / norms
    return nsk_center, NSK, nsk_x
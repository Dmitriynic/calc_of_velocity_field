import numpy as np
import math
from src import w_z

def extra_roll_angle(nsk_center, nsk_x, NSK, O1, ang_dir_par, mode, yaw_angle, t_2, R):
    nsk_x = np.linalg.inv(NSK.transpose()).dot(np.array([nsk_x[0], nsk_x[1], nsk_x[2]])) - np.linalg.inv(NSK.transpose()).dot(nsk_center)
    if ang_dir_par > 0:
        nsk_delta_y = -w_z * math.sin(ang_dir_par) * t_2 * R
    else:
        nsk_delta_y = w_z * math.sin(ang_dir_par) * t_2 * R
    if mode != 'HALF_PLATE':
        if yaw_angle > 0:
            nsk_delta_y -= 2*nsk_x[1]
        else:
            nsk_delta_y += 2*nsk_x[1]
    delta_y = NSK.transpose().dot([0, nsk_delta_y, 0]) + nsk_center
    delta_y_vec = [delta_y[i] - O1[i] for i in range(3)]
    nsk_center_vec = [nsk_center[i] - O1[i] for i in range(3)]
    dot_product = delta_y_vec[0] * nsk_center_vec[0] +  delta_y_vec[1] * nsk_center_vec[1] +  delta_y_vec[2] * nsk_center_vec[2]
    vector1_length = math.sqrt(delta_y_vec[0]**2 + delta_y_vec[1]**2 + delta_y_vec[2]**2)
    vector2_length = math.sqrt(nsk_center_vec[0]**2 + nsk_center_vec[1]**2 + nsk_center_vec[2]**2)
    addit_roll_angle = math.acos(round(dot_product / (vector1_length * vector2_length), 15))
    if nsk_delta_y > 0:
        return addit_roll_angle
    else:
        return -addit_roll_angle
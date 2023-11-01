import numpy as np
import math

def angle_dir_parallel(x_rv, y_rv, nsk_x, NSK, nsk_center):
    nsk_x_1 = nsk_x
    dir_par = np.array([1, -x_rv/y_rv, 0])
    angle_dir_par =  math.acos((nsk_x_1[0] - nsk_center[0] + (nsk_x_1[1] - nsk_center[1])* dir_par[1]) / (math.sqrt((nsk_x_1[0] - nsk_center[0])**2 + (nsk_x_1[1] - nsk_center[1])**2 + (nsk_x_1[2] - nsk_center[2])**2)*math.sqrt(dir_par[0]**2 + dir_par[1]**2)))
    if angle_dir_par > math.pi/2:
       angle_dir_par = math.pi - angle_dir_par
    if nsk_x[2] - nsk_center[2] < 0:
        angle_dir_par = -angle_dir_par
    return angle_dir_par
    
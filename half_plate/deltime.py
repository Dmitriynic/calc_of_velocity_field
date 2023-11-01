import math
from src import w_z

def deltime(nsk_center, nsk_x_surface, angle_between_NSKs, mode, ang_dir_par, n_0, R):
    delta = math.sqrt((nsk_center[0] - nsk_x_surface[0])**2 + (nsk_center[1] - nsk_x_surface[1])**2 + (nsk_center[2] - nsk_x_surface[2])**2)
    if mode != 'HALF_PLATE':
        t_2 = 2 * math.asin((delta*math.cos(angle_between_NSKs))/R) / (n_0 - w_z * math.cos(ang_dir_par))
    else:
        t_2 = 2 * math.asin(delta / R) / (n_0-w_z * math.cos(ang_dir_par))
    return t_2
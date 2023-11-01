import math
import numpy as np

def angle_between_NSKs(nsk_x, NSK, nsk_center):
    nsk_x = np.linalg.inv(NSK.transpose()).dot(np.array([nsk_x[0], nsk_x[1], nsk_x[2]])) - np.linalg.inv(NSK.transpose()).dot(nsk_center)
    alpha = math.acos((nsk_x[0] * 1 + nsk_x[1] * 0)/ (math.sqrt(nsk_x[0]**2 + nsk_x[1]**2)))
    return alpha
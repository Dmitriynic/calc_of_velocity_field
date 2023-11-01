import math
import numpy as np
from basic.earth_intersection import earth_intersection
from src import w_z

def calculate_earth_point(O1, K1, KSC, coords_plane2, e_point, delta_t, R):
    for it in range(len(coords_plane2)):
        point_in_KSC = KSC.transpose().dot(np.array([coords_plane2[it][0], coords_plane2[it][1], 0])) + K1  #Координаты точки в КСК
        dir = O1 - point_in_KSC
        dir = dir / np.linalg.norm(dir)
        tmp = min(earth_intersection(point_in_KSC, dir, R)[0], earth_intersection(point_in_KSC, dir, R)[1])
        e_p = point_in_KSC + tmp * dir
        if delta_t == 0:
            e_point.append(e_p)
        if tmp != 0 and delta_t !=0:
            α_1 = w_z * delta_t #Угол поворота земли за время экспозиции(или другое заданное время)
            e_point.append([math.cos(α_1) * e_p[0] - math.sin(α_1) * e_p[1], math.sin(α_1) * e_p[0] + math.cos(α_1) * e_p[1], e_p[2]])
    return e_point
import numpy as np
from src import V_x, V_y

def result_speed(O1_new, K1_new, KSC_new, coords_plane2, e_point, delta_t):
    V_x = []
    V_y = []
    vec_norm = O1_new - K1_new
    vec_norm = vec_norm / np.linalg.norm(vec_norm)
    for it in range(min(len(coords_plane2), len(e_point))):
        D_coefficient = -np.dot(vec_norm, K1_new) #Коэффициент D из уравнения фокальной плоскости
        dir = O1_new - e_point[it]              #Направляющий вектор
        dir = dir / np.linalg.norm(dir)
        tmp = -(np.dot(e_point[it], vec_norm) + D_coefficient) / (np.dot(dir, vec_norm))
        e_point[it] = e_point[it] + tmp * dir
        V = np.linalg.inv(KSC_new.transpose()).dot(e_point[it]) - np.linalg.inv(KSC_new.transpose()).dot(K1_new)
        V_x.append((V[0] - coords_plane2[it][0])/delta_t)
        V_y.append((V[1] - coords_plane2[it][1])/delta_t)
    return [V_x, V_y]
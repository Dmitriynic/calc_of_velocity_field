import numpy as np
from scipy import integrate
from src import coords_x, coords_y

#отличия от calc_min_field, что не нужно высчитать лишь 1 из 3ех параметров
def calc_transverse_comp(a0, b0, n0, m0, coords_plane2, coords_2, V_x, V_y, V_x_2, V_y_2, num):
    coords_x = []
    coords_y = []
    for i in range(n0*num): #первый индекс по y, вторая по x
        for j in range(m0):
            coords_2[i][j] = coords_plane2[i * m0 + j]
            V_x_2[i][j] = V_x[i * m0 + j]
            V_y_2[i][j] = V_y[i * m0 + j]
    u_y = 0
    #метод симпсона используем scipy.integrate.simpson
    #для вычисления повторного интеграла
    for it in range(num):
        coords_x = []
        coords_y = []
        for j in range(m0):
            coords_x.append(coords_2[it*n0][j][0])
        for j in range(n0):
            coords_y.append(coords_2[j+it*n0][0][1])
        Iy = [x for x in range(m0)] 
        delty = [x for x in range(n0)]
        u_y = 0
        for j in range(m0):
            for k in range(n0):
                delty[k] = V_y_2[k+it*n0][j]# - coords_y[k]
            Iy[j] = integrate.simpson(delty, coords_y)
        u_y += 1 / (4 * a0 * b0) * integrate.simpson(Iy, coords_x)

    #print("Поперечная составляющая:", u_y)
    return u_y
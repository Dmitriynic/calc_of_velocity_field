import math
import numpy as np
from scipy import integrate
from src import coords_x, coords_y

#вычисления угла и вектора для минимизации поля скоростей
def min_field(a0, b0, n0, m0, l0, coords_plane2, V_x, V_y, num):
    w_t = 0
    u_x = 0
    u_y = 0
    for it in range(num):   #метод симпсона используем scipy.integrate.simpson
        coords_x = []       #для вычисления повторного интеграла
        coords_y = []
        for j in range(m0):
            coords_x.append(coords_plane2[it*n0*m0 + j][0])
        for j in range(n0):
            coords_y.append(coords_plane2[(j+it*n0)*m0][1])

        Ip = [x for x in range(m0)]
        deltp = [x for x in range(n0)]
        for j in range(m0):
            for k in range(n0):
                deltp[k] = V_y[(k+it*n0)*m0 + j] * coords_plane2[(k+it*n0)*m0 + j][0] - V_x[(k+it*n0)*m0+j] * coords_plane2[(k+it*n0)*m0+j][1]
            Ip[j] = integrate.simpson(deltp, coords_y)
        w_t += 3 / (4*((a0) ** 3 * b0 + (b0)**3 * a0)) * integrate.simpson(Ip, coords_x)

        Ix = [x for x in range(n0)]
        deltx = [x for x in range(m0)]
        u_x = 0
        for j in range(n0):
            for k in range(m0):
                deltx[k] = V_x[(j+it*n0)*m0 + k]
            Ix[j] = integrate.simpson(deltx, coords_x)
        u_x += 1 / (4 * a0 * b0) * integrate.simpson(Ix, coords_y)

        Iy = [x for x in range(m0)] 
        delty = [x for x in range(n0)]
        u_y = 0
        for j in range(m0):
            for k in range(n0):
                delty[k] = V_y[(k+it*n0)*m0+j]
            Iy[j] = integrate.simpson(delty, coords_y)
        u_y += 1 / (4 * a0 * b0) * integrate.simpson(Iy, coords_x)

    print("Оптимальная компенсирующая угловая скорость вращения ПЗС-линейки(1/c):", w_t)
    print("Компоненты вектора скорости смещения центра ПЗС-линейки:", V_x[l0], V_y[l0])
    print("Компоненты оптимального компенсирующего вектора:", u_x, u_y)
    print("Среднеквадратическое значение длины вектора ПЗС-линейки", math.sqrt(u_x**2 + u_y**2))
    return [w_t, u_x, u_y]
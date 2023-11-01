import numpy as np
import math
import matplotlib.pyplot as plt
from min_field.min_field import min_field
from src import V_x_old, V_y_old, V_x_alpha, V_y_alpha, V_x_new_no_alpha, V_y_new_no_alpha, V_x_new, V_y_new

def field_image(a0, b0, n0, m0, n1, m1, l0, V_x, V_y, u_x, u_y, w_t, coords_plane2, scale_prm, num, delta_t, coords_2): #число микросхем в пластине
    n0 = num*n0
    n1 = num*n1
    if num > 1:
        m1 = m1*2
        a0 = a0*num + n1/2
        b0 = b0*2 + m1
        l0 = int((n0*m0-1)/2)
    #print(coords_plane2)
    if num > 1:
        fig = plt.figure(figsize = (3, 6), dpi=200, num = 1)
        fig.subplots_adjust(left=0.05, right=0.97, bottom=0.06, top=0.99)
    else:
        fig = plt.figure(num = 1)
    ax = fig.add_subplot()
    ticks_x = np.linspace(-b0, b0, m0)
    ticks_y = np.linspace(-a0, a0, n0)
    ax.set_xticks(ticks_x)
    ax.set_yticks(ticks_y)
    ax.tick_params(axis='y', length = 3, width = 0.3, labelsize=5)
    ax.tick_params(axis='x', length = 3, width = 0.3, labelsize=3.5)
    [i.set_linewidth(0.4) for i in ax.spines.values()] #изменение ширины subplot
    # ax.tick_params(axis='both', which='minor', labelsize=1)
    V_x_old = []
    V_y_old = []
    for it in range(len(V_x)):
        V_x_old.append(V_x[it])# - V_x[l0])
        V_y_old.append(V_y[it])# - V_y[l0])
    #построение поля смещения до минимизации с учетом вычета вектора центра прямоугольника
    #масштабирование картинки
    len_coords_0 = math.sqrt(V_x_old[0] ** 2 + V_y_old[0] ** 2)
    len_coords_1 = math.sqrt(V_x_old[m0-1] ** 2 + V_y_old[m0-1] ** 2)
    len_coords_2 = math.sqrt(V_x_old[len(coords_plane2) - m0 + 1] ** 2 + V_y_old[len(coords_plane2) - m0 + 1] ** 2)
    len_coords_3 = math.sqrt(V_x_old[len(coords_plane2) - 1] ** 2 + V_y_old[len(coords_plane2) - 1] ** 2)
    len_coords = (len_coords_0 + len_coords_1 + len_coords_2 + len_coords_3) / 4

    for it in range(len(V_x)):
        #ax.quiver(coords_plane2[it][0], coords_plane2[it][1], V_x_old[it] - coords_plane2[it][0], V_y_old[it] - coords_plane2[it][1],  angles = 'xy', scale_units = 'xy', width = 0.0025, scale = len_coords / scale_prm)#scale = len_coords / 0.008)#scale=0.00032 и 0.000042)
        ax.quiver(coords_plane2[it][0], coords_plane2[it][1], V_x_old[it], V_y_old[it],  angles = 'xy', scale_units = 'xy', width = 0.0025, scale = len_coords / scale_prm)#scale = len_coords / 0.008)#scale=0.00032 и 0.000042)
    if num>1:
        ax.grid(color = 'green', linewidth = 0.3)
    else:
        ax.grid(color = 'green')
    ax.set_aspect('equal')
    ax.set_aspect(abs((b0/a0*num)))
    ax.set_xlabel('OX, дм', fontsize = 8)
    ax.set_ylabel('OY, дм', fontsize = 8)
    if num > 1:
        plt.xlim([-(b0 + m1), b0 + m1])
        plt.ylim([-(a0 + n1/num), a0 + n1/num])
    else:
        plt.xlim([-(b0 + 3 * m1), b0 + 3 * m1])
        plt.ylim([-(a0 + 3 * n1), a0 + 3 * n1])

    #построение поля смещения после вычисления результата минимизации
    if num > 1:
        fig1 = plt.figure(figsize = (3, 6), dpi=200, num = 2)
        fig1.subplots_adjust(left=0.05, right=0.97, bottom=0.06, top=0.99)
    else:
        fig1 = plt.figure(num = 2)
    ax1 = fig1.add_subplot()
    ticks_x = np.linspace(-b0, b0, m0)
    ticks_y = np.linspace(-a0, a0, n0)
    ax1.set_xticks(ticks_x)
    ax1.set_yticks(ticks_y)
    if num > 1:
        ax1.tick_params(axis='y', length = 3, width = 0.3, labelsize=5)
        ax1.tick_params(axis='x', length = 3, width = 0.3, labelsize=3.5)
    else:
        ax1.tick_params(axis='y', length = 3, width = 0.3, labelsize=10)
        ax1.tick_params(axis='x', length = 3, width = 0.3, labelsize=8)
    [i.set_linewidth(0.4) for i in ax1.spines.values()] #изменение ширины subplot

    V_x_alpha = []
    V_y_alpha = []
    #также вычислим поле с учетом вычета вектора центра прямоугольника
    for it in range(len(V_x)):
        V_x_alpha.append(V_x[it] - V_x[l0])
        V_y_alpha.append(V_y[it] - V_y[l0])

    #также вычислим поле с учетом вычета оптимального компенсирующего вектора, но не учитывая опитмальный угол вращения ПЗС-линейки
    for it in range(len(V_x)):
        V_x_new_no_alpha.append(V_x[it] - u_x)
        V_y_new_no_alpha.append(V_y[it] - u_y)

    for it in range(len(V_x)):
        x = V_x[it]
        y = V_y[it]
        V_x[it] = x* math.cos(w_t*delta_t) + y * math.sin(w_t*delta_t)
        V_y[it] = -x * math.sin(w_t*delta_t) + y * math.cos(w_t*delta_t)

    #также вычислим поле с учетом вычета вектора центра прямоугольника  и поворота на оптимальный угол вращения ПЗС-линейки
    for it in range(len(V_x)):
        V_x_alpha.append(V_x[it] - V_x[l0])
        V_y_alpha.append(V_y[it] - V_y[l0])

    V_x_new = []
    V_y_new = []
    for it in range(len(V_x)):
        V_x_new.append(V_x[it] - u_x)
        V_y_new.append(V_y[it] - u_y)

    #print('V(0, 0) = ', math.sqrt(V_x[len(V_x) - 1] ** 2 + V_y[0] ** 2))
    w_t_none, u_x_new, u_y_new = min_field(a0, b0, n0, m0, l0, coords_plane2, V_x_new, V_y_new, num)
    print('Среднеквадратичное значение длины вектора ПЗС-линейки', math.sqrt(u_x_new ** 2 + u_y_new ** 2))
    DV = []
    for i in range(len(V_x)):
        #DV.append(math.sqrt((V_x_new[i] - coords_plane2[i][0]) ** 2 + (V_y_new[i] - coords_plane2[i][1]) ** 2))
        DV.append(math.sqrt(V_x_new[i] ** 2 + V_y_new[i]** 2))
    print('Максимальное значение длины вектора ПЗС-линейки', max(DV))
    #масштабирование картинки
    len_coords_0 = math.sqrt(V_x_new[0] ** 2 + V_y_new[0] ** 2)
    len_coords_1 = math.sqrt(V_x_new[m0-1] ** 2 + V_y_new[m0-1] ** 2)
    len_coords_2 = math.sqrt(V_x_new[len(coords_plane2) - m0 + 1] ** 2 + V_y_new[len(coords_plane2) - m0 + 1] ** 2)
    len_coords_3 = math.sqrt(V_x_new[len(coords_plane2) - 1] ** 2 + V_y_new[len(coords_plane2) - 1] ** 2)
    len_coords = (len_coords_0 + len_coords_1 + len_coords_2 + len_coords_3) / 4

    for it in range(len(V_x)):
        #ax1.quiver(coords_plane2[it][0], coords_plane2[it][1], (V_x_new[it] - coords_plane2[it][0])/delta_t, (V_y_new[it] - coords_plane2[it][1])/delta_t,  angles = 'xy', scale_units = 'xy', width = 0.0015, scale = len_coords / scale_prm)#scale = len_coords / 0.008)#scale=0.00032 и 0.000042)
        ax1.quiver(coords_plane2[it][0], coords_plane2[it][1], V_x_new[it], V_y_new[it],  angles = 'xy', scale_units = 'xy', width = 0.0015, scale = len_coords / scale_prm)#scale = len_coords / 0.008)#scale=0.00032 и 0.000042)
    # print("Сумма длин векторов поля смещений с учетом вычета вектора центра ПЗС-линейки:", l1)
    # print("Сумма длин векторов поля смещений с учетом вычета вектора центра ПЗС-линейки и оптимального угла вращения:", l2)
    # print("Сумма длин векторов поля смещений с учетом вычета оптимального компенсирующего вектора, но без учета угла:", l3)
    # print("Сумма длин векторов поля смещений после минимизации:", l4)
    ax1.set_aspect(abs((b0/a0*num)))
    if num > 1:
        ax1.grid(color = 'green', linewidth = 0.3)
        ax1.set_xlabel('OX, мм', fontsize = 8)
        ax1.set_ylabel('OY, мм', fontsize = 8)
        plt.xlim([-(b0 + m1), b0 + m1])
        plt.ylim([-(a0 + n1/num), a0 + n1/num])
    else:
        ax1.grid(color = 'green', linewidth = 0.2)
        ax1.set_xlabel('OX, мм', fontsize = 12)
        ax1.set_ylabel('OY, мм', fontsize = 12)
        plt.xlim([-(b0 + 8 * m1), b0 + 3 * m1])
        plt.ylim([-(a0 + 2 * n1), a0 + 3 * n1])

    return max(DV)
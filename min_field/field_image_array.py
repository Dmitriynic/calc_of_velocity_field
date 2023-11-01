import numpy as np
import math
import matplotlib.pyplot as plt
from src import V_x_old, V_y_old, V_x_alpha, V_y_alpha, V_x_new_no_alpha, V_y_new_no_alpha, V_x_new, V_y_new, mx_arr

from min_field.min_field import min_field

def field_image_array(a0, b0, n0, m0, n1, m1, l0, V_x, V_y, u_x, u_y, w_t, coords_plane2, scale_prm, num, k, delta_t, mode, pix_len, t_2_arr, coords_2, t_0): #число микросхем в пластине
    t_2_sum = np.sum(t_2_arr)
    V_x_old_arr = [[]]
    V_y_old_arr = [[]]
    V_x_new_arr = [[]]
    V_y_new_arr = [[]]
    n0_new = num*n0
    n1_new = num*n1
    if num >= 1:
        m1_new = m1*2
        a0_new = a0*num + n1_new/2
        b0_new = b0*2 + m1
        l0 = int((n0*m0-1)/2)
    else:
        m1_new = m1
        a0_new = a0
        b0_new = b0
    if num > 1:
        fig = plt.figure(figsize = (3, 6), dpi=200)
        fig.subplots_adjust(left=0.05, right=0.97, bottom=0.06, top=0.99)
    else:
        fig = plt.figure()
    ax = fig.add_subplot()
    ticks_x = np.linspace(-b0_new, b0_new*k, m0)
    ticks_y = np.linspace(-a0_new, a0_new, n0_new)
    ax.set_xticks(ticks_x)
    ax.set_yticks(ticks_y)
    ax.tick_params(axis='y', length = 3, width = 0.3, labelsize=5)
    ax.tick_params(axis='x', length = 3, width = 0.3, labelsize=3.5)
    [i.set_linewidth(0.4) for i in ax.spines.values()] #изменение ширины subplot
    for i in range(k):
        V_x_old = []
        V_y_old = []
        for it in range(len(V_x[0])):
            V_x_old.append(V_x[i][it])# - V_x[l0])
            V_y_old.append(V_y[i][it])# - V_y[l0])
        V_x_old_arr.append(V_x_old)
        V_y_old_arr.append(V_y_old)
    V_x_old_arr.remove([])
    V_y_old_arr.remove([])
    len_coords_0 = math.sqrt(V_x_old_arr[0][0] ** 2 + V_y_old_arr[0][0] ** 2)
    len_coords_1 = math.sqrt(V_x_old_arr[0][m0-1] ** 2 + V_y_old_arr[0][m0-1] ** 2)
    len_coords_2 = math.sqrt(V_x_old_arr[0][len(coords_plane2) - m0 + 1] ** 2 + V_y_old_arr[0][len(coords_plane2) - m0 + 1] ** 2)
    len_coords_3 = math.sqrt(V_x_old_arr[0][len(coords_plane2) - 1] ** 2 + V_y_old[len(coords_plane2) - 1] ** 2)
    len_coords = (len_coords_0 + len_coords_1 + len_coords_2 + len_coords_3) / 4
    for i in range(k):
        if i % 2 == 0:
            for it in range(len(V_x[0])):
                #ax.quiver(coords_plane2[it][0] + i*b0_new, coords_plane2[it][1], V_x_old_arr[i][it] - coords_plane2[it][0], V_y_old_arr[i][it] - coords_plane2[it][1],  angles = 'xy', scale_units = 'xy', width = 0.0015, scale = len_coords / scale_prm, color = 'red')#scale = len_coords / 0.008)#scale=0.00032 и 0.000042)
                ax.quiver(coords_plane2[it][0] + i*b0_new, coords_plane2[it][1], V_x_old_arr[i][it], V_y_old_arr[i][it],  angles = 'xy', scale_units = 'xy', width = 0.0025, scale = len_coords / scale_prm, color = 'red')
        else:
            for it in range(len(V_x[0])):
                ax.quiver(coords_plane2[it][0] + i*b0_new, coords_plane2[it][1], V_x_old_arr[i][it], V_y_old_arr[i][it],  angles = 'xy', scale_units = 'xy', width = 0.0025, scale = len_coords / scale_prm, color = 'blue')
    if num>1:
        ax.grid(color = 'green', linewidth = 0.3)
    else:
        ax.grid(color = 'green')
    ax.set_aspect('equal')
    ax.set_aspect(abs((b0_new/a0_new*num)))
    if num > 1:
        ax.set_xlabel('OX, дм', fontsize = 5)
        ax.set_ylabel('OY, дм', fontsize = 3.5)
        plt.xlim([-(b0_new + m1_new), b0_new*(k+1) + m1_new])
        plt.ylim([-(a0_new + n1), a0_new + n1])
    else:
        ax.set_xlabel('OX, дм', fontsize = 8)
        ax.set_ylabel('OY, дм', fontsize = 8)
        plt.xlim([-(b0_new + m1_new), b0_new + 4 * m1_new])
        plt.ylim([-(a0_new + 3 * n1_new), a0_new + 3 * n1_new])
    plt.show()
    #построение поля смещения после вычисления результата минимизации
    if num > 1:
        fig1 = plt.figure(figsize = (3, 6), dpi=200)
        fig1.subplots_adjust(left=0.05, right=0.97, bottom=0.06, top=0.99)
    else:
        fig1 = plt.figure()
    ax1 = fig1.add_subplot()
    ticks_x = np.linspace(-b0_new, b0_new*k, m0)
    ticks_y = np.linspace(-a0_new, a0_new, n0_new)
    ax1.set_xticks(ticks_x)
    ax1.set_yticks(ticks_y)
    if num > 1:
        ax1.tick_params(axis='y', length = 3, width = 0.3, labelsize=5)#5
        ax1.tick_params(axis='x', length = 3, width = 0.3, labelsize=5)#
    else:
        ax1.tick_params(axis='y', length = 3, width = 0.3, labelsize=8)#5
        ax1.tick_params(axis='x', length = 3, width = 0.3, labelsize=8)#
    [i.set_linewidth(0.4) for i in ax1.spines.values()] #изменение ширины subplot

    if mode == 'FIELD_SAVE':
        root_square_saved = []
        root_square_tip = []
        maxes_saved = []
        maxes_saved_tip = []
        j = 0
        for i in range(k):
            V_x_new = []
            V_y_new = []
            V_x_new_saved = []
            V_y_new_saved = []
            mx_new = []
            mx_new_saved = []
            for it in range(len(V_x[0])):
                x = V_x[i][it]* math.cos(w_t[j]*delta_t) + V_y[i][it] * math.sin(w_t[j]*delta_t)
                y = -V_x[i][it] * math.sin(w_t[j]*delta_t) + V_y[i][it] * math.cos(w_t[j]*delta_t)
                V_x_new_saved.append(x - u_x[j])
                V_y_new_saved.append(y - u_y[j])
                mx_new_saved.append(math.sqrt(V_x_new_saved[it]**2 + V_y_new_saved[it]**2))
                x = V_x[i][it]* math.cos(w_t[i]*delta_t) + V_y[i][it] * math.sin(w_t[i]*delta_t)
                y = -V_x[i][it] * math.sin(w_t[i]*delta_t) + V_y[i][it] * math.cos(w_t[i]*delta_t)
                V_x_new.append(x - u_x[i])
                V_y_new.append(y - u_y[i])
                mx_new.append(math.sqrt(V_x_new[it]**2 + V_y_new[it]**2))
            maxes_saved.append(max(mx_new_saved))
            maxes_saved_tip.append(max(mx_new))
            V_x_new_arr.append(V_x_new_saved)
            V_y_new_arr.append(V_y_new_saved)
            w_t_none, u_x_saved, u_y_saved = min_field(a0, b0, n0, m0, l0, coords_plane2, V_x_new_saved, V_y_new_saved, num)
            w_t_none, u_x_tip, u_y_tip = min_field(a0, b0, n0, m0, l0, coords_plane2, V_x_new, V_y_new, num)
            root_square_saved.append(math.sqrt(u_x_saved**2+u_y_saved**2))
            root_square_tip.append(math.sqrt(u_x_tip**2 + u_y_tip**2))
        for i in range(k):
            if (root_square_saved[i] - root_square_tip[i])*delta_t > pix_len:
                print('Количество кадров, для которых можно сохранить результаты минимизации, средние векторы', i)
                break
        for i in range(k):
            if (maxes_saved[i] - maxes_saved_tip[i])*delta_t > pix_len:
                print('Количество кадров, для которых можно сохранить результаты минимизации, макс векторы', i)
                break
        V_x_new_arr.remove([])
        V_y_new_arr.remove([])
        fig4 = plt.figure(figsize = (3, 6), dpi=200)
        ax4 = fig4.add_subplot()
        ax4.set_xlabel('Время, c', fontsize = 7)
        ax4.set_ylabel('Среднеквадратичные значения длин векторов поля скоростей, 10^-7 м/c', fontsize = 7)
        ax4.tick_params(axis='y', length = 3, width = 0.3, labelsize=7)#5
        ax4.tick_params(axis='x', length = 3, width = 0.3, labelsize=7)#
        x = []
        t_2_1 = 0
        for i in range(k):
            x.append(t_0+t_2_1)
            t_2_1 += t_2_arr[i]
        print('Среднеквадратичные значения длин векторов снимков', root_square_saved)
        print('Максимальные значения длин векторов снимков', maxes_saved)
        print('Моменты времени выполнения фотосъемок', x)
        for i in range(k):
            root_square_saved[i] = root_square_saved[i] * 10**4
        ax4.plot(x, root_square_saved, 'o-', markersize=1.005, linewidth=0.6)
        ax4.grid(color = 'green', linewidth = 0.3)
        plt.xlim([0, 1.1*(t_0 + t_2_sum - t_2_arr[len(t_2_arr)-1])])
        plt.ylim([0, 1.1*root_square_saved[k-1]])
        plt.locator_params(axis='both', nbins=k)

        fig5 = plt.figure(figsize = (3, 6), dpi=200)
        ax5 = fig5.add_subplot()
        ax5.set_xlabel('Время, c', fontsize = 7)
        ax5.set_ylabel('Максимальные значения длин векторов поля скоростей, 10^-7 м/c', fontsize = 7)
        ax5.tick_params(axis='y', length = 3, width = 0.3, labelsize=7)#5
        ax5.tick_params(axis='x', length = 3, width = 0.3, labelsize=7)#
        x = []
        t_2_1 = 0
        for i in range(k):
            x.append(t_0+t_2_1)
            t_2_1 += t_2_arr[i]
        for i in range(k):
            maxes_saved[i] = maxes_saved[i]*10**4
        ax5.plot(x, maxes_saved, 'o', markersize=1.005, linewidth=0.6)
        trend = np.polyfit(x, maxes_saved, 2)
        trendpoly = np.poly1d(trend)
        ax5.plot(x, trendpoly(x), linewidth = 0.8, color = 'blue')
        ax5.grid(color = 'green', linewidth = 0.2)
        plt.xlim([0, 1.1*(t_0 + t_2_sum - t_2_arr[len(t_2_arr)-1])])
        plt.ylim([0, 1.1*maxes_saved[k-1]])
        plt.locator_params(axis='both', nbins=k)
    else:
        root_square = []
        maxes = []
        for i in range(k):
            mx = []
            V_x_new = []
            V_y_new = []
            for it in range(len(V_x[0])):
                x = V_x[i][it]
                y = V_y[i][it]
                V_x[i][it] = x* math.cos(w_t[i]*delta_t) + y * math.sin(w_t[i]*delta_t)
                V_y[i][it] = -x * math.sin(w_t[i]*delta_t) + y * math.cos(w_t[i]*delta_t)
                V_x_new.append(V_x[i][it] - u_x[i])
                V_y_new.append(V_y[i][it] - u_y[i])
                mx.append(math.sqrt(V_x_new[it]**2 + V_y_new[it]**2))
            maxes.append(max(mx))
            V_x_new_arr.append(V_x_new)
            V_y_new_arr.append(V_y_new)
            w_t_none, u_x_tip, u_y_tip = min_field(a0, b0, n0, m0, l0, coords_plane2, V_x_new, V_y_new, num)
            root_square.append(math.sqrt(u_x_tip**2 + u_y_tip**2))
        V_x_new_arr.remove([])
        V_y_new_arr.remove([])
        fig3 = plt.figure(figsize = (3, 6), dpi=200)
        ax3 = fig3.add_subplot()
        ax3.set_xlabel('Время, c', fontsize = 7)
        ax3.set_ylabel('Среднеквадратичные значения длин векторов поля скоростей, 10^-10 м/c', fontsize = 7)
        ax3.tick_params(axis='y', length = 3, width = 0.3, labelsize=7)#5
        ax3.tick_params(axis='x', length = 3, width = 0.3, labelsize=7)#
        x = []
        t_2_1 = 0
        for i in range(k):
            x.append(t_0+t_2_1)
            t_2_1 += t_2_arr[i]
        print('Среднеквадратичные значения длин векторов снимков', root_square)
        print('Максимальные значения длин векторов снимков', maxes)
        print('Моменты времени выполнения фотосъемок', x)
        ax3.plot(x, root_square, 'o-', markersize=1.005, linewidth=1)
        ax3.grid(color = 'green', linewidth = 0.3)
        plt.xlim([0, 1.1*(t_0 + t_2_sum - t_2_arr[len(t_2_arr)-1])])
        plt.ylim([0, 1.1*root_square[k-1]])
        plt.locator_params(axis='both', nbins = k)

        fig5 = plt.figure(figsize = (3, 6), dpi=200)
        ax5 = fig5.add_subplot()
        ax5.set_xlabel('Время, c', fontsize = 7)
        ax5.set_ylabel('Максимальные значения длин векторов поля скоростей, 10^-3 м/c', fontsize = 7)
        ax5.tick_params(axis='y', length = 3, width = 0.3, labelsize=7)#5
        ax5.tick_params(axis='x', length = 3, width = 0.3, labelsize=7)#
        x = []
        t_2_1 = 0
        for i in range(k):
            x.append(t_0+t_2_1)
            t_2_1 += t_2_arr[i]
        ax5.plot(x, maxes, 'o-', markersize=1.005, linewidth=1)
        ax5.grid(color = 'green', linewidth = 0.3)
        plt.xlim([0, 1.1*(t_0 + t_2_sum - t_2_arr[len(t_2_arr)-1])])
        plt.ylim([0, 1.1*maxes[k-1]])
        plt.locator_params(axis='both', nbins=k)
    len_coords_0 = math.sqrt(V_x_new_arr[0][0] ** 2 + V_y_new_arr[0][0] ** 2)
    len_coords_1 = math.sqrt(V_x_new_arr[0][m0-1] ** 2 + V_y_new_arr[0][m0-1] ** 2)
    len_coords_2 = math.sqrt(V_x_new_arr[0][len(coords_plane2) - m0 + 1] ** 2 + V_y_new_arr[0][len(coords_plane2) - m0 + 1] ** 2)
    len_coords_3 = math.sqrt(V_x_new_arr[0][len(coords_plane2) - 1] ** 2 + V_y_new_arr[0][len(coords_plane2) - 1] ** 2)
    len_coords = (len_coords_0 + len_coords_1 + len_coords_2 + len_coords_3) / 4
    for i in range(k):
        if i % 2 == 0:
            for it in range(len(V_x[0])):
                #ax1.quiver(coords_plane2[it][0] + i*(b0_new - m1_new/2), coords_plane2[it][1], V_x_new_arr[i][it] - coords_plane2[it][0], V_y_new_arr[i][it] - coords_plane2[it][1],  angles = 'xy', scale_units = 'xy', width = 0.0015, scale = len_coords / scale_prm, color = "red")#scale = len_coords / 0.008)#scale=0.00032 и 0.000042)
                ax1.quiver(coords_plane2[it][0] + i*b0_new, coords_plane2[it][1], V_x_new_arr[i][it], V_y_new_arr[i][it],  angles = 'xy', scale_units = 'xy', width = 0.0015, scale = len_coords / scale_prm, color = "red")#scale = len_coords / 0.008)#scale=0.00032 и 0.000042)
        else:
            for it in range(len(V_x[0])):
                ax1.quiver(coords_plane2[it][0] + i*b0_new, coords_plane2[it][1], V_x_new_arr[i][it], V_y_new_arr[i][it],  angles = 'xy', scale_units = 'xy', width = 0.0015, scale = len_coords / scale_prm, color = "blue")
    if num>1:
        ax1.grid(color = 'green', linewidth = 0.3)
    else:
        ax1.grid(color = 'green')
    ax1.set_aspect(abs((b0_new/a0_new*num)))
    if num > 1:
        ax1.grid(color = 'green', linewidth = 0.3)
        ax1.set_xlabel('OX, 10^-3 м', fontsize = 5)
        ax1.set_ylabel('OY, 10^-3 м', fontsize = 5)
        plt.xlim([-(b0_new + m1_new), b0_new*k + m1_new])
        plt.ylim([-(a0_new + n1_new), a0_new + n1_new])
    else:
        ax1.grid(color = 'green', linewidth = 0.2)
        ax1.set_xlabel('OX, 10^-3 м', fontsize = 12)
        ax1.set_ylabel('OY, 10^-3 м', fontsize = 12)
        plt.xlim([-(b0_new + 10 * m1), b0_new + 8 * m1])
        plt.ylim([-(a0_new + n1_new), a0_new + 3 * n1_new])
    plt.show()
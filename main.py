import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.cbook as cbook
from src import *
from matplotlib.ticker import FormatStrFormatter

from basic.prep_calc import prep_calc
from basic.satellite_orbit import satellite_orbit
from basic.satellite_arrays import satellite_arrays
from basic.KSK_nadir import KSK_nadir

from visual.animation_2d import map_2d
from visual.animation_3d import animation_3d
from visual.trace_points import trace_points

from speed_field.conversion import conversion
from speed_field.calculate_earth_point import calculate_earth_point
from speed_field.result_speed import result_speed

from min_field.min_field import min_field
from min_field.field_image import field_image
from min_field.field_image_array import field_image_array

from half_plate.nsk import nsk
from half_plate.nsk_dots import nsk_dots
from half_plate.earth_picture import earth_picture
from half_plate.deltime import deltime

from aircraft_angles.aircraft_angle_rot import aircraft_angle_rot
from aircraft_angles.extra_roll_angle import extra_roll_angle
from aircraft_angles.angle_between_NSKs import angle_between_NSKs
from aircraft_angles.angle_dir_parallel import angle_dir_parallel

from transverse_component.transverse_component import calc_transverse_comp

from plate import Plate, Plates

from pickle import TRUE
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import math
from scipy.optimize import bisect

def calculate(mode, coords_plane2, a, e, i, Ω_0, ω_0, M_0, t_0, t, step, R):     #функция для режимов работы VISUAL и MIN_FIELD
    for t_1 in np.arange(t_0 - step, t + step, step):
        [x_rv, y_rv, z_rv, r, OSC, O1, e3] = satellite_orbit(t_1, a, e, i, Ω_0, ω_0, M_0, t_0, n_0, p, step, d, None)
        satellite_arrays(x_rv, y_rv, z_rv, r, O1, OSC)
    if mode != 'VISUAL':
        K1, KSC = KSK_nadir(O1, OSC, d, r)
        global V_x, V_y
        e_point = []
        e_point = calculate_earth_point(O1, K1, KSC, coords_plane2, e_point, delta_t, R)
        #print(e_point)
        [x_rv, y_rv, z_rv, r, OSC, O1, e3] = satellite_orbit(t_1 + delta_t, a, e, i, Ω_0, ω_0, M_0, t_0, n_0, p, step, d, None)
        K1_new, KSC_new = KSK_nadir(O1, OSC, d, r)
        [V_x, V_y] = result_speed(O1, K1_new, KSC_new, coords_plane2, e_point, delta_t)
        print(e3)
         
def calculate_2(mode, coords_plane2, a, e, i, Ω_0, ω_0, M_0, t_0, t, step, R, photo_num, k):    #функция для режимов работы HALF_PLATE и ADD_ROLL_ANGLE
    for t_1 in np.arange(t_0 - step, t + step, step):
        [x_rv, y_rv, z_rv, r, OSC, O1, e3] = satellite_orbit(t_1, a, e, i, Ω_0, ω_0, M_0, t_0, n_0, p, step, d, None)
    if mode == 'HALF_PLATE':
        yaw_angle = 0
        roll_angle = 0
        K1, KSC = KSK_nadir(O1, OSC, d, r)
        nsk_center, NSK, nsk_x = nsk(O1, K1, KSC, a0, b0 + m1/2, R)    #находим центр и направляющие векторы НСК -  фото поверхности земли
        ang_dir_par = angle_dir_parallel(x_rv, y_rv, nsk_x, NSK, nsk_center)
        t_2 = deltime(nsk_center, nsk_x, 0, mode, ang_dir_par, n_0, R)
        roll_angle += extra_roll_angle(nsk_center, nsk_x, NSK, O1, ang_dir_par, mode, yaw_angle, t_2, R)
        print('roll_angle', roll_angle)
    else:
        yaw_angle = -math.pi/15#-0.05489079668564045#-math.pi/15
        roll_angle = 0
        K1_nadir, KSC_nadir = KSK_nadir(O1, OSC, d, r)
        K1, KSC = aircraft_angle_rot(0, roll_angle, yaw_angle, O1, OSC, r, d)
        nsk_center_nadir, NSK, nsk_x_nadir = nsk(O1, K1_nadir, KSC_nadir, a0, b0 + m1/2, R)#находим центр и направляющие векторы НСК -  фото поверхности земли
        nsk_center, NSK_angle, nsk_x = nsk(O1, K1, KSC, a0, b0 + m1/2, R)
        ang_dir_par = angle_dir_parallel(x_rv, y_rv, nsk_x_nadir, NSK, nsk_center_nadir)
        angle_between_NSK = angle_between_NSKs(nsk_x, NSK, nsk_center)
        t_2 = deltime(nsk_center, nsk_x, angle_between_NSK, mode, ang_dir_par, n_0, R)   #находим время, спустя которое нужно сделать следующий кадр
        roll_angle += extra_roll_angle(nsk_center, nsk_x, NSK, O1, ang_dir_par, mode, yaw_angle, t_2, R)
        roll_angle = 0
    t_2_arr = []
    O1_arr = []
    K1_arr = []
    KSC_arr = []
    t_2_arr.append(t_2)
    O1_arr.append(O1)
    K1_arr.append(K1)
    KSC_arr.append(KSC)
    t_2_sum = t_2
    for it in range(1, photo_num):
        [x_rv, y_rv, z_rv, r, OSC, O1, e3] = satellite_orbit(t_1 + t_2_sum, a, e, i, Ω_0, ω_0, M_0, t_0, n_0, p, step, d, None)
        if mode == 'HALF_PLATE':
            K1_new, KSC_new = aircraft_angle_rot(0, roll_angle, yaw_angle, O1, OSC, r, d)
            nsk_center_new, NSK_new, nsk_x_new = nsk(O1, K1_new, KSC_new, a0, b0 + m1/2, R)
            ang_dir_par = angle_dir_parallel(x_rv, y_rv, nsk_x_new, NSK_new, nsk_center_new)
            t_2 = deltime(nsk_center_new, nsk_x_new, 0, mode, ang_dir_par, n_0, R)
            roll_angle += extra_roll_angle(nsk_center_new, nsk_x_new, NSK_new, O1, ang_dir_par, mode, yaw_angle, t_2, R)
        else:
            K1_new_0, KSC_new_0 = aircraft_angle_rot(0, roll_angle, 0, O1, OSC, r, d)
            K1_new, KSC_new = aircraft_angle_rot(0, roll_angle, yaw_angle, O1, OSC, r, d)
            nsk_center_new_0, NSK_new_0, nsk_x_new_0 = nsk(O1, K1_new_0, KSC_new_0, a0, b0 + m1/2, R)
            nsk_center_new, NSK_new, nsk_x_new = nsk(O1, K1_new, KSC_new, a0, b0 + m1/2, R)
            ang_dir_par = angle_dir_parallel(x_rv, y_rv, nsk_x_new_0, NSK_new_0, nsk_center_new_0)
            t_2 = deltime(nsk_center_new, nsk_x_new, angle_between_NSK, mode, ang_dir_par, n_0, R)
            roll_angle += extra_roll_angle(nsk_center_new_0, nsk_x_new, NSK_new_0, O1, ang_dir_par, mode, yaw_angle, t_2, R)
            roll_angle = 0
        t_2_sum += t_2
        t_2_arr.append(t_2)
        O1_arr.append(O1)
        K1_arr.append(K1_new)
        KSC_arr.append(KSC_new)
    e_point = [[] for _ in range(photo_num)]
    for it in range(0, photo_num):
        t_2_sum -= t_2_arr[photo_num - it - 1]
        e_point[it] = calculate_earth_point(O1_arr[it], K1_arr[it], KSC_arr[it], coords_plane2, e_point[it], t_2_sum, R)
        earth_dots.append(nsk_dots(nsk_center, NSK, e_point[it]))
    earth_picture(earth_dots, k)

def calculate_3(mode, coords_plane2, a, e, i, Ω_0, ω_0, M_0, t_0, t, step, R, photo_num, k, pix_len, num):  #функция для режимов работы FIELD_SEQUENCE и FIELD_SAVE
    roll_angle = 0#-math.pi/60   #самолетные углы вращения пластины
    yaw_angle = 0
    for t_1 in np.arange(t_0 - step, t + step, step):
        [x_rv, y_rv, z_rv, r, OSC, O1, e3] = satellite_orbit(t_1, a, e, i, Ω_0, ω_0, M_0, t_0, n_0, p, step, d, None)
    def transverse_component(yaw_angle):     #функция для вычисления поперечной составляющей смаза в зависимости от угла рыскания
        e_point_1 = []
        nonlocal O1, OSC, r, e3
        O1_loc = O1
        OSC_loc = OSC
        r_loc = r
        K1_loc, KSC_loc = aircraft_angle_rot(0, roll_angle, yaw_angle, O1_loc, OSC_loc, r_loc, d)
        e_point_1 = calculate_earth_point(O1_loc, K1_loc, KSC_loc, coords_plane2, e_point_1, delta_t, R)
        [x_rv, y_rv, z_rv, r_loc, OSC_loc, O1_loc, e3_loc] = satellite_orbit(t_1 + delta_t, a, e, i, Ω_0, ω_0, M_0, t_0, n_0, p, step, d, 'memorize')
        K1_1_loc, KSC_1_loc = aircraft_angle_rot(0, roll_angle, yaw_angle, O1_loc, OSC_loc, r_loc, d)
        [V_x_loc, V_y_loc] = result_speed(O1_loc, K1_1_loc, KSC_1_loc, coords_plane2, e_point_1, delta_t)
        return calc_transverse_comp(a0, b0, n0, m0, coords_plane2, coords_2, V_x_loc, V_y_loc, V_x_2, V_y_2, num)
    
    yaw_angle = bisect(transverse_component, -1.25, 1.25)
    print('Угол рыскания в результате вычислений:', yaw_angle)
    K1_nadir, KSC_nadir = KSK_nadir(O1, OSC, d, r)
    K1, KSC = aircraft_angle_rot(0, roll_angle, yaw_angle, O1, OSC, r, d)
    nsk_center_nadir, NSK, nsk_x_nadir = nsk(O1, K1_nadir, KSC_nadir, a0, b0 + m1/2, R)
    nsk_center, NSK_angle, nsk_x = nsk(O1, K1, KSC, a0, b0 + m1/2, R)
    ang_dir_par = angle_dir_parallel(x_rv, y_rv, nsk_x_nadir, NSK, nsk_center_nadir)
    angle_between_NSK = angle_between_NSKs(nsk_x, NSK, nsk_center)
    t_2 = deltime(nsk_center, nsk_x, angle_between_NSK, mode, ang_dir_par, n_0, R)
    t_2_sum = t_2
    roll_angle_prev = roll_angle
    roll_angle += extra_roll_angle(nsk_center, nsk_x, NSK, O1, ang_dir_par, mode, yaw_angle, t_2, R)
    print('roll_angle', roll_angle)
    t_2_arr = []
    O1_arr = []
    K1_arr = []
    KSC_arr = []
    t_2_arr.append(t_2)
    O1_arr.append(O1)
    K1_arr.append(K1)
    KSC_arr.append(KSC)
    e_point = [[] for _ in range(photo_num)]
    e_point[0] = calculate_earth_point(O1, K1, KSC, coords_plane2, e_point[0], delta_t, R)
    [x_rv, y_rv, z_rv, r, OSC, O1, e3] = satellite_orbit(t_1 + delta_t, a, e, i, Ω_0, ω_0, M_0, t_0, n_0, p, step, d, 'memorize')
    K1_1, KSC_1 = aircraft_angle_rot(0, roll_angle_prev, yaw_angle, O1, OSC, r, d)
    [V_x, V_y] = result_speed(O1, K1_1, KSC_1, coords_plane2, e_point[0], delta_t)
    [w_t, u_x, u_y] = min_field(a0, b0, n0, m0, l0, coords_plane2, V_x, V_y, num)
    V_x_arr.append(V_x)
    V_y_arr.append(V_y)
    w_t_arr.append(w_t)
    u_x_arr.append(u_x)
    u_y_arr.append(u_y)
    for it in range(1, photo_num):
        roll_angle_prev = 0
        [x_rv, y_rv, z_rv, r, OSC, O1, e3] = satellite_orbit(t_1 + t_2_sum, a, e, i, Ω_0, ω_0, M_0, t_0, n_0, p, step, d, None)
        K1_new_0, KSC_new_0 = aircraft_angle_rot(0, roll_angle, 0, O1, OSC, r, d)
        K1_new, KSC_new = aircraft_angle_rot(0, roll_angle, yaw_angle, O1, OSC, r, d)
        nsk_center_new_0, NSK_new_0, nsk_x_new_0 = nsk(O1, K1_new_0, KSC_new_0, a0, b0 + m1/2, R)
        nsk_center_new, NSK_new, nsk_x_new= nsk(O1, K1_new, KSC_new, a0, b0 + m1/2, R)
        ang_dir_par = angle_dir_parallel(x_rv, y_rv, nsk_x_new_0, NSK_new_0, nsk_center_new_0)
        roll_angle_prev = roll_angle
        t_2 = deltime(nsk_center_new, nsk_x_new, angle_between_NSK, mode, ang_dir_par, n_0, R)
        roll_angle += extra_roll_angle(nsk_center_new_0, nsk_x_new, NSK_new_0, O1, ang_dir_par, mode, yaw_angle, t_2, R)
        print('roll_angle', roll_angle)
        e_point[it] = calculate_earth_point(O1, K1_new, KSC_new, coords_plane2, e_point[it], delta_t, R)
        t_2_arr.append(t_2)
        O1_arr.append(O1)
        K1_arr.append(K1_new)
        KSC_arr.append(KSC_new)
        [x_rv, y_rv, z_rv, r, OSC, O1, e3] = satellite_orbit(t_1 + t_2_sum + delta_t, a, e, i, Ω_0, ω_0, M_0, t_0, n_0, p, step, d, 'memorize')
        K1_1_new, KSC_1_new = aircraft_angle_rot(0,  roll_angle_prev, yaw_angle, O1, OSC, r, d)
        [V_x, V_y] = result_speed(O1, K1_1_new, KSC_1_new, coords_plane2, e_point[it], delta_t)
        [w_t, u_x, u_y] = min_field(a0, b0, n0, m0, l0, coords_plane2, V_x, V_y, num)
        V_x_arr.append(V_x)
        V_y_arr.append(V_y)
        w_t_arr.append(w_t)
        u_x_arr.append(u_x)
        u_y_arr.append(u_y)
        t_2_sum += t_2
    e_point_1 = [[] for _ in range(photo_num)]
    for it in range(0, photo_num):
        t_2_sum -= t_2_arr[photo_num - it - 1]
        e_point_1[it] = calculate_earth_point(O1_arr[it], K1_arr[it], KSC_arr[it], coords_plane2, e_point_1[it], t_2_sum, R)
        earth_dots.append(nsk_dots(nsk_center, NSK,  e_point_1[it]))
    earth_picture(earth_dots, k)
    if mode == 'FIELD_SEQUENCE':
        field_image_array(a0, b0, n0, m0, n1, m1, l0, V_x_arr, V_y_arr, u_x_arr, u_y_arr, w_t_arr, coords_plane2, scale_prm, num, photo_num, delta_t, mode, 0, t_2_arr, coords_2, t_0)
    else:
        field_image_array(a0, b0, n0, m0, n1, m1, l0, V_x_arr, V_y_arr, u_x_arr, u_y_arr, w_t_arr, coords_plane2, scale_prm, num, photo_num, delta_t, mode, pix_len, t_2_arr, coords_2, t_0)

if __name__ == "__main__":
    mode =  'MIN_FIELD_GRAPH'    #выбор режима работы программы

    if mode == 'VISUAL':
        a = 8578245 #(метры) большая полуось
        e = 0   #Эксцентриситет
        i = 60      #(градусы) наклонение орбиты
        Ω_0 = 0     #(град) долгота восходящего узла
        ω_0 = 0     #(град) начальный угол наклона вектора скорости к экватору(аргумент перигея)
        M_0 = 45    #(град) средняя аномалия в эпоху кеплеровой орбиты
        t_0 = 0     #26300 #(с) начальный момент времени
        t = 18701#13701   #40000   #(c) конечный момент времени
        step = 5    #шаг по времени
        f_m, n_0, T, p = prep_calc(a, e, f, m)
        calculate(mode, None, a, e, i, Ω_0, ω_0, M_0, t_0, t, step, R)
        dataSet = np.array([longitude[1: len(dolg) - 1], latitude[1: len(shir) - 1]])
        trace_points(step, dataSet_4)
        map_2d(dataSet, x_trace, y_trace, step, t_0, t)
        animation_3d(step, dataSet_2, dataSet_3, dataSet_4, O2)
    elif mode == 'MIN_FIELD':
        a = 6578245 #(метры) большая полуось
        e = 0   #Эксцентриситет
        i = 60      #(градусы) наклонение орбиты
        Ω_0 = 0     #(град) долгота восходящего узла
        ω_0 = 0     #(град) начальный угол наклона вектора скорости к экватору(аргумент перигея)
        M_0 = 179.9998    #(град) средняя аномалия в эпоху кеплеровой орбиты
        t_0 = 0 #(с) начальный момент времени
        t =  0.0002  #(c) конечный момент времени
        step = 0.0001    #шаг по времени
        k = 3
        num = 1 #число микросхем пластины
        a0 = 0.08#0.063524   #1/2 длины ПЗС линейки по оси Oy(метры)
        b0 = 0.0066#0.007854   #1/2 длины ПЗС линейки по оси Оx(метры)
        n0 = 13
        m0 = 13
        n1 = 2 * a0 / (n0 - 1)   #шаг по оси Оy
        m1 = 2 * b0 / (m0 - 1)   #шаг по оси Ox
        #a0 = a0 * 8 + 7 * n1
        #print(a0)
        l0 = int((n0*m0-1)/2) #номер точки центра ПЗС линейки (для нечетного числа пикселей)
        a0, b0, n1, m1, a, f, d, R = conversion(k, a, f, d, R, a0, b0, n1, m1)
        for it in np.linspace(-a0, a0, n0):
            for j in np.linspace(-b0, b0, m0):
                coords_plane2.append([round(j, 10), round(it, 10)])
        coords_2 = [[0] * m0 for i in range(n0)]
        V_x = []
        V_y = []
        scale_prm = 0.005
        scale_prm = scale_prm * 10 ** k
        f_m, n_0, T, p = prep_calc(a, e, f, m)
        calculate(mode, coords_plane2, a, e, i, Ω_0, ω_0, M_0, t_0, t, step, R)
        [w_t, u_x, u_y] = min_field(a0, b0, n0, m0, l0, coords_plane2, V_x, V_y, num)
        field_image(a0, b0, n0, m0, n1, m1, l0, V_x, V_y, u_x, u_y, w_t, coords_plane2, scale_prm, num, delta_t, coords_2)
        plt.show()
    elif mode == 'HALF_PLATE':
        a = 6578245 #(метры) большая полуось
        e = 0   #Эксцентриситет
        i = 85      #(градусы) наклонение орбиты
        Ω_0 = 0     #(град) долгота восходящего узла
        ω_0 = 0     #(град) начальный угол наклона вектора скорости к экватору(аргумент перигея)
        M_0 = 0    #(град) средняя аномалия в эпоху кеплеровой орбиты
        t_0 = 0 #(с) начальный момент времени
        t =  0.0002  #(c) конечный момент времени
        step = 0.0001    #шаг по времени
        k = 3
        num = 8 #число микросхем пластины   
        a0 = 0.0088 #0.0088/13 * 7 + 0.0088 * 8   #1/2 длины ПЗС линейки по оси Oy(метры)
        print(a0)
        b0 = 0.0066#0.007854   #1/2 длины ПЗС линейки по оси Оx(метры)
        n0 = 13 #*8
        m0 = 13
        l0 = int((n0*m0-1)/2) #номер точки центра ПЗС линейки (для нечетного числа пикселей)
        n1 = 2 * a0 / (n0 - 1)   #шаг по оси Оy
        m1 = 2 * b0 / (m0 - 1)   #шаг по оси Ox
        photo_num = 1   #количество снимков
        a0, b0, n1, m1, a, f, d, R = conversion(k, a, f, d, R, a0, b0, n1, m1)
        f_m, n_0, T, p = prep_calc(a, e, f, m)
        # for it in np.linspace(-a0, a0, n0):
        #     for j in np.linspace(-b0, b0, m0):
        #        coords_plane2.append([round(j, 10), round(it, 10)])
        p8 = Plates(a0, b0, n0, m0, n1, m1, num)
        calculate_2(mode, p8.coords, a, e, i, Ω_0, ω_0, M_0, t_0, t, step, R, photo_num, k)
    elif mode == 'ADD_ROLL_ANGLE':
        a = 6578245 #(метры) большая полуось
        e = 0   #Эксцентриситет
        i = 85      #(градусы) наклонение орбиты
        Ω_0 = 0     #(град) долгота восходящего узла
        ω_0 = 0     #(град) начальный угол наклона вектора скорости к экватору(аргумент перигея)
        M_0 = 0    #(град) средняя аномалия в эпоху кеплеровой орбиты
        t_0 = 0 #(с) начальный момент времени
        t =  0.0002  #(c) конечный момент времени
        step = 0.0001    #шаг по времени
        k = 3
        num = 8
        a0 = 0.0088#0.063524   #1/2 длины ПЗС линейки по оси Oy(метры)
        b0 = 0.0066#0.007854   #1/2 длины ПЗС линейки по оси Оx(метры)
        n0 = 7
        m0 = 7
        l0 = int((n0*m0-1)/2) #номер точки центра ПЗС линейки (для нечетного числа пикселей)
        n1 = 2 * a0 / (n0 - 1)   #шаг по оси Оy
        m1 = 2 * b0 / (m0 - 1)   #шаг по оси Ox
        photo_num = 5   #количество снимков
        a0, b0, n1, m1, a, f, d, R = conversion(k, a, f, d, R, a0, b0, n1, m1)
        f_m, n_0, T, p = prep_calc(a, e, f, m)
        p8 = Plates(a0, b0, n0, m0, n1, m1, num)
        # for it in np.linspace(-a0, a0, n0):
        #     for j in np.linspace(-b0, b0, m0):
        #         coords_plane2.append([round(j, 10), round(it, 10)])
        calculate_2(mode, p8.coords, a, e, i, Ω_0, ω_0, M_0, t_0, t, step, R, photo_num, k)
    elif mode == 'FIELD_SEQUENCE':
        a = 6578245      #(метры) большая полуось
        e = 0            #Эксцентриситет
        i = 85           #(градусы) наклонение орбиты
        Ω_0 = 0          #(град) долгота восходящего узла
        ω_0 = 0          #(град) начальный угол наклона вектора скорости к экватору(аргумент перигея)
        M_0 = 0          #(град) средняя аномалия в эпоху кеплеровой орбиты
        t_0 = 0          #(с) начальный момент времени
        t =  0.0002      #(c) конечный момент времени
        step = 0.0001    #шаг по времени
        k = 3
        num = 1             #число миксросхем в ПЗС-линейке
        a0 = 0.08       #0.063524#0.0088#0.063524   #1/2 длины ПЗС линейки по оси Oy(метры)
        b0 = 0.0066         #0.007854#0.0066#0.007854   #1/2 длины ПЗС линейки по оси Оx(метры)
        n0 = 14
        m0 = 7
        n1 = 2 * a0 / (n0 - 1)   #шаг по оси Оy
        m1 = 2 * b0 / (m0 - 1)   #шаг по оси Ox
        l0 = int((n0*m0-1)/2)    #номер точки центра ПЗС линейки (для нечетного числа пикселей)
        photo_num = 5            #количество снимков
        a0, b0, n1, m1, a, f, d, R = conversion(k, a, f, d, R, a0, b0, n1, m1)
        f_m, n_0, T, p = prep_calc(a, e, f, m)
        coords_2 = [[0] * m0 for i in range(n0*num)]
        V_x_2 = [[0] * m0 for i in range(n0*num)]
        V_y_2 = [[0] * m0 for i in range(n0*num)]
        V_x_arr = []
        V_y_arr = []
        u_x_arr = []
        u_y_arr = []
        w_t_arr = []
        scale_prm = 0.01
        scale_prm = scale_prm * 10 ** k
        #p8 = Plates(a0, b0, n0, m0, n1, m1, num)
        for it in np.linspace(-a0, a0, n0):
            for j in np.linspace(-b0, b0, m0):
                coords_plane2.append([round(j, 16), round(it, 16)])
        calculate_3(mode, coords_plane2, a, e, i, Ω_0, ω_0, M_0, t_0, t, step, R, photo_num, k, 0, num)#p3.coords, num, 0, photo_num)
    elif mode == 'FIELD_SAVE':
        a = 6578245 #(метры) большая полуось
        e = 0       #Эксцентриситет
        i = 85      #(градусы) наклонение орбиты
        Ω_0 = 0     #(град) долгота восходящего узла
        ω_0 = 0     #(град) начальный угол наклона вектора скорости к экватору(аргумент перигея)
        M_0 = 0     #(град) средняя аномалия в эпоху кеплеровой орбиты
        t_0 = 0     #(с) начальный момент времени
        t =  0.0002    #(c) конечный момент времени
        step = 0.0001   #шаг по времени
        a0 = 0.08   #0.063524#0.0088#0.063524   #1/2 длины ПЗС линейки по оси Oy(метры)
        b0 = 0.0066     #0.007854#0.0066#0.007854   #1/2 длины ПЗС линейки по оси Оx(метры)
        n0 = 14
        m0 = 7
        n1 = 2 * a0 / (n0 - 1)   #шаг по оси Оy
        m1 = 2 * b0 / (m0 - 1)   #шаг по оси Ox
        l0 = int((n0*m0-1)/2)    #номер точки центра ПЗС линейки (для нечетного числа пикселей)
        k = 3
        photo_num = 20           #количество снимков
        a0, b0, n1, m1, a, f, d, R = conversion(k, a, f, d, R, a0, b0, n1, m1)
        f_m, n_0, T, p = prep_calc(a, e, f, m)
        num = 1                  #число миксросхем в ПЗС-линейке
        coords_2 = [[0] * m0 for i in range(n0*num)]
        V_x_2 = [[0] * m0 for i in range(n0*num)]
        V_y_2 = [[0] * m0 for i in range(n0*num)]
        V_x_arr = []
        V_y_arr = []
        u_x_arr = []
        u_y_arr = []
        w_t_arr = []
        scale_prm = 0.01
        scale_prm = scale_prm * 10 ** k
        pix_len = 0.0000001
        #p3 = Plates(a0, b0, n0, m0, n1, m1, num)
        for it in np.linspace(-a0, a0, n0):
            for j in np.linspace(-b0, b0, m0):
                coords_plane2.append([round(j, 16), round(it, 16)])
        calculate_3(mode, coords_plane2, a, e, i, Ω_0, ω_0, M_0, t_0, t, step, R, photo_num, k, pix_len, num)#p3.coords, num, 0, photo_num)
    elif mode == 'MIN_FIELD_GRAPH':
        a = 6578245 #(метры) большая полуось
        e = 0   #Эксцентриситет
        i = 85      #(градусы) наклонение орбиты
        Ω_0 = 0     #(град) долгота восходящего узла
        ω_0 = 0     #(град) начальный угол наклона вектора скорости к экватору(аргумент перигея)
        M_0 = 179.9998    #(град) средняя аномалия в эпоху кеплеровой орбиты
        t_0 = 0 #(с) начальный момент времени
        t =  0.0002  #(c) конечный момент времени
        step = 0.0001    #шаг по времени
        k = 3
        num = 1 #число микросхем пластины
        a0 = 0.08#0.063524   #1/2 длины ПЗС линейки по оси Oy(метры)
        b0 = 0.0066#0.007854   #1/2 длины ПЗС линейки по оси Оx(метры)
        n0 = 13
        m0 = 13
        n1 = 2 * a0 / (n0 - 1)   #шаг по оси Оy
        m1 = 2 * b0 / (m0 - 1)   #шаг по оси Ox
        l0 = int((n0*m0-1)/2) #номер точки центра ПЗС линейки (для нечетного числа пикселей)
        max_vectors = []
        M0_arr = np.array([359.999999, 11.259999, 22.499999, 33.749999, 44.999999, 56.249999, 67.499999, 78.249999, 89.999999, 101.249999, 112.499999, 123.749999, 134.999999, 146.249999, 157.49999, 168.749999, 179.999999])
        k = 3
        a0, b0, n1, m1, a, f, d, R = conversion(k, a, f, d, R, a0, b0, n1, m1)
        f_m, n_0, T, p = prep_calc(a, e, f, m)
        for it in range(17):
            coords_plane2 = []
            coords_2 = []
            M_0 = M0_arr[it]
            i = 90
            num = 1 #число микросхем пластины
            for it in np.linspace(-a0, a0, n0):
                for j in np.linspace(-b0, b0, m0):
                    coords_plane2.append([round(j, 10), round(it, 10)])
            coords_2 = [[0] * m0 for j in range(n0)]
            V_x = []
            V_y = []
            scale_prm = 0.005
            scale_prm = scale_prm * 10 ** k
            calculate(mode, coords_plane2, a, e, i, Ω_0, ω_0, M_0, t_0, t, step, R)
            [w_t, u_x, u_y] = min_field(a0, b0, n0, m0, l0, coords_plane2, V_x, V_y, num)
            max_vectors.append(field_image(a0, b0, n0, m0, n1, m1, l0, V_x, V_y, u_x, u_y, w_t, coords_plane2, scale_prm, num, delta_t, coords_2))
            print(len(V_x))

        fig6 = plt.figure()
        ax6 = fig6.add_subplot()
        ax6.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        ax6.set_xlabel('Истинная аномалия, градусы', fontsize = 10)
        ax6.set_ylabel('Максимальные значения длин векторов поля скоростей, 10^-6 м/c', fontsize = 10)
        ax6.tick_params(axis='y', length = 3, width = 0.3, labelsize=10)#5
        ax6.tick_params(axis='x', length = 3, width = 0.3, labelsize=10)#
        x = [0, 11.25, 22.5, 33.75, 45, 56.25, 67.5, 78.75, 90, 101.25, 112.5, 123.75, 135, 146.25, 157.5, 168.75, 180]
        for i in range(len(M0_arr)):
            max_vectors[i] = max_vectors[i]*10**3
        ax6.plot(x, max_vectors, 'o-', markersize=1.005, linewidth=1)
        ax6.grid(color = 'green', linewidth = 0.3)
        ax6.set_xticks(np.arange(0, 181, 22.5))
        plt.xlim([-5, 185])
        plt.ylim([0, 1.1*max(max_vectors)])
        plt.locator_params(axis='both', nbins=9)
        plt.gcf()
        plt.close(1)
        plt.close(2)
        plt.show()
    else:
        None
import math
from src import *
import numpy as np

def satellite_orbit(t_1, a, e, i, Ω_0, ω_0, M_0, t_0, n_0, p, step, d, mode_1):
    M = M_0 + math.degrees(n_0 * (t_1 - t_0))   #(град) средняя аномалия на заданный момент времени
    #задавшись точностью вычислений ε(град), методом последовательных приближений вычисляем
    #эксцентрическую аномалю
    ε = 10e-9
    E_0 = M + math.degrees(e * math.sin(math.radians(M)))
    E = M + math.degrees(e * math.sin(math.radians(E_0)))
    while abs(E_0 - E) > ε:
        E_0 = E
        E = M + math.degrees(e * math.sin(math.radians(E)))
    ξ = E + 2 * math.degrees(math.atan(e * math.sin(math.radians(E)) / (1 + math.sqrt(1 - e ** 2) - e * math.cos(math.radians(E)))))  #(град)истинная аномалия
    #print("Истинная аномалия(град)", ξ)
    u = ω_0 + ξ #(град)аргумент широты
    sh = math.degrees(math.asin(math.sin(math.radians(i)) * math.sin(math.radians(u)))) #(град)геоцентрическая широта
    latitude.append(sh)
    r = p / (1 + e * math.cos(ξ)) #геоцентрическое расстояние до спутника
    if (u % 360 >= 0 and u % 360 <= 90):    #(град) дуга АВ
        AB = math.degrees(math.asin(math.tan(math.radians(sh)) / math.tan(math.radians(i))))
    elif (u % 360 > 90 and u % 360 <= 270):
        AB = 180 - math.degrees(math.asin(math.tan(math.radians(sh)) / math.tan(math.radians(i))))
    else: 
        AB = math.degrees(math.asin(math.tan(math.radians(sh)) / math.tan(math.radians(i))))
    do = Ω_0 + AB - S_g #(град) долгота подспутниковой точки(в гринвической СК)
    do_2d = do - math.degrees(w_z * (t_1 - t_0 + step))
    do_2d = do_2d % 360
    if do_2d >= 180 and do_2d <= 360:
        do_2d = do_2d - 360
    longitude.append(do_2d)
    x_rv = r * math.cos(math.radians(sh)) * math.cos(math.radians(do)) #прямоугольные гринвические координаты
    y_rv = r * math.cos(math.radians(sh)) * math.sin(math.radians(do))
    z_rv = r * math.sin(math.radians(sh))
    O1 = np.array([x_rv, y_rv, z_rv]) #центр ОСК(ССК) в ИСК
    e3 = np.copy(O1)
    e3 = e3 / np.linalg.norm(e3)
    O_2 = np.copy(O1)
    if len(O2) >= 1:
        O_2 = np.copy(O2[-1])
    e2 = np.cross(e3, O_2)
    e2 = e2 / np.linalg.norm(e2)
    e3 = -e3
    e1 = np.cross(e2, e3) 
    e1 = e1 / np.linalg.norm(e1)
    OSC = np.array([e1, e2, e3]) #Орбитальная система координат
    OSC = OSC / np.linalg.norm(OSC)
    if mode_1 != 'memorize':
        O2.append(O1)
    norms = np.linalg.norm(OSC, axis=0) # нормирование столбцов
    OSC = OSC / norms
    return [x_rv, y_rv, z_rv, r, OSC, O1, e3]
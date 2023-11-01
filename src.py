import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import animation
import matplotlib.cbook as cbook
import os
from PIL import Image

delta_t = 0.033#0.011#0.033  #Время экспозиции
α = math.pi / 8 #Угол между осью OZ в ОСК и ССК (угол крена)
d = 1.5         #Фокусное расстояние пластины(милиметры)
w_z = 2 * math.pi / 86344
S_g = 0            #(град) звездное время по Гринвичу
eps = 0.40596358    #(рад) угол между плоскостью эклиптики и экваториальной плоскостью (23.26 градуса)
m = 5.9722 * 10 ** 24  #(кг) масса Земли
f = 6.6743151515 * 10 ** (-11) #((метры)^3 * c^(-2) * кг^(-1)) постоянная притяжения
R = 6378245#155 #(метры) радиус Земли
step = 3#0.0001#3#0.001#0.01#0.0001#10 #Шаг(промежуток)
dolg = []
shir = []
dataSet = []
dataSet_2 = [[], [], []]
dataSet_3 = [[], [], []]
dataSet_4 = [[], [], []]
longitude = [] #Долгота
latitude = [] #Широта
x_trace = [] #Трасса камеры спутника на земле
y_trace = []
O2 = []     #Массив точек спутника в ИСК
V_x = []    #Скорости точек пластины КСК для построения поля скоростей
V_y = []
V_x_old = []
V_y_old = []
V_x_alpha = []
V_y_alpha = []
V_x_new_no_alpha = []
V_y_new_no_alpha = []
V_x_new = []
V_y_new = []
V_check_x = []  #Скорости точек пластины КСК для построения и дальнейшей проверки поля скоростей
V_check_y = []
coords_plane2 = []
coords_x = []
coords_y = []
cwd = os.getcwd() #Для доступа к директории в одной папке с файлом .py
with cbook.get_sample_data('%s/map.jpg'%(cwd)) as image_file:
    image = plt.imread(image_file)
earth_dots = []
nsk_centers = []
mx_arr = []
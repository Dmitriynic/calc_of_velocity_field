import numpy as np
from src import image
from matplotlib import animation
import matplotlib.pyplot as plt

#Функция построения 2-д графика
def animate_func_1(num, dataSet, x_trace, y_trace, ax_1, tt):
    ax_1.clear()  # очищаем фигуру для обновления линии, точки,
    ax_1.imshow(image, extent = [-180, 180, -90, 90]) #добавляем фоновое изображение
    ax_1.set_title(type(image))

    ax_1.scatter(dataSet[0, :num + 1], dataSet[1, :num + 1], color = 'red', marker = 'o', s = 0.03, edgecolors = 'none')
    ax_1.scatter(dataSet[0, num], dataSet[1, num], color = 'black', marker = 'o', s = 0.1, edgecolors = 'none')
    ax_1.scatter(x_trace[:num + 1], y_trace[:num + 1], color = 'purple', marker = 'o', s = 0.03, edgecolors = 'none')
    # добавляем постоянную начальную точку
    ax_1.spines['top'].set_linewidth(0.05)
    ax_1.spines['left'].set_linewidth(0.05)
    ax_1.spines['right'].set_linewidth(0.05)
    ax_1.spines['bottom'].set_linewidth(0.05)
    ax_1.set_xlim([-180, 180])
    ax_1.set_ylim([-90, 90])
    ax_1.xaxis.labelpad = 1
    ax_1.yaxis.labelpad = 1
    # Добавляем метки
    ax_1.set_title('\nМомент времени t = ' + str(np.round(tt[num], decimals=5)) + ' с', fontsize = 0.0001, pad = 1)
    ax_1.set_xlabel('долгота', fontsize = 0.0001, labelpad = 0.01)
    ax_1.set_ylabel('широта', fontsize = 0.0001, labelpad = 0.01)
    ax_1.tick_params(axis='y', length = 0.5, width = 0.05, labelsize=0.001, pad = 0.05)
    ax_1.tick_params(axis='x', length = 0.5, width = 0.05, labelsize=0.001, pad = 0.05)

#вставляем изображение карты Земли
def map_2d(dataSet, x_trace, y_trace, step, t_0, t):
    fig_1 = plt.figure(figsize = (0.6, 0.4), dpi=2300)
    ax_1 = fig_1.add_subplot()
    tt = np.arange(t_0, t+step/10, step)
    line_2d = animation.FuncAnimation(fig_1, animate_func_1, fargs=(dataSet, x_trace, y_trace, ax_1, tt), interval = 1, frames = len(tt))
    plt.show()
    #создадим pdf
    f = r"D://UCHEBA_MIREA/diploma/Диплом оформление/new/check_3/2d_animation.gif"
    writergif = animation.PillowWriter(fps = 50)
    line_2d.save(f, writer = writergif)
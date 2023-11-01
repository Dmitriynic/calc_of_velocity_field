import numpy as np
import math
import matplotlib.pyplot as plt
from src import V_x_old, V_y_old, w_z

def earth_picture(earth_dots, k):
    fig = plt.figure(figsize = (5, 7), dpi=170)
    fig.subplots_adjust(left=0.18, right=0.99, bottom=0.067, top=0.97)
    ax = fig.add_subplot()
    ticks_x = np.linspace(-5000, 10000, 10)
    ticks_y = np.linspace(-13500, 13500, 11)
    ax.set_xticks(ticks_x)
    ax.set_yticks(ticks_y)
    ax.tick_params(axis='both', which='major', labelsize=6)
    ax.scatter(0, 0, s = 0.2, color = 'black')
    for i in range(len(earth_dots)):
        if i % 2 == 0:
            for it in range(len(earth_dots[i])):
                ax.scatter(earth_dots[i][it][0]/(10**k), earth_dots[i][it][1]/(10**k), s=0.1, color = 'red')
        else:
            for it in range(len(earth_dots[i])):
                ax.scatter(earth_dots[i][it][0]/(10**k), earth_dots[i][it][1]/(10**k), s=0.1, color = 'blue')

    ax.grid(color = 'green', linewidth = 0.05)
    ax.set_aspect('equal')
    ax.set_aspect(1)
    ax.set_xlabel('OX, м')
    ax.set_ylabel('OY, м')
    plt.xlim([-(5000 + 3 * 1000), 10000 + 3 * 1000])
    plt.ylim([-(13500 + 3 * 1000), 13500 + 3 * 1000])
    plt.show()
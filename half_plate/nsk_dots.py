import numpy as np

def nsk_dots(nsk_center, NSK, e_point):
    earth_dots = []
    for it in range(len(e_point)):
        nsk_dot = np.linalg.inv(NSK.transpose()).dot(np.array([e_point[it][0], e_point[it][1], e_point[it][2]])) - np.linalg.inv(NSK.transpose()).dot(nsk_center) #Координаты точки в НСК
        earth_dots.append(nsk_dot.tolist())
    return earth_dots
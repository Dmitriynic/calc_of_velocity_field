from src import *
from basic.earth_intersection import earth_intersection

def satellite_arrays(x_rv, y_rv, z_rv, r, O1, OSC):
    #Массив точки спутника в прямоугольных гринвических координатах
    dataSet_2[0].append(np.array([x_rv]))
    dataSet_2[1].append(np.array([y_rv]))
    dataSet_2[2].append(np.array([z_rv]))
    #Массивы проекции спутника на поверхность Земли в прямоугольных гринвических координатах
    dataSet_3[0].append(np.array([x_rv * R / r]))
    dataSet_3[1].append(np.array([y_rv * R / r]))
    dataSet_3[2].append(np.array([z_rv * R / r]))
    rotation_matrix = np.array([[1, 0, 0], [0, math.cos(α), -math.sin(α)], [0, math.sin(α), math.cos(α)]])
    X_1 = np.array([0, 0, 1]) #Направляющий вектор OZ ССК в ССК
    X = OSC.transpose().dot(rotation_matrix.dot(X_1))   #ССК в ИСК(луч фотоаппарата)
    dir = X / np.linalg.norm(X)
    tmp = min(earth_intersection(O1, dir, R)[0], earth_intersection(O1, dir, R)[1])
    if(tmp > 0):
        POINT = [O1[0] + tmp * dir[0], O1[1] + tmp * dir[1], O1[2] + tmp * dir[2]]

        dataSet_4[0].append(np.array(POINT[0]))
        dataSet_4[1].append(np.array(POINT[1]))
        dataSet_4[2].append(np.array(POINT[2]))
    else:
        None
import numpy as np

def KSK_nadir(O1, OSC, d, r):
    dir = O1 / np.linalg.norm(O1)
    K1 = np.array((d + r) * dir)
    KSC = np.copy(OSC) #КСК
    norms = np.linalg.norm(KSC, axis=0) #нормировка столбцов
    KSC = KSC / norms
    return K1, KSC
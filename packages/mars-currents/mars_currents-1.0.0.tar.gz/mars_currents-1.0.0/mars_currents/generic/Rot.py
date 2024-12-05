import numpy as np

def Rot(th, axis = 'x'):
    if axis== 'x':
        rot_m = [[1,          0,           0],
                 [0, np.cos(th), -np.sin(th)],
                 [0, np.sin(th),  np.cos(th)]]
    elif axis == 'y':
        rot_m = [[np.cos(th), 0,  np.sin(th)],
                 [0,          1,           0],
                 [-np.sin(th), 0, np.cos(th)]]
    elif axis == 'z':
        rot_m = [[np.cos(th), -np.sin(th), 0],
                 [np.sin(th),  np.cos(th), 0],
                 [0,           0,          1]]
    return rot_m

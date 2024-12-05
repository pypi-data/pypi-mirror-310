import numpy as np

def cart_to_sph(th, phi):

    return np.matrix([[np.sin(th)*np.cos(phi), np.sin(th)*np.sin(phi),  np.cos(th)],
            [np.cos(th)*np.cos(phi), np.cos(th)*np.sin(phi), -np.sin(th)],
            [-np.sin(phi),           np.cos(phi),                     0]])
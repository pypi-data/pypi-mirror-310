import numpy as np
from .cart_to_sph import cart_to_sph

def cart_to_sph_vf(A, th, phi):
    
    #th = np.deg2rad(th); phi = np.deg2rad(phi)
    
    points_rot = [cart_to_sph(theta, phi) for theta, phi in zip(th, phi)]
    rotated_to_sph = [np.dot(rot_m, point) for rot_m, point in zip(points_rot, A)]
    
    return rotated_to_sph
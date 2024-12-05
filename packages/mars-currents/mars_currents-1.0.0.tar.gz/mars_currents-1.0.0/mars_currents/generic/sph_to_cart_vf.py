import numpy as np
from .cart_to_sph import cart_to_sph

def sph_to_cart_vf(A, th, phi):
    
    #th = np.deg2rad(th); phi = np.deg2rad(phi)
    if isinstance(th, list) and isinstance(phi, list):
        
        points_rot = [cart_to_sph(theta, phii).T for theta, phii in zip(th, phi)]
    #print(points_rot[0])
        rotated_to_cart = [np.dot(rot_m, point) for rot_m, point in zip(points_rot, A)]
    else:
        
        rot_m = cart_to_sph(th, phi).T
        rotated_to_cart = np.dot(rot_m, A)
        
    return rotated_to_cart
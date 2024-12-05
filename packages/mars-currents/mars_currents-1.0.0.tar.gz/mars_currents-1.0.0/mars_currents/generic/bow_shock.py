import numpy as np 
def bow_shock(x0, L, eps, th):
    #x0 = 0.74; L = 1.82; eps = 1.01
    #th = np.linspace(np.deg2rad(-90), np.deg2rad(90), 30)
    return L*(1+eps*np.cos(th))**(-1)
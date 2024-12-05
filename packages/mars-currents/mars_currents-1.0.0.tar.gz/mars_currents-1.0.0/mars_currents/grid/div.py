import numpy as np

def div(center, neighbours, field):
    
    for coordinate in neighbours.keys():
        for direction in neighbours[coordinate].keys():
            if neighbours[coordinate][direction] == None or np.isnan(neighbours[coordinate][direction][field+'r']):
                neighbours[coordinate][direction] = center
    
    th0 = center["th_c"]; r0 = center["r_c"];
    
    divergence = 1/r0*(2*center[field + "r"] \
               + (neighbours["th"][+1][field + "th"] - neighbours["th"][-1][field + "th"])/(neighbours['th'][+1]['th_c'] - neighbours['th'][-1]['th_c'])) + 1/(r0*np.sin(th0))*(np.cos(th0)*center[field + 'th'] \
               + (neighbours['phi'][+1][field + 'phi'] - neighbours['phi'][-1][field + 'phi'])/(neighbours['phi'][+1]['phi_c'] - neighbours['phi'][-1]['phi_c'])) \
               + (neighbours['r'][+1][field + 'r'] - neighbours['r'][-1][field + 'r'])/(neighbours['r'][+1]['r_c'] - neighbours['r'][-1]['r_c'])
    
    return divergence
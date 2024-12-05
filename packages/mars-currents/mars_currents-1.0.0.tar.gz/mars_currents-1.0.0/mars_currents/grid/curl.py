import numpy as np

def curl(center, neighbours, field):
        
    for coordinate in neighbours.keys():
        for direction in neighbours[coordinate].keys():
            if neighbours[coordinate][direction] == None or np.isnan(neighbours[coordinate][direction][field+'r']):
                neighbours[coordinate][direction] = center
    
    th0 = center["th_c"]; r0 = center["r_c"]; 

    curl_r = np.cos(th0)/(r0*np.sin(th0))*center[field + 'phi'] \
           + 1/r0 * (neighbours['th'][+1][field+'phi'] - neighbours['th'][-1][field+'phi'])/(neighbours['th'][+1]['th_c'] - neighbours['th'][-1]['th_c']) \
           - 1/(r0*np.sin(th0)) * (neighbours['phi'][+1][field+'th'] - neighbours['phi'][-1][field+'th'])/(neighbours['phi'][+1]['phi_c'] - neighbours['phi'][-1]['phi_c'])

    curl_th = 1/(r0*np.sin(th0))*(neighbours['phi'][+1][field+'r'] - neighbours['phi'][-1][field+'r'])/(neighbours['phi'][+1]['phi_c'] - neighbours['phi'][-1]['phi_c']) \
            - center[field+'phi']/r0 \
            - (neighbours['r'][+1][field+'phi'] - neighbours['r'][-1][field+'phi'])/(neighbours['r'][+1]['r_c'] - neighbours['r'][-1]['r_c'])

    curl_phi = center[field+'th']/r0 \
             + (neighbours['r'][+1][field+'th'] - neighbours['r'][-1][field+'th'])/(neighbours['r'][+1]['r_c'] - neighbours['r'][-1]['r_c']) \
             - 1/r0 * (neighbours['th'][+1][field+'r'] - neighbours['th'][-1][field+'r'])/(neighbours['th'][+1]['th_c'] - neighbours['th'][-1]['th_c'])

    return [curl_r, curl_th, curl_phi]
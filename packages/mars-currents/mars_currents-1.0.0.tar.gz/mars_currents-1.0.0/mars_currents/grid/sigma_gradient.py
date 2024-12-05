import numpy as np

def sigma_gradient(center, neighbours, field, comp, resp):
    
    for coordinate in neighbours.keys():
        for direction in neighbours[coordinate].keys():
            if neighbours[coordinate][direction] == None or np.isnan(neighbours[coordinate][direction][field+'r']):
                neighbours[coordinate][direction] = center

    sigma_gr = np.sqrt(neighbours[resp][-1]['sigma_'+field+comp]**2 + 2*center['sigma_'+field+comp]**2 + neighbours[resp][+1]['sigma_'+field+comp]**2)/(np.sqrt(2)*center['d'+resp])

    return sigma_gr
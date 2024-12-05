import os
import pickle
from .spherical_grid import Grid

def load_grid(grid_dict = None, load_from_file = False, file_path = None, data = None):
    
    if load_from_file:
            
        if os.path.exists(file_path):
            
            with open(file_path, 'rb') as f:
                
                grid_dict = pickle.load(f)
                data = grid_dict["data"]
                grid_name = f'dr{grid_dict["dr"]}_dth{grid_dict["dth_deg"]}_dphi{grid_dict["dphi_deg"]}'  
        else:

            print(f'File {file_path} not found.')
                
    else:
                
        grid_name = f'dr{grid_dict["dr"]}_dth{grid_dict["dth_deg"]}_dphi{grid_dict["dphi_deg"]}'
        
    return Grid(grid_dict, load_from_file, file_path, data, grid_name)
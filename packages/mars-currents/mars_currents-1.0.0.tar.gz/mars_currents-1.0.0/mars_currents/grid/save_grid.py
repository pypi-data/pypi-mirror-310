import re
import pickle 

def save_grid(grid):

    with open(f"grid_{grid.grid_name}__{re.sub('.csv','', re.sub(r'.*/' ,'', grid.data))}.pickle", "wb") as f:
        grid.grid_to_dict()
        pickle.dump(grid.save_dict, f)
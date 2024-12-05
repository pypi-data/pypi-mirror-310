from .mag_files_list import mag_files_list
import glob

def create_paths(start, end, frame, sampl, data_path, verbose=True):
    
    """Returns a list of paths for the mag files. """
    
    paths = []
    not_exist = []
    for name in mag_files_list(start, end, frame, sampl):
        
        year = name[11:15]; month = name[-12:-10]
        
        file_path = f'{data_path}/{year}/{month}/{name}.sts'
        file_in_path = glob.glob(file_path)
        
        if not bool(file_in_path):
            not_exist.append(file_path)
        elif len(file_in_path)>1:
            paths.append(file_in_path[-1])
        else:
            paths.append(file_in_path[0])
            
    if verbose:
        print('Paths of files: \n', paths)
    
    return [paths, not_exist]
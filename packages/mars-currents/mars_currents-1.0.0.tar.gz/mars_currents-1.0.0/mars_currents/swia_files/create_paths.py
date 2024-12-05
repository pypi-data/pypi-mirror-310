import glob
from .swia_files_list import swia_files_list

def create_paths(start, end, kind, data_path, verbose=True):

    """Returns a list of paths for the swia files. """

    paths = []
    not_exist = []
    for name in swia_files_list(start, end, kind):
                
        name_st = 'mvn_swi_l2_'
        year = name.replace(f'{name_st}{kind}_', '')[:4]
        month = name.replace(f'{name_st}{kind}_{year}', '')[:2]
        day = name.replace(f'{name_st}{kind}_{year}{month}', '')[:2]  
        file_path = f'{data_path}/{year}/{month}/{name}.cdf'
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
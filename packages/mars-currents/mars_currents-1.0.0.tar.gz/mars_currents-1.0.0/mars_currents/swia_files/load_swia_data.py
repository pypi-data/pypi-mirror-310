from .swia_files_list import swia_files_list 
import glob
from ..spice_codes.load_spice_kernels import load_spice_kernels
from cdflib.xarray import cdf_to_xarray
import xarray as xr
import warnings
from .create_paths import create_paths

def load_swia_data(start, end, kind, data_path, kernel_path, resampling = None, verbose=True, thin_n = None):

    load_spice_kernels(kernel_path)
    paths, not_exist = create_paths(start, end, kind, data_path, False)
    
    if verbose:
        print('These files do not exist: \n')
        for no_file in not_exist:
            print(f'{no_file}')
        print('--------------------------------------------------------------------')
    
    if verbose: print('Loading files: \n')
    
    for path in paths:
        if verbose: print("\r", path, end =" ")
        if path==paths[0]:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                
                if resampling is not None:
                    xar0 = cdf_to_xarray(path, to_unixtime=False, to_datetime=True)
                else:
                    xar0 = cdf_to_xarray(path, to_unixtime=False, to_datetime=False)

                
                if resampling is not None:
                    
                    if resampling['mode'] == 'median':
                        
                        xar0 = xar0.resample(epoch=resampling['res_freq']).median(dim ='epoch')
                        
                    else:
                        
                        xar0 = xar0.resample(epoch=resampling['res_freq']).mean(dim ='epoch')
                    
                    
                elif thin_n is not None:
                    
                    xar0 = xar0.thin(indexers = dict(epoch=thin_n))
                    
            if xar0['epoch'].attrs['units']=='ns':
                
                xar0['epoch'].attrs['units'] = 's'; xar0['epoch'].attrs['UNITS'] = 's';
                old_xar_attrs = xar0['epoch'].attrs
                new_t = xar0['epoch'].values*1e-9
                xar0 = xar0.assign_coords(epoch = new_t)
                xar0['epoch'].attrs.update(old_xar_attrs)
                
        else:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                
                if resampling is not None:
                    xar1 = cdf_to_xarray(path, to_unixtime=False, to_datetime=True)
                else:
                    xar1 = cdf_to_xarray(path, to_unixtime=False, to_datetime=False)
                    
                if resampling is not None:
                    
                    if resampling['mode'] == 'median':

                        xar1 = xar1.resample(epoch=resampling['res_freq']).median(dim ='epoch')

                    else:

                        xar1 = xar1.resample(epoch=resampling['res_freq']).mean(dim ='epoch')

                elif thin_n is not None:
                    
                    xar1 = xar1.thin(indexers = dict(epoch=thin_n))
                    
            if xar1.epoch[0] < xar0.epoch[-1]:
                
                xar1 = xar1.where(xar1.epoch>xar0.epoch[-1], drop = True)
            
            if xar1['epoch'].attrs['units']=='ns':
                xar1['epoch'].attrs['units'] = 's'; xar1['epoch'].attrs['UNITS'] = 's';
                old_xar_attrs = xar1['epoch'].attrs
                new_t = xar1['epoch'].values*1e-9
                xar1 = xar1.assign_coords(epoch = new_t)
                xar1['epoch'].attrs.update(old_xar_attrs)
            
            xar0 = xr.combine_by_coords(data_objects = [xar0, xar1], combine_attrs='override')#, compat = 'override',)# coords= 'all')
    
    return xar0
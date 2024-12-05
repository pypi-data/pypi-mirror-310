from ..time_operations import datetime2doy
from ..time_operations import reduce_date_time
from ..time_operations import time
from ..time_operations import yearisLeap
from ..time_operations import year_doy2date_str


def _mag_file_name(date_time, frame, sampl = ''):

    """Outputs the mag l2_v01_r01 file name, given the date, time, frame of reference and sampling rate."""

    day_of_year = datetime2doy(date_time, out = 'str')
    year, month, day = reduce_date_time(date_time)[0:3]

    name = f'mvn_mag_l2_{year}{day_of_year}{frame}{sampl}_{year}{month}{day}_v**_r**' 
    
    return name

def mag_files_list(start, end, frame, sampl):

    t = time(start)
    finish = time(end)
    list_file_names = []
   
    while int(t.doy) <= int(finish.doy) or t.year<finish.year:

        date_time = year_doy2date_str(t.year, t.doy)
        date_str = f'{date_time}'
        list_file_names.append(_mag_file_name(date_str, frame, sampl))
        
        if t.doy >= int(yearisLeap(t.year))+365: 
            
            t.year +=1
            t.doy = 0

        t.doy = int(t.doy)+1

    return list_file_names

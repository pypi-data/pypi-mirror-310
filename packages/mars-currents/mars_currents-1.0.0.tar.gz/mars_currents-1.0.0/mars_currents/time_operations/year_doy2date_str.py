from .doy2datetime import doy2datetime
        
def year_doy2date_str(year, doy):#, fmt='YYYY-MM-DDTHH:MM:SC.####'):
    # year_str=str(int(year))
    year, month, day, hour, minutes, sec= doy2datetime(int(year), doy)
    return f'{year}-{month}-{day}T{hour}:{minutes}:{sec}'
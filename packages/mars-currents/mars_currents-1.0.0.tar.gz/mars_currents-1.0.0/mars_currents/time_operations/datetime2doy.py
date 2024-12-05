from .reduce_date_time import reduce_date_time
from .days_in_months import days_in_months
import numpy as np

def datetime2doy(date_time, out = 'str'):

    """Convert date from YYYY-MM-DDTHH:MM:SC.### format to day of the year. If out = 'str' returns the numpy.floor(doy)
    as a string. If out is not 'str' it returns the day of year as a decimal day."""

    year, month, day, hour, minute, sec = reduce_date_time(date_time)
    months_days = days_in_months(int(year))
    hour_in_sec = float(hour)*3600.0
    min_in_sec = float(minute)*60.0
    total_sec = hour_in_sec + min_in_sec + float(sec)
    sec_in_days = total_sec/86400.0
    day_of_year =  np.nansum([days for days in months_days.values()][:int(month)-1]) + float(day) + sec_in_days
    if out == 'str':

        if day_of_year >= 100:
            day_of_year = str(int(day_of_year))
        elif day_of_year < 100 and day_of_year >= 10:
            day_of_year = '0' + str(int(day_of_year))
        else:
            day_of_year = '00' + str(int(day_of_year))

    return day_of_year
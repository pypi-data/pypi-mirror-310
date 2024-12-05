
def reduce_date_time(date_time:str, out = 'str'):

    """Extract year, month, day, hour, minute, sec values from date, time in format YYYY-MM-DD-THH:MM:SC.###.
    Output is a list of the above in string type if out = 'str' (Default value), otherwise it returns a list
    of the above in float type."""

    year, month, day_time= date_time.split('-')
    day, time = day_time.split('T')
    hour, minute, sec = time.split(':')
    date_time_list = [year, month, day, hour, minute, sec]

    if out == 'str':
        return date_time_list
    
    return [float(x) for x in date_time_list]
from .datetime2doy import datetime2doy
from .reduce_date_time import reduce_date_time

class time:

    """Time class with year, month, day, hour, minute, sec and day_of_year as attributes (float)"""

    def __init__(self, date_time):
        self.year, self.month, self.day, self.hour, self.minute, self.sec = reduce_date_time(date_time, out='float')
        self.doy = datetime2doy(date_time, out = 'float')
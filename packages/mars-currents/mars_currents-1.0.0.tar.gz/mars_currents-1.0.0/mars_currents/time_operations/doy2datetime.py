from .days_in_months import days_in_months
import numpy as np

def doy2datetime(year, doy):

    """Takes year (float) and decimal day (float) of year and returns year, month, day, hour, decimal sec as strings, to be
     used in YYYY-MM-DD-THH:MM:SC.### format, by doy2date."""
    
    months_keys = [key for key in days_in_months(year).keys()]
    
    months_days = [value for value in days_in_months(year).values()]
    
    days = doy - months_days[0]
    month_i=0
    while days>0:
        month_i += 1
        days = days - months_days[month_i]

    month = int(months_keys[month_i])

    day_of_month_dec = days + months_days[month_i]
    day_of_month = int(days + months_days[month_i])

    hour_dec = (day_of_month_dec - day_of_month)*24
    hour = int(hour_dec)

    minutes_dec = (hour_dec - hour)*60
    minutes = int(minutes_dec)

    sec = np.around((minutes_dec-minutes)*60, 4)
    if sec==60:
        if minutes+1==60:
            if hour+1==24:
                if day_of_month+1==months_days[month_i]:
                    if month+1==13:
                        year=year+1; month = '1'; day_of_month=1; hour=0; minutes=0; sec=0.0
                    else:
                        month +=1; day_of_month=1; hour=0; minutes=0; sec=0.0
                else:
                    day_of_month +=1; hour=0; minutes=0; sec=0.0
            else:
                hour +=1; minutes=0; sec=0.0
        else:
            minutes +=1; sec=0.0

    if (sec*10).is_integer(): 
        sec = str(sec)+'00'
    elif (sec*100).is_integer():
        sec = str(sec)+'0'
    else:
        sec = str(sec)
    
    return str(year), ('0'+str(month))[-2:], ('0'+str(day_of_month))[-2:], ('0'+str(hour))[-2:], ('0'+str(minutes))[-2:], ('0'+sec)[-6:]
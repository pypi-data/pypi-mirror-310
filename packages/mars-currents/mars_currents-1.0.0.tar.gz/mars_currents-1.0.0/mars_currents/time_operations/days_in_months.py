from .yearisLeap import yearisLeap

def days_in_months(year):
    if yearisLeap(int(year)): 
        Feb_days=29
    else:
        Feb_days=28
    months_days = {'01':31 , '02':Feb_days, '03':31, '04':30, '05':31, '06':30, '07':31, '08':31, '09':30,
                   '10':31, '11':30, '12':31}
    return months_days
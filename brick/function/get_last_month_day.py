# -*- coding: utf-8 -*-
#取上个月的时间

from datetime import date
import datetime

def get_last_month_day():
    d = date.today()
    year = d.year
    month = d.month
    day = d.day + 1
    month -= 1
    if month == 0 :
        month = 12
        year -= 1
    elif month == 2:
        day = 29 if year % 4 == 0 else 28
    elif month in (4,6,9,11):
        if day == 31:
            day = 1
    else:
        if day == 32:
            day = 1
    result = datetime.datetime(year,month,day).strftime('%Y-%m-%d')
    print result
    return result
get_last_month_day()
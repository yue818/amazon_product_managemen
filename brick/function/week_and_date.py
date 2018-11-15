# coding=utf-8

import datetime



def getweekmsg(strdate):
    """
    给定日期的字符串格式，输出该日期的周数
    :param strdate: 日期的字符串格式
    :return:
    """
    date_input = datetime.datetime.strptime(strdate, '%Y%m%d')
    weekmsg = date_input.isocalendar()
    return weekmsg
    ####strdate为字符串格式，如20140828  输出为(2014, 35, 4)


# weekflag格式为201435（即2014年第35周）
def get_day_range(strweek):
    """
    输入周数字符串，获得该周开始和结束日期
    :param strweek:
    :return:
    """
    yearnum = strweek[0:4]  # 取到年份
    weeknum = strweek[4:6]  # 取到周
    stryearstart = yearnum + '0101'  # 当年第一天
    yearstart = datetime.datetime.strptime(stryearstart, '%Y%m%d')  # 格式化为日期格式
    yearstartcalendarmsg = yearstart.isocalendar()  # 当年第一天的周信息
    # yearstartweek = yearstartcalendarmsg[1]
    yearstartweekday = yearstartcalendarmsg[2]
    yearstartyear = yearstartcalendarmsg[0]
    if yearstartyear < int(yearnum):
        daydelat = (8 - int(yearstartweekday)) + (int(weeknum) - 1) * 7
    else:
        daydelat = (8 - int(yearstartweekday)) + (int(weeknum) - 2) * 7

    week_start = (yearstart + datetime.timedelta(days=daydelat)).date()
    week_end = week_start + datetime.timedelta(7)
    return str(week_start), str(week_end)
    # 输出2014年第35周的开始时间
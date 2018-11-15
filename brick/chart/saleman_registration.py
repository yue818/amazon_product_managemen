# -*- coding: utf-8 -*-

from django.db import connection
import datetime
import sys
# import MySQLdb

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

DATABASES = {
    'PORT': '3306',
    'NAME': 'hq_db',
    'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
    'USER': 'by15161458383',
    'PASSWORD': 'K120Esc1'
}

DEPARTMENT_DICT = {
    '1': u'一部',
    '2': u'二部',
    '3': u'三部',
    '4': u'四部',
    '5': u'五部',
}

CHOICECATEGORY = {
    'researched': 'onesurvey',
    'entered': 'onetimelanding',
    'published': 'twopublication',
    'userd': 'twotimecollardosage',
    'restart': 'publishrestarts',
}

MONTH_DAY = {
    '1': 'FirstDay',
    '2': 'SecondDay',
    '3': 'ThirdDay',
    '4': 'FourthDay',
    '5': 'FifthDay',
    '6': 'SixthDay',
    '7': 'SeventhDay',
    '8': 'EighthDay',
    '9': 'NinthDay',
    '10': 'TenthDay',
    '11': 'EleventhDay',
    '12': 'TwelfthDay',
    '13': 'ThirteenthDay',
    '14': 'FourteenthDay',
    '15': 'FifteenthDay',
    '16': 'SixteenthDay',
    '17': 'SeventeenthDay',
    '18': 'EighteenthDay',
    '19': 'NineteenthDay',
    '20': 'TwentiethDay',
    '21': 'TwentyFirstDay',
    '22': 'TwentySecondDay',
    '23': 'TwentyThirdDay',
    '24': 'TwentyFourthDay',
    '25': 'TwentyFifthDay',
    '26': 'TwentySixthDay',
    '27': 'TwentySeventhDay',
    '28': 'TwentyEighthDay',
    '29': 'TwentyNinthDay',
    '30': 'ThirtiethDay',
    '31': 'ThirtiethFirstDay',
}

# try:
#     db_conn = MySQLdb.connect(DATABASES['HOST'], DATABASES['USER'], DATABASES['PASSWORD'], DATABASES['NAME'], charset="utf8")
# except Exception as e:
#     error = 'Connect mysql db error %s' % e
#     print error

def getYesterday():
    # 获取昨天的日期
    today=datetime.date.today()
    oneday=datetime.timedelta(days=1)
    yesterday=today-oneday
    return yesterday

def get_db_info(sql):
    # 执行SELECT并将数据整理成列表嵌套字典的类型返回
    print 'execute sql: ', sql
    cursor = connection.cursor()
    # cursor = db_conn.cursor()
    cursor.execute(sql)
    columns = cursor.description
    result = []
    for value in cursor.fetchall():
        tmp = {}
        for (index,column) in enumerate(value):
            tmp[columns[index][0]] = column
        result.append(tmp)

    cursor.close()
    return result

def execute_db(sql):
    # 执行INSERT or UPDATE
    print 'execute sql: ', sql
    try:
        cursor = connection.cursor()
        # cursor = db_conn.cursor()
        cursor.execute(sql)
        cursor.execute('commit;')
        cursor.close()
        return True
    except Exception as e:
        print 'execute sql error: %s' % e
        return False

def get_research_info(day):
    # 一次调研
    sql = "SELECT KFStaffName,COUNT(1) as Num FROM t_product_enter_ed WHERE KFTime='%s' GROUP BY KFStaffName;" % (day)
    entered_info = get_db_info(sql)
    sql = "SELECT KFStaffName,COUNT(1) as Num FROM v_product_allsku" \
          " WHERE KFTime='%s' AND T IN ('信息审核', '正在建资料', '正在开发', " \
          "'正在询价', '信息录入', '调研审核', '正在调研', '已调研待开发', '已开发待询价', '信息领取') " \
          "GROUP BY KFStaffName;" % (day)
    not_enter_info = get_db_info(sql)

    research_info = entered_info + not_enter_info
    research_dict = dict()
    for i in research_info:
        if i['KFStaffName'] not in research_dict.keys():
            research_dict[i['KFStaffName']] = i['Num']
        else:
            research_dict[i['KFStaffName']] += i['Num']
    return research_dict
 
def get_enter_info(day):
    # 一次落地
    sql = "SELECT KFStaffName,COUNT(1) as Num FROM t_product_enter_ed WHERE LRTime='%s' GROUP BY KFStaffName;" % (day)
    enter_info = get_db_info(sql)
    enter_dict = dict()
    for i in enter_info:
        enter_dict[i['KFStaffName']] = i['Num']
    return enter_dict

def get_published_info(day):
    # 一次刊登
    sql = "SELECT PublishedInfo from t_product_depart_get WHERE PublishedInfo LIKE '%s';" % ('%'+str(day)+'%')
    published_info = get_db_info(sql)
    published_dict = dict()
    for p_info in published_info:
        for i in p_info['PublishedInfo'].split(';'):
            Pub = i.split(',')
            Pub_T = Pub[0].split('-')
            name = ''
            if len(Pub_T)>=2:
                name = Pub_T[1]
                if name in published_dict.keys():
                    published_dict[name] += 1
                else:
                    published_dict[name] = 1
            
    return published_dict

def get_used_info(day):
    # 一次领用
    sql = "SELECT StaffName,COUNT(1) as Num FROM t_product_depart_get WHERE LYTime LIKE '%s' GROUP BY StaffName;" % (str(day)+'%')
    used_info = get_db_info(sql)
    used_dict = dict()
    for i in used_info:
        used_dict[i['StaffName']] = i['Num']
    return used_dict

def get_publish_restart_info(day):
    # 刊登重启量
    day = day + '%'
    sql = "SELECT Seller,COUNT(1) as Num from t_online_info_wish WHERE DateUploaded='%s' GROUP BY Seller;" % (day)
    publish_restart_info = get_db_info(sql)
    publish_restart_dict = dict()
    for i in publish_restart_info:
        publish_restart_dict[i['Seller']] = i['Num']
    return publish_restart_dict

def get_user_department(users):
    # 用户部门关系
    user_department_dict = dict()
    for user in users:
        sql = "SELECT DISTINCT Department from t_store_configuration_file " \
              "WHERE Seller='%s' OR Operators='%s' OR Submitter='%s';" % (user, user, user)
        user_department_info = get_db_info(sql)
        user_department_dict[user] = ''
        for i in user_department_info:
            if not i['Department']:
                user_department_dict[user] = DEPARTMENT_DICT[str(i['Department'])]
                break
    return user_department_dict

def update_info(username, num, day, month, year, category, department):
    # 跟新或者新建数据记录
    sql = "SELECT id from not_clothing_salesman_registration WHERE " \
        "Salesperson='%s' AND ThisMonth='%s' AND ThisYear='%s' AND Category='%s';" % (username, month, year, category)
    info_exist = get_db_info(sql)
    if not info_exist:
        sql = "INSERT INTO not_clothing_salesman_registration " \
            "(Category, Department, Salesperson, ThisMonth, ThisYear, %s, LatestRevisionTime) " \
            "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (MONTH_DAY[str(day)], category, department, username, month, year, num, datetime.datetime.now())
        res = execute_db(sql)
    else:
        sql = "UPDATE not_clothing_salesman_registration SET %s='%s', LatestRevisionTime='%s' " \
            "WHERE Salesperson='%s' AND ThisMonth='%s' AND ThisYear='%s' AND Category='%s' AND Department='%s';" % (MONTH_DAY[str(day)], num, datetime.datetime.now(), username, month, year, category, department)
        res = execute_db(sql)

def create_all_user_registration(username, month, year, category, department):
    # 跟新或者新建数据记录
    sql = "SELECT id from not_clothing_salesman_registration WHERE " \
        "Salesperson='%s' AND ThisMonth='%s' AND ThisYear='%s' AND Category='%s';" % (username, month, year, category)
    info_exist = get_db_info(sql)
    if not info_exist:
        sql = "INSERT INTO not_clothing_salesman_registration " \
            "(Category, Department, Salesperson, ThisMonth, ThisYear, LatestRevisionTime) " \
            "VALUES ('%s', '%s', '%s', '%s', '%s', '%s');" % (category, department, username, month, year, datetime.datetime.now())
        res = execute_db(sql)

def get_sellers():
    # 获取销售员人员列表
    sql = "SELECT DISTINCT Seller from t_store_configuration_file;"
    sellers = get_db_info(sql)
    seller_list = list()
    for seller in sellers:
        if seller['Seller'] in ['N/A', 'suspended']:
            continue
        if seller['Seller']:
            seller_list.append(seller['Seller'])
            # name = seller['Seller'].split(',')
            # name = seller['Seller'].split(u'\uff0c')
            # for i in name:
            #     if i and i not in seller_list:
            #         seller_list.append(i.strip())

    return seller_list

def saleman_registration(yesterday=None):
    # 信息统计
    if not yesterday:
        yesterday = getYesterday()
    research_info = get_research_info(yesterday.strftime('%Y-%m-%d'))
    enter_info = get_enter_info(yesterday.strftime('%Y-%m-%d'))
    published_info = get_published_info(yesterday.strftime('%Y-%m-%d'))
    used_info = get_used_info(yesterday.strftime('%Y-%m-%d'))
    publish_restart_info = get_publish_restart_info(yesterday.strftime('%Y-%m-%d'))
    sellers = get_sellers()
    year = yesterday.year
    month = yesterday.month
    if len(str(month)) < 2:
        month = '0' + str(month)
    day = yesterday.day

    # 每个月1号生成所有的销售员当月报表
    if str(day) == '1':
        all_user_department = get_user_department(sellers)
        for user in sellers:
            for k, v in CHOICECATEGORY.items():
                create_all_user_registration(user, month, year, v, all_user_department[user])

    # 去除非销售人员的信息
    for name in research_info.keys():
        if name not in sellers:
            research_info.pop(name)
    for name in enter_info.keys():
        if name not in sellers:
            enter_info.pop(name)
    for name in published_info.keys():
        if name not in sellers:
            published_info.pop(name)
    for name in used_info.keys():
        if name not in sellers:
            used_info.pop(name)
    for name in publish_restart_info.keys():
        if name not in sellers:
            publish_restart_info.pop(name)

    users = research_info.keys() + enter_info.keys() + published_info.keys() + used_info.keys()
    users = list(set(users))
    user_department_info = get_user_department(users)

    if research_info:
        for k, v in research_info.items():
            user_department = user_department_info.get(k)
            update_info(k, v, day, month, year, CHOICECATEGORY['researched'], user_department)
    if enter_info:
        for k, v in enter_info.items():
            user_department = user_department_info.get(k)
            update_info(k, v, day, month, year, CHOICECATEGORY['entered'], user_department)
    if published_info:
        for k, v in published_info.items():
            user_department = user_department_info.get(k)
            update_info(k, v, day, month, year, CHOICECATEGORY['published'], user_department)
    if used_info:
        for k, v in used_info.items():
            user_department = user_department_info.get(k)
            update_info(k, v, day, month, year, CHOICECATEGORY['userd'], user_department)
    if publish_restart_info:
        for k, v in publish_restart_info.items():
            user_department = user_department_info.get(k)
            update_info(k, v, day, month, year, CHOICECATEGORY['restart'], user_department)

def dateRange(start, end, step=1, format="%Y-%m-%d"):
    # 获取日期列表, 返回日期范围包含start, 不包含end
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    days = (strptime(end, format) - strptime(start, format)).days
    return [strftime(strptime(start, format) + datetime.timedelta(i), format) for i in xrange(0, days, step)]

# 批量统计历史记录
# days = dateRange("2018-01-01", "2018-02-05")
# print days
# for yesterday in days:
#     yesterday = datetime.datetime.strptime(yesterday, '%Y-%m-%d')
#     saleman_registration(yesterday)

# yesterday = getYesterday()
# saleman_registration(yesterday=yesterday)
# db_conn.close()
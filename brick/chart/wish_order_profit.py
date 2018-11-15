# -*- coding: utf-8 -*-

from django.db import connection
from brick.function import week_and_date
import MySQLdb
import datetime
import sys
import os

DATABASES = {
    'PORT': '3306',
    'NAME': 'hq_db',
    'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
    'USER': 'by15161458383',
    'PASSWORD': 'K120Esc1'
}

REFUND_ORDER_STATE = (
    'CANCELLED BY CUSTOMER',
    'CANCELLED BY WISH (FLAGGED TRANSACTION)',
    'REFUNDED',
    'REFUNDED BY MERCHANT',
    'REFUNDED BY WISH',
    'REFUNDED BY WISH FOR MERCHANT'
)

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

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

def month_week_str(data):
    m_w = lambda x: '0'+str(x) if len(str(x)) < 2 else str(x)
    return m_w(data)

def is_leap_year(year):
    if year % 400 == 0 or year % 4 ==0 and year % 100 != 0:
        return True
    else:
        return False

def get_week_month_to_update_profit(days, shop_name_list=None):
    datetime_list = list(map(lambda x:datetime.datetime.strptime(x, '%Y-%m-%d').strftime('%Y%m%d'), days))
    # 去重年月
    month_dict = dict()
    map(lambda x:month_dict.update({x[0:6]: datetime.datetime.strptime(x, '%Y%m%d')}), datetime_list)
    month_list = month_dict.values()
    # 获取日期所在周
    week_list = list(map(lambda x:week_and_date.getweekmsg(x), datetime_list))
    # 去重周
    weeks = list()
    for i in week_list:
        week = month_week_str(i[1])
        yearweek = str(i[0]) + week
        if yearweek not in weeks:
            weeks.append(yearweek)
    week_range = dict()
    map(lambda x:week_range.update({x: week_and_date.get_day_range(x)}), weeks)

    #WEEK PROFIT
    for i in week_range:
        sd, ed = week_range[i]
        if shop_name_list:
            for shopname in shop_name_list:
                update_week_month_shop_profit(sd ,ed, 'week', shopname)
        else:
            update_week_month_all_profit(sd ,ed, 'week')

    #MONTH PROFIT
    for i in month_list:
        the_year = str(i.year)
        the_month = month_week_str(i.month)
        if the_month in ['01', '03', '05', '07', '08', '10', '12']:
            the_month_range = (the_year+'-'+the_month+'-'+'01', the_year+'-'+the_month+'-'+'31')
        elif the_month in ['04', '06', '09', '11']:
            the_month_range = (the_year+'-'+the_month+'-'+'01', the_year+'-'+the_month+'-'+'30')
        else:
            if is_leap_year(i.year):
                the_month_range = (the_year+'-'+the_month+'-'+'01', the_year+'-'+the_month+'-'+'29')
            else:
                the_month_range = (the_year+'-'+the_month+'-'+'01', the_year+'-'+the_month+'-'+'28')
        sd, ed = the_month_range
        if shop_name_list:
            for shopname in shop_name_list:
                update_week_month_shop_profit(sd ,ed, 'month', shopname)
        else:
            update_week_month_all_profit(sd ,ed, 'month')

def update_week_month_all_profit(sd ,ed, pro_type):
    get_price = lambda x: float(x) if x else 0.0
    select_sql = "SELECT SUM(SalesPrice) AS SalesPrice, SUM(Profit) AS Profit FROM t_chart_wish_all_profit " \
        "WHERE StartDate>='%s' AND EndDate<='%s' AND Period='%s';" % (sd, ed, 'day')
    res = get_db_info(select_sql)
    if not res:
        return
    else:
        sp = 0.0
        pf = 0.0
        for j in res:
            sp += get_price(j['SalesPrice'])
            pf += get_price(j['Profit'])
        if not sp == 0.0:
            pfr = pf / sp
        else:
            pfr = 0.0
        pfr = '%.2f' % (pfr * 100)
        sele_sql = "SELECT id FROM t_chart_wish_all_profit " \
            "WHERE StartDate='%s' AND EndDate='%s' AND Period='%s';" % ((sd, ed, pro_type))
        res = get_db_info(sele_sql)
        if res:
            sql = "UPDATE t_chart_wish_all_profit SET SalesPrice=%s, Profit=%s, ProfitRate=%s " \
                "WHERE StartDate='%s' AND EndDate='%s' AND Period='%s';" % (sp, pf, pfr, sd, ed, pro_type)
        else:
            sql = "INSERT INTO t_chart_wish_all_profit (SalesPrice, Profit, ProfitRate, StartDate, EndDate, Period) " \
                "VALUES (%s, %s, %s, '%s', '%s', '%s');" % (sp, pf, pfr, sd, ed, pro_type)
        execute_db(sql)

def update_week_month_shop_profit(sd ,ed, pro_type, shopname):
    get_price = lambda x: float(x) if x else 0.0
    select_sql = "SELECT SUM(SalesPrice) AS SalesPrice, SUM(Profit) AS Profit FROM t_chart_wish_shop_profit " \
        "WHERE ShopName='%s' AND StartDate>='%s' AND EndDate<='%s' AND Period='%s';" % (shopname, sd, ed, 'day')
    res = get_db_info(select_sql)
    if not res:
        return
    else:
        sp = 0.0
        pf = 0.0
        for j in res:
            sp += get_price(j['SalesPrice'])
            pf += get_price(j['Profit'])
        if not sp == 0.0:
            pfr = pf / sp
        else:
            pfr = 0.0
        pfr = '%.2f' % (pfr * 100)
        sele_sql = "SELECT id FROM t_chart_wish_shop_profit " \
            "WHERE ShopName='%s' AND StartDate='%s' AND EndDate='%s' AND Period='%s';" % (shopname, sd, ed, pro_type)
        res = get_db_info(sele_sql)
        if res:
            sql = "UPDATE t_chart_wish_shop_profit SET SalesPrice=%s, Profit=%s, ProfitRate=%s " \
                "WHERE StartDate='%s' AND EndDate='%s' AND Period='%s' AND ShopName='%s';" % (sp, pf, pfr, sd, ed, pro_type, shopname)
        else:
            sql = "INSERT INTO t_chart_wish_shop_profit (SalesPrice, Profit, ProfitRate, StartDate, EndDate, Period, ShopName) " \
                "VALUES (%s, %s, %s, '%s', '%s', '%s', '%s');" % (sp, pf, pfr, sd, ed, pro_type, shopname)
        execute_db(sql)

def generate_all_profit(order_info, rate):
    order_date_dict = dict()
    # rate = get_rate()
    for i in order_info:
        date = i['OrderDate'].split('T')[0]
        if order_date_dict.get(date):
            order_date_dict[date].append(i)
        else:
            order_date_dict[date] = list()
            order_date_dict[date].append(i)
    for k, v in order_date_dict.items():
        saleprice = float()
        costprice = float()
        refundprice = float()
        profit = float()
        profitrate = float()
        for i in v:
            if i['OrderState'] in REFUND_ORDER_STATE:
                sp = (i['Price'] + i['Shipping']) * i['Quantity'] * rate
                refundprice += sp + i['PackFee'] + (sp * 0.15)
                continue
            saleprice += (i['Price'] + i['Shipping']) * i['Quantity'] * rate
            costprice += i['CostPrice'] + i['PackFee']
        costprice += saleprice * 0.15
        profit = saleprice - costprice - refundprice
        if not saleprice == 0.0:
            profitrate = profit / saleprice
        else:
            profitrate = 0.0
        profitrate = '%.2f' % (profitrate * 100)
        sql = "SELECT * FROM t_chart_wish_all_profit WHERE StartDate='%s' AND EndDate='%s' AND Period='%s';" % (k, k, 'day')
        all_profit_date_obj = get_db_info(sql)
        if not all_profit_date_obj:
            sql = "INSERT INTO t_chart_wish_all_profit (StartDate, EndDate, SalesPrice, Profit, ProfitRate, Period) " \
                "VALUES ('%s', '%s', %s, %s, %s, '%s');" % (k, k, saleprice, profit, profitrate, 'day')
            execute_db(sql)
        else:
            saleprice += float(all_profit_date_obj[0]['SalesPrice'])
            profit += float(all_profit_date_obj[0]['Profit'])
            if not saleprice == 0.0:
                profitrate = profit / saleprice
            else:
                profitrate = 0.0
            profitrate = '%.2f' % (profitrate * 100)
            sql = "UPDATE t_chart_wish_all_profit SET SalesPrice=%s, Profit=%s, ProfitRate=%s " \
                "WHERE StartDate='%s' AND EndDate='%s' AND Period='%s';" % (saleprice, profit, profitrate, k, k, 'day')
            execute_db(sql)
    return order_date_dict.keys()
    # get_week_month_to_update_profit(order_date_dict.keys(), shop_name_list=None)

def generate_shop_profit(order_info, rate):
    order_date_dict = dict()
    # rate = get_rate()
    for i in order_info:
        date = i['OrderDate'].split('T')[0]
        if order_date_dict.get(date):
            if order_date_dict[date].get(i['ShopName']):
                order_date_dict[date][i['ShopName']].append(i)
            else:
                order_date_dict[date][i['ShopName']] = list()
                order_date_dict[date][i['ShopName']].append(i)
        else:
            order_date_dict[date] = dict()
            order_date_dict[date][i['ShopName']] = list()
            order_date_dict[date][i['ShopName']].append(i)

    shop_name_list = list()
    for k, v in order_date_dict.items():
        for shopname, pro_info in v.items():
            if shopname not in shop_name_list:
                shop_name_list.append(shopname)
            saleprice = float()
            costprice = float()
            refundprice = float()
            profit = float()
            profitrate = float()
            for i in pro_info:
                if i['OrderState'] in REFUND_ORDER_STATE:
                    sp = (i['Price'] + i['Shipping']) * i['Quantity'] * rate
                    refundprice += sp + i['PackFee'] + (sp * 0.15)
                    continue
                saleprice += (i['Price'] + i['Shipping']) * i['Quantity'] * rate
                costprice += i['CostPrice'] + i['PackFee']
            costprice += saleprice * 0.15
            profit = saleprice - costprice - refundprice
            if not saleprice == 0.0:
                profitrate = profit / saleprice
            else:
                profitrate = 0.0
            profitrate = '%.2f' % (profitrate * 100)
            sql = "SELECT * FROM t_chart_wish_shop_profit WHERE " \
                "ShopName='%s' AND StartDate='%s' AND EndDate='%s' AND Period='%s';" % (shopname, k, k, 'day')
            all_profit_date_obj = get_db_info(sql)
            if not all_profit_date_obj:
                sql = "INSERT INTO t_chart_wish_shop_profit (StartDate, EndDate, SalesPrice, Profit, ProfitRate, Period, ShopName) " \
                    "VALUES ('%s', '%s', %s, %s, %s, '%s', '%s');" % (k, k, saleprice, profit, profitrate, 'day', shopname)
                execute_db(sql)
            else:
                saleprice += float(all_profit_date_obj[0]['SalesPrice'])
                profit += float(all_profit_date_obj[0]['Profit'])
                if not saleprice == 0.0:
                    profitrate = profit / saleprice
                else:
                    profitrate = 0.0
                profitrate = '%.2f' % (profitrate * 100)
                sql = "UPDATE t_chart_wish_shop_profit SET SalesPrice=%s, Profit=%s, ProfitRate=%s " \
                    "WHERE ShopName='%s' AND StartDate='%s' AND EndDate='%s' AND Period='%s';" % (saleprice, profit, profitrate, shopname, k, k, 'day')
                execute_db(sql)
    return order_date_dict.keys(), shop_name_list
    # get_week_month_to_update_profit(order_date_dict.keys(), shop_name_list=shop_name_list)

def genrate_week_month_all_notes(firstday):
    week_first_day = []
    year = firstday.year
    day_flag = firstday
    while year == day_flag.year:
        week_first_day.append(day_flag.strftime('%Y%m%d'))
        day_flag += datetime.timedelta(7)
    week_first_day.append((day_flag+datetime.timedelta(7)).strftime('%Y%m%d'))
    week_list = list(map(lambda x:week_and_date.getweekmsg(x), week_first_day))
    weeks = list()
    for i in week_list:
        week = month_week_str(i[1])
        yearweek = str(i[0]) + week
        if yearweek not in weeks:
            weeks.append(yearweek)
    week_range = dict()
    map(lambda x:week_range.update({x: week_and_date.get_day_range(x)}), weeks)
    genrate_initialization_db_info(week_range, 'week')
    month_range = dict()
    for i in range(12):
        month = month_week_str(i+1)
        if month in ['01', '03', '05', '07', '08', '10', '12']:
            month_range[month] = (str(year)+'-'+month+'-'+'01', str(year)+'-'+month+'-'+'31')
        elif month in ['04', '06', '09', '11']:
            month_range[month] = (str(year)+'-'+month+'-'+'01', str(year)+'-'+month+'-'+'30')
        else:
            if is_leap_year(year):
                month_range[month] = (str(year)+'-'+month+'-'+'01', str(year)+'-'+month+'-'+'29')
            else:
                month_range[month] = (str(year)+'-'+month+'-'+'01', str(year)+'-'+month+'-'+'28')
    genrate_initialization_db_info(month_range, 'month')

def genrate_week_month_shop_notes(firstday, shop_names):
    week_first_day = []
    year = firstday.year
    day_flag = firstday
    while year == day_flag.year:
        week_first_day.append(day_flag.strftime('%Y%m%d'))
        day_flag += datetime.timedelta(7)
    week_first_day.append((day_flag+datetime.timedelta(7)).strftime('%Y%m%d'))
    week_list = list(map(lambda x:week_and_date.getweekmsg(x), week_first_day))
    weeks = list()
    for i in week_list:
        week = month_week_str(i[1])
        yearweek = str(i[0]) + week
        if yearweek not in weeks:
            weeks.append(yearweek)
    week_range = dict()
    map(lambda x:week_range.update({x: week_and_date.get_day_range(x)}), weeks)
    for sp in shop_names:
        genrate_initialization_db_info(week_range, 'week', shopname=sp)
    month_range = dict()
    for i in range(12):
        month = month_week_str(i+1)
        if month in ['01', '03', '05', '07', '08', '10', '12']:
            month_range[month] = (str(year)+'-'+month+'-'+'01', str(year)+'-'+month+'-'+'31')
        elif month in ['04', '06', '09', '11']:
            month_range[month] = (str(year)+'-'+month+'-'+'01', str(year)+'-'+month+'-'+'30')
        else:
            if is_leap_year(year):
                month_range[month] = (str(year)+'-'+month+'-'+'01', str(year)+'-'+month+'-'+'29')
            else:
                month_range[month] = (str(year)+'-'+month+'-'+'01', str(year)+'-'+month+'-'+'28')
    for sp in shop_names:
        genrate_initialization_db_info(month_range, 'month', shopname=sp)

def genrate_initialization_db_info(data, data_type, shopname=None):
    if not shopname:
        for i in data:
            sd, ed = data[i]
            select_sql = "SELECT id FROM t_chart_wish_all_profit " \
                "WHERE StartDate='%s' AND EndDate='%s' AND Period='%s';" % (sd, ed, data_type)
            res = get_db_info(select_sql)
            if not res:
                insert_sql = "INSERT INTO t_chart_wish_all_profit (StartDate, EndDate, Period) " \
                    "VALUES ('%s', '%s', '%s');" % (sd, ed, data_type)
                execute_db(insert_sql)
    else:
        for i in data:
            sd, ed = data[i]
            select_sql = "SELECT id FROM t_chart_wish_shop_profit " \
                "WHERE ShopName='%s' AND StartDate='%s' AND EndDate='%s' AND Period='%s';" % (shopname, sd, ed, data_type)
            res = get_db_info(select_sql)
            if not res:
                insert_sql = "INSERT INTO t_chart_wish_shop_profit (ShopName, StartDate, EndDate, Period) " \
                    "VALUES ('%s', '%s', '%s', '%s');" % (shopname, sd, ed, data_type)
                execute_db(insert_sql)

def get_order_info(orderids):
    if len(orderids) > 1:
        orderid_list = '\', \''.join(orderids)
        orderid_list = '\'' + orderid_list + '\''
        orderid_list = orderid_list.replace('\\', '\\\\')
    elif len(orderids) == 1:
        orderid_list = '\'' + orderids[0] + '\''
        orderid_list = orderid_list.replace('\\', '\\\\')
    else:
        return None
    sql = "SELECT OrderId, OrderState, SKU, ShopSKU, ShopName, ProductID, OrderDate, Quantity, Price, Shipping " \
        "FROM t_order WHERE Orderid IN (%s);" % orderid_list
    order_info = get_db_info(sql)
    for i in order_info:
        i['Quantity'] = int(i['Quantity'])
        i['Price'] = float(i['Price'])
        i['Shipping'] = float(i['Shipping'])
    return order_info

def get_order_sku(shopsku):
    if len(shopsku) > 1:
        shopsku_list = '\', \''.join(shopsku)
        shopsku_list = '\'' + shopsku_list + '\''
        shopsku_list = shopsku_list.replace('\\', '\\\\')
    elif len(shopsku) == 1:
        shopsku_list = '\'' + shopsku[0] + '\''
        shopsku_list = shopsku_list.replace('\\', '\\\\')
    else:
        return None
    sql = "SELECT SKU, ShopSKU FROM py_db.b_goodsskulinkshop WHERE ShopSKU IN (%s);" % shopsku_list
    sku_info = get_db_info(sql)
    sku_dict = dict()
    for i in sku_info:
        sku_dict[i['ShopSKU']] = i['SKU']
    return sku_dict

def get_order_log():
    sql = "SELECT id, OrderID, OrderState, OrderFlag FROM t_chart_wish_refund_log WHERE SaleDeleteFlag=0 LIMIT 10000;"
    order_log = get_db_info(sql)
    if not order_log:
        return None
    # ids = []
    # for i in order_log:
    #     ids.append(str(i['id']))
    # id_list = ', '.join(ids)
    # sql = "UPDATE t_chart_wish_refund_log SET SaleDeleteFlag=1 WHERE id IN (%s);" % id_list
    # execute_db(sql)
    return order_log

def update_order_log(order_log_id, flag='start'):
    sql_sel = "SELECT SaleDeleteFlag FROM t_chart_wish_refund_log WHERE id in (%s);" % order_log_id
    if flag == 'start':
        sql = "UPDATE t_chart_wish_refund_log SET SaleDeleteFlag=2 WHERE id IN (%s);" % order_log_id
    else:
        sql = "UPDATE t_chart_wish_refund_log SET SaleDeleteFlag=1 WHERE id IN (%s);" % order_log_id
        execute_db(sql)
        return 0
    res = get_db_info(sql_sel)
    if res:
        if str(res[0]['SaleDeleteFlag']) == '2' or str(res[0]['SaleDeleteFlag']) == '1':
            return 1
        else:
            execute_db(sql)
            return 0
    else:
        return 1

def get_b_goods_info(sku):
    if len(sku) > 1:
        sku_list = '\', \''.join(sku)
        sku_list = '\'' + sku_list + '\''
        sku_list = sku_list.replace('\\', '\\\\')
    elif len(sku) == 1:
        sku_list = '\'' + sku[0] + '\''
        sku_list = sku_list.replace('\\', '\\\\')
    else:
        return None
    sql = "SELECT CostPrice, PackFee, SKU FROM py_db.b_goods WHERE SKU IN (%s);" % sku_list
    sku_info = get_db_info(sql)
    sku_dict = dict()
    for i in sku_info:
        sku_dict[i['SKU']] = dict()
        sku_dict[i['SKU']]['CostPrice'] = float(i['CostPrice'])
        sku_dict[i['SKU']]['PackFee'] = float(i['PackFee'])
    return sku_dict

def get_all_shopname():
    sql = "SELECT DISTINCT ShopName FROM t_order;"
    shopnames = get_db_info(sql)
    shop_name = list()
    for i in shopnames:
        shop_name.append(i['ShopName'])
    return shop_name

def get_rate():
    sql = "SELECT V FROM t_sys_param WHERE Type=40 AND Seq=1;"
    rate = get_db_info(sql)[0]['V']
    rate = float(rate) / 100.0
    return rate

def backup_table():
    cmd_all = "mysqldump -u%s -p%s -h %s %s %s > %s.sql" % (DATABASES['USER'], DATABASES['PASSWORD'], DATABASES['HOST'], DATABASES['NAME'], 't_chart_wish_all_profit', '/opt/t_chart_wish_all_profit')
    cmd_shop = "mysqldump -u%s -p%s -h %s %s %s > %s.sql" % (DATABASES['USER'], DATABASES['PASSWORD'], DATABASES['HOST'], DATABASES['NAME'], 't_chart_wish_shop_profit', '/opt/t_chart_wish_shop_profit')
    print 'cmd_all', cmd_all
    print 'cmd_shop', cmd_shop
    os.system(cmd_all)
    os.system(cmd_shop)

def wish_order_profit():
    rate = get_rate()
    today = datetime.datetime.today()
    if today.month == 1 and today.day == 1 and today.hour <= 4:
        genrate_week_month_all_notes(today)
        shop_names = get_all_shopname()
        genrate_week_month_shop_notes(today, shop_names)
    all_dates = []
    shop_dates = []
    shopnames = []
    while True:
        new_orders = get_order_log()
        if new_orders:
            for i in new_orders:
                orderids = []
                order_log_id = None
                order_log_id = i['id']
                if order_log_id:
                    res = update_order_log(order_log_id, flag='start')
                    if res == 1:
                        print 'This order log had been set'
                        continue
                else:
                    print 'Can not get order log id'
                    continue
                if i['OrderFlag'] == 'OrderInsert':
                    orderids.append(i['OrderID'])
                elif i['OrderFlag'] == 'OrderUpdate' and i['OrderState'] in REFUND_ORDER_STATE:
                    orderids.append(i['OrderID'])
                if not orderids:
                    print 'This order does not need to update'
                    res = update_order_log(order_log_id, flag='end')
                    continue
                order_info = get_order_info(orderids)
                if not order_info:
                    print 'Can not get order_info'
                    res = update_order_log(order_log_id, flag='end')
                    continue
                shopskus = []
                for i in order_info:
                    shopskus.append(i['ShopSKU'])
                sku_dict = get_order_sku(shopskus)
                if not sku_dict:
                    print 'Can not get sku_dict'
                    res = update_order_log(order_log_id, flag='end')
                    continue
                b_goods_info = get_b_goods_info(sku_dict.values())
                if not b_goods_info:
                    print 'Can not get b_goods_info'
                    res = update_order_log(order_log_id, flag='end')
                    continue
                order_info_list = list()
                for i in order_info:
                    if not sku_dict.get(i['ShopSKU']):
                        print 'Can not get order_info ShopSKU'
                        res = update_order_log(order_log_id, flag='end')
                        continue
                    i['SKU'] = sku_dict[i['ShopSKU']]
                    if b_goods_info.get(i['SKU']):
                        i['CostPrice'] = b_goods_info[i['SKU']]['CostPrice']
                        i['PackFee'] = b_goods_info[i['SKU']]['PackFee']
                        order_info_list.append(i)
                    else:
                        print 'Can not get b_goods_info SKU'
                        res = update_order_log(order_log_id, flag='end')
                        continue
                if not order_info_list:
                    print 'order_info_list is empty'
                    res = update_order_log(order_log_id, flag='end')
                    continue
                order_info = order_info_list
                ad = generate_all_profit(order_info, rate)
                sd, sns = generate_shop_profit(order_info, rate)
                for i in ad:
                    if i not in all_dates:
                        all_dates.append(i)
                for i in sd:
                    if i not in shop_dates:
                        shop_dates.append(i)
                for i in sns:
                    if i not in shopnames:
                        shopnames.append(i)
                res = update_order_log(order_log_id, flag='end')
            continue
        else:
            break
    print 'all_dates: ', all_dates
    print 'shop_dates: ', shop_dates
    print 'shopnames: ', shopnames
    get_week_month_to_update_profit(all_dates, shop_name_list=None)
    get_week_month_to_update_profit(shop_dates, shop_name_list=shopnames)
    backup_table()

def wish_all_order_profit():
    now = datetime.datetime.today()
    i = 0
    sql = "UPDATE t_chart_wish_refund_log SET SaleDeleteFlag=1 WHERE SaleDeleteFlag=0"
    execute_db(sql)
    sql_del_all_profit = "DELETE FROM t_chart_wish_all_profit WHERE Period='day';"
    sql_del_shop_profit = "DELETE FROM t_chart_wish_shop_profit WHERE Period='day';"
    execute_db(sql_del_all_profit)
    execute_db(sql_del_shop_profit)
    t_order_count = 0
    while True:
        print '================ day ================', now
        print '================ t_order_count ================', t_order_count
        sql = "SELECT OrderId, OrderState, SKU, ShopSKU, ShopName, ProductID, OrderDate, Quantity, Price, Shipping " \
            "FROM t_order WHERE LastUpdated LIKE '%s';" % (now.strftime('%Y-%m-%d')+'%')
        now = now - datetime.timedelta(days=1)
        order_info = get_db_info(sql)
        if order_info:
            i = 0
            print '================ len(order_info) ================', len(order_info)
            t_order_count += len(order_info)
            for i in order_info:
                i['Quantity'] = int(i['Quantity'])
                i['Price'] = float(i['Price'])
                i['Shipping'] = float(i['Shipping'])
            shopskus = []
            for i in order_info:
                if i['ShopSKU'] not in shopskus:
                    shopskus.append(str(i['ShopSKU']))
            sku_dict = get_order_sku(shopskus)
            b_goods_info = get_b_goods_info(sku_dict.values())
            order_info_list = list()
            for i in order_info:
                if not sku_dict.get(i['ShopSKU']):
                    continue
                i['SKU'] = sku_dict[i['ShopSKU']]
                if b_goods_info.get(i['SKU']):
                    i['CostPrice'] = b_goods_info[i['SKU']]['CostPrice']
                    i['PackFee'] = b_goods_info[i['SKU']]['PackFee']
                    order_info_list.append(i)
                else:
                    continue
            order_info = order_info_list
            generate_all_profit(order_info)
            generate_shop_profit(order_info)
            all_backup = 't_chart_wish_all_profit' + now.strftime('%Y%m%d')
            shop_backup = 't_chart_wish_shop_profit' + now.strftime('%Y%m%d')
            cmd_all = "mysqldump -u%s -p%s -h %s %s %s > %s.sql" % (DATABASES['USER'], DATABASES['PASSWORD'], DATABASES['HOST'], DATABASES['NAME'], 't_chart_wish_all_profit', all_backup)
            cmd_shop = "mysqldump -u%s -p%s -h %s %s %s > %s.sql" % (DATABASES['USER'], DATABASES['PASSWORD'], DATABASES['HOST'], DATABASES['NAME'], 't_chart_wish_shop_profit', shop_backup)
            print 'cmd_all', cmd_all
            print 'cmd_shop', cmd_shop
            os.system(cmd_all)
            os.system(cmd_shop)
        else:
            i += 1
            if i > 30:
                break
            else:
                continue

def update_all_w_m_all_profit():
    sql = "SELECT DISTINCT StartDate FROM t_chart_wish_all_profit WHERE Period='day' ORDER BY StartDate DESC;"
    startdates = get_db_info(sql)
    startdate_list = []
    for i in startdates:
        if i['StartDate'] not in startdate_list:
            startdate_list.append(str(i['StartDate']))
    get_week_month_to_update_profit(startdate_list, shop_name_list=None)

def update_all_w_m_shop_profit():
    sql = "SELECT DISTINCT StartDate FROM t_chart_wish_shop_profit WHERE Period='day' ORDER BY StartDate DESC;"
    startdates = get_db_info(sql)
    startdate_list = []
    for i in startdates:
        if i['StartDate'] not in startdate_list:
            startdate_list.append(str(i['StartDate']))
    sql = "SELECT DISTINCT ShopName FROM t_chart_wish_shop_profit;"
    shopnames = get_db_info(sql)
    shop_name_list = []
    for i in shopnames:
        if i['ShopName'] not in shop_name_list:
            shop_name_list.append(i['ShopName'])
    get_week_month_to_update_profit(startdate_list, shop_name_list=shop_name_list)

# wish_order_profit()
# wish_all_order_profit()
# update_all_w_m_shop_profit()
# update_all_w_m_all_profit()

# db_conn.close()

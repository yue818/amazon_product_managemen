# coding=utf-8

"""
WISH在线listing 30、60、90天退款率统计
"""

from __future__ import division
import datetime
import requests
from django.db import connection
from get_wish_rating import get_product_rating
from app_djcelery.celery import app


# def connect_to_mysql():
#     """
#         连接MySQL数据库
#         返回值：MySQL连接
#     """
#     import MySQLdb, time
#     HOST = 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com'
#     PORT = 3306
#     USER = 'by15161458383'
#     PASSWORD = 'K120Esc1'
#     DB = 'hq_db'
#     CHARSET = 'utf8'
#     try:
#         mysqlClient = MySQLdb.connect(host=HOST, port=PORT, user=USER, passwd=PASSWORD, db=DB, charset=CHARSET)
#     except MySQLdb.Error, e:
#         print '38------------MySQL Error:%s，30秒后重新连接……' % str(e)
#         time.sleep(30)
#         connect_to_mysql()
#     return mysqlClient


class DbOperation(object):

    def __init__(self, cur):
        self.cur = cur

    def update_refund_everyweek(self):
        """调用存储过程计算WISH在线listing退款信息"""
        sql = 'CALL p_szc_wish_listing_refund'
        self.cur.execute(sql)


    def get_product_id(self):
        """获得在线listing productid"""
        sql = 'select distinct ProductID from t_chart_wish_listing_refund_statistics'
        self.cur.execute(sql)
        productid_infos = self.cur.fetchall()
        productid_list = []
        for productid_info in productid_infos:
            productid_list.append(productid_info[0])
        return productid_list


    def update_statistics(self, product_id, rating):
        """更新listing退款统计表的评分为最新评分"""
        sql = 'update t_chart_wish_listing_refund_statistics set Rating=%s WHERE ProductID=%s;'
        self.cur.execute(sql, (rating, product_id))


    def judge_rating_record(self, product_id):
        """根据ProductID查询评分记录是否存在"""
        sql = 'select id, RatingDict from t_chart_wish_listing_rating WHERE ProductID=%s'
        self.cur.execute(sql, (product_id,))
        rating_record_info = self.cur.fetchone()
        if rating_record_info:
            rating_record_dict = {'id': rating_record_info[0], 'rating_dict': eval(rating_record_info[1])}
        else:
            rating_record_dict = {}
        return rating_record_dict


    def change_rating_record(self, param, flag):
        """更新或新增一条评分记录"""
        update_sql = 'update t_chart_wish_listing_rating set RatingDict=%s, RefreshTime=%s WHERE id=%s'
        insert_sql = 'insert into t_chart_wish_listing_rating(ProductID, RatingDict) VALUES (%s, %s)'
        if flag == 'update':
            self.cur.execute(update_sql, param)
        else:
            self.cur.execute(insert_sql, param)


# def get_listing_rating(product_id):
#     url = 'http://47.251.3.95:83/wish/getRatingById?productID=%s' % product_id
#     rating = None
#     try:
#         response = requests.get(url, timeout=30)
#         response = response.json()
#         if response['code'] == 0:
#             rating = response['rating']
#     except Exception, e:
#         print e
#     return rating


def get_current_week():
    """获取当前周开始和结束日期"""
    strdate = str(datetime.date.today()).replace('-', '')
    date_input = datetime.datetime.strptime(strdate, '%Y%m%d')
    strweek = date_input.isocalendar()
    yearnum = str(strweek[0])  # 取到年份
    weeknum = str(strweek[1])  # 取到周
    stryearstart = yearnum + '0101'  # 当年第一天
    yearstart = datetime.datetime.strptime(stryearstart, '%Y%m%d')  # 格式化为日期格式
    yearstartcalendarmsg = yearstart.isocalendar()  # 当年第一天的周信息
    yearstartweekday = yearstartcalendarmsg[2]
    yearstartyear = yearstartcalendarmsg[0]
    if yearstartyear < int(yearnum):
        daydelat = (8 - int(yearstartweekday)) + (int(weeknum) - 1) * 7
    else:
        daydelat = (8 - int(yearstartweekday)) + (int(weeknum) - 2) * 7
    week_start = (yearstart + datetime.timedelta(days=daydelat)).date()
    week_end = week_start + datetime.timedelta(7)
    return str(week_start), str(week_end)


# def wish_listing_refund_statistics():
#     cur = connection.cursor()
#     week_start, week_end = get_current_week()
#     DbOperation_obj = DbOperation(cur)
#     # DbOperation_obj.update_refund_everyweek()
#     productid_list = DbOperation_obj.get_product_id()
#     cur.close()
#     # length = len(productid_list)
#     # i = 0
#     for product_id in productid_list:
#         process_rating.delay(product_id, week_start)
#         # process_rating(product_id, week_start)
#         # rating = get_listing_rating(product_id=product_id)
#         # if rating is None:
#         #     continue
#         # DbOperation_obj.update_statistics(product_id=product_id, rating=rating)
#         # rating_record_dict = DbOperation_obj.judge_rating_record(product_id=product_id)
#         # if rating_record_dict:
#         #     time_now = datetime.datetime.now()
#         #     id = rating_record_dict['id']
#         #     rating_dict = rating_record_dict['rating_dict']
#         #     rating_dict[week_start] = rating
#         #     param = (str(rating_dict), time_now, id)
#         #     flag = 'update'
#         # else:
#         #     rating_dict = {week_start: rating}
#         #     param = (product_id, str(rating_dict))
#         #     flag = 'insert'
#         # DbOperation_obj.change_rating_record(param=param, flag=flag)
#         #
#         # i += 1
#         # if i % 50 == 0:
#         #     cur.execute('commit;')
#         # print 'product_id:%s--------total:%s----------ed:%s' % (product_id, length, i)
#
#
# @app.task
# def process_rating(product_id, week_start):
#     cur_1 = connection.cursor()
#     DbOperation_obj_1 = DbOperation(cur_1)
#
#     rating = get_product_rating(product_id=product_id).get('rating', None)
#     if rating is None:
#         return
#     DbOperation_obj_1.update_statistics(product_id=product_id, rating=rating)
#     rating_record_dict = DbOperation_obj_1.judge_rating_record(product_id=product_id)
#     if rating_record_dict:
#         time_now = datetime.datetime.now()
#         id = rating_record_dict['id']
#         rating_dict = rating_record_dict['rating_dict']
#         rating_dict[week_start] = rating
#         param = (str(rating_dict), time_now, id)
#         flag = 'update'
#     else:
#         rating_dict = {week_start: rating}
#         param = (product_id, str(rating_dict))
#         flag = 'insert'
#     DbOperation_obj_1.change_rating_record(param=param, flag=flag)
#
#     cur_1.execute('commit;')
#     cur_1.close()
#
#     print 'ProductID: %s ' % product_id

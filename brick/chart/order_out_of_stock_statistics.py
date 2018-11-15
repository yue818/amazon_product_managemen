# coding=utf-8

from django.db import connection
from django_redis import get_redis_connection
redis_db = get_redis_connection(alias='schedule')


def get_b_goods_info(sku, cur):
    """
    根据sku返回采购人、sku开发时间、业绩归属人2
    :param sku: 商品SKU
    :return: sku信息的NID，用于关联kc_currentstock里的goodsID    采购人
    """
    sql = 'select Purchaser, SalerName2, DevDate from py_db.b_goods WHERE SKU=\"%s\"; ' % sku
    cur.execute(sql)
    b_goods_infos = cur.fetchone()

    purchaser = ''
    saler_name2 = ''
    dev_date = None
    if b_goods_infos:
        purchaser = b_goods_infos[0]
        saler_name2 = b_goods_infos[1]
        dev_date = b_goods_infos[2]
    return purchaser, saler_name2, dev_date


def get_insert_chart_param(purchaser, start_date, end_date, num, cur, username):
    """
    获取待插入或者待更新的数据信息
    :param purchaser:
    :param export_date:
    :return:
    """
    statistics_infos = select_from_statistics_table(purchaser, start_date, end_date, cur)
    if statistics_infos is None:
        statistics_param = [start_date, end_date, purchaser, num, 'day', username]
    else:
        statistics_param = [statistics_infos[1] + num, statistics_infos[0]]

    return statistics_param


def select_from_statistics_table(purchaser, start_date, end_date, cur):
    """
    查询统计表里已有的统计信息
    :param purchaser:
    :param export_date:
    :return:
    """
    sql = 'select id, Num from t_chart_out_of_stock_statistics WHERE Purchaser=%s AND StartDate=%s AND EndDate=%s; '
    cur.execute(sql, (purchaser, start_date, end_date))
    statistics_infos = cur.fetchone()
    return statistics_infos


def insert_into_chart_table(day_param, cur):
    """
    更新或者插入到统计表中的信息
    :param param_1:
    :param param_2:
    :param param_3:
    :return:
    """
    insert_sql = 'insert into t_chart_out_of_stock_statistics(StartDate, EndDate, Purchaser, Num, Period, UserName) VALUES (%s,%s,%s,%s,%s,%s); '
    update_sql = 'update t_chart_out_of_stock_statistics set Num=%s WHERE id=%s; '

    if len(day_param) == 2:
        cur.execute(update_sql, day_param)
    else:
        cur.execute(insert_sql, day_param)
    cur.execute('commit;')


def get_insert_detail_param(start_date, end_date, sku, num, purchaser, saler_name2, dev_date, cur, username):
    """
    获取待插入或者更新详细信息表的数据
    :return:
    """
    select_param = (start_date, end_date, sku)
    detail_info = select_from_detail_table(select_param, cur)
    if detail_info is None:
        param = (start_date, end_date, sku, num, purchaser, saler_name2, dev_date, username)
    else:
        param = (detail_info[1] + num, detail_info[0])
    return param


def select_from_detail_table(select_param, cur):
    """
    获取缺货订单详情表已有的信息
    :param export_date: 导入日期（统计日期）
    :param sku: 商品sku
    :param purchaser: 采购人
    :param possess_man2: 业绩归属人2
    :return:
    """
    sql = 'select id, Num from t_chart_out_of_stock_statistics_detail WHERE StartDate=%s AND EndDate=%s AND SKU=%s'
    cur.execute(sql, select_param)
    detail_info = cur.fetchone()
    return detail_info


def insert_into_detail_table(param, cur):
    """
    插入到订单详情页面
    :param param:
    :return:
    """
    update_sql = 'update t_chart_out_of_stock_statistics_detail set Num=%s WHERE id=%s'
    insert_sql = 'insert into t_chart_out_of_stock_statistics_detail(StartDate, EndDate, SKU, Num, Purchaser, SalerName2, CreateTime, UserName) ' \
                 'VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
    if len(param) == 2:
        cur.execute(update_sql, param)
    else:
        cur.execute(insert_sql, param)
    cur.execute('commit;')


def process_param(details, start_date, end_date, cur, username):
    """
    处理统计日的订单信息，判断是否将统计结果插入到报表中
    :param order:
    :return:
    """
    sku_num_list = details.split(';')

    for sku_num in sku_num_list[:-1]:
        sku = sku_num.split('*')[0]
        try:
            num = int(sku_num.split('*')[1])
        except:
            num = 1
            pass
        purchaser, saler_name2, dev_date = get_b_goods_info(sku, cur)
        statistics_param = get_insert_chart_param(purchaser, start_date, end_date, num, cur, username)
        details_param = get_insert_detail_param(start_date, end_date, sku, num, purchaser, saler_name2, dev_date, cur, username)
        insert_into_chart_table(statistics_param, cur)
        insert_into_detail_table(details_param, cur)


def order_out_of_stock_statistics(start_date, end_date, username, schedule_name):
    cur = connection.cursor()
    delete_statistics_sql = 'delete from t_chart_out_of_stock_statistics WHERE UserName=\"%s\"' % username
    delete_details_sql = 'delete from t_chart_out_of_stock_statistics_detail WHERE UserName=\"%s\"' % username
    cur.execute(delete_statistics_sql)
    cur.execute(delete_details_sql)
    cur.execute('commit; ')

    sql = 'select Details from t_order_out_of_stock WHERE ExportDate >= %s AND ExportDate <= %s;'
    cur.execute(sql, (start_date, end_date))
    order_infos = cur.fetchall()

    redis_db.hset(schedule_name, 'total', len(order_infos))
    redis_db.hset(schedule_name, 'start', start_date)
    redis_db.hset(schedule_name, 'end', end_date)

    i = 0
    for order_info in order_infos:
        details = order_info[0]
        process_param(details, start_date, end_date, cur, username)
        i += 1
        redis_db.hset(schedule_name, 'processed', i)
    cur.close()
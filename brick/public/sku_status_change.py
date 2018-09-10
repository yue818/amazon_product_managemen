# coding=utf-8


from datetime import datetime
from django.db import connection


def select_from_goods(cur):
    """
    根据时间增量查询b_goods表里状态改变的记录
    :param cur:
    :return:
    """
    date_sql = 'select left(MAX(UpdateTime), 10) from b_goods_sku_status_change'
    cur.execute(date_sql)
    date_info = cur.fetchone()
    max_date_str = str(date_info[0])
    sql = 'select sku, GoodsStatus, changestatustime from py_db.b_goods WHERE LEFT(ChangeStatusTime, 10)>%s'
    cur.execute(sql, (max_date_str, ))
    goods_infos = cur.fetchall()
    return goods_infos


def select_from_status_change(cur, sku):
    """
    根据sku查询b_goods_sku_status_change里的记录
    :param cur:
    :param sku:
    :return:
    """
    sql = 'select id, NowGoodsStatus from b_goods_sku_status_change WHERE SKU=%s ORDER BY id DESC '
    cur.execute(sql, (sku, ))
    status_change_info = cur.fetchone()
    return status_change_info


def change_sku_status(cur, param):
    """
    根据参数对b_goods_sku_status_change进行插入或者更新操作
    :param cur:
    :param param:
    :return:
    """
    if len(param) == 7:
        sql = 'insert into b_goods_sku_status_change(SKU, LastGoodsStatus, NowGoodsStatus, ChangeStatusTime, ' \
              'DisplayFlag, OperationFlag, UpdateTime) VALUES (%s,%s,%s,%s,%s,%s,%s)'
        cur.execute(sql, param)
    else:
        sql = 'update b_goods_sku_status_change set LastGoodsStatus=%s, NowGoodsStatus=%s, ChangeStatusTime=%s,' \
              'DisplayFlag=1, OperationFlag=0, UpdateTime=%s WHERE id=%s'
        cur.execute(sql, param)
    cur.execute('commit;')


def sku_status_change():
    """
    根据b_goods_sku_status_change里sku是否存在和b_goods表状态是否改变，进行插入或者更新操作
    :param cur:
    :return:
    """
    cur = connection.cursor()
    goods_infos = select_from_goods(cur)
    for goods_info in goods_infos:
        sku = goods_info[0]
        print sku
        goods_status_cn = goods_info[1]
        change_status_time = goods_info[2]
        update_time = datetime.now()

        status_change_info = select_from_status_change(cur, sku)
        if status_change_info:
            if status_change_info[1] == goods_status_cn:
                continue
            else:
                last_goods_status = status_change_info[1]
                now_goods_status = goods_status_cn
                param = (last_goods_status, now_goods_status, change_status_time, update_time, status_change_info[0])
                change_sku_status(cur, param)
        else:
            last_goods_status = goods_status_cn
            now_goods_status = goods_status_cn
            param = (sku, last_goods_status, now_goods_status, change_status_time, 0, 1, update_time)
            change_sku_status(cur, param)

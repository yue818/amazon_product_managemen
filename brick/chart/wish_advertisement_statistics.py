# coding=utf-8

from __future__ import  division
from django.db import connection
from datetime import datetime



def select_from_wish_pb_table(cur):
    """
    全量查询t_wish_pb表的数据
    :param cur:
    :return:
    """
    # 按照更新时间增量更新
    date_sql = 'select left(MAX(UpdateTime), 10) from t_chart_wish_advertisement_info'
    cur.execute(date_sql)
    date_info = cur.fetchone()
    if date_info:
        max_date_str = str(date_info[0])
    else:
        max_date_str = ''

    increment_sql = 'select ProductID, ShopName, Pic, ProductName, PbKey, ActivityID, ActivityStatus, Duration,PbOrder, ' \
          'PbCharge, PbFee, PbData, PbCount, id, DepletedFlag from t_wish_pb WHERE LEFT(updateTime, 10)>%s ;'
    cur.execute(increment_sql, (max_date_str,))
    pb_infos = cur.fetchall()
    return pb_infos


def select_from_online_wish(cur, product_id):
    """
    根据productID在t_online_info_wish表中查询店长、主SKU、刊登时间
    :param cur:
    :param product_id:
    :return:
    """
    seller, main_sku, date_uploaded = '', '', None
    sql = 'select Seller, MainSKU, DateUploaded from t_online_info_wish where ProductID=\"%s\";' % product_id
    cur.execute(sql)
    wish_info = cur.fetchone()
    if wish_info:
        if wish_info[0]:
            seller = wish_info[0]
        if wish_info[1]:
            main_sku = wish_info[1]
        if wish_info[2]:
            date_uploaded = str(wish_info[2])[:10]
    return seller, main_sku, date_uploaded


def insert_into_advertisement_table(cur, param, activity_id, product_id):
    """
    插入到t_wish_advertisement_info
    :param cur:
    :param param:
    :return:
    """
    delete_sql = 'delete from t_chart_wish_advertisement_info WHERE ActivityID=%s AND ProductID=%s'
    cur.execute(delete_sql, (activity_id, product_id))

    sql = 'insert into t_chart_wish_advertisement_info (ProductID, ShopName, Seller, MainSKU, Pic, ProductName, PbKey, ' \
          'PublishDate, ActivityID, ActivityStatus, ActivityStart, ActivityEnd, ProductOrder, PbCharge, PbFee, PbData, ' \
          'PbCount, ConversionRate, `As`, UpdateTime, LargeCate, ClotheCate1, ClotheCate2, ClotheCate3, DepletedFlag) ' \
          'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    cur.execute(sql, param)
    cur.execute('commit; ')

def get_cate(cur, mainsku):
    """
    根据MasinSKU获得大类和服装三级分类
    :param cur:
    :param mainsku:
    :return:
    """
    large_cate = []
    clothe_cate_1 = []
    clothe_cate_2 = []
    clothe_cate_3 = []
    if mainsku:
        mainsku_list = mainsku.split(',')
        for each in mainsku_list:
            sql_1 = 'select CategoryCode from py_db.b_goods WHERE sku like \"%s%%\"; ' % each.replace('\\', '\\\\')
            sql_2 = 'select ClothingSystem1, ClothingSystem2, ClothingSystem3 from t_product_enter_ed WHERE MainSKU=\"%s\"; ' % each.replace('\\', '\\\\')

            cur.execute(sql_1)
            large_cate_info = cur.fetchone()
            if large_cate_info:
                cate_list = large_cate_info[0].split('|')
                if len(cate_list) > 1:
                    large_cate.append(cate_list[0] + '|' + cate_list[1] + '|')

            cur.execute(sql_2)
            clothe_cate_info = cur.fetchone()
            if clothe_cate_info:
                if clothe_cate_info[0]:
                    clothe_cate_1.append(clothe_cate_info[0])
                if clothe_cate_info[1]:
                    clothe_cate_2.append(clothe_cate_info[1])
                if clothe_cate_info[2]:
                    clothe_cate_3.append(clothe_cate_info[2])
    return ','.join(list(set(large_cate))), ','.join(list(set(clothe_cate_1))), ','.join(list(set(clothe_cate_2))), ','.join(list(set(clothe_cate_3)))


def generate_statistics(cur, increment_id_list, increment_product_id_set):
    """
    WISH广告统计信息
    :param cur:
    :param increment_product_id_list: 增量广告统计的商品ID
    :return:
    """
    # 增量
    sql = 'insert into t_chart_wish_advertisement_statistics select 0, ShopName, Seller, ProductID, Pic, MainSKU, ' \
            'ProductName, PbKey, AVG(PbCharge), sum(PbFee), sum(PbData), sum(ProductOrder), sum(PbCount), ' \
            'sum(ProductOrder)/sum(PbData)*100, sum(PbFee)/sum(PbCount)*100, LargeCate, ClotheCate1, ClotheCate2,' \
            ' ClotheCate3, now(), PublishDate from t_chart_wish_advertisement_info WHERE ProductID=%s;'
    delete_sql = 'delete from t_chart_wish_advertisement_statistics WHERE ProductID IN ' \
                 '(select ProductID from t_wish_pb WHERE id in %s)' % str(tuple(increment_id_list))
    cur.execute(delete_sql)
    cur.execute('commit; ')
    for increment_product_id in increment_product_id_set:
        print 'advertisement_statistics------id--------%s' % increment_product_id
        cur.execute(sql, (increment_product_id, ))
        cur.execute('commit; ')


def get_percent(num_1, num_2):
    """
    求百分比
    """
    result = None
    try:
        result = '%.2f' % (float(num_1) / float(num_2) * 100)
    except:
        pass
    return result


def get_shopname_by_productID(cur, product_id):
    sql = 'select ShopName from t_online_info_wish WHERE ProductID=%s;'
    cur.execute(sql, (product_id, ))
    shop_info = cur.fetchone()
    if shop_info:
        shop_name = shop_info[0]
    else:
        shop_name = ''
    return shop_name


def update_refresh_result(cur, update_time):
    """
    更新店铺刷新成功标识
    :param cur:
    :param update_time:
    :return:
    """
    sql_1 = 'select storeName, alertInfo from t_service_run_log where LEFT(alertTime, 10)=%s and serviceType="getpb"; '
    sql_2 = 'update t_chart_wish_advertisement_info set RefreshFlag=%s where ShopName=%s;'
    sql_3 = 'update t_chart_wish_advertisement_info set RefreshFlag=NULL ;'
    sql_4 = 'update t_chart_wish_advertisement_info set RefreshFlag="error" WHERE RefreshFlag is NULL ;'

    # 先将前一天的刷新状态置空
    cur.execute(sql_3)
    cur.execute('commit;')

    # 根据今日运行状态填写刷新状态
    cur.execute(sql_1, (update_time, ))
    log_infos = cur.fetchall()
    for log_info in log_infos:
        shop_name = log_info[0][:9]
        result = log_info[1]
        cur.execute(sql_2, (result, shop_name))
    cur.execute('commit;')

    # 将没有运行记录的店铺刷新状态置error
    cur.execute(sql_4)
    cur.execute('commit;')


def delete_illegal_productid_info(cur):
    """
    删除t_wish_pb中productid为空的条数
    :param cur:
    :return:
    """
    sql = 'delete from t_wish_pb where productID=""; '
    cur.execute(sql)
    cur.execute('commit; ')


def wish_advertisement_statistics():
    cur = connection.cursor()

    increment_id_list = []
    increment_product_id_list = []
    refresh_date = str(datetime.now())[:10]
    delete_illegal_productid_info(cur)
    pb_infos = select_from_wish_pb_table(cur)
    for pb_info in pb_infos:
        print 'advertisement_info------id--------%s' % pb_info[13]
        update_time = str(datetime.now())
        product_id = pb_info[0]
        increment_id_list.append(int(pb_info[13]))
        increment_product_id_list.append(product_id)
        depleted_flag = pb_info[14]

        seller, main_sku, date_uploaded = select_from_online_wish(cur, product_id)
        large_cate, clothe_cate_1, clothe_cate_2, clothe_cate_3 = get_cate(cur, main_sku)
        shop_name = get_shopname_by_productID(cur, product_id)
        if not shop_name:
            shop_name = pb_info[1][:9]
        pic = pb_info[2]
        product_name = pb_info[3]
        pb_key = pb_info[4]
        activity_id = pb_info[5]
        activity_status = pb_info[6]
        try:
            activity_start_list = pb_info[7][:10].split('/')
            activity_end_list = pb_info[7][-10:].split('/')
            activity_start = '-'.join([activity_start_list[2], activity_start_list[0], activity_start_list[1]])
            activity_end = '-'.join([activity_end_list[2], activity_end_list[0], activity_end_list[1]])

            pb_order = 0 if pb_info[8] == u'无相关信息' else int(str(pb_info[8]).replace(',', ''))
            pb_charge = 0 if pb_info[9] == u'无相关信息' else float(str(pb_info[9]).replace('$', '').replace(',', ''))
            pb_fee = 0 if pb_info[10] == u'无相关信息' else float(str(pb_info[10]).replace('$', '').replace(',', ''))
            pb_data = 0 if pb_info[11] == u'无相关信息' else int(str(pb_info[11]).replace('$', '').replace(',', ''))
            pb_count = 0 if pb_info[12] == u'无相关信息' else float(str(pb_info[12]).replace('$', '').replace(',', ''))
        except Exception, e:
            print e
        conversion_rate = get_percent(pb_order, pb_data)
        as_cloum = get_percent(pb_fee, pb_count)

        param = (product_id, shop_name, seller, main_sku, pic, product_name, pb_key, date_uploaded, activity_id,
                 activity_status, activity_start, activity_end, pb_order, pb_charge, pb_fee, pb_data, pb_count,
                 conversion_rate, as_cloum, update_time, large_cate, clothe_cate_1, clothe_cate_2, clothe_cate_3,
                 depleted_flag)
        insert_into_advertisement_table(cur, param, activity_id, product_id)

    update_refresh_result(cur, refresh_date)
    if increment_id_list:
        generate_statistics(cur, increment_id_list, set(increment_product_id_list))
    cur.close()
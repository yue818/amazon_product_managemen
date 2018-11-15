# coding=utf-8

"""
WISH退款订单
"""
from __future__ import  division
from django.db import connection
from brick.function.week_and_date import *
import datetime


# 服装大类
CLOTHING_CATEGORY = ('0|1|', '0|2|', '0|33|85|', '0|25|104|', '0|25|105|')
# 退款状态
REFUND_ORDER_STATE = ('CANCELLED BY CUSTOMER', 'CANCELLED BY WISH (FLAGGED TRANSACTION)', 'REFUNDED',
                      'REFUNDED BY MERCHANT', 'REFUNDED BY WISH', 'REFUNDED BY WISH FOR MERCHANT')

def get_lagrge_category(sku, cur):
    """
    根据SKU从b_goods表查询大类信息
    :param sku:
    :return:
    """
    sql = 'select CategoryCode, SalerName, Purchaser from py_db.b_goods where SKU=%s;'
    cur.execute(sql, (sku, ))
    category_info = cur.fetchone()
    if category_info:
        category = category_info[0]
        saler = category_info[1]
        purchaser = category_info[2]
    else:
        category = ''
        saler = ''
        purchaser = ''
    return category, saler, purchaser


def insert_or_update_refund(param, flag, cur):
    """
    插入或更新wish退款表
    :param param:
    :param flag:
    :return:
    """
    try:
        if flag == 'update':
            sql = 'update t_chart_wish_refund set OrderNum=%s,ThirtyDaysRefundNum=%s,ThirtyDaysRefundRate=%s,SixtyDaysRefundNum=%s,' \
                         'SixtyDaysRefundRate=%s,NinetyDaysRefundNum=%s,NinetyDaysRefundRate=%s,RefundNum=%s,RefundRate=%s, UpdateDate=%s WHERE id=%s'
        else:
            sql = 'insert into t_chart_wish_refund VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
        cur.execute(sql, param)
        cur.execute('commit;')
    except:
        pass


def select_from_refund(main_sku, start_date, end_date, cur):
    """
    查询主SKU该时间周的数据是否存在
    :param main_sku:
    :param start_date:
    :param end_date:
    :return:
    """
    sql = 'select id, OrderNum, ThirtyDaysRefundNum, SixtyDaysRefundNum, NinetyDaysRefundNum, RefundNum from t_chart_wish_refund' \
          ' where SKU=%s AND StartDate=%s AND EndDate=%s'
    cur.execute(sql, (main_sku, start_date, end_date))
    refund_info = cur.fetchone()
    return refund_info


def get_30_60_90_last_date(order_date):
    """
    计算订单日起30，60,90天的日期范围
    :param order_date: 订单日字符串
    :return:
    """

    order_date_format = datetime.datetime.strptime(order_date.replace('-', ''), '%Y%m%d')
    last_30_date = order_date_format + datetime.timedelta(30)
    last_60_date = order_date_format + datetime.timedelta(60)
    last_90_date = order_date_format + datetime.timedelta(90)

    thirty_days_range = [order_date, str(last_30_date)]
    sixty_days_range = [str(last_30_date), str(last_60_date)]
    ninety_days_range = [str(last_60_date), str(last_90_date)]
    return thirty_days_range, sixty_days_range, ninety_days_range


def get_percent(num_1, num_2):
    """
    求百分比
    """
    result = 0.00
    try:
        result = '%.2f' % (num_1 / num_2 * 100)
    except:
        pass
    return float(result)


def process_order_num(main_sku, refund_date, order_date, order_state, last_update, quantity, date_now, order_flag, cur,
                      saler, purchaser):
    """
    根据订单日、订单状态计算订单数，30、60、90天的退款数、退款率
    :param main_sku: 主SKU
    :param refund_date: 退款日期
    :param order_date: 订单日期
    :param order_state: 订单状态
    :param last_update: 订单最后更新日期
    :return:
    """
    # 获得订单日的30、60、90天的范围
    thirty_days_range, sixty_days_range, ninety_days_range = get_30_60_90_last_date(order_date)
    # 获得订单日所在自然周的开始日期和结束日期
    week_tuple = getweekmsg(order_date.replace('-', ''))
    week_num = str(week_tuple[0]) + str(week_tuple[1])
    start_date, end_date = get_day_range(week_num)
    # 根据主SKU，自然周开始和结束日期查询是否已经存在该SKU的自然周记录
    refund_info = select_from_refund(main_sku, start_date, end_date, cur)

    # 如果该SKU的当前周的这条数据已经存在
    if refund_info:
        flag = 'update'

        # 如果此order只是更新为退款状态，则订单数不变，只更改相应退款数目，，，如果order为新增，则订单数增加，退款数根据状态判断增减
        if order_flag == 'OrderUpdate':
            order_num = refund_info[1]
        else:
            order_num = refund_info[1] + quantity

        thirty_days_refund_num = refund_info[2]
        sixty_days_refund_num = refund_info[3]
        ninety_days_refund_num = refund_info[4]
        refund_num = refund_info[5]
        # 如果这条订单状态是退款状态，则按退款时间相应在三十、六十、九十天退款数加1
        if order_state in REFUND_ORDER_STATE:
            refund_num = refund_info[5] + quantity
            if (refund_date >= thirty_days_range[0] and refund_date < thirty_days_range[1]) or \
                    ( last_update >= thirty_days_range[0] and last_update < thirty_days_range[1]):

                thirty_days_refund_num = refund_info[2] + quantity
                sixty_days_refund_num = refund_info[3] + quantity
                ninety_days_refund_num = refund_info[4] + quantity
            elif (refund_date >= sixty_days_range[0] and refund_date < sixty_days_range[1]) or \
                    ( last_update >= sixty_days_range[0] and last_update < sixty_days_range[1]):

                sixty_days_refund_num = refund_info[3] + quantity
                ninety_days_refund_num = refund_info[4] + quantity
            elif (refund_date >= ninety_days_range[0] and refund_date < ninety_days_range[1]) or \
                    ( last_update >= ninety_days_range[0] and last_update < ninety_days_range[1]):

                ninety_days_refund_num = refund_info[4] + quantity

    # 一条新纪录
    else:
        flag = 'insert'
        order_num = quantity
        thirty_days_refund_num = 0
        sixty_days_refund_num = 0
        ninety_days_refund_num = 0
        refund_num = 0

        # 如果这条订单状态是退款状态，则按退款时间相应在三十、六十、九十天退款数加1
        if order_state in REFUND_ORDER_STATE:
            refund_num = 1
            if (refund_date >= thirty_days_range[0] and refund_date < thirty_days_range[1]) or \
                    (last_update >= thirty_days_range[0] and last_update < thirty_days_range[1]):

                thirty_days_refund_num = quantity
                sixty_days_refund_num = quantity
                ninety_days_refund_num = quantity
            elif (refund_date >= sixty_days_range[0] and refund_date < sixty_days_range[1]) or \
                    (last_update >= sixty_days_range[0] and last_update < sixty_days_range[1]):

                sixty_days_refund_num = quantity
                ninety_days_refund_num = quantity
            elif (refund_date >= ninety_days_range[0] and refund_date < ninety_days_range[1]) or \
                    (last_update >= ninety_days_range[0] and last_update < ninety_days_range[1]):

                ninety_days_refund_num = quantity

    thirty_days_refund_rate = get_percent(thirty_days_refund_num, order_num)
    sixty_days_refund_rate = get_percent(sixty_days_refund_num, order_num)
    ninety_days_refund_rate = get_percent(ninety_days_refund_num, order_num)
    refund_rate = get_percent(refund_num, order_num)

    if flag == 'update':
        param = (order_num, thirty_days_refund_num, thirty_days_refund_rate, sixty_days_refund_num,sixty_days_refund_rate,
                 ninety_days_refund_num, ninety_days_refund_rate, refund_num, refund_rate, date_now, refund_info[0])
    else:
        param = (0, main_sku, start_date, end_date, order_num, thirty_days_refund_num, thirty_days_refund_rate, sixty_days_refund_num,
                 sixty_days_refund_rate, ninety_days_refund_num, ninety_days_refund_rate, refund_num, refund_rate, saler, purchaser, date_now)
    return param, flag


def wish_order_syn():
    """
    增量更新WISH订单退款率
    :return:
    """
    cur = connection.cursor()
    log_select_sql = 'select id, OrderID, OrderState, OrderFlag from t_chart_wish_refund_log WHERE RefundDeleteFlag=0;'
    cur.execute(log_select_sql)
    log_infos = cur.fetchall()

    id_list = []

    for log_info in log_infos:
        id_list.append(str(int(log_info[0])))
        order_flag = log_info[3]
        # 如果是订单更新且为退款，或者为新增的订单才会进行累计
        if (order_flag == 'OrderUpdate' and log_info[2] in REFUND_ORDER_STATE) or (order_flag == 'OrderInsert'):
            date_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sql = 'select OrderDate, ShopSKU, OrderState, LastUpdated, RefundDate, Quantity, ShopName from t_order WHERE OrderID=%s; '
            cur.execute(sql, (log_info[1], ))
            order_info = cur.fetchone()
            if order_info:
                order_date = order_info[0][:10]
                shop_sku = order_info[1]
                order_state = order_info[2]
                last_update = order_info[3][:10]
                refund_date = order_info[4]
                quantity = order_info[5]
                shop_name = order_info[6]

                # 根据店铺sku到redis查询绑定的商品sku，未找到退出循环
                # sku = classshopsku_obj.getSKU(shop_sku)
                sku = get_sku_by_shopsku_shopname(shop_sku, shop_name, cur)
                if sku is None:
                    continue
                print 'sku---------------------%s' % sku

                # 如果该SKU大类是服装，则结束本轮循环
                category, saler, purchaser = get_lagrge_category(sku, cur)
                if category in CLOTHING_CATEGORY:
                    main_sku = sku
                else:
                    # 非服装大类的SKU，根据商品sku到redis查询主sku
                    # main_sku = classsku_obj.get_bemainsku_by_sku(sku)
                    main_sku = get_sku_by_productsku(sku, cur)

                if main_sku is None:
                    continue
                print 'shop_sku=%s-----sku=%s-----main_sku=%s' % (shop_sku, sku, main_sku)

                param, flag = process_order_num(main_sku, refund_date, order_date, order_state, last_update, quantity,
                                                date_now, order_flag, cur, saler, purchaser)
                insert_or_update_refund(param, flag, cur)
    id_str = '(' + ','.join(id_list) + ')'
    log_update_sql = 'update t_chart_wish_refund_log set RefundDeleteFlag=1 WHERE id in %s; ' % id_str
    cur.execute(log_update_sql)
    cur.execute('commit;')
    cur.close()


def get_sku_by_shopsku_shopname(shopsku, shopname, cur):
    """
    根据店铺sku和店铺名查询商品sku
    :param shopsku:
    :param shopname:
    :param cur:
    :return:
    """
    sql = 'select sku from t_online_info WHERE ShopSKU=%s AND ShopName=%s'
    cur.execute(sql, (shopsku, shopname[:9]))
    sku_info = cur.fetchone()
    if sku_info:
        sku = sku_info[0]
    else:
        sku = None
    return sku


def get_sku_by_productsku(product_sku, cur):
    """
    根据商品sku获得main_sku
    :param product_sku:
    :param cur:
    :return:
    """
    sql = 'select MainSKU from t_product_mainsku_sku WHERE ProductSKU = %s ;'
    cur.execute(sql, (product_sku, ))
    mainsku_info = cur.fetchone()
    if mainsku_info:
        main_sku = mainsku_info[0]
    else:
        main_sku = None
    return main_sku
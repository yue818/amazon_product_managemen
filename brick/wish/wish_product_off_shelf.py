# coding=utf-8

from django.db import connection
import xlrd
import copy
from datetime import datetime
import requests
import time
from app_djcelery.celery import app
from brick.classredis.classlisting import classlisting
from brick.classredis.classskuableornot import classskuableornot
from brick.classredis.classshopsku import classshopsku
from django_redis import get_redis_connection
redis_conn = get_redis_connection(alias='product')


# 变体信息检索API
retrieve_product_variation_api = ' https://merchant.wish.com/api/v2/variant'
# 变体下架API
disable_product_variation_api = 'https://merchant.wish.com/api/v2/variant/disable'
# 变体上架API
enable_product_variation_api = 'https://merchant.wish.com/api/v2/variant/enable'
# 刷新token API
refresh_access_token_api = 'https://merchant.wish.com/api/v2/oauth/refresh_token'


def read_wish_excel(file_obj):
    """
    读取EXCEL文件内的信息
    :param file_obj: 待下架商品EXCEL文件对象
    :return: 返回EXCEL文件内的商品SKU或店铺SKU
    """
    data = xlrd.open_workbook(filename=None, file_contents=file_obj.read())

    table = data.sheets()[0]
    nrows = table.nrows
    sku_list = []

    for rownum in range(nrows):
        row = table.row_values(rownum)
        if row:
            productsku = str(row[0])
            try:
                shopname = str(row[1])
            except:
                shopname = ''
                pass
            if productsku.strip() != '':
                single_sku_list = [productsku, shopname]
                sku_list.append(single_sku_list)
    return sku_list


def get_shopname_shopsku_info(sku, flag):
    """
    根据商品sku或者店铺sku去t_online_info查询店铺名和店铺sku
    :param productsku: 商品sku
    :return: 查询结果集
    """
    shopsku_shopname_list = []
    cur = connection.cursor()
    if flag == 'productsku':
        sql = 'select ShopSKU, ShopName, SKU, ProductID from t_online_info WHERE SKU=\"%s\" ;' % sku[0]
    else:
        sql = 'select ShopSKU, ShopName, SKU, ProductID from t_online_info WHERE ShopSKU=\"%s\" AND ShopName=\"%s\";' % (sku[0].replace('\\', '\\\\'), sku[1][:9])

    cur.execute(sql)
    shopsku_infos = cur.fetchall()
    for shopsku_info in shopsku_infos:
        shopsku = shopsku_info[0]
        shopname = shopsku_info[1]
        sku = shopsku_info[2]
        product_id = shopsku_info[3]
        if shopname.startswith('Wish'):
            shopsku_shopname_list.append([shopsku, shopname[:9], sku, product_id])
    cur.close()
    return shopsku_shopname_list


def get_access_token(cur, shopname):
    """
    根据店铺名获取access_token
    :param shopName: 店铺名
    :return: shopName下的配置信息
    """
    auth_info = {'shop_name': shopname}
    sql = 'select IP,`Name`,K,V from t_config_online_amazon  where name= %s'
    cur.execute(sql, (shopname[:9],))
    config_infos = cur.fetchall()

    for config_info in config_infos:
        k = config_info[2]
        v = config_info[3]
        auth_info[k] = v
    return auth_info


def judge_promoted(productID):
    """
    获取商品是否加钻（促销）
    :param productID: 在线listing的ID
    :return: 加钻返回True，不加钻返回False
    """
    classlisting_obj = classlisting(db_conn=connection, redis_conn=redis_conn)
    return classlisting_obj.get_is_promoted_listingid(productID)


def judge_week_order_num(cur, productID):
    """
    判断七天order数是否大于50
    :param sku:
    :return: 大于50返回True，小于50或没查到返回False
    """
    sql = 'select Orders7Days from t_online_info_wish WHERE ProductID=%s ORDER BY Orders7Days DESC '
    cur.execute(sql, (productID,))
    info = cur.fetchone()
    if not info:
        result = False
    else:
        if info[0] >= 50:
            result = True
        else:
            result = False
    return result


def judge_enable(sku):
    """
    判断商品状态，包括商品状态是否正常、商品是否侵权
    :param sku:
    :return: 正常返回True，不正常返回False
    """
    classskuableornot_obj = classskuableornot(db_conn=connection, redis_conn=redis_conn)
    return classskuableornot_obj.judgeskuableornotWish(sku)


def update_shop_config_info(cur, new_auth_info):
    """
    更新config配置表信息
    :param new_auth_info: 原始的config信息
    """
    # 执行access_token更新
    sql_access_token = 'update t_config_online_amazon set V= \'%s\' where Name =\'%s\' and K =\'%s\' ' % (
        new_auth_info['access_token'], new_auth_info['ShopName'], 'access_token')
    print sql_access_token
    cur.execute(sql_access_token)

    # 执行refresh_token更新
    sql_refresh_token = 'update t_config_online_amazon set V= \'%s\' where Name =\'%s\' and K =\'%s\' ' % (
        new_auth_info['refresh_token'], new_auth_info['ShopName'], 'refresh_token')
    print sql_refresh_token
    cur.execute(sql_refresh_token)

    # 执行更新时间插入
    last_refresh_token_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql_time = 'insert into t_config_online_amazon(Name,K,V) values(%s,%s,%s)'
    cur.execute(sql_time, (new_auth_info['ShopName'], 'last_refresh_token_time', last_refresh_token_time))
    cur.execute('commit ;')


def refresh_token(original_auth_info):
    """
    更新access_token
    :param original_auth_info: 该店铺原始的认证信息
    :return: 更新access_token后的认真信息
    """
    new_auth_info = copy.deepcopy(original_auth_info)

    data = {
        'client_id': original_auth_info['client_id'],
        'client_secret': original_auth_info['client_secret'],
        'refresh_token': original_auth_info['refresh_token'],
        'grant_type': 'refresh_token',
    }

    resp = requests.post(refresh_access_token_api, params=data, timeout=30)
    content = eval(resp.content.replace(':null,', ':0,'))

    new_auth_info['access_token'] = content['data']['access_token']
    new_auth_info['refresh_token'] = content['data']['refresh_token']

    return new_auth_info


def execute_off_shelf(url, shopsku, auth_info, flag):
    """
    检索或者下架商品，根据参数url的不同而定
    :param shopsku: 店铺sku
    :param auth_info: 店铺认证信息
    :return: 下架请求结果
    """
    data = {
        'sku': shopsku,
        'access_token': auth_info['access_token']
    }

    resp = requests.post(url, params=data, timeout=30)
    if resp.status_code == 200:
        result = eval(resp.content)
    else:
        if flag == 'retrieve':
            result = {'code': resp.status_code, 'message': u'检索时网络错误'}
        elif flag == 'disable':
            result = {'code': resp.status_code, 'message': u'下架时网络错误'}
        else:
            result = {'code': resp.status_code, 'message': u'上架时网络错误'}

    if flag == 'disable':
        print 'disable_requests_result-----------%s' % result

    if flag == 'enable':
        print 'enable_requests_result-----------%s' % result

    return result


def requests_error_retry(cur, shopsku, auth_info, error_flag, request_flag):
    """
    access_token或者connection failed错误重试三次
    :param shopsku: 店铺sku
    :param auth_info: 店铺认证信息
    :return: 下架请求重试结果
    """
    i = 0
    j = 0

    # token错误，重试三次，直至成功
    if error_flag == 'token_error':
        while i < 3:
            new_auth_info = refresh_token(auth_info)

            time.sleep(1)
            if request_flag == 'retrieve':
                result = execute_off_shelf(retrieve_product_variation_api, shopsku, new_auth_info, 'retrieve')
            elif request_flag == 'disable':
                result = execute_off_shelf(disable_product_variation_api, shopsku, new_auth_info, 'disable')
            else:
                result = execute_off_shelf(enable_product_variation_api, shopsku, new_auth_info, 'enable')

            if result['code'] == 0:
                update_shop_config_info(cur, new_auth_info)
                break
            i += 1

    # 网络错误，重试三次，直至成功
    else:
        while j < 3:
            time.sleep(2)

            if request_flag == 'retrieve':
                result = execute_off_shelf(retrieve_product_variation_api, shopsku, auth_info, 'retrieve')
            elif request_flag == 'disable':
                result = execute_off_shelf(disable_product_variation_api, shopsku, auth_info, 'disable')
            else:
                result = execute_off_shelf(enable_product_variation_api, shopsku, auth_info, 'enable')

            if result['code'] == 0:
                break

            j += 1
    return result


def insert_into_mysql(cur, param):
    """
    将结果插入到表中
    :param param: 结果
    """
    sql = 'insert into t_product_wish_off_shelf VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    cur.execute(sql, tuple(param))
    cur.execute('commit ;')


def disable_detail_processing(param, shopsku_infos, flag, reason):
    """
    细节处理环节，
    :param param: 带插入数据库的参数
    :param shopsku_infos: [ [shopsku, shopname]…… ]
    :return:
    """

    cur = connection.cursor()
    # 如果根据商品sku能查到店铺sku信息
    if shopsku_infos:
        for shopsku_info in shopsku_infos:
            shopsku = shopsku_info[0]
            shopname = shopsku_info[1]
            # sku = shopsku_info[2]
            # productID = shopsku_info[3]

            param[2] = shopsku
            param[3] = shopname
            # 上架预警
            # if reason == 'sj':
            #     # 如果商品状态不正常，跳出此次循环
            #     if not judge_enable(sku):
            #         param[8] = 'ENABLE_CANCELL'
            #         param[9] = u'该商品检测到WISH侵权或商品状态不正常'
            #         param[10] = ''
            #         insert_into_mysql(cur, param)
            #         continue
            # # 下架预警
            # else:
            #     # 如果检测到产品加钻或者七天订单数大于50，跳出此次循环
            #     if eval(judge_promoted(productID)) or judge_week_order_num(productID):
            #         param[8] = 'DISABLE_CANCELL'
            #         param[9] = u'该商品检测到加钻或七天订单数大于50'
            #         param[10] = ''
            #         insert_into_mysql(cur, param)
            #         continue

            auth_info = get_access_token(cur, shopname)
            time.sleep(1)

            # 检索结果
            retrieve_result = execute_off_shelf(retrieve_product_variation_api, shopsku, auth_info, 'retrieve')

            # access_token错误，则重试三次
            if retrieve_result['code'] == 1015 or retrieve_result['code'] == 1016:
                retrieve_result = requests_error_retry(cur, shopsku, auth_info, 'token_error', 'retrieve')

            # 网络连接失败，
            if retrieve_result['code'] == 400:
                retrieve_result = requests_error_retry(cur, shopsku, auth_info, 'connection_error', 'retrieve')

            # 检索请求成功
            if retrieve_result['code'] == 0:
                # 商品为在线状态
                if retrieve_result['data']['Variant']['enabled'] == 'True':
                    # 如果人为操作不是上架，则进行下架
                    if reason != 'sj':
                        disable_result = execute_off_shelf(disable_product_variation_api, shopsku, auth_info, 'disable')

                        # access_token错误，则重试三次
                        if disable_result['code'] == 1015 or disable_result['code'] == 1016:
                            disable_result = requests_error_retry(cur, shopsku, auth_info, 'token_error', 'disable')

                        if disable_result['code'] == 400:
                            disable_result = requests_error_retry(cur, shopsku, auth_info, 'connection_error', 'disable')

                        if disable_result['code'] == 0:
                            param[8] = 'DISABLE_SUCCESS'
                            param[9] = disable_result['message']
                            param[10] = 'API'

                            update_state_after_success(cur, shopsku_info, 'Disabled')
                        else:
                            param[8] = 'DISABLE_FAILED'
                            param[9] = disable_result['message']
                            param[10] = ''
                    # 如果人为操作是上架，则提醒已经是上架状态
                    else:
                        param[8] = 'ENABLE_FAILED'
                        param[9] = u'该店铺SKU已经是上架状态'
                        param[10] = ''

                # 商品为不在线状态
                else:
                    # 如果人为操作不是上架，则不做处理
                    if reason != 'sj':
                        param[8] = 'DISABLE_FAILED'
                        param[9] = u'该店铺SKU已经是下架状态'
                        param[10] = ''

                    # 如果人为操作是上架，则对不在线的变体进行上架操作
                    else:
                        enable_result = execute_off_shelf(enable_product_variation_api, shopsku, auth_info, 'enable')

                        # access_token错误，则重试三次
                        if enable_result['code'] == 1015 or enable_result['code'] == 1016:
                            enable_result = requests_error_retry(cur, shopsku, auth_info, 'token_error', 'disable')

                        if enable_result['code'] == 400:
                            enable_result = requests_error_retry(cur, shopsku, auth_info, 'connection_error', 'disable')

                        if enable_result['code'] == 0:
                            param[8] = 'ENABLE_SUCCESS'
                            param[9] = enable_result['message']
                            param[10] = 'API'

                            update_state_after_success(cur, shopsku_info, 'Enabled')
                        else:
                            param[8] = 'ENABLE_FAILED'
                            param[9] = enable_result['message']
                            param[10] = ''
            else:
                param[8] = 'RETRIEVE_FAILED'
                param[9] = retrieve_result['message']
                param[10] = ''
            insert_into_mysql(cur, param)

    else:
        if flag == 'productsku':
            param[8] = 'RELATED_FAILED'
            param[9] = u'未发现该商品SKU绑定的店铺SKU'
        else:
            param[8] = 'UNKNOW_SHOPSKU'
            param[9] = u'该店铺SKU未找到对应的店铺'
        insert_into_mysql(cur, param)
    cur.close()


def update_state_after_success(cur, shopsku_info, state):
    """
    在上架或下架成功后更改redis、t_goods_shelves、t_online_info里的商品状态
    :param shopsku_info:
    :param state:
    :return:
    """
    shopsku = shopsku_info[0]
    productID = shopsku_info[3]

    classshopsku_obj = classshopsku(db_conn=connection, redis_conn=redis_conn)
    classshopsku_obj.setStatus(shopsku=shopsku, status=state)

    goods_shelves_sql = 'update t_goods_shelves set Status=%s WHERE ProductID=%s AND ShopSKU=%s'
    online_info_sql = 'update t_online_info set Status=%s WHERE ProductID=%s AND ShopSKU=%s'
    cur.execute(goods_shelves_sql, (state, productID, shopsku))
    cur.execute(online_info_sql, (state, productID, shopsku))
    cur.execute('commit; ')

    # 更新listing在线状态
    update_wish_listing_status(cur, productID)


def update_wish_listing_status(cur, productID):
    # 店铺SKU状态结果集
    sstatuslist = get_shopskustatus_by_productid(cur, productID)
    b1 = 0
    if 'Enabled' in sstatuslist:
        b1 = 1
    b2 = 0
    if 'Disabled' in sstatuslist:
        b2 = 1
    ShopsFlag = b1 * 10 + b2

    if 'Enabled' in sstatuslist:
        sql = 'update t_online_info_wish set ShopsFlag=%s, Status="Enabled" where ProductID=%s; '
    else:
        sql = 'update t_online_info_wish set ShopsFlag=%s, Status="Disabled" where ProductID=%s; '
    cur.execute(sql, (ShopsFlag, productID))
    cur.execute('commit;')


def get_shopskustatus_by_productid(cur, productID):
    cur.execute("select DISTINCT Status from t_online_info WHERE ProductID=%s;", (productID,))
    infos = cur.fetchall()
    infolist = []
    for info in infos:
        infolist.append(info[0])
    return infolist


from app_djcelery.tasks import wish_product_off_shelf, wish_product_on_shelf, wish_product_off_shelf_urgent
def wish_product_shelf_enter(file_obj, now_time, first_name, reason):
    """
    未绑定下架：shopsku+shopname下架
    清仓或者可卖天数小于7的下架：productsku下架
    上架：shopsku+shopname上架
    紧急下架：shopsku+shopname下架 或者 productsku下架
    """
    create_time = now_time.strftime('%Y-%m-%d %H:%M:%S')
    create_staff = first_name

    original_param = [0, '', '', '', reason, file_obj.name, create_time, create_staff, '', '', '']
    sku_list = read_wish_excel(file_obj)
    print sku_list

    if reason == 'sj':
        for single_sku_list in sku_list:
            wish_product_on_shelf.delay(single_sku_list, reason, original_param)
    elif reason == 'urgent_off_sku' or reason == 'urgent_off_shopsku':
        for single_sku_list in sku_list:
            wish_product_off_shelf_urgent.delay(single_sku_list, reason, original_param)
    else:
        for single_sku_list in sku_list:
            wish_product_off_shelf.delay(single_sku_list, reason, original_param)
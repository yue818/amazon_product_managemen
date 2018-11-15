# coding=utf-8

from django.db import connection
from brick.classredis.classsku import classsku
from django_redis import get_redis_connection


# def connnectToMysql():
#     """连接MySQL数据库"""
#     import MySQLdb, time
#     HOST = 'hequskuapp.mysql.rds.aliyuncs.com'
#     PORT = 3306
#     USER = 'by15161458383'
#     PASSWORD = 'K120Esc1'
#     DB = 'hq_db'
#     CHARSET = 'utf8'
#     try:
#         mysqlClient = MySQLdb.connect(host=HOST, port=PORT, user=USER, passwd=PASSWORD, db=DB, charset=CHARSET)
#     except MySQLdb.Error, e:
#         print 'MySQL Error:%s，30秒后重新连接……' % str(e)
#         time.sleep(30)
#         connnectToMysql()
#     return mysqlClient

def select_public_info(cur):
    """
    查询公共模板中待更新的信息
    :param cur:
    :return:
    """
    all_list = []
    sql = 'select id, Variants, SrcProductID from t_templet_public_wish'
    cur.execute(sql)
    public_infos = cur.fetchall()
    for public_info in public_infos:
        update_id = int(public_info[0])
        try:
            variants = eval(public_info[1])
        except:
            continue
        product_id = public_info[2]
        temp_list = [update_id, variants, product_id]
        all_list.append(temp_list)
    return all_list


def update_public_info(cur, id, variants):
    """
    更新公共模板信息
    :param cur:
    :param id: 待更新id
    :param variants: 变体信息
    :return:
    """
    sql = 'update t_templet_public_wish set Variants=%s WHERE id=%s'
    cur.execute(sql, (str(variants), id))


def select_online_info(cur, product_id):
    """
    根据productID查询listing在线信息
    :param cur:
    :param product_id:
    :return:
    """
    all_list = []
    sql = 'select SKU from t_online_info WHERE productID=%s'
    cur.execute(sql, (product_id, ))
    online_infos = cur.fetchall()
    for online_info in online_infos:
        product_sku = online_info[0]
        single_list = [product_sku]
        all_list.append(single_list)
    return all_list


def refresh_templet_listing_status():
    # connection = connnectToMysql()
    cur = connection.cursor()
    redis_coon = get_redis_connection(alias='product')
    classsku_obj = classsku(connection, redis_coon)
    public_info_list = select_public_info(cur)
    i = 0
    for public_info in public_info_list:
        i += 1
        update_id, variants, product_id =  public_info[0], public_info[1], public_info[2]
        print 'public_id--------------------%s' % update_id
        print 'before_variants-------------------%s' % variants
        online_info_list = select_online_info(cur, product_id)
        for online_info in online_info_list:
            product_sku = online_info[0]
            print 'product_sku--%s' % product_sku
            for variant in variants:
                if variant['Variant']['productSKU'] == product_sku:
                    goodsStatus = classsku_obj.get_goodsstatus_by_sku(product_sku)
                    if goodsStatus == u'正常':
                        variant['Variant']['enabled'] = True
                    else:
                        variant['Variant']['enabled'] = False
        update_public_info(cur, update_id, variants)
        print 'after_variants-------------------%s' % variants
        if i % 500 == 0:
            cur.execute('commit;')

    cur.execute('commit;')
    cur.close()
    connection.close()

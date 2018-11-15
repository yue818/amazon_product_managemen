# coding=utf-8

"""
wish生成公共模板的同时生成joom采集箱信息
"""

from django.db import connection


def create_collection_box_from_wish(joom_id, user, time):
    cur = connection.cursor()
    if len(joom_id) == 1:
        sql = 'select id, MainSKU, Title, Description, Tags, MainImage, ExtraImages, Status, Variants, CreateTime, CreateStaff, UpdateTime, UpdateStaff, CoreWords, CoreTags, SrcProductID, SkuState from t_templet_public_wish_review where id= ' + str(joom_id[0])
    else:
        sql = 'select id, MainSKU, Title, Description, Tags, MainImage, ExtraImages, Status, Variants, CreateTime, CreateStaff, UpdateTime, UpdateStaff, CoreWords, CoreTags, SrcProductID, SkuState from t_templet_public_wish_review where id IN ' + str(tuple(joom_id))
    cur.execute(sql)
    wish_objs = cur.fetchall()
    for wish_tuple in wish_objs:
        wish_list = list(wish_tuple)
        for i in range(len(wish_list)):
            if wish_list[i] == None:
                wish_list[i] = ''
        variants = eval(wish_tuple[8])
        b_cost_weight = []
        for variant in variants:
            b_cost_weight.append(select_py_info(variant['Variant']['productSKU']))
        wish_list[0] = 0
        wish_list[7] = 0
        wish_list[9] = time.strftime('%Y-%m-%d %H:%M:%S')
        wish_list[10] = user
        wish_list[11] = time.strftime('%Y-%m-%d %H:%M:%S')
        wish_list[12] = user
        wish_list.append(str(b_cost_weight))
        wish_list.append('WISH')
        insert_sql = 'insert into t_templet_joom_collection_box(id, MainSKU, Title, Description, Tags, MainImage,' \
                     'ExtraImages, Status, Variants, CreateTime, CreateStaff, UpdateTime, UpdateStaff, CoreWords, ' \
                     'CoreTags, SrcProductID, SkuState, B_cost_weight, Source) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,' \
                     '%s,%s,%s,%s,%s,%s,%s,%s)'
        cur.execute(insert_sql, tuple(wish_list))
    cur.close()


def select_py_info(sku):
    sku_cost_weight = {}
    cost_weight = {}

    if sku == '':
        pass
    else:
        cur = connection.cursor()
        sql = 'select CostPrice, Weight from py_db.b_goods where sku=\"%s\"; ' % sku
        cur.execute(sql)
        b_goods_obj = cur.fetchall()
        cur.close()

        if len(b_goods_obj) != 0:

            cost_weight['cost_price'] = ''
            try:
                cost_weight['cost_price'] = str(b_goods_obj[0][0])
            except:
                pass

            cost_weight['weight'] = ''
            try:
                cost_weight['weight'] = str(b_goods_obj[0][1])
            except:
                pass

    sku_cost_weight[sku] = cost_weight
    return sku_cost_weight

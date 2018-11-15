# coding=utf-8

"""
WISH铺货信息展开
"""

import re
from copy import deepcopy
from django.db import connection
from random import choice, uniform
from datetime import datetime, timedelta
from brick.wish.wish_distribution.db_operation import DbOperation
from brick.public.shopsku_apply import shopsku_apply


def get_shopName(shop):
    """生成店铺名称"""
    shopcode = re.findall(r'[0-9]', shop)
    code = ''.join(shopcode)
    new_shopname = 'Wish-%s' % (code.zfill(4))
    return new_shopname

def char_process(illegal_str):
    """处理字符串里的不合法字符"""
    legal_str = illegal_str.replace("&#39;", "'").replace("&amp;", "&").replace("\\/", '/').replace("&quot;", '`').replace("'", '`').replace('\uff1a', ':')
    return legal_str

def get_params_variants(info):
    """获取基础信息"""
    params = {'first': {'url': 'https://merchant.wish.com/api/v2/product/add', 'product': {}},
              'second': {'url': 'https://merchant.wish.com/api/v2/variant/add', 'product': []},
              }
    params['first']['product']['name'] = char_process(info['title'])
    params['first']['product']['description'] = char_process('description')
    params['first']['product']['tags'] = char_process('tags')
    params['first']['product']['extra_images'] = info[4]
    variants = eval(char_process(info['variants']))
    return params, variants

def generate_new_title(core_words_list, title):
    core_word = choice(core_words_list)
    position = choice([0, 1])
    if position == 0:
        title = core_word + ' ' + title
    else:
        title = title + ' ' + core_word
    return title

def generate_schedule_time(time_plan_str, j):
    """获得铺货定时"""
    time_plan = eval(time_plan_str)
    interval_time = time_plan['interval']
    start_time = time_plan['start']
    inval = float(interval_time) * (uniform(0.9, 1.1)) + (float(interval_time) * j)
    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    schedule_time = (start_time + timedelta(minutes=inval)).strftime("%Y-%m-%d %H:%M:%S")
    return schedule_time

def wish_open(wait_open_id_tuple):
    """展开待铺货模板到铺货前的审核"""
    cur = connection.cursor()
    DbOperation_obj = DbOperation(cur=cur)
    get_wait_open_result = DbOperation_obj.get_wait_open(wait_open_id_tuple)
    if get_wait_open_result['error_code'] == 0:
        wait_open_list = get_wait_open_result['wait_open_list']
        core_words_list = DbOperation_obj.get_core_list()['core_words_list']
        for each in wait_open_list:
            original_variants = eval(each['variants'])
            main_image_list = DbOperation_obj.get_main_image(main_sku=each['main_sku'])['main_image_list']
            variant_num = len(original_variants)
            j = 0
            for shop in each['shop_sets'].split(','):
                parent_sku = None
                variants = deepcopy(original_variants)
                shop_name = get_shopName(shop=shop)
                j += 1
                new_title = generate_new_title(core_words_list, char_process(each['title']))
                schedule_time = generate_schedule_time(each['time_plan'], j)

                if len(main_image_list) != 0:
                    main_image = choice(main_image_list)
                else:
                    main_image = each['main_image']

                for i in range(variant_num):
                    orginal_shopsku = variants[i]['Variant']['sku']
                    product_sku = variants[i]['Variant']['productSKU']
                    shopsku_apply_result = shopsku_apply(input_sku=product_sku, shop_name=shop_name, first_name=each['create_staff'])
                    shopsku_productsku_dict = shopsku_apply_result.get('success_sku', '')
                    if shopsku_productsku_dict:
                        shop_sku = shopsku_productsku_dict.keys()[0]
                        num_str = ''
                        if '*' in orginal_shopsku:
                            num_str = '*' + orginal_shopsku.split('*')[-1]
                        shop_sku = shop_sku + num_str
                        if i == 0:
                            parent_sku = shop_sku
                        variants[i]['Variant']['sku'] = shop_sku
                        variants[i]['Variant']['parent_sku'] = parent_sku
                    else:
                        continue
                review_param = (
                    each['main_sku'], parent_sku, new_title, char_process(each['description']),
                    char_process(each['tags']), main_image, each['extra_images'], str(variants), shop_name,
                    schedule_time, each['core_words'], each['create_staff'], str(each['post_time']),
                    'UNSUBMITTED', 'UNREVIEW'
                )
                DbOperation_obj.insert_into_distribution_review(review_param=review_param)
            DbOperation_obj.update_wait_upload(each['id'])
    cur.close()

def to_distribution(distribution_id_tuple):
    """将审核之后的展开数据插入到指令表中"""
    cur = connection.cursor()
    DbOperation_obj = DbOperation(cur=cur)
    get_wait_open_result = DbOperation_obj.get_distribution_info(distribution_id_tuple)
    if get_wait_open_result['error_code'] == 0:
        wait_distribution_list = get_wait_open_result['wait_distribution_list']
        for each in wait_distribution_list:
            params = {'first': {'url': 'https://merchant.wish.com/api/v2/product/add', 'product': {}},
                      'second': {'url': 'https://merchant.wish.com/api/v2/variant/add', 'product': []},
                      'main_image': each['main_image']
                      }
            distribution_id = each['id']
            main_sku = each['main_sku']
            title = each['title']
            description = each['description']
            tags = each['tags']
            extra_images = each['extra_images']
            variants = eval(each['variants'])
            shop_name = each['shop_name']
            schedule = each['schedule']
            parent_sku = each['parent_sku']
            create_staff = each['create_staff']
            post_time = datetime.now()
            goods_exits_in_shop_result = DbOperation_obj.goods_exits_in_shop(main_sku=main_sku, shop_name=shop_name)
            if goods_exits_in_shop_result['error_code'] == 0:
                params['first']['product']['name'] = title
                params['first']['product']['description'] = description
                params['first']['product']['tags'] = tags
                params['first']['product']['extra_images'] = extra_images
                variant_num = len(variants)
                for i in range(variant_num):
                    if i == 0:
                        params['first']['product'] = dict(params['first']['product'], **variants[i]['Variant'])
                    else:
                        variant = variants[i]['Variant']
                        variant.pop('shipping')
                        params['second']['product'].append(variant)

                if DbOperation_obj.judge_exists_result(main_sku=main_sku, shop_name=shop_name):
                    result_status = 'ING'
                    result_id = DbOperation_obj.insert_into_result(main_sku, distribution_id, shop_name, result_status, create_staff, post_time, schedule, params, parent_sku, params['main_image'])
                    params['id'] = result_id['result_id']
                    DbOperation_obj.insert_into_schedule(shop_name, schedule, str(params), params['id'])
                else:
                    result_status = 'EXISTS'
                    DbOperation_obj.insert_into_result(main_sku, distribution_id, shop_name, result_status, create_staff, post_time, schedule)
            else:
                result_status = 'REPETITION'
                DbOperation_obj.insert_into_result(main_sku, distribution_id, shop_name, result_status, create_staff, post_time)
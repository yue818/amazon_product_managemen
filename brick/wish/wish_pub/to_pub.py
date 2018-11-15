#-*-coding:utf-8-*-
u"""
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: to_pub.py
 @time: 2018/6/12 10:35
"""
from brick.wish.api.wishapi import cwishapi
import json
import logging
from retrying import retry

from django.db import connection

logger = logging.getLogger('sourceDns.webdns.views')

def update_RetryNum(pid):
    cursor = connection.cursor()
    cursor.execute("update t_templet_wish_publish_result set RetryNum = RetryNum + 1 WHERE pid = %s ;", (pid,))
    cursor.execute("commit;")
    cursor.close()


@retry(stop_max_attempt_number=3,wait_exponential_multiplier=500,wait_exponential_max=3000)
def create_product(fristparam, pid):
    fResult = cwishapi().wish_goods_upload_api(fristparam)
    # fResult = {'errorcode': 1, 'errortext': 'wwwwwwwwwwwwwwwwww', 'productid': '123123123123123123'}
    if fResult['errorcode'] == 1:
        return fResult
    else:
        # update_RetryNum(pid)
        raise Exception(u'An error occurred while creating the product: {}'.format(fResult['errortext']))


@retry(stop_max_attempt_number=3,wait_exponential_multiplier=500,wait_exponential_max=3000)
def create_variant(secondparam, id, pid):
    sResult = cwishapi().wish_variant_goods_add_api(secondparam)
    # sResult = {'errorcode': 0, 'errortext': 'eeeeeeeeeeeeeeeeeeeeee'}
    if sResult['errorcode'] == 1:
        return sResult
    # elif sResult.get('apicode') == 1000:  # code = 1000 店铺SKU已经存在   可能是刊登已经成功，只是wish返回失败
    #     return sResult
    else:
        update_RetryNum(pid)
        raise Exception(u'An error occurred while creating the variant: {}; Please remove the exception link：{}, regenerate the ShopSKU and ParentSKU , and published again!'.format(sResult['errortext'], id))


@retry(stop_max_attempt_number=3,wait_exponential_multiplier=500,wait_exponential_max=3000)
def update_first_variant_img(imgparam, id, pid):
    uResult = cwishapi().update_vinfo(imgparam)
    # uResult = {'errorcode': 1, 'errortext': 'ggggggggggggggggggg'}
    if uResult['errorcode'] == 1:
        return uResult
    else:
        # update_RetryNum(pid)
        raise Exception(u'Error modifying the first variant map. ProductID: {}; {} Instead of returning to repost, you can go to store management and change the first variant.'.format(id, uResult['errortext']))


def to_pub(data, pid):
    try:
        param = json.loads(data)

        fristurl   = param['first']['url']
        fristparam = param['first']['product']

        mainimage = param['main_image']
        fristvpic = param['first']['product']['main_image']

        fristparam['main_image'] = mainimage  # 先将主图替换了，创建产品是 第一个变体图替换

        fResult = create_product(fristparam, pid)

        secondurl = param['second']['url']
        if param['second']['product']:
            for secondparam in param['second']['product']:
                try:
                    sResult = create_variant(secondparam, fResult['productid'], pid)
                except Exception as e:
                # if sResult and sResult['errorcode'] != 1:
                    try:  # 如果创建变体时出现错误，则执行该链接的下架操作
                        dis_param = {
                            'access_token': param['first']['product']['access_token'],
                            'format': 'json',
                            'ProductID': fResult['productid'],
                            'ParentSKU': ''
                        }
                        r = cwishapi().disable_by_wish_api(dis_param)
                    except Exception as ex:
                        print u'%s:%s' % (Exception, ex)
                    # 不管下架操作执行是否成功，都抛出异常
                    raise Exception(e)

        if fristvpic:  # 如果 第一变体 有图片
            imgparam = {  # 如果有其他变体，在将第一个变体的图片 修改回来
                'access_token': param['first']['product']['access_token'],
                'format': 'json',
                'sku': param['first']['product']['sku'],
                'main_image': fristvpic,
                "update_product_image": "False",   #  不改变主产品的图片  这个是关键
            }
            # logger.error("imgparam===%s" % (imgparam,))
            uResult = update_first_variant_img(imgparam, fResult['productid'], pid)

        return {'errorcode':1, 'errortext': '', 'productid': fResult['productid']}
    except Exception, e:
        print u'%s:%s' % (Exception, e)
        return {'errorcode': -1, 'errortext': u'%s:%s' % (Exception, e)}


























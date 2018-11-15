# -*- coding: utf-8 -*-
"""
@desc:写redis和更新t_onlin_info_wish(goodsflag)、t_online_info(goodsstatus)
@author: wangzhiyang
@software: PyCharm
@file:t_delete_goodsattr.py
@time: 20180523
"""

import sys
import os
sys.path.append('/data/djangostack-1.9.7/apps/django/django_projects/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Project.settings')
from t_event_database import t_event_database
from t_online_info_event_function import t_online_info_event_function
from brick.classredis.classsku import classsku,connRedis
import  time

classsku_obj = classsku()

'''
说明：根据事件触发调用该函数，设置redis和更新t_onlin_info_wish(goodsflag)、t_online_info(goodsstatus)
入参：josn格式数据（{"sku":"WF-1197-WT-S","old":"正常","new":"","used":""}）
'''
def run(josnData):
    try:
        result = {}
        goodsstatus = None
        dbconnect = t_event_database()
        dbResult = dbconnect.run()
        assert dbResult['errorcode'] == 0, 'line =%s mysql connect error'%(sys._getframe().f_lineno)
        # 开启 事务
        mysqlCursor = (dbResult['db_conn']).cursor()
        mysqlCursor.execute("begin;")
        strSKU = josnData["sku"]
        strOldStatus = josnData["old"]
        strNewStatus = josnData["new"]
        strUsed = josnData["used"]

        t_online_info_event_function_obj = t_online_info_event_function(dbResult['db_conn'])
        pResultAllProduct = t_online_info_event_function_obj.get_allProductid_by_sku(strSKU)
        assert pResultAllProduct['errorcode'] == 1, 'line=%s,%s'%(sys._getframe().f_lineno,pResultAllProduct['errortext'])
        if len(pResultAllProduct['list']) == 0:
            result['errorcode'] = 0
            connRedis.hdel(strSKU, 'GoodsStatus')
            result['errortext'] = "no recorde"
            return result

        #置商品状态为空  SKU设置为空
        pReturnResult = t_online_info_event_function_obj.updata_by_sku(None, strSKU)
        assert pReturnResult['errorcode'] == 1, 'line=%s,%s'%(sys._getframe().f_lineno,pReturnResult['errortext'])
        pReturnResult = t_online_info_event_function_obj.updata_sku_by_sku(strSKU)
        assert pReturnResult['errorcode'] == 1, 'line=%s,%s' % (sys._getframe().f_lineno, pReturnResult['errortext'])

        strProductID = "'" + "','".join(pResultAllProduct['list']) + "'"
        pReturnStatus = t_online_info_event_function_obj.get_goodsstatus_by_productid(strProductID,strSKU)
        assert pReturnStatus['errorcode'] == 1, 'line=%s,%s'%(sys._getframe().f_lineno,pReturnStatus['errortext'])
        statuslist = pReturnStatus['list']
        a1 = 0
        if '1' in statuslist:
            a1 = 1
        a2 = 0
        if '2' in statuslist:
            a2 = 1
        a3 = 0
        if '3' in statuslist:
            a3 = 1
        a4 = 0
        if '4' in statuslist:
            a4 = 1
        GoodsFlag = a1 * 1000 + a2 * 100 + a3 * 10 + a4

        pReturnResult = t_online_info_event_function_obj.updata_by_productid(strProductID,GoodsFlag)
        assert pReturnResult['errorcode'] == 1, 'line=%s,%s'%(sys._getframe().f_lineno,pReturnResult['errortext'])

        connRedis.hdel(strSKU, 'GoodsStatus')
        dbResult['db_conn'].commit()
        result['errorcode'] = 0
        result['errortext'] = 'sku=%s delete success' % (strSKU)
    except Exception, ex:
        dbResult['db_conn'].rollback()
        result['errorcode'] = -1
        result['errortext'] = '%s' % ( ex)
        print("{}".format(result))
        mysqlCursor.close()
        dbResult['db_conn'].close()
        return result
    mysqlCursor.close()
    dbResult['db_conn'].close()
    return result

#josnData = {"sku":"W1287WT-L","old":"正常","new":"","used":""}
#run(josnData)

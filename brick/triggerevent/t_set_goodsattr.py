# -*- coding: utf-8 -*-
"""
@desc:写redis和更新t_onlin_info_wish(goodsflag)、t_online_info(goodsstatus)
@author: wangzhiyang
@software: PyCharm
@file:t_set_goodsattr.py
@time: 20180523
"""

import sys
import os
sys.path.append('/data/djangostack-1.9.7/apps/django/django_projects/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Project.settings')
from t_event_database import t_event_database
from t_online_info_event_function import t_online_info_event_function
from brick.classredis.classsku import classsku
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
        if str(strUsed) == '1':
            goodsstatus = '4'
        else:
            mysqlCursor.execute("select statuscode from goodsstatus_compare WHERE hq_GoodsStatus = %s ;", (strNewStatus,))
            statusobj = mysqlCursor.fetchone()
            if statusobj:
                goodsstatus = statusobj[0]
            else:
                assert 2 == 1, 'line=%s goodsstaus=%s not in goodsstatus_compare'%(sys._getframe().f_lineno,strNewStatus)
        t_online_info_event_function_obj = t_online_info_event_function(dbResult['db_conn'])
        pResultAllProduct = t_online_info_event_function_obj.get_allProductid_by_sku(strSKU)
        assert pResultAllProduct['errorcode'] == 1, 'line=%s,%s'%(sys._getframe().f_lineno,pResultAllProduct['errortext'])
        if len(pResultAllProduct['list']) == 0:
            result['errorcode'] = 0
            result['errortext'] = "no recorde"
            classsku_obj.set_goodsstatus_by_sku(strSKU, goodsstatus)
            updateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            classsku_obj.set_updatetime_by_sku(strSKU, updateTime)
            return result
        pReturnResult = t_online_info_event_function_obj.updata_by_sku(goodsstatus, strSKU)
        assert pReturnResult['errorcode'] == 1, 'line=%s,%s'%(sys._getframe().f_lineno,pReturnResult['errortext'])
        # strProductID = "'" + "','".join(pResultAllProduct['list']) + "'"
        for sRowProdcutID in pResultAllProduct['list']:
            pReturnStatus = t_online_info_event_function_obj.get_goodsstatus_by_productid(sRowProdcutID,strSKU)
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

            pReturnResult = t_online_info_event_function_obj.updata_by_productid(sRowProdcutID,GoodsFlag)
            assert pReturnResult['errorcode'] == 1, 'line=%s,%s'%(sys._getframe().f_lineno,pReturnResult['errortext'])

        classsku_obj.set_goodsstatus_by_sku(strSKU, goodsstatus)
        updateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        classsku_obj.set_updatetime_by_sku(strSKU, updateTime)

        dbResult['db_conn'].commit()
        result['errorcode'] = 0
        result['errortext'] = 'sku=%s insert or update success'%(strSKU)
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

#josnData = {"sku":"GS-116-BK","old":"正常","new":"正常","used":"0"}
#run(josnData)
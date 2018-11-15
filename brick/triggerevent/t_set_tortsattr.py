# -*- coding: utf-8 -*-
"""
@desc:写redis和更新t_onlin_info_wish(goodsflag)、t_online_info(goodsstatus)
@author: wangzhiyang
@software: PyCharm
@file:t_set_tortattr.py
@time: 20180523
"""

import sys
import os
sys.path.append('/data/djangostack-1.9.7/apps/django/django_projects/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Project.settings')
from t_event_database import t_event_database
from t_online_info_wish_event_function import t_online_info_wish_event_function
from brick.classredis.classmainsku import classmainsku
from django_redis import get_redis_connection
connRedis = get_redis_connection(alias='product')
import  time

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
        classmainsku_obj = classmainsku(dbconnect, connRedis)
        # 开启 事务
        mysqlCursor = (dbResult['db_conn']).cursor()
        mysqlCursor.execute("begin;")
        strMainSKU = josnData["mainsku"]
        strOldStatus = josnData["old"]
        strNewStatus = josnData["new"]
        strStatus = strNewStatus
        if len(strNewStatus) == 0:
            strStatus = 'N'
        if len(strMainSKU) == 0:
            result['errorcode'] = 0
            result['errortext'] = 'mainsku=%s is null' % (strMainSKU)
            return  result
        t_online_info_wish_event_function_obj = t_online_info_wish_event_function(dbResult['db_conn'])
        pResult = t_online_info_wish_event_function_obj.set_tortstatus_by_mainsku(strMainSKU,strStatus)
        assert pResult['errorcode'] == 1, 'line=%s,%s'%(sys._getframe().f_lineno,pResult['errortext'])

        if len(strNewStatus) == 0:
            connRedis.hdel(strMainSKU,'TortInfo')
        else:
            classmainsku_obj.set_tortstatus_by_mainsku(strMainSKU, strStatus)

        dbResult['db_conn'].commit()
        result['errorcode'] = 0
        result['errortext'] = 'mainsku=%s deal success' % (strMainSKU)
    except Exception, ex:
        dbResult['db_conn'].rollback()
        result['errorcode'] = -1
        result['messages'] = '%s' % (ex)
        print("{}".format(result))
        mysqlCursor.close()
        dbResult['db_conn'].close()
        return result
    mysqlCursor.close()
    dbResult['db_conn'].close()
    return result

#josnData = {"mainsku":"BB-053","old":"","new":"Y","used":"0"}
#run(josnData)

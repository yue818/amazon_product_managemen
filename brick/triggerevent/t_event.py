#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@desc:数据一致性事件触发实时进程
@author: dingjun
@software: PyCharm
@file:t_event.py
@time: 2018/5/20
@数据一致性事件触发实时进程
"""
import sys
import importlib
import time
from t_event_class import *
from t_event_database import *

db_conn = {}

while True:
    try:
        #连接数据库
        if len(db_conn) == 0:
            dbconnect = t_event_database()
            db_conn = dbconnect.run()
            t_config_even_objs = t_event_class(db_conn['db_conn'])
        #获取事件对应的函数列表
        function_objs = t_config_even_objs.get_event_functions()
        #获取事件函数失败 等待1分钟后 重试
        if function_objs['errorcode'] != 0:
            time.sleep(60)
            db_conn['db_conn'].close()
            print "fail wait 60s reconnect,time:%s" %(datetime.datetime.now())
            db_conn = {}
            continue
        # 获取事件函数为0 等待1分钟后 重取
        if len(function_objs['result']) ==0:
            print "get events num =0 wait 60s reget,time:%s" %(datetime.datetime.now())
            time.sleep(60)
            continue
        #遍历事件函数并执行
        for function_obj in function_objs['result']:
            try:
                params = {}
                result = {}
                function_path = function_obj[6]
                module = importlib.import_module(function_path)
                params = t_config_even_objs.format_params(function_obj[3])
                try:
                    result = module.run(params)
                    if str(result['errorcode']) == function_obj[8]:
                        t_config_even_objs.move_event_to_his(function_obj,"SUCCESS",result['errorcode'],result['errortext'])
                    else:
                        t_config_even_objs.move_event_to_his(function_obj,"FAIL",result['errorcode'],result['errortext'])
                except Exception,ex:
                    result['errorcode'] = -1
                    result['errortext'] = 'Exception = %s ex=%s  __LINE__=%s'%(Exception,ex,sys._getframe().f_lineno)
                    print 'module.run Exception = %s ex=%s  __LINE__=%s'%(Exception,ex,sys._getframe().f_lineno)
            except Exception,ex:
                result['errorcode'] = -1
                result['errortext'] = 'Exception = %s ex=%s  __LINE__=%s'%(Exception,ex,sys._getframe().f_lineno)

    except Exception, ex:
        print 'module.run Exception = %s ex=%s  __LINE__=%s' % (Exception, ex, sys._getframe().f_lineno)
    time.sleep(1)
    print "one loop,time:%s" %(datetime.datetime.now())

#关闭数据库连接
db_conn['db_conn'].close()

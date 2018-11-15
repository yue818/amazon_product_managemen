#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@desc:数据一致性事件触发实时进程
@author: dingjun
@software: PyCharm
@file:t_event_class.py
@time: 2018/5/20
@数据一致性事件触发实时进程对象
"""
import sys
import simplejson as json

def run(obj):
    try:
        result = {}
        print 88888888888
        print obj
        print obj["sku"]
        print obj["old"]
        print obj["new"]
        print obj["used"]
        result['errorcode'] = 1
    except Exception, ex:
        result['errorcode']  = -1
        print 'Exception = %s ex=%s  __LINE__=%s' % (Exception, ex, sys._getframe().f_lineno)
    return result


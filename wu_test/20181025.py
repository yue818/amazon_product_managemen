# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: 20181025.py
 @time: 2018/10/25 17:26
"""
from mws import MWSError

try:
    a = 1/0
except MWSError, ConnectionError:
    print 1
except Exception as e:
    print e
    print 3
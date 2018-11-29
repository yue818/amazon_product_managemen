# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: 20181119.py
 @time: 2018/11/19 19:42
"""  
import copy

m1 = ['m1', 28, [1, 2, 3]]
print m1
print id(m1)
print [id(m) for m in m1]
print
m2 = copy.copy(m1)
print m2
print id(m2)
print [id(m) for m in m2]

print '\n'*3
m1[0] = 'm2'
print m1
print id(m1)
print [id(m) for m in m1]
print
print m2
print id(m2)
print [id(m) for m in m2]
# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: pythonic.py
 @time: 2018-04-28 15:02
"""  


L = [i*i for i in range(5)]
print L
for index, data in enumerate(L, 1):
    print index, ':', data
print
for i in range(len(L)):
    print i+1, ':', L[i]
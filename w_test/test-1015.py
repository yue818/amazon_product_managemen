# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: test-1015.py
 @time: 2018/10/15 15:58
"""  
a = {'a':'b'}
b = a.keys()
print a, b
print '------------------------'
for i in range(0,4):
    print  '-------------c is :%s' % b
    print '--------------b is :%s' % b
    c = b[:]
    print c,a,b
    for j in range(0,2):
        a['c'] = 'c'
        c.append('d')
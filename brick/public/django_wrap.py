# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: nextrow.py
 @time: 2017-12-30 13:12

"""

def django_wrap(obj, code, num):
    planlist = obj.split(code)
    rt = ''
    a = len(planlist) % num
    rt = ''
    if a != 0:
        newlist = planlist[:-a]
    else:
        newlist = planlist
    for i in range(0, len(newlist), num):
        for f in range(0, num):
            rt = '%s%s%s' % (rt, planlist[i + f],code)
        rt = rt[:-1] + '<br>'
    if a != 0:
        b = planlist[-a:]
        rt = rt + code.join(b)
    return rt

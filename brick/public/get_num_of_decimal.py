# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: get_num_of_decimal.py
 @time: 2017-12-30 13:25

"""
import re

# 生成给定的小数位数

def get_num(num,i):
    numlist = str(num).split('.')
    if len(numlist) >= 2:
        mm = re.findall(r'[0-9]',numlist[1])
        if len(mm) > i:
            if mm[i]>4:
                a = ''
                for m in range(0,i):
                    a = '%s%s'%(a,mm[m])
                num = numlist[0] + '.' + str(int(a)+1)
    return num
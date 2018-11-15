# encoding: utf-8
"""
@author: ZhangYu
@contact: 292724306@qq.com
@site: 
@software: PyCharm
@file: mainSKU.py
@time: 2018-01-04 14:13
"""
import re


# 获得MainSKU方法  第一个 数字字母  截断        HB001AB ==》 HB001
def getMainSKU(SKU):
    value = re.compile(r'\d')
    value1 = re.compile(r'\D')
    MainSKUTmp = ''
    for i in range(0, len(SKU)):
        rt = SKU[i]
        if i < (len(SKU) - 1):
            rt1 = SKU[i + 1]
            if value.match(rt) and value1.match(rt1):
                MainSKUTmp = str(SKU[:(i + 1)])
                break
    if MainSKUTmp == '':
        MainSKUTmp = SKU

    return MainSKUTmp

#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: wish_change_shipping.py
 @time: 2018-04-07 17:23
"""
class change_shipping():
    @staticmethod
    def j_shipping(country, HH):
        if country == 'CA':
            return 0
        elif country == 'DE':
            if HH <= 4.00:
                return 0.31
            elif HH >= 4.01 and HH <= 6.00:
                return 0.48
            elif HH >= 6.01 and HH <= 8.00:
                return 0.60
            elif HH >= 8.01 and HH <= 10.00:
                return 0.75
            else:
                return 0.94
        elif country == 'FR':
            if HH <= 4.00:
                return 0.33
            elif HH >= 4.01 and HH <= 6.00:
                return 0.53
            elif HH >= 6.01 and HH <= 8.00:
                return 0.68
            elif HH >= 8.01 and HH <= 10.00:
                return 0.86
            else:
                return 1.05
        elif country == 'GB':
            if HH <= 4.00:
                return 0.24
            elif HH >= 4.01 and HH <= 6.00:
                return 0.35
            elif HH >= 6.01 and HH <= 8.00:
                return 0.49
            elif HH >= 8.01 and HH <= 10.00:
                return 0.58
            else:
                return 0.68
        elif country == 'US':
            if HH <= 4.00:
                return 0.38
            elif HH >= 4.01 and HH <= 6.00:
                return 0.58
            elif HH >= 6.01 and HH <= 8.00:
                return 0.88
            elif HH >= 8.01 and HH <= 10.00:
                return 1.09
            else:
                return 0.00
        elif country == 'BR':
            if HH <= 4.00:
                return 0.38
            elif HH >= 4.01 and HH <= 6.00:
                return 0.59
            elif HH >= 6.01 and HH <= 8.00:
                return 0.84
            elif HH >= 8.01 and HH <= 10.00:
                return 0.00
            else:
                return 0.00
        else:
            if HH <= 4.00:
                return 0.35
            elif HH >= 4.01 and HH <= 6.00:
                return 0.52
            elif HH >= 6.01 and HH <= 8.00:
                return 0.69
            elif HH >= 8.01 and HH <= 10.00:
                return 0.86
            else:
                return 1.65

    @staticmethod
    def j_SE(country, HH):
        if country == 'SE':
            if HH <= 4.00:
                return 2.06
            elif HH >= 4.01 and HH <= 6.00:
                return 2.05
            elif HH >= 6.01 and HH <= 8.00:
                return 2.02
            elif HH >= 8.01 and HH <= 10.00:
                return 1.99
            else:
                return 1.89
        else:
            return 0.00
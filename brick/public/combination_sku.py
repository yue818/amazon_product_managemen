#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: combination_sku.py
 @time: 2018-04-26 14:36
"""
from brick.table.t_combination_sku_log import t_combination_sku_log

def G_ZHSKU(setsku,coon,cName,cSID,cTime,title=''):
    t_combination_sku_log_obj = t_combination_sku_log(coon)
    ZHSKU = t_combination_sku_log_obj.ObtainZHSKU(setsku)  # 商品SKU组合编码
    code = 0
    if ZHSKU is None:
        MZHSKU = t_combination_sku_log_obj.Obtain_M_ZHSKU()
        if MZHSKU is None:
            ZHSKU = 'ZH0001'
        else:
            MCode = MZHSKU.split('ZH')[-1]  # 0001
            Code = int(MCode) + 1    # 2
            ZHSKU = 'ZH%s'%str(Code).zfill(len(MCode))

        code = t_combination_sku_log_obj.INSERTZHSKU(setsku,ZHSKU,cName,cSID,cTime,title)
    else:
        code = 2

    return {'code':code,'ZHSKU':ZHSKU}


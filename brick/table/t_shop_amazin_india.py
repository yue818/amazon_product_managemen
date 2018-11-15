#-*-coding:utf-8-*-


"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_shop_amazin_india.py
 @time: 2018/6/12 10:07
"""   
class t_shop_amazon_india():
    def __init__(self, db_conn=None):
        self.cnxn = db_conn

    def get_company_by_shopname(self, shopname):
        shocur = self.cnxn.cursor()
        shocur.execute("select Company from t_shop_amazon_india where ShopName = %s ;", (shopname,))
        t_shop_amazon_india_obj = shocur.fetchone()
        t_shop_amazon_india_temp = {}
        if t_shop_amazon_india_obj:
            t_shop_amazon_india_temp['Company'] = t_shop_amazon_india_obj[0]
        shocur.close()
        return t_shop_amazon_india_temp
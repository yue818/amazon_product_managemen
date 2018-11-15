#-*-coding:utf-8-*-


"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_sku_color.py
 @time: 2018/6/12 15:45
"""   
class t_sku_color():
    def __init__(self, db_conn=None):
        self.cnxn = db_conn

    def get_color_name_us_by_sku(self, sku_color):
        shocur = self.cnxn.cursor()
        shocur.execute("select color_name_us from t_sku_color where sku_color = %s ;", (sku_color,))
        t_sku_color_obj = shocur.fetchone()
        t_sku_color_temp = {}
        if t_sku_color_obj:
            t_sku_color_temp['color_name_us'] = t_sku_color_obj[0]
        shocur.close()
        return t_sku_color_temp


    def get_wish_color_name_us_by_sku(self, sku_color):
        shocur = self.cnxn.cursor()
        shocur.execute("select color_name_us from t_sku_color_wish where sku_color = %s ;", (sku_color,))
        t_sku_color_obj = shocur.fetchone()
        t_sku_color_temp = {}
        if t_sku_color_obj:
            t_sku_color_temp['color_name_us'] = t_sku_color_obj[0]
        shocur.close()
        return t_sku_color_temp





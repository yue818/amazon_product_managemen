#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: get_wish_product_order_updatetime.py
 @time: 2018-02-22 12:50
"""
class get_wish_product_order_updatetime():
    def __init__(self,db_coon,shopname):
       self.db_coon = db_coon
       self.shopname = shopname

    def get_updatetime(self,type):
        procur = self.db_coon.cursor()
        procur.execute("select lastupdatetime,nowupdatetime from t_wish_shop_update_time "
                       "WHERE  stype=%s and shopname=%s ;",(type,self.shopname,))
        obj = procur.fetchone()
        procur.close()
        return obj

    def update_time_or_insert(self,lastupdatetime,nowupdatetime,type):
        updcur = self.db_coon.cursor()
        updcur.execute("insert into t_wish_shop_update_time set lastupdatetime=%s,"
                       "nowupdatetime=%s,stype=%s,shopname=%s "
                       "on duplicate KEY update lastupdatetime=%s,nowupdatetime=%s;",
                       (lastupdatetime,nowupdatetime,type,self.shopname,lastupdatetime,nowupdatetime))
        updcur.execute("commit;")
        updcur.close()


#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_product_depart_get.py
 @time: 2018-03-22 16:23
"""

class t_product_depart_get():
    def __init__(self,db_conn):
        self.db_conn = db_conn

    def get_sname_mainsku(self,mainsku):
        sncur = self.db_conn.cursor()
        sncur.execute("select StaffName,LargeCategory,SmallCategory from t_product_depart_get WHERE MainSKU = %s ;",(mainsku,))
        obj = sncur.fetchone()
        sncur.close()
        return obj













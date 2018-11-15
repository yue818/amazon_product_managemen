# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_overseas_warehouse_information.py
 @time: 2018-01-08 19:50

"""
class t_overseas_warehouse_information():
    def __init__(self,db_cnxn):
        self.db_cnxn = db_cnxn

    def get_overseas_warehouse_information(self,Nickname_WareHouse):
        getcur = self.db_cnxn.cursor()
        getcur.execute("select WareHouse,CompanyAddress,City,StateProvince,PostalCode,Country,"
                       "TelephoneNo,ContactName,CompanyName,Nickname_WareHouse from t_overseas_warehouse_information "
                       "WHERE Nickname_WareHouse = %s ;",(Nickname_WareHouse,))
        obj = getcur.fetchone()
        getcur.close()
        return obj

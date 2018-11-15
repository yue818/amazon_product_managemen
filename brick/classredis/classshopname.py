# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: classshopname.py
 @time: 2018-01-13 11:23

"""   
class classshopname():
    def __init__(self,db_conn=None,redis_cnxn=None):
        self.db_conn = db_conn
        self.redis_cnxn = redis_cnxn

    #公共方法
    def __private_set_attr(self,name,key,value):
        if self.redis_cnxn is not None and value is not None:
            self.redis_cnxn.hset(name, key,value)

    def __private_get_attr(self,name,key):
        if self.redis_cnxn is not None:
            return self.redis_cnxn.hget(name,key)

    def __private_del_attr(self,name,key):
        if self.redis_cnxn is not None:
            return self.redis_cnxn.hdel(name,key)

    def set_api_status_by_shopname(self,shopname,status):
        self.__private_set_attr(shopname,'ApiStatus',status)

    def get_api_status_by_shopname(self,shopname):
        apistatus = self.__private_get_attr(shopname,'ApiStatus')
        return apistatus

    def del_api_status_by_shopname(self,shopname):
        self.__private_del_attr(shopname,'ApiStatus')

    def set_api_time_by_shopname(self,shopname,status):
        self.__private_set_attr(shopname,'ApiTime',status)

    def get_api_time_by_shopname(self,shopname):
        apistatus = self.__private_get_attr(shopname,'ApiTime')
        return apistatus

    def del_api_time_by_shopname(self,shopname):
        self.__private_del_attr(shopname,'ApiTime')

    # 这里是用来查找 店长/销售员
    def set_seller(self,shopname,seller):
        self.__private_set_attr(shopname,'Seller',seller)

    def get_seller(self,shopname):
        seller = self.__private_get_attr(shopname,'Seller')
        if seller is None and self.db_conn is not None:
            selcur = self.db_conn.cursor()
            selcur.execute("select Seller from t_store_configuration_file WHERE ShopName = %s;",(shopname,))
            obj = selcur.fetchone()
            selcur.close()
            if obj:
                seller = obj[0]
                if seller is not None and seller.strip() != '':
                    self.set_seller(shopname,seller)
                else:
                    seller = None
        return seller

    # 这里是用来查找 店铺 刊登人
    def set_Published(self, shopname, Published):
        self.__private_set_attr(shopname, 'Published', Published)

    def get_Published(self, shopname):
        Published = self.__private_get_attr(shopname, 'Published')
        if Published is None and self.db_conn is not None:
            pubcur = self.db_conn.cursor()
            pubcur.execute("select Published from t_store_configuration_file WHERE ShopName = %s;", (shopname,))
            obj = pubcur.fetchone()
            pubcur.close()
            if obj:
                Published = obj[0]
                if Published is not None and Published.strip() != '':
                    self.set_Published(shopname, Published)
                else:
                    Published = None
        return Published

    # 这里是用来查找 店铺 的所属部门
    def set_DepartmentID(self, shopname, DepartmentID):
        self.__private_set_attr(shopname, 'DepartmentID', DepartmentID)

    def get_DepartmentID(self, shopname):
        DepartmentID = self.__private_get_attr(shopname, 'DepartmentID')
        if DepartmentID is None and self.db_conn is not None:
            pubcur = self.db_conn.cursor()
            pubcur.execute("select Department from t_store_configuration_file WHERE ShopName = %s;", (shopname,))
            obj = pubcur.fetchone()
            pubcur.close()
            if obj:
                DepartmentID = obj[0]
                if DepartmentID is not None and DepartmentID.strip() != '':
                    self.set_DepartmentID(shopname, DepartmentID)
                else:
                    DepartmentID = None
        return DepartmentID



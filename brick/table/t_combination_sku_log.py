#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_combination_sku_log.py
 @time: 2018-04-26 14:03
"""

class t_combination_sku_log():
    def __init__(self,db_conn):
        self.db_conn = db_conn

    def ObtainZHSKU(self,skuset):
        cursor = self.db_conn.cursor()
        cursor.execute("select Com_SKU from t_combination_sku_log WHERE Pro_SKU=%s LIMIT 1;",(skuset,))
        obj = cursor.fetchone()
        cursor.close()
        csku = None
        if obj:
            csku = obj[0]
        return csku

    def Obtain_M_ZHSKU(self):
        cursor = self.db_conn.cursor()
        cursor.execute("select max(Com_SKU) from t_combination_sku_log;")
        obj = cursor.fetchone()
        cursor.close()
        msku = None
        if obj:
            msku = obj[0]
        return msku

    def INSERTZHSKU(self,sSKU,cSKU,cName,cSID,cTime):
        try:
            cursor = self.db_conn.cursor()
            cursor.execute("insert into t_combination_sku_log "
                           "SET Pro_SKU=%s,Com_SKU=%s,CreateName=%s,CreateStaffID=%s,CreateTime=%s;",
                           (sSKU,cSKU,cName,cSID,cTime))
            cursor.execute("commit;")
            return 0
        except:
            return 1







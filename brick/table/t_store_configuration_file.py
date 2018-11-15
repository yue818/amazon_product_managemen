# -*- coding: utf-8 -*-
"""
 @desc:
 @author: 李杨杨
 @site:
 @software: PyCharm
 @file: t_store_configuration_file.py
 @time: 2017-12-15 12:46
"""
import traceback


class t_store_configuration_file():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def getsellerbyshopcode(self, shopcode):
        setcur = self.db_conn.cursor()
        setcur.execute("select Seller from t_store_configuration_file where ShopName_temp = %s ;", (shopcode,))
        objs = setcur.fetchone()
        setcur.close()
        seller = ''
        if objs:
            seller = objs[0]
        return seller

    def find_shopnames(self, ):
        result = {}
        try:
            cursor = self.db_conn.cursor()
            cursor.execute("select DISTINCT ShopName_temp from t_store_configuration_file where ShopName_temp is not null;")
            result['data'] = cursor.fetchall()
            result['code'] = 0
            cursor.close()
            return result
        except Exception, ex:
            result['code'] = 1
            print '%s_%s:%s' % (traceback.print_exc(), Exception, ex)
            return result

    def find_shopname_by_name(self, username):
        result = {}
        try:
            cursor = self.db_conn.cursor()
            sql = 'select DISTINCT ShopName_temp from t_store_configuration_file where Seller = %s'
            cursor.execute(sql, (username,))
            result['data'] = cursor.fetchall()
            result['code'] = 0
            cursor.close()
            return result
        except Exception, ex:
            result['code'] = 1
            print '%s_%s:%s' % (traceback.print_exc(), Exception, ex)
            return result

    def getPublishedbyshopcode(self, shopcode):
        pubcur = self.db_conn.cursor()
        pubcur.execute("select Published from t_store_configuration_file where ShopName_temp = %s ;", (shopcode,))
        objs = pubcur.fetchone()
        pubcur.close()
        Published = ''
        if objs:
            Published = objs[0]
        return Published

    def getDepartmentbyshopcode(self, shopcode):
        depcur = self.db_conn.cursor()
        depcur.execute("select Department from t_store_configuration_file where ShopName_temp = %s ;", (shopcode,))
        objs = depcur.fetchone()
        depcur.close()
        Department = ''
        if objs:
            Department = objs[0]
        return Department

    def get_shopname_by_code(self, shopcode):
        shocur = self.db_conn.cursor()
        shocur.execute("select ShopName from t_store_configuration_file where ShopName_temp = %s ;", (shopcode,))
        objs = shocur.fetchone()
        shocur.close()
        shopname = ''
        if objs:
            shopname = objs[0]
        return shopname

    def getinfobyshopcode(self, shopname):
        pubcur = self.db_conn.cursor()
        sql = "SELECT Department, Seller, Published FROM t_store_configuration_file WHERE ShopName=%s;"
        pubcur.execute(sql, (shopname,))
        objs = pubcur.fetchone()
        pubcur.close()
        Published = ''
        Department = ''
        Seller = ''
        if objs:
            Department = objs[0]
            Seller = objs[1]
            Published = objs[2]
        return Department, Seller, Published


    def update_shopStatus(self,info,shopcode):
        try:
            if info:
                upcur = self.db_conn.cursor()
                upcur.execute("update t_store_configuration_file set `Status`=%s where ShopName_temp = %s ;",(info,shopcode,))
                upcur.execute("commit;")
                upcur.close()
            return {'errorcode': 0, 'errortext': info}
        except Exception,e:
            return {'errorcode': -1, 'errortext': '%s:%s' % (Exception, e)}


    def getshopStatusbyshopcode(self, shopname):
        try:
            pubcur = self.db_conn.cursor()
            sql = "SELECT `Status` FROM t_store_configuration_file WHERE ShopName_temp=%s;"
            pubcur.execute(sql, (shopname[0:9],))
            objs = pubcur.fetchone()
            pubcur.close()
            status = ''
            if objs:
                status = objs[0]
            return {'errorcode': 0, 'status': status}
        except Exception, e:
            return {'errorcode': -1, 'errortext': '%s:%s' % (Exception, e)}


    def status_num(self):
        try:
            cursor = self.db_conn.cursor()
            sql = "SELECT COUNT(*), PlatformID,`Status` FROM t_store_configuration_file  GROUP BY PlatformID,`Status` ORDER BY PlatformID;"
            cursor.execute(sql)
            objs = cursor.fetchall()
            cursor.close()
            return {'errorcode': 1, 'errortext': '', 'data': objs}
        except Exception as e:
            return {'errorcode': -1, 'errortext': u'%s' % e}










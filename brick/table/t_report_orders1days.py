# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_report_orders1days.py
 @time: 2017-12-22 14:28

"""
import datetime

class t_report_orders1days():
    def __init__(self,db_cnxn):
        self.db_cnxn = db_cnxn

    def getSoldTheDay(self,productid,yyyymmdd):
        nowtime = (datetime.datetime.strptime(yyyymmdd,'%Y%m%d') + datetime.timedelta(days=-1)).strftime('%Y%m%d')
        mycur = self.db_cnxn.cursor()
        mycur.execute("SELECT OrdersLast1Days from t_report_orders1days "
                      "WHERE YYYYMMDD = %s AND ProductID = %s ;", (nowtime,productid,))
        obj = mycur.fetchone()
        mycur.close()
        order1 = 0
        if obj and obj[0] is not None:
            order1 = obj[0]

        return order1


    def getSoldYesterday(self,productid,yyyymmdd):
        yesttime = (datetime.datetime.strptime(yyyymmdd,'%Y%m%d') + datetime.timedelta(days=-2)).strftime('%Y%m%d')
        mycur = self.db_cnxn.cursor()
        mycur.execute("SELECT OrdersLast1Days from t_report_orders1days "
                      "WHERE YYYYMMDD = %s AND ProductID = %s;", (yesttime,productid,))
        obj = mycur.fetchone()
        mycur.close()
        order2 = 0
        if obj and obj[0] is not None:
            order2 = obj[0]

        return order2


    def getOrders7Days(self,productid,yyyymmdd):
        sevtimeq = (datetime.datetime.strptime(yyyymmdd,'%Y%m%d') + datetime.timedelta(days=-8)).strftime('%Y%m%d')
        sevtimej = (datetime.datetime.strptime(yyyymmdd,'%Y%m%d') + datetime.timedelta(days=-1)).strftime('%Y%m%d')
        mycur = self.db_cnxn.cursor()
        mycur.execute("SELECT sum(OrdersLast1Days) as Orders7Days from  t_report_orders1days "
                      "where YYYYMMDD BETWEEN %s and %s and ProductID = %s ;", (sevtimeq,sevtimej,productid,))
        obj = mycur.fetchone()
        mycur.close()
        order7 = 0
        if obj and obj[0] is not None:
            order7 =obj[0]
        return order7

    def getOrders7Days_WarehouseName(self,productid,yyyymmdd,warehousename):
        sevtimeq = (datetime.datetime.strptime(yyyymmdd,'%Y%m%d') + datetime.timedelta(days=-8)).strftime('%Y%m%d')
        sevtimej = (datetime.datetime.strptime(yyyymmdd,'%Y%m%d') + datetime.timedelta(days=-1)).strftime('%Y%m%d')

        sql = "SELECT sum(OrdersLast1Days) as Orders7Days from  t_report_orders1days_wish_overseas_warehouse " \
              "where YYYYMMDD BETWEEN %s and %s and ProductID = %s AND WarehouseName LIKE \"{}%%\";".format(warehousename)

        mycur = self.db_cnxn.cursor()
        mycur.execute(sql,(sevtimeq,sevtimej,productid,))
        obj = mycur.fetchone()
        mycur.close()
        order7 = 0
        if obj and obj[0] is not None:
            order7 =obj[0]
        return order7

    def ofSales_Of_ProductID_WarehouseName(self,productid,warehousename):
        sql = "SELECT sum(OrdersLast1Days) as ofSales from  t_report_orders1days_wish_overseas_warehouse " \
              "where ProductID = %s AND WarehouseName  LIKE \"{}%%\";".format(warehousename)

        mycur = self.db_cnxn.cursor()
        mycur.execute(sql, (productid,))
        obj = mycur.fetchone()
        mycur.close()
        ofSales = obj[0] if obj and obj[0] else 0
        return ofSales


    def insertinto(self,objs):
        inscur = self.db_cnxn.cursor()

        inscur.execute("insert into t_report_orders1days set YYYYMMDD = %s,PlatformName = %s,ShopName=%s,"
                       "ProductID = %s,OrdersLast1Days = %s,OrdersLast7Days = %s,UpdateTime = %s "
                       " on duplicate KEY update OrdersLast1Days = %s,OrdersLast7Days = %s,UpdateTime = %s;",
                       (objs['YYYYMMDD'],objs['PlatformName'],objs['ShopName'],objs['ProductID'],
                        objs['OrdersLast1Days'],objs['OrdersLast7Days'],objs['UpdateTime'],
                        objs['OrdersLast1Days'],objs['OrdersLast7Days'],objs['UpdateTime']))
        inscur.execute("commit;")
        inscur.close()


    def insertinto_WarehouseName(self,objs):
        inscur = self.db_cnxn.cursor()

        inscur.execute("insert into t_report_orders1days_wish_overseas_warehouse set YYYYMMDD = %s,PlatformName = %s,"
                       "ShopName=%s,"
                       "ProductID = %s,OrdersLast1Days = %s,OrdersLast7Days = %s,UpdateTime = now(),WarehouseName=%s "
                       " on duplicate KEY update OrdersLast1Days = %s,OrdersLast7Days = %s,UpdateTime = now();",
                       (objs['YYYYMMDD'],objs['PlatformName'],objs['ShopName'],objs['ProductID'],
                        objs['OrdersLast1Days'],objs['OrdersLast7Days'],objs['WarehouseName'],
                        objs['OrdersLast1Days'],objs['OrdersLast7Days']))
        inscur.execute("commit;")
        inscur.close()


    def deletedata_befor60day(self,productid):
        befortime = (datetime.datetime.utcnow() + datetime.timedelta(days=-60)).strftime('%Y%m%d')
        delcur = self.db_cnxn.cursor()
        delcur.execute("delete from t_report_orders1days WHERE YYYYMMDD < %s and ProductID = %s;",(befortime,productid,))
        delcur.execute("commit;")
        delcur.close()


    def lastweeksSales(self, productid):
        try:
            cursor = self.db_cnxn.cursor()
            sql = 'SELECT sum(OrdersLast1Days) from t_report_orders1days where YEARWEEK(YYYYMMDD) = YEARWEEK(utc_date())-1 ' \
                  'and ProductID = %s;'
            cursor.execute(sql, (productid,))
            obj = cursor.fetchone()
            if obj and obj[0]:
                data = int(obj[0])
            else:
                data = 0
            return {'errorcode': 1, 'errortext': '', 'data': data}
        except Exception as e:
            return {'errorcode': -1, 'errortext': u'%s' % e}


    def nextlastweeksSales(self, productid):
        try:
            cursor = self.db_cnxn.cursor()
            sql = 'SELECT sum(OrdersLast1Days) from t_report_orders1days where YEARWEEK(YYYYMMDD) = YEARWEEK(utc_date())-2 ' \
                  'and ProductID = %s;'
            cursor.execute(sql, (productid,))
            obj = cursor.fetchone()
            if obj and obj[0]:
                data = int(obj[0])
            else:
                data = 0
            return {'errorcode': 1, 'errortext': '', 'data': data}
        except Exception as e:
            return {'errorcode': -1, 'errortext': u'%s' % e}














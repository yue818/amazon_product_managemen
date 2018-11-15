# -*-coding:utf-8-*-
"""
 @desc:
 @author: changyang
 @site:
 @software: PyCharm
 @file: t_report_sales_daily.py.py
 @time: 2018-04-09 16:55
"""
import pymssql
import pandas as pd
# import pymysql
from django.db import connection

# connection = pymysql.connect(user="by15161458383",passwd="K120Esc1",host="rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com",db="hq_db",port=3306,charset='utf8')

class Sales_Report(object):
    def __init__(self):
        self.pyuanConn = pymssql.connect(host='122.226.216.10', port=18794, user='fancyqube', password='K120Esc1',
                                         database='ShopElf', charset='utf8')

    def processID(self, processType, idRange=''):

        if processType == 1:
            SQL = "select maxid1 from t_report_sales_daily_idrange where tablename='t_report_sales_daily'"
            with connection.cursor() as cursor:
                cursor.execute(SQL)
                if cursor.rowcount > 0:
                    return cursor.fetchone()[0]
                else:
                    return False

        elif processType == 2:
            SQL = "update t_report_sales_daily_idrange set maxid1=%s,maxid2=%s, updatetime=sysdate() where tablename='t_report_sales_daily'"
            SQL = SQL % (idRange)
            with connection.cursor() as cursor:
                cursor.execute(SQL)
            connection.commit()

            return True

    def getreport_daily(self):

        idStart = self.processID(1)
        if idStart == False:
            print u'get RangeID Fail.'
            return

        SQL = '''
            SELECT dt.nid,CONVERT(varchar(10), DATEADD(hour,8, pt.ORDERTIME), 23) as ORDDATE,
            pt.AddressOwner as PlatformName,pt.Suffix as ShopName,dt.L_NUMBER as ProductID,dt.SKU,dt.eBaySKU as ShopSKU,dt.L_QTY as SalesVolume
            FROM P_Trade pt, P_TradeDt dt 
            where pt.nid=dt.tradenid
            and dt.nid>%s ''' % (idStart,)

        df = pd.read_sql(SQL, con=self.pyuanConn)

        if df['nid'].count() <= 0:
            print u'None Data!......'
            return

        maxID = df[u'nid'].max()

        OrderDay = df[u'ORDDATE']
        PlatformName = df[u'PlatformName']
        ProductID = df[u'ProductID']
        ShopName = df[u'ShopName']
        SKU = df[u'SKU']
        ShopSKU = df[u'ShopSKU']
        SalesVolume = df[u'SalesVolume']

        updata = zip(OrderDay, PlatformName, ProductID, ShopName, SKU, ShopSKU, SalesVolume)

        sql = 'truncate table t_report_sales_daily_temp'
        with connection.cursor() as cursor:
            cursor.execute(sql)
        connection.commit()

        sql = '''INSERT INTO t_report_sales_daily_temp(OrderDay,PlatformName,ProductID,ShopName,SKU,ShopSKU,SalesVolume)
                 values (%s, %s, %s, %s, %s, %s, %s)'''

        with connection.cursor() as cursor:
            cursor.executemany(sql, updata)
        connection.commit()

        sql = 'call p_process_report_sales_daily()'
        with connection.cursor() as cursor:
            cursor.execute(sql)
        connection.commit()

        result = self.processID(2, (maxID, idStart,))
        if result:
            print u'Run Success!......'
        else:
            print u'Run Fail!......'

    def closeconn(self):
        self.pyuanConn.close()
        connection.close()


if __name__ == '__main__':
    rep = Sales_Report()
    rep.getreport_daily()

    rep.closeconn()
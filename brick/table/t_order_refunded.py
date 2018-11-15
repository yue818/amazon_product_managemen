# -*- coding: utf-8 -*-
import sys
import traceback
from brick.db import dbconnect
from django_redis import get_redis_connection
redis_conn = get_redis_connection(alias='product')
from django.db import connection
from brick.classredis.classshopsku import classshopsku
classshopskuobjs = classshopsku(connection, redis_conn)


class t_order_refunded():

    def __init__(self,db_conn):
        self.db_conn = db_conn

    def queryRefund(self,StrTime,EndTime):
        result = {}
        try:
            print 'input StrTime=%s EndTime=%s'%(StrTime, EndTime)
            cursor = self.db_conn.cursor()
            sql = "SELECT ORDERID,'',OrderState ,'',ShopSKU ,'',Quantity,TotalCost,"\
                           "RefundDate,RefundReason,ShopName,OrderDate,Shippedon FROM t_order where orderstate "\
                           " in('REFUNDED','REFUNDED BY MERCHANT','REFUNDED BY WISH','REFUNDED BY WISH FOR MERCHANT',"\
                           "'CANCELLED BY CUSTOMER','CANCELLED BY WISH (FLAGGED TRANSACTION)')"\
                           "and LEFT(RefundDate,10) between %s and %s"
            cursor.execute(sql, (StrTime, EndTime))
            datas = cursor.fetchall()
            datasrc = []
            for data in datas:
                productsku = classshopskuobjs.getSKU(data[4])
                pdata = list(data)
                pdata.insert(5,productsku)
                pdata = tuple(pdata)
                datasrc.append(pdata)
            result['datasrcset'] = tuple(datasrc)
            result['errorcode']  = 0
            cursor.close()
            return result
        except Exception, ex:
            result['errorcode'] = -1
            print '%s_%s:%s' % (traceback.print_exc(), Exception, ex)
            return result
            



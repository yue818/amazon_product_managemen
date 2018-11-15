# -*- coding: utf-8 -*-
class t_order_amazon_india():
    def __init__(self, cnxn):
        self.cnxn = cnxn

    def select_AmazonOrderId(self, order_id):
        cursor = self.cnxn.cursor()
        sql = u"select AmazonOrderId " \
              u"from t_order_amazon_india  " \
              u"where id=%s" % (order_id)
        print '\n1.get AmazonOrderId sql is:\n%s' %sql
        cursor.execute(sql)
        t_order_amazon_india_obj = cursor.fetchone()
        AmazonOrderId = ''
        if t_order_amazon_india_obj is not None:
            AmazonOrderId = t_order_amazon_india_obj[0]
        cursor.close()
        return AmazonOrderId

    def update_PYNo(self,dealResult,upTime,pyOrderNumber,dealResultInfo,
                    AmazonOrderId,applyTracking):
        cursor = self.cnxn.cursor()
        sql = u'update t_order_amazon_india ' \
              u'set dealResult="%s", dealTime="%s", pyOrderNumber="%s",' \
              u'dealResultInfo="%s",applyTracking=%s ' \
              u'where AmazonOrderId="%s"; '\
              %(dealResult,upTime,pyOrderNumber,dealResultInfo,
                applyTracking,AmazonOrderId)
        print '\n10.update_PYNo sql is \n%s' % sql
        cursor.execute(sql)
        self.cnxn.commit()
        cursor.close()

    def update_when_fail(self,dealResult,upTime,AmazonOrderId,applyTracking):
        cursor = self.cnxn.cursor()
        sql = u"update t_order_amazon_india set dealResult='%s', dealTime='%s',applyTracking='%s' " \
              u"where AmazonOrderId='%s'; " \
              %(dealResult,upTime,applyTracking,AmazonOrderId)
        cursor.execute(sql)
        self.cnxn.commit()
        cursor.close()
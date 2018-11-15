# -*- coding: utf-8 -*-
class t_order_track_info_amazon_india():
    def __init__(self, cnxn):
        self.cnxn = cnxn

    def select_trackNumber(self, order_id):
        cursor = self.cnxn.cursor()
        sql = u"select trackNumber " \
              u"from t_order_track_info_amazon_india  " \
              u"where AmazonOrderId='%s'" % (order_id)
        cursor.execute(sql)
        t_order_track_info_amazon_india_obj = cursor.fetchone()
        trackNumber = ''
        if t_order_track_info_amazon_india_obj is not None:
            trackNumber = t_order_track_info_amazon_india_obj[0]
        cursor.close()
        return trackNumber

    def insert_trackNumber(self,AmazonOrderId,trackNumber,track_company,
                           track_service,upTime):
        cursor = self.cnxn.cursor()
        sql = u"insert into t_order_track_info_amazon_india " \
              u"(AmazonOrderId,trackNumber,track_company,track_service," \
              u"UpdateTime) " \
              u"VALUES ('%s','%s','%s','%s','%s');  "\
              %(AmazonOrderId,trackNumber,track_company,track_service,upTime)
        print '\n5.insert_trackNumber sql is \n%s' % sql
        cursor.execute(sql)
        self.cnxn.commit()
        cursor.close()

    def update_LableData(self,LableData,upTime,trackNumber):
        cursor = self.cnxn.cursor()
        sql = u'update t_order_track_info_amazon_india ' \
              u'set LableData="%s", UpdateTime="%s" ' \
              u'where trackNumber="%s"; '%(LableData,upTime,trackNumber)
        print '\n8.update_LableData sql is \n%s' % sql
        cursor.execute(sql)
        self.cnxn.commit()
        cursor.close()
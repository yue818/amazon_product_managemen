# -*- coding: utf-8 -*-
import traceback

class t_large_small_corresponding_cate():

    def __init__(self,db_conn):
        self.db_conn = db_conn

    def getLargeClass(self,):
        result = {}
        try:
            cursor = self.db_conn.cursor()
            cursor.execute("select distinct LCode, LargeClass from t_large_small_corresponding_cate where LargeClass is not null ;")
            result['data'] = cursor.fetchall()
            result['code'] = 0
            cursor.close()
            return result
        except Exception, ex:
            result['code'] = -1
            print '%s_%s:%s' % (traceback.print_exc(), Exception, ex)
            return result

    def getSmallClass(self,):
        result ={}
        try:
            cursor = self.db_conn.cursor()
            cursor.execute("select distinct SCode, SmallClass from t_large_small_corresponding_cate where SmallClass is not null" )
            result['data'] = cursor.fetchall()
            result['code'] = 0
            cursor.close()
            return result
        except Exception, ex:
            result['code'] = -1
            print '%s_%s:%s' % (traceback.print_exc(), Exception, ex)
            return result

    def getLargeClassBySmallClass(self,smallclass):
        try:
            cursor = self.db_conn.cursor()
            cursor.execute(
                "select distinct LCode, LargeClass,SCode,SmallClass from t_large_small_corresponding_cate where SCode = %s;", (smallclass,))
            obj = cursor.fetchone()
            cursor.close()
            if obj:
                return {'code': 1,'errortext': '', 'largecode': obj[0], 'largeclass': obj[1],'smallcode': obj[2], 'smallclass': obj[3]}
            else:
                return {'code': 0,'errortext': u'小类代码错误，没有找到对应大类！'}
        except Exception, ex:
            return {'code': -1, 'errortext': '%s' % ex}












#-*-coding:utf-8-*-
"""
 @desc:
 @author: wangzy
 @site:
 @software: PyCharm
 @file: t_online_info_wish_event_function.py
 @time: 2018/5/25 13:47
"""


class t_online_info_wish_event_function():
    def __init__(self,db_conn):
        self.cnxn = db_conn

    '''
    说明:根据sku获取t_online_info表中ProductID
    入参:商品SKU
    出参:列表中存放ProductID
    '''
    def set_tortstatus_by_mainsku(self,mainsku,sTortStatus):
        try:
            cursor = self.cnxn.cursor()
            cursor.execute(
                "select count(1) from t_online_info WHERE SKU = %s;", (mainsku,))
            obj = cursor.fetchone()
            if obj is None:
                return {'errorcode': 1, 'errortext': u't_online_info_wish not found mainsku=%s'%(mainsku), 'list': []}
            cursor.execute(
                "update  t_online_info_wish set TortInfo=%s WHERE MainSKU = %s;", (sTortStatus,mainsku,))
            cursor.close()
            return {'errorcode': 1, 'errortext': u'deal t_online_info_wish success', 'list': []}
        except Exception, e:
            return {'errorcode': -1, 'errortext': 'set_tortstatus_by_mainsku:%s:%s' % (Exception, e)}

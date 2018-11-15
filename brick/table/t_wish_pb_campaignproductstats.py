#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_wish_pb_campaignproductstats.py
 @time: 2018/7/3 9:49
"""

class t_wish_pb_campaignproductstats():
    def __init__(self, conn):
        self.conn = conn

    def j_ad(self,product_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("select campaign_state from t_wish_pb_campaignproductstats WHERE product_id=%s ;", (product_id,))
            objs = cursor.fetchall()
            cursor.close()
            statelist = []
            for obj in objs:
                if obj:
                    statelist.append(obj[0])
            if statelist:
                return {'errorcode': 1, 'errortext': '', 'datalist': statelist}
            else:
                return {'errorcode': 0, 'errortext': 'product_id: %s' % product_id, 'datalist': statelist}
        except Exception as e:
            return {'errorcode': -1, 'errortext': u'%s' % e}




#-*-coding:utf-8-*-


"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_order_track_info_amazon_india.py
 @time: 2018/2/6 15:16
"""   
class t_order_track_info_amazon_india():
    def __init__(self,db_cnxn=None):
        self.cnxn = db_cnxn

    def get_track_info_by_amazon_order_id(self, amazonOrderId):
        cursor = self.cnxn.cursor()
        sql = "select track_info,trackNumber from t_order_track_info_amazon_india where AmazonOrderId='%s'" % amazonOrderId
        cursor.execute(sql)
        order_track_info_item = cursor.fetchone()
        cursor.close()
        amazon_track_info = {}
        if order_track_info_item:
            amazon_track_info['track_info'] = order_track_info_item[0]
            amazon_track_info['trackNumber'] = order_track_info_item[1]
        return amazon_track_info
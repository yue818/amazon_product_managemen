#-*-coding:utf-8-*-
from brick.table.t_order_track_info_amazon_india import *
from brick.table.t_order_amazon_india import *
from brick.table.t_amazon_schedule_ing import *
from brick.table.t_config_online_amazon import *
import datetime,time

"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: feed_Amazon_trackNo.py
 @time: 2018/2/6 14:12
"""   
class feed_Amazon_trackNo():
    def __init__(self,db_conn=None):
        self.cnxn = db_conn

    def local2utc(self,local_st):
        import datetime
        """本地时间转UTC时间（-8:00）"""
        time_struct = time.mktime(local_st.timetuple())
        utc_st = datetime.datetime.utcfromtimestamp(time_struct)
        return utc_st

    def deal_Amazon_trackNo_to_schedule(self, params):
        order_item_infos = params['order_item_infos']
        t_order_track_info_amazon_india_tmp = t_order_track_info_amazon_india(self.cnxn)
        t_order_amazon_india_tmp = t_order_amazon_india(self.cnxn)
        t_amazon_schedule_ing_tmp = t_amazon_schedule_ing(self.cnxn)
        t_config_online_amazon_tmp = t_config_online_amazon(self.cnxn)
        print params['shopName']
        auth_info = t_config_online_amazon_tmp.getauthByShopName(params['shopName'])
        request_str = []
        for i in range(0,len(order_item_infos)):
            order_item_info = order_item_infos[i]
            amazonOrderId = order_item_info['AmazonOrderId']
            t_order_track_info_amazon_india_obj = t_order_track_info_amazon_india_tmp.get_track_info_by_amazon_order_id(amazonOrderId)
            if t_order_track_info_amazon_india_obj:
                track_info = t_order_track_info_amazon_india_obj['track_info']
                textStr = 'Check In Scan'
                deal_track_infos = eval(track_info)
                track_date = ''
                for deal_track_info in deal_track_infos:
                    if deal_track_info:
                        if textStr in deal_track_info['Info']:
                            track_date = deal_track_info['DateTime'] + ":00"
                            date_time = datetime.datetime.strptime(track_date, '%Y-%m-%d %H:%M:%S')
                            # date_time = date_time + datetime.timedelta(days=-1)
                            utc_tran = self.local2utc(date_time).strftime("%Y-%m-%dT%H:%M:%SZ")
                            track_date = str(utc_tran)
                if track_date == '':
                    lastShipDateDict = t_order_amazon_india_tmp.get_lastShipDate_by_AmazonOrderId(amazonOrderId)
                    if lastShipDateDict:
                        lastShipDate = lastShipDateDict['LatestShipDate']
                        date_time = datetime.datetime.strptime(lastShipDate, '%Y-%m-%dT%H:%M:%SZ')
                        date_time = date_time + datetime.timedelta(days=-1)
                        utc_tran = self.local2utc(date_time).strftime("%Y-%m-%dT%H:%M:%SZ")
                        track_date = str(utc_tran)
                    else:
                        continue
                trackNo = t_order_track_info_amazon_india_obj['trackNumber']
                track_company = "Delhivery"
                if trackNo.find('EQ9') == 0:
                    track_company = "India Post"
                if trackNo.find('2') == 0 and len(trackNo) == 9:
                    track_company = "ECOM EXPRESS"
                # if trackNo.find('23') == 0 and len(trackNo) == 9:
                #     track_company = "ECOM EXPRESS"
                request_str_child = '{"track_date": "%s", "track_company": "%s", "track_num": "%s", "AmazonOrderId": "%s", "shopName": "%s"}' % (
                                        track_date, track_company, trackNo, amazonOrderId, params['shopName'])
                request_str.append(request_str_child)
                if i != (len(order_item_infos) - 1):
                    if (i+1)%50 == 0:
                        insert_schedule_dict = {'shopName': params['shopName'], 'insert_time': datetime.datetime.now(),
                                                'request_str': str(request_str).replace("'", '').replace("u{", '{'), 'ShopNameIP': auth_info['IP']}
                        t_amazon_schedule_ing_tmp.insert_need_feed_amazon_info(insert_schedule_dict)
                        request_str = []
                else:
                    insert_schedule_dict = {'shopName': params['shopName'], 'insert_time': datetime.datetime.now(),
                                            'request_str': str(request_str).replace("'", '').replace("u{", '{'), 'ShopNameIP': auth_info['IP']}
                    t_amazon_schedule_ing_tmp.insert_need_feed_amazon_info(insert_schedule_dict)
            else:
                pass

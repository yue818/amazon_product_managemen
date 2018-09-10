# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: amazon_cpc_ad.py
 @time: 2018-05-17 9:13
"""
import requests
from bs4 import BeautifulSoup
from mws import Reports
import pymysql as MySQLdb
import logging
import logging.handlers
import datetime
import time
import traceback
import pika
import uuid

DATABASE = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hq_db',
        'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
        'PORT': '3306',
        'USER': 'by15161458383',
        'PASSWORD': 'K120Esc1'
            }

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(filename)s %(funcName)s:%(lineno)d] %(thread)d %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='amazon_cps_ads.log',
                    filemode='a')

logging.handlers.RotatingFileHandler('amazon_cps_ads.log',
                                     maxBytes=10 * 1024 * 1024,
                                     backupCount=10)


class GetLocalIPAndMqInfo:
    """
    获取当前vps服务器IP；从数据库获取MQ信息
    """
    def __init__(self):
        self.db_conn = MySQLdb.connect(DATABASE['HOST'],
                                       DATABASE['USER'],
                                       DATABASE['PASSWORD'],
                                       DATABASE['NAME'])

    @staticmethod
    def get_real_url(url=r'http://www.ip138.com/'):
        r = requests.get(url)
        txt = r.text
        soup = BeautifulSoup(txt, "html.parser").iframe
        return soup["src"]

    @staticmethod
    def get_out_ip(url):
        r = requests.get(url)
        txt = r.text
        ip = txt[txt.find("[") + 1: txt.find("]")]
        print('ip:' + ip)
        return ip

    def get_mq_info(self):
        cursor = self.db_conn.cursor()
        try:
            rabbit_mq = {}
            sql = "select ip, k, v from t_config_mq_info where name = 'Amazon-RabbitMQ-Server'"
            cursor.execute(sql)
            mq_config_info = cursor.fetchall()
            cursor.close()
            for mq_config_info_obj in mq_config_info:
                rabbit_mq['hostname'] = mq_config_info_obj[0]
                k = mq_config_info_obj[1]
                v = mq_config_info_obj[2]
                rabbit_mq[k] = v
            return rabbit_mq
        except Exception as e:
            cursor.close()
            print e
            return None


class GetCpcAdsInfo:
    """
    获取广告业绩信息
    """
    def __init__(self, auth_info):
        self.auth_info = auth_info
        self.report_public = Reports(self.auth_info['AWSAccessKeyId'],
                                     self.auth_info['SecretKey'],
                                     self.auth_info['SellerId'],
                                     self.auth_info['ShopSite']
                                     )
        self.db_conn = MySQLdb.connect(DATABASE['HOST'],
                                       DATABASE['USER'],
                                       DATABASE['PASSWORD'],
                                       DATABASE['NAME'])

    def submit_report_request(self, report_type):
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print 'submit'
        logging.debug('submit report, report type is:%s' % report_type)
        market_place_ids = [self.auth_info['MarketplaceId']]
        start_date = None
        end_date = None
        report_response = self.report_public.request_report(report_type,
                                                            start_date=start_date,
                                                            end_date=end_date,
                                                            marketplaceids=market_place_ids)

        request_response_dic = report_response.parsed
        report_request_id = request_response_dic['ReportRequestInfo']['ReportRequestId']['value']
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print 'get submit request id'
        logging.debug('get submit request id is: %s' % report_request_id)
        return report_request_id

    def get_report_status(self, report_request_id):
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print 'get status'
        logging.debug('get report status, report_request_id is: %s' % report_request_id)
        report_status = self.report_public.get_report_request_list(requestids=[report_request_id])
        report_status_dic = report_status.parsed
        report_processing_status = report_status_dic['ReportRequestInfo']['ReportProcessingStatus']['value']
        if report_processing_status == '_DONE_':
            generated_report_id = report_status_dic['ReportRequestInfo']['GeneratedReportId']['value']
        else:
            generated_report_id = ''
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print 'get status result'
        logging.debug('get status result, report_processing_status is:%s, generated_report_id is : %s' % (report_processing_status, generated_report_id))
        return [report_processing_status, generated_report_id]

    def get_report_result(self, generated_report_id):
        logging.debug('begin get result data')
        report_result = self.report_public.get_report(generated_report_id)
        report_result_datas = report_result.original.splitlines()
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print 'get result data'
        logging.debug('end get result data')
        return report_result_datas

    def insert_cpc_ads_data(self, col, val):
        # print col
        val_split = val.split(',')
        delete_sql = "delete from t_amazon_ad_report where shopname = '%s' and shopsite ='%s' and AdvertisedSKU =%s and StartDate =%s and EndDate =%s" \
                     %(self.auth_info['ShopName'], self.auth_info['ShopSite'], val_split[2], val_split[5], val_split[6])
        print '\n delete_sql is %s' % delete_sql
        logging.debug('sql_insert is %s' % delete_sql)
        self.execute_db(delete_sql)
        column = "CampaignName,AdGroupName,AdvertisedSKU,Keyword,MatchType,StartDate,EndDate,Clicks,Impressions,CTR,TotalSpend,AverageCPC,Currency,DayOrdersPlaced,DayOrderedProductSales,DayConversionRate,DaySameSKUUnitsOrdered,DayOtherSKUUnitsOrdered,DaySameSKUUnitsSales,DayOtherSKUUnitsSales,WeekOrdersPlaced,WeekOrderedProductSales,WeekConversionRate,WeekSameSKUUnitsOrdered,WeekOtherSKUUnitsOrdered,WeekSameSKUUnitsSales,WeekOtherSKUUnitsSales,MonthOrdersPlaced,MonthOrderedProductSales,MonthConversionRate,MonthSameSKUUnitsOrdered,MonthOtherSKUUnitsOrdered,MonthSameSKUUnitsSales,MonthOtherSKUUnitsSales"
        sql_insert = "insert into t_amazon_ad_report ( %s, shopname, shopsite) values (%s, '%s', '%s')" \
                     % (column, val, self.auth_info['ShopName'], self.auth_info['ShopSite'])
        print '\n sql_insert is %s' % sql_insert
        logging.debug('sql_insert is %s' % sql_insert)
        self.execute_db(sql_insert)


    def update_shop_status(self, auth_info, status):
        """
        记录店铺的刷新状态
        """
        cursor = self.db_conn.cursor()
        sql_record_exists = "select  name from t_config_amazon_ad_shop_status where name = '%s'" % auth_info['ShopName']
        cursor.execute(sql_record_exists)
        shop_exists_obj = cursor.fetchone()
        if shop_exists_obj is None or shop_exists_obj[0] is None :
            sql_insert = "insert into t_config_amazon_ad_shop_status (name,shop_name,shop_site,IP,uuid,synType,status) " \
                         "values ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                         %(auth_info['ShopName'], auth_info['ShopName'][0:9], auth_info['ShopSite'], auth_info['ShopIP'], auth_info['uuid'], auth_info['update_type'],status)
            print 'sql_insert: %s' % sql_insert
            logging.debug('update shop status sql_insert_1 is: %s' % sql_insert)
            cursor.execute(sql_insert)
            cursor.execute('commit;')
        else:
            sql_update = "update t_config_amazon_ad_shop_status set uuid = '%s', synType = '%s', status = '%s' where name = '%s'" \
                         %(auth_info['uuid'], auth_info['update_type'], status, auth_info['ShopName'])
            print 'sql_update: %s' % sql_update
            logging.debug('update shop status sql_insert_2 is: %s' % sql_update)
            cursor.execute(sql_update)
            cursor.execute('commit;')
        cursor.close()

    def product_update(self, col, val, product_sku):
        sql_delete = "delete from %s where seller_sku = '%s'  and shopname = '%s'" \
                     %(self.auth_info['table_name'], product_sku, self.auth_info['ShopName'])
        sql_insert = "insert into %s (%s, shopname, shopsite, deal_action, deal_result) values (%s, '%s','%s', 'refresh_product', 'Success')" \
                     % (self.auth_info['table_name'], col, val, self.auth_info['ShopName'], self.auth_info['ShopSite'])
        print '\n sql_delete is %s' %sql_delete
        logging.debug('sql_delete is %s' %sql_delete)
        self.execute_db(sql_delete)
        print '\n sql_insert is %s' % sql_insert
        logging.debug('sql_insert is %s' % sql_insert)
        self.execute_db(sql_insert)

    def execute_db(self, sql):
        cursor = self.db_conn.cursor()
        try:
            cursor.execute(sql)
            cursor.execute('commit;')
            cursor.close()
        except Exception as e:
            cursor.close()
            print e

    def insert_progress_status(self, auth_info, status):
        """
        记录进度，供进度条使用
        """
        try:
            if auth_info.has_key('uuid'):
                cursor = self.db_conn.cursor()
                sql = "insert into t_config_amazon_progress_bar(uuid, ip, shopname, status, syntype) values ('%s', '%s', '%s', '%s', '%s')" \
                      % (auth_info['uuid'], auth_info['ShopIP'], auth_info['ShopName'], status, auth_info['update_type'])
                cursor.execute(sql)
                logging.debug('insert_progress_status sql is: %s' % sql)
                cursor.execute('commit;')
                cursor.close()
        except Exception, ex:
            cursor.close()
            print '%s_%s:%s' % (traceback.print_exc(), Exception, ex)

    def get_column(self, report_result_datas):
        for i, val in enumerate(report_result_datas):
            if i == 0:  # get  information's column
                report_result_data_column = val.split('\t')
                table_column = str(report_result_data_column)
                table_column = table_column.replace('[', '')
                table_column = table_column.replace(']', '')
                table_column = table_column.replace("'", '')
                table_column = table_column.replace('-', '_')
                break
        return table_column

    def get_value(self, val):
        report_result_data = val.split('\t')
        report_result_data[5] = time.strftime("%Y-%m-%d", time.strptime(report_result_data[5], "%m/%d/%Y %H:%M"))
        report_result_data[6] = time.strftime("%Y-%m-%d", time.strptime(report_result_data[6], "%m/%d/%Y %H:%M"))
        table_val = str(report_result_data)
        table_val = table_val.replace('[', '')
        table_val = table_val.replace(']', '')
        return table_val

    def report_flow(self, report_type):
        # report_request_id = self.submit_report_request(report_type)
        report_request_id = '66440017658'
        time_sleep = 10
        count = 0
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print 'result id is: %s, now wait for  10 seconds  then check deal status.' % report_request_id
        logging.debug('result id is: %s, now wait for  10 seconds  then check deal status.' % report_request_id)
        while count < 5:
            time.sleep(time_sleep)
            time_sleep += time_sleep  # doubled wait time（10,20,40,80,160）
            count += 1
            try:
                report_processing_status = self.get_report_status(report_request_id)[0]
                if report_processing_status == '_DONE_':
                    self.insert_progress_status(self.auth_info, 'done')
                    generated_report_id = self.get_report_status(report_request_id)[1]
                    self.insert_progress_status(self.auth_info, 'getdata')
                    report_result_datas = self.get_report_result(generated_report_id)
                    date1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    data_cnt = len(report_result_datas) - 1
                    table_column = self.get_column(report_result_datas)
                    self.insert_progress_status(self.auth_info, 'backfill-' + str(data_cnt))
                    for i, val in enumerate(report_result_datas):
                        if i == 0:
                            continue
                        table_val = self.get_value(val)
                        self.insert_cpc_ads_data(table_column, table_val)
                    self.update_shop_status(self.auth_info, 'success')

                    self.insert_progress_status(self.auth_info, 'success')
                    print date1
                    print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    return report_result_datas
                else:
                    if report_processing_status == '_SUBMITTED_':
                        self.insert_progress_status(self.auth_info, 'submit')
                    elif report_processing_status == '_IN_PROGRESS_':
                        self.insert_progress_status(self.auth_info, 'progress')
                    elif report_processing_status == '_CANCELLED_':
                        self.insert_progress_status(self.auth_info, 'cancel')

                    print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print 'processing_status is:%s, we will wait for %s seconds ' % (report_processing_status, time_sleep)
                    logging.debug('processing_status is:%s, we will wait for %s seconds ' % (report_processing_status, time_sleep))
            except Exception as e:
                self.insert_progress_status(self.auth_info, 'fail')
                print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                traceback.print_exc()
                logging.error('traceback.format_exc():\n%s' % traceback.format_exc())

        else:  # 循环超过5次，即总等待时长超过 31*time_sleep，则计为超时
            print 'Get submit_feed reuslt timeout'
            self.insert_progress_status(self.auth_info, 'timeout')
            self.update_shop_status(self.auth_info, 'timeout')
            logging.error('Get submit_feed reuslt timeout')


get_info_obj = GetLocalIPAndMqInfo()
while True:
    try:
        local_ip = get_info_obj.get_out_ip(get_info_obj.get_real_url())
    except Exception as e:
        print e
        local_ip = '120.25.235.160'
    if local_ip:
        break
print 'local_ip is:%s' % local_ip
RABBIT_MQ = get_info_obj.get_mq_info()
print 'RABBIT_MQ is: %s' % str(RABBIT_MQ)


def deal_and_response_request(ch, method, props, body):
    logging.debug('get message from mq, message is: %s' % body)
    auth_info = eval(body)
    print auth_info
    if local_ip == auth_info['ShopIP']:
        if auth_info['update_type'] == 'refresh_ads_info':
            get_ads_info_obj = GetCpcAdsInfo(auth_info)
            get_ads_info_obj.report_flow('_GET_SP_MEGA_REPORT_')
        else:
            pass
    else:
        logging.error('The ip in auth_info:%s does not match local ip: %s' % (auth_info['ShopIP'], local_ip))
        print 'The ip in auth_info:%s does not match local ip: %s' % (auth_info['ShopIP'], local_ip)


def listen_client():
    credentials = pika.PlainCredentials(RABBIT_MQ['MQUser'], RABBIT_MQ['MQPassword'])
    parameters = pika.ConnectionParameters(RABBIT_MQ['hostname'], RABBIT_MQ['MQPort'], '/', credentials, heartbeat=0)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    queue = 'amazon_' + local_ip + '_refresh_ad_data'
    print 'queue is: %s' % queue
    channel.queue_declare(queue=queue)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(deal_and_response_request, queue=queue, no_ack=True)
    print(" [x] Awaiting RPC requests")
    channel.start_consuming()

def retry_listen():
    try:
        listen_client()
    except Exception as e:
        print e
        traceback.print_exc()
        logging.debug(e)
        time.sleep(5)
        retry_listen()

# if __name__ == '__main__':
#     # print 'The file running now is: %s' % sys.argv[0].split('\\')[-1]
#     retry_listen()
auth_info = dict()
auth_info['ShopIP'] = '120.25.235.160'
auth_info['uuid'] = str(uuid.uuid4())
auth_info['ShopName'] = 'AMZ-0091-Feihoudei-US/PJ'
auth_info['update_type'] = 'refresh_ads_info'
auth_info['SellerId'] = 'A3KDZSH7PTLS7P'
auth_info['MarketplaceId'] = 'ATVPDKIKX0DER'
auth_info['AWSAccessKeyId'] = 'AKIAIS3UD5DWPTSF24GQ'
auth_info['SecretKey'] = '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'
auth_info['ShopSite'] = 'US'
get_ads_info_obj = GetCpcAdsInfo(auth_info)
get_ads_info_obj.report_flow('_GET_SP_MEGA_REPORT_')
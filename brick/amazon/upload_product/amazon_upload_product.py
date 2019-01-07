# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: amazon_upload_product_20181226.py
 @time: 2018/12/26 14:46
"""
from mws import Feeds, Products
import time
import logging.handlers
import datetime
import traceback
from django.db import connection
import chardet


log_day = datetime.datetime.now().strftime("%Y%m%d")
log_formatter = logging.Formatter('%(asctime)s [%(filename)s %(funcName)s:%(lineno)d] %(thread)d %(levelname)s %(message)s')
logFile = r'/tmp/amazon_upload_log/amazon_upload_product' + log_day + '.log'
my_handler = logging.handlers.RotatingFileHandler(
    logFile,
    mode='a',
    maxBytes=20 * 1024 * 1024,
    backupCount=4,
    encoding=None,
    delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.DEBUG)
logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)
logger.addHandler(my_handler)


class UpdateProductInfo:
    """
    产品信息修改
    """
    def __init__(self, db_connect, auth_info_update):
        self.db_conn = db_connect
        self.auth_info = auth_info_update
        self.submit_feed_public = Feeds(self.auth_info['AWSAccessKeyId'],
                                        self.auth_info['SecretKey'],
                                        self.auth_info['SellerId'],
                                        self.auth_info['ShopSite'],
                                        proxy_host=self.auth_info['IP']
                                        )

    def submit_feed(self, data, feed_type):
        submit_feed_public = self.submit_feed_public
        market_place_ids = [self.auth_info['MarketplaceId']]
        submit_feed_rsp = submit_feed_public.submit_feed(data, feed_type, marketplaceids=market_place_ids)
        submit_feed_rsp_dict = submit_feed_rsp.parsed
        print submit_feed_rsp_dict
        logger.error('submit_feed_rsp_dict: %s' % str(submit_feed_rsp_dict))
        return submit_feed_rsp_dict

    def get_deal_status(self, feed_id):
        """
            获取提交所提交请求的处理状态，当为 '_DONE_' 时表示处理完成，此时方可提交申请获取处理结果信息
        """
        get_status_public = self.submit_feed_public
        get_status_rsp = get_status_public.get_feed_submission_list([feed_id])
        get_status_rsp_dict = get_status_rsp.parsed
        feed_processing_status = get_status_rsp_dict['FeedSubmissionInfo']['FeedProcessingStatus']['value']
        return feed_processing_status

    def get_deal_result(self, data):
        """
         获取处理结果信息，设定总共等待31倍time_sleep时长检查请求是否处理完成（本例等待 31*10=310 秒）
        超过等待时长则设为处理超时
        """
        get_result_public = self.submit_feed_public
        feed_id = data['FeedSubmissionInfo']['FeedSubmissionId']['value']

        print '\n'
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print 'result id is: %s, now wait for  10 seconds  then check deal status.' % feed_id
        logger.error('result id is: %s, now wait for  10 seconds  then check deal status.' % feed_id)

        time_sleep = 10
        count = 0
        while count < 5:
            time.sleep(time_sleep)
            time_sleep += time_sleep  # 每次等待时长翻倍（即10,20,40,80,160）
            count += 1
            try:
                feed_processing_status = self.get_deal_status(feed_id)
                if feed_processing_status == '_DONE_':
                    print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print 'now we can get the result'
                    logger.error('now we can get the result')
                    feed_result = get_result_public.get_feed_submission_result(feed_id)
                    print 'get result raw'
                    logger.error('get result raw')
                    response = feed_result._response_dict
                    print 'get result dict'
                    logger.error('get result dict: %s' % str(response))
                    print response
                    return response
                else:
                    print '\n'
                    print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print 'processing_status is:%s, we will wait for %s seconds ' %(feed_processing_status,time_sleep)
                    logger.error('processing_status is:%s, we will wait for %s seconds ' %(feed_processing_status,time_sleep))
            except Exception as e:
                print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print 'error: %s' % e
                logger.error('error: %s' % e)
        else:  # 循环超过5次，即总等待时长超过 31*time_sleep，则计为超时
            print 'Get submit_feed reuslt timeout'
            logger.error('Get submit_feed reuslt timeout')
            return None

    def update_local_db(self):
        auth_info = self.auth_info
        cursor = self.db_conn.cursor()
        if auth_info['update_type'] == 'load_product':
            for sku in auth_info['product_list']:
                sql = "update %s set quantity = 999, deal_result = 'Success', status = 'Active', updatetime= '%s' where shopname = '%s' and seller_sku = '%s'" \
                      %(auth_info['table_name'], datetime.datetime.now(), auth_info['ShopName'], sku)
                print 'load sql: %s' % sql
                logger.error('load sql: %s' % sql)
                cursor.execute(sql)
                cursor.execute('commit;')
            cursor.close()
        elif auth_info['update_type'] == 'unload_product':
            for sku in auth_info['product_list']:
                sql = "update %s set quantity = 0 , deal_result = 'Success', status = 'Inactive', updatetime= '%s' where shopname = '%s' and seller_sku = '%s'" \
                      % (auth_info['table_name'], datetime.datetime.now(), auth_info['ShopName'], sku)
                print 'unload sql: %s' % sql
                logger.error('unload sql: %s' % sql)
                cursor.execute(sql)
                cursor.execute('commit;')
            cursor.close()
        elif auth_info['update_type'] == 'auto_load_product':
            for sku in auth_info['product_list']:
                sql = "update %s set quantity = 999, deal_result = 'Success', status = 'Active', updatetime= '%s' where shopname = '%s' and seller_sku = '%s'" \
                      % (auth_info['table_name'], datetime.datetime.now(), auth_info['ShopName'], sku)
                sql_auto = "update  t_amazon_auto_load set deal_result = 'Success', deal_time = '%s' where batch_id = '%s' and shop_name = '%s' and seller_sku = '%s'" \
                           % (datetime.datetime.now(), auth_info['batch_id'], auth_info['ShopName'], sku)
                logger.error('load sql: %s' % sql)
                logger.error('load sql_auto: %s' % sql_auto)
                cursor.execute(sql)
                cursor.execute(sql_auto)
                cursor.execute('commit;')
            cursor.close()
        elif auth_info['update_type'] == 'auto_unload_product':
            for sku in auth_info['product_list']:
                sql = "update %s set quantity = 0 , deal_result = 'Success', status = 'Inactive', updatetime = '%s' where shopname = '%s' and seller_sku = '%s'" \
                      % (auth_info['table_name'], datetime.datetime.now(), auth_info['ShopName'], sku)
                sql_auto = "update  t_amazon_auto_load set deal_result = 'Success', deal_time = '%s' where batch_id = '%s' and shop_name = '%s' and seller_sku = '%s'" \
                           % (datetime.datetime.now(), auth_info['batch_id'], auth_info['ShopName'], sku)
                logger.error('unload sql: %s' % sql)
                logger.error('unload sql_auto: %s' % sql_auto)
                cursor.execute(sql)
                cursor.execute(sql_auto)
                cursor.execute('commit;')
            cursor.close()
        elif auth_info['update_type'] == 'product_price_modify':
                sql = "update %s set price = '%s', sale_price='%s',sale_from_date='%s',sale_end_date='%s' , deal_result = 'Success',  updatetime= '%s' where shopname = '%s' and seller_sku = '%s'" \
                      % (auth_info['table_name'], auth_info['price_info_dic']['standard_price'], auth_info['price_info_dic']['sale_price'], auth_info['price_info_dic']['start_date'], auth_info['price_info_dic']['end_date'],  datetime.datetime.now(), auth_info['ShopName'], auth_info['seller_sku'])
                print 'sql is:%s' % sql
                logger.error('sql is:%s' % sql)
                cursor.execute(sql)
                cursor.execute('commit;')
        elif auth_info['update_type'] == 'product_price_modify_multi':
            price_info_dic = auth_info['price_info_dic']
            for sku, price in price_info_dic.items():
                sql = "update %s set price = '%s',deal_result = 'Success',  updatetime= '%s' where shopname = '%s' and seller_sku = '%s'" \
                      % (auth_info['table_name'], price, datetime.datetime.now(), auth_info['ShopName'], sku)
                print 'sql is:%s' % sql
                logger.error('sql is:%s' % sql)
                cursor.execute(sql)
                cursor.execute('commit;')

                sql_log = "update t_amazon_operation_log set deal_result = 1, end_time='%s' where batch_id = '%s' and shop_name = '%s' and seller_sku ='%s'" \
                          % (datetime.datetime.now(), auth_info['batch_id'], auth_info['ShopName'], sku)
                print 'sql_log is:%s' % sql_log
                logger.error('sql_log is:%s' % sql_log)
                cursor.execute(sql_log)
                cursor.execute('commit;')

        elif auth_info['update_type'] == 'product_image_modify':
            sql = "update %s set image_url = '%s', deal_result = 'Success',  updatetime= '%s' where shopname = '%s' and seller_sku = '%s'" \
                  % (auth_info['table_name'], auth_info['image_info_dic']['pic_url'], datetime.datetime.now(), auth_info['ShopName'], auth_info['seller_sku'])
            print 'sql is:%s' % sql
            logger.error('sql is:%s' % sql)
            cursor.execute(sql)
            cursor.execute('commit;')
        elif auth_info['update_type'] == 'product_info_modify':
            set_sql = ''.encode('utf-8')
            for key, val in auth_info['product_info_dic'].items():
                set_sql += key + '="' + val + '",'

            sql = "update %s set %s deal_result = 'Success',  updatetime= '%s' where shopname = '%s' and seller_sku = '%s'" \
                  % (auth_info['table_name'], set_sql, datetime.datetime.now(), auth_info['ShopName'], auth_info['seller_sku'])
            print 'sql is:%s' % sql
            logger.error('sql is:%s' % sql)
            cursor.execute(sql)
            cursor.execute('commit;')
        else:
            print 'other'
            pass

    def update_db_when_error(self, error_msg, error_desc_dict=None):
        cursor = self.db_conn.cursor()
        auth_info = self.auth_info
        error_msg = str(error_msg)
        try:
            if auth_info['update_type'] in ('product_info_modify', 'product_price_modify', 'product_image_modify'):
                sql = "update %s set deal_result = 'Fail', deal_result_info = '%s', updatetime= '%s' where shopname = '%s' and seller_sku = '%s'" \
                      % (auth_info['table_name'], error_msg.replace("'", '`'), datetime.datetime.now(), auth_info['ShopName'], auth_info['seller_sku'])
                print 'sql is:%s' % sql
                cursor.execute(sql)
                cursor.execute('commit;')
            # elif auth_info['update_type'] == 'product_price_modify_multi':
            #     pass
            elif auth_info['update_type'] in ('auto_load_product', 'auto_unload_product'):
                for sku in auth_info['product_list']:
                    if error_desc_dict:
                        error_msg = error_desc_dict.get(sku, error_msg)
                    sql_auto_fail = "update  t_amazon_auto_load set deal_result = 'Fail', deal_remark ='%s', deal_time = '%s' where batch_id = '%s' and shop_name = '%s' and seller_sku = '%s'" \
                           % (error_msg.replace("'", '`'), datetime.datetime.now(), auth_info['batch_id'], auth_info['ShopName'], sku)

                    sql = "update %s set deal_result = 'Fail', deal_result_info = '%s', updatetime= '%s' where shopname = '%s' and seller_sku = '%s'" \
                          % (auth_info['table_name'], error_msg.replace("'", '`'), datetime.datetime.now(), auth_info['ShopName'], sku)

                    print 'error sql: %s' % sql
                    logger.error('error sql: %s' % sql)
                    cursor.execute(sql)

                    logger.error('sql_auto_fail sql: %s' % sql_auto_fail)
                    cursor.execute(sql_auto_fail)
                    cursor.execute('commit;')
            else:
                for sku in auth_info['product_list']:
                    sql = "update %s set deal_result = 'Fail', deal_result_info = '%s', updatetime= '%s' where shopname = '%s' and seller_sku = '%s'" \
                          % (auth_info['table_name'], error_msg.replace("'", '`'), datetime.datetime.now(), auth_info['ShopName'], sku)
                    print 'error sql: %s' % sql
                    logger.error('error sql: %s' % sql)
                    cursor.execute(sql)
                    cursor.execute('commit;')
                    if auth_info['update_type'] == 'product_price_modify_multi':
                        sql_log = "update t_amazon_operation_log set deal_result = -1, deal_result_info = '%s', end_time='%s' where batch_id = '%s' and shop_name = '%s' and seller_sku ='%s'" \
                                  % (error_msg.replace("'", '`'), datetime.datetime.now(), auth_info['batch_id'], auth_info['ShopName'], sku)
                        print 'sql_log is:%s' % sql_log
                        logger.error('sql_log is:%s' % sql_log)
                        cursor.execute(sql_log)
                        cursor.execute('commit;')

        except Exception as e:
            print e
            traceback.print_exc()
            logger.error(traceback.format_exc())
        finally:
            cursor.close()

    def feed_start(self):
        """
                '_POST_INVENTORY_AVAILABILITY_DATA_'  => 库存
                '_POST_PRODUCT_PRICING_DATA_'               => 价格
                '_POST_PRODUCT_DATA_'                               => 商品信息
                '_POST_PRODUCT_IMAGE_DATA_'                 => 图片

            处理结果中 MessagesWithError 为0表示处理成功
        """
        auth_info = self.auth_info
        try:
            feed_data = auth_info['feed_xml'].encode('utf-8')
            if auth_info['update_type'] in ('load_product', 'unload_product','auto_load_product', 'auto_unload_product'):
                feed_type = '_POST_INVENTORY_AVAILABILITY_DATA_'
            elif auth_info['update_type'] == 'product_info_modify':
                feed_type = '_POST_PRODUCT_DATA_'
            elif auth_info['update_type'] in ('product_price_modify', 'product_price_modify_multi'):
                feed_type = '_POST_PRODUCT_PRICING_DATA_'
            elif auth_info['update_type'] == 'product_image_modify':
               pass
            else:
                feed_type = ''

            submit_feed_response = self.submit_feed(feed_data, feed_type)
            submit_feed_result = self.get_deal_result(submit_feed_response)

            if submit_feed_result \
                    and submit_feed_result['Message']['ProcessingReport']['ProcessingSummary']['MessagesWithError']['value'] == '0':
                self.update_local_db()
                return 'Success'
            else:
                if submit_feed_result and submit_feed_result.get('Message').get('ProcessingReport').get('Result') and auth_info.get('product_list'):
                    error_list = list()
                    error_desc_dict = dict()
                    result_obj = submit_feed_result.get('Message').get('ProcessingReport').get('Result')
                    if isinstance(result_obj, list):
                        for val in result_obj:
                            sku = val.get('AdditionalInfo').get('SKU').get('value')
                            err_desc = val.get('ResultDescription').get('value')
                            error_list.append(sku)
                            error_desc_dict[sku] = err_desc
                    elif isinstance(result_obj, dict):
                        sku = result_obj.get('AdditionalInfo').get('SKU').get('value')
                        err_desc = result_obj.get('ResultDescription').get('value')
                        error_list.append(sku)
                        error_desc_dict[sku] = err_desc
                    success_list = list(set(auth_info.get('product_list')) - set(error_list))
                    auth_info['product_list'] = success_list
                    self.update_local_db()

                    auth_info['product_list'] = error_list
                    self.update_db_when_error('MessagesWithError is not 0 in mws API processing report ', error_desc_dict)
                else:
                    self.update_db_when_error('MessagesWithError is not 0 in mws API processing report ')
                return 'Fail'
            # feed_data = auth_info['feed_xml']
            # feed_type = '_POST_INVENTORY_AVAILABILITY_DATA_'
            # submit_feed_response = self.submit_feed(auth_info, feed_data, feed_type)
            # submit_feed_result = self.get_deal_result(auth_info, submit_feed_response)
            # if submit_feed_result \
            #         and submit_feed_result['Message']['ProcessingReport']['ProcessingSummary']['MessagesWithError']['value'] == '0':
            #     self.update_local_db(auth_info)
            #     return 'Success'
            # else:
            #     self.update_db_when_error(auth_info, 'MessagesWithError is not 0 in mws API processing report ')
            #     return 'Fail'
        except Exception, ex:
            print ex
            logger.error('feed_start: traceback.format_exc():\n%s' % traceback.format_exc())
            self.update_db_when_error(ex)
            return 'Fail'


class FeedProduct:
    def __init__(self, auth_info_feed, db_conncetion=connection):
        self.auth_info = auth_info_feed
        self.feed_public = Feeds(self.auth_info['AWSAccessKeyId'],
                                 self.auth_info['SecretKey'],
                                 self.auth_info['SellerId'],
                                 region=self.auth_info['ShopSite'],
                                 proxy_host=self.auth_info['IP'])
        self.product_public = Products(self.auth_info['AWSAccessKeyId'],
                                       self.auth_info['SecretKey'],
                                       self.auth_info['SellerId'],
                                       region=self.auth_info['ShopSite'],
                                       proxy_host=self.auth_info['IP'])
        self.db_conn = db_conncetion

    def submitfeed(self, data, feed_type):
        logger.error('feed_type is %s' % feed_type)
        logger.error('data is %s' % data)
        submitfeed = self.feed_public
        marketplaceids = [self.auth_info['MarketplaceId']]
        try:
            submitfeed_rsp = submitfeed.submit_feed(data, feed_type, marketplaceids=marketplaceids)
        except Exception as e:
            logger.error('traceback.format_exc():\n%s' % traceback.format_exc())
            logger.error('we will submit feed again after 5 minutes')
            time.sleep(300)
            try:
                submitfeed_rsp = submitfeed.submit_feed(data, feed_type, marketplaceids=marketplaceids)
            except Exception as e:
                return 'Error'
        submitfeed_rsp_dict = submitfeed_rsp.parsed
        return submitfeed_rsp_dict

    def get_deal_status(self, feed_id):
        """
            获取提交所提交请求的处理状态，当为 '_DONE_' 时表示处理完成，此时方可提交申请获取处理结果信息
        """
        get_status_public = self.feed_public
        get_status_rsp = get_status_public.get_feed_submission_list([feed_id])
        get_status_rsp_dict = get_status_rsp.parsed
        feed_processing_status = get_status_rsp_dict['FeedSubmissionInfo']['FeedProcessingStatus']['value']
        return feed_processing_status

    def get_deal_result(self, data):
        """
         获取处理结果信息，设定总共等待31倍time_sleep时长检查请求是否处理完成（本例等待 31*10=310 秒）
        超过等待时长则设为处理超时
        返回
            Error：获取结果出错
            Timeout：获取结果超时
            response：正常获取到的结果
        """
        if data == 'Error':
            return 'Error'

        get_result_public = self.feed_public
        feed_id = data['FeedSubmissionInfo']['FeedSubmissionId']['value']
        logger.error('result id is: %s, now wait for  10 seconds  then check deal status.' % feed_id)

        time_sleep = 10
        count = 0
        while count < 5:
            time.sleep(time_sleep)
            time_sleep += time_sleep  # 每次等待时长翻倍（即10,20,40,80,160）
            count += 1
            try:
                feed_processing_status = self.get_deal_status(feed_id)
                if feed_processing_status == '_DONE_':
                    logger.error('now we can get the result')
                    feed_result = get_result_public.get_feed_submission_result(feed_id)
                    response = feed_result.parsed
                    logger.error('get result dict: %s' % str(response))
                    return response
                else:
                    logger.error('processing_status is:%s, we will wait for %s seconds ' % (feed_processing_status,time_sleep))
            except:
                logger.error('traceback.format_exc():\n%s' % traceback.format_exc())
                return 'Error'
        else:  # 循环超过5次，即总等待时长超过 31*time_sleep，则计为超时
            logger.error('Get submit_feed reuslt timeout')
            return 'Timeout'

    def parse_feed_result(self, feed_result, seller_sku_list, feed_type):
        # 结果为'Error', 'Timeout'时直接返回
        if feed_result in ('Error', 'Timeout'):
            sku_des_dict = {sku: feed_type + ':' + feed_result for sku in seller_sku_list}
            return sku_des_dict

        report = feed_result['ProcessingReport']
        # 处理失败记录数，为0时表示成功，不为0提取具体的店铺SKU
        # {'!$@_(@{!11036': 'Product:Please reduce your generic keyword length to less than "200" bytes.', ……}
        message_with_error = report['ProcessingSummary']['MessagesWithError']['value']
        if message_with_error == '0':
            return 'all success'
        else:
            report_detail = report['Result']
            sku_des_dict = dict()
            re_description = ''
            # 根据返回的详细原因组合出 {SKU: feed类型+失败原因说明} 字典
            if isinstance(report_detail, list):
                for report_detail_each in report_detail:
                    sku = report_detail_each.get('AdditionalInfo').get('SKU').get('value') if report_detail_each.get('AdditionalInfo') else None
                    re_description = report_detail_each.get('ResultDescription').get('value') if report_detail_each.get('ResultDescription') else ''
                    if sku:
                        sku_des_dict[sku] = feed_type + ': ' + re_description
            elif isinstance(report_detail, dict):
                sku = report_detail.get('AdditionalInfo').get('SKU').get('value') if report_detail.get('AdditionalInfo') else None
                re_description = report_detail.get('ResultDescription').get('value') if report_detail.get('ResultDescription') else ''
                if sku:
                    sku_des_dict[sku] = feed_type + ': ' + re_description
            # 未单个指出SKU错误时，认为该批次所有SKU均失败
            if not sku_des_dict:
                all_sku_reason = re_description if re_description else 'Error'
                sku_des_dict = {sku: feed_type + all_sku_reason for sku in seller_sku_list}
            return sku_des_dict

    def get_product_info_by_seller_sku(self, seller_sku_list):
        product_public = self.product_public
        try:
            product_info_response = product_public.get_matching_product_for_id(self.auth_info['MarketplaceId'],
                                                                               'SellerSKU',
                                                                               [seller_sku_list])
            product_info_response_dic = product_info_response._response_dict
        except:
            time.sleep(10)  # 防止超请求限制，重新提交
            product_info_response = product_public.get_matching_product_for_id(self.auth_info['MarketplaceId'],
                                                                               'SellerSKU',
                                                                               [seller_sku_list])
            product_info_response_dic = product_info_response._response_dict
        return product_info_response_dic

    def refresh_data_by_seller_sku(self, seller_sku_list):
        for seller_sku in seller_sku_list:
            product_info = self.get_product_info_by_seller_sku(seller_sku)
            print product_info
            logger.error('product_info:%s ' % product_info)
            product_result = product_info['GetMatchingProductForIdResult']
            product_asin = product_result['Products']['Product']['Identifiers']['MarketplaceASIN']['ASIN']['value']
            product_infos = product_result['Products']['Product']['AttributeSets']['ItemAttributes']
            item_name = product_infos['Title']['value']
            if 'ListPrice' in product_infos.keys():
                price = product_infos['ListPrice']['Amount']['value']
                # currency = product_infos['ListPrice']['CurrencyCode']['value']
            else:
                price = None
            # brand = product_infos['Brand']['value']
            image_url = product_infos['SmallImage']['URL']['value']
            # Manufacturer = product_infos['Manufacturer']['value']

            sql = "INSERT INTO t_online_info_amazon(seller_sku, asin1, item_name, price, image_url, ShopName, shopsite, status) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                  % (seller_sku, product_asin, item_name, price, image_url, self.auth_info['ShopName'], self.auth_info['ShopName'].split('-')[-1].split('/')[0], 'Active')
            self.write_result_to_db(sql)

    def write_result_to_db(self, sql):
        with self.db_conn.cursor() as cursor:
            try:
                print 'write_result_to_db sql: ', sql
                logger.error('write_result_to_db sql: %s' % sql)
                cursor.execute(sql)
                cursor.execute('commit;')
            except Exception as e:
                logger.error('Update product info faild, Execute sql: %s, Error info: %s' % (sql, e))

    def update_error_info_to_db(self, updatetime, error_msg_dic, product_list, is_pic_lost=0):
        """
            error_msg_dic ={
            '!$@_(@{!11036': 'Please reduce your generic keyword length to less than "200" bytes.', '
            !$@_(@{!11037': 'Please reduce your generic keyword length to less than "200" bytes.', '
            !$@_(@{!11034': 'Please reduce your generic keyword length to less than "200" bytes.',
            ……
            }
            product_list = [{
                    "seller_sku_list": ["NBWXH:010150", "NBWXH:010158", "NBWXH:010157", "NBWXH:010156", "NBWXH:010155", "NBWXH:010154", "NBWXH:010153", "NBWXH:010152", "NBWXH:010151"],
                    "amazon_upload_id": 36202,
                    "amazon_upload_result_id": 36202
                },
                {
                    "seller_sku_list": ["NBWXH:010150", "NBWXH:010158", "NBWXH:010157", "NBWXH:010156", "NBWXH:010155", "NBWXH:010154", "NBWXH:010153", "NBWXH:010152", "NBWXH:010151"],
                    "amazon_upload_id": 36203,
                    "amazon_upload_result_id": 36203
                }
            ]

            遍历product_list中的每个seller_sku_list，若sku在error_msg_dic中有记录，则表示该upload_id刊登失败
            组合该upload_id下所有SKU失败原因，写入errorMessages字段
            结合is_pic_lost信息，添加失败或图片缺失记录

        """
        table_column_str = '''upload_product_type,recommended_browse_nodes,recommended_browse_nodes_id,
                               dataFromUrl,item_sku,external_product_id,external_product_id_type,item_name,manufacturer,
                               part_number,feed_product_type,item_type,product_subtype,product_description,brand_name,
                               update_delete,item_package_quantity,standard_price,sale_price,sale_from_date,sale_end_date,
                               condition_type,quantity,merchant_shipping_group_name,bullet_point1,bullet_point2,bullet_point3,
                               bullet_point4,bullet_point5,generic_keywords,main_image_url,other_image_url1,other_image_url2,
                               other_image_url3,other_image_url4,other_image_url5,other_image_url6,other_image_url7,
                               other_image_url8,fulfillment_center_id,model_name,warranty_description,variation_theme,model,
                               mfg_minimum,mfg_minimum_unit_of_measure,swatch_image_url,department_name,fit_type,
                               unit_count,unit_count_type,fulfillment_latency,display_dimensions_unit_of_measure,generic_keywords1,
                               generic_keywords2,generic_keywords3,generic_keywords4,generic_keywords5,department_name1,
                               department_name2,department_name3,department_name4,department_name5,material_type,
                               metal_type,setting_type,ring_size,gem_type,target_audience_keywords1,target_audience_keywords2,
                               target_audience_keywords3,productSKU,createUser,createTime,updateUser,updateTime,status,
                               ShopSets,resultInfo,errorMessages,mqResponseInfo,prodcut_variation_id,clothing_color,clothing_size,
                               toy_color,jewerly_color,item_shape,homes_color,homes_size,can_upload'''
        for product in product_list:
            this_product_error_msg = dict()
            for seller_sku in product['seller_sku_list']:
                if seller_sku in error_msg_dic:
                    this_product_error_msg[seller_sku] = error_msg_dic[seller_sku]
            if this_product_error_msg:
                sql_upload_result = '''UPDATE t_templet_amazon_upload_result
                                                           SET updateTime = '%s', status = '%s', errorMessages = '%s'
                                                         WHERE id = %s
                                        ''' % (updatetime, 'FAILED', str(this_product_error_msg).replace("'", '`'), product['amazon_upload_result_id'])
                sql_wait_result = "UPDATE t_templet_amazon_wait_upload SET status='FAILED' WHERE id=%s;" % product['amazon_upload_id']

                if is_pic_lost == 0:
                    table_name = 't_templet_amazon_upload_fail'
                else:
                    table_name = 't_templet_amazon_upload_result_lose_pic'
                sql_insert_fail = '''insert into %s (%s) 
                                                              select %s from t_templet_amazon_upload_result where id = %s
                                                              ''' % (table_name, table_column_str, table_column_str, product['amazon_upload_result_id'])
                self.write_result_to_db(sql_upload_result)
                self.write_result_to_db(sql_wait_result)
                self.write_result_to_db(sql_insert_fail)

    def feed_flow(self, xml_body):
        """
        {
            "AWSAccessKeyId": "AKIAICN3FGEFM77PYWKQ",
            "ShopName": "AMZ-0196-XJ-UK/HF",
            "SecretKey": "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",
            "SellerId": "A2ZYQC864YKAML",
            "MarketplaceId": "A1F83G8C2ARO7P",
            "IP": "123.206.14.69",
            "product_list": [{
                "sku": "BG2694",
                "seller_sku_list": ["NBWXH:010150", "NBWXH:010158", "NBWXH:010157", "NBWXH:010156", "NBWXH:010155", "NBWXH:010154", "NBWXH:010153", "NBWXH:010152", "NBWXH:010151"],
                "amazon_upload_id": 36202,
                "variation": 1,
                "upcIds": {
                    "BG2694H07andNL7378andKEY3643H02andOSS4862H04": "NBWXH:010152",
                    "BG2694H01andNL7378andKEY3643H01andOSS4862H08": "NBWXH:010158",
                    "BG2694H08andNL7378andKEY3643H04andOSS4862H06": "NBWXH:010151",
                    "BG2694H06andNL7378andKEY3643H08andOSS4862H05": "NBWXH:010153",
                    "BG2694H04andNL7378andKEY3643H03andOSS4862H03": "NBWXH:010155",
                    "BG2694H02andNL7378andKEY3643H06andOSS4862H07": "NBWXH:010157",
                    "BG2694H03andNL7378andKEY3643H05andOSS4862H02": "NBWXH:010156",
                    "BG2694H05andNL7378andKEY3643H07andOSS4862H01": "NBWXH:010154"
                },
                "amazon_upload_result_id": 36202
            },
            ]
        }

        """
        logger.error("xml body is  %r" % xml_body)

        # 商品信息修改及上下架
        if self.auth_info.get('update_type') and self.auth_info['update_type'] in ('auto_load_product',
                                                                                   'auto_unload_product', 'load_product', 'unload_product',
                                                                                   'product_info_modify', 'product_price_modify',
                                                                                   'product_image_modify', 'product_price_modify_multi'):
            server = UpdateProductInfo(self.db_conn, self.auth_info)
            server.feed_start()
            return

        # 图片补传
        if self.auth_info.get('operate_type') and self.auth_info['operate_type'] == 'reupload_image':
            pass
            return

        # 刊登部分
        # 全量店铺SKU信息
        product_list = self.auth_info.get('product_list')
        if product_list:
            seller_sku_list = [sku for product in product_list for sku in product['seller_sku_list']]
        else:
            logger.error('product_list not given')
            return
        logger.error('seller_sku_list %s' % seller_sku_list)

        # xml文件 转换为UTF-8编码格式
        product_xml_data = xml_body.get('Product')
        try:
            product_xml_data = product_xml_data.encode('utf-8')
        except UnicodeDecodeError:
            char_set = chardet.detect(product_xml_data)['encoding']
            product_xml_data = product_xml_data.decode(char_set).encode('utf-8')

        inventory_xml_data = xml_body.get('Inventory')
        price_xml_data = xml_body.get('Price')
        relationships_xml_data = xml_body.get('Relationship')
        image_xml = xml_body.get('Image')

        # 返回结果
        all_submit_result = dict()

        # 首先提交产品信息并根据处理结果决定是否提交后续相关信息
        product_submit_data = self.submitfeed(product_xml_data, '_POST_PRODUCT_DATA_')
        logger.error('product_submit_data: %s' % product_submit_data)
        time.sleep(60)
        product_response_result = self.get_deal_result(product_submit_data)
        all_submit_result['_POST_PRODUCT_DATA_'] = self.parse_feed_result(product_response_result, seller_sku_list, 'Product')
        if all_submit_result['_POST_PRODUCT_DATA_'] != 'all success':
            # 判断是否全部产品失败，若有部分成功则还需提交后续的库存，价格等信息; 若全部失败则直接退出
            all_upload_id_list = [sku_list['amazon_upload_id'] for sku_list in product_list]
            fail_upload_id_list = [product['amazon_upload_id'] for product in product_list for seller_sku in product['seller_sku_list'] if seller_sku in all_submit_result['_POST_PRODUCT_DATA_']]
            if set(all_upload_id_list) == set(fail_upload_id_list):
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.update_error_info_to_db(now, all_submit_result['_POST_PRODUCT_DATA_'], product_list)
                return

        # 提交其他刊登信息
        if inventory_xml_data:
            inventory_submit_data = self.submitfeed(inventory_xml_data, '_POST_INVENTORY_AVAILABILITY_DATA_')
            logger.error('inventory_submit_data: %s' % inventory_submit_data)
        if price_xml_data:
            price_submit_data = self.submitfeed(price_xml_data, '_POST_PRODUCT_PRICING_DATA_')
            logger.error('price_submit_data: %s' % price_submit_data)
        if relationships_xml_data:
            relationships_submit_data = self.submitfeed(relationships_xml_data, '_POST_PRODUCT_RELATIONSHIP_DATA_')
            logger.error('relationships_submit_data: %s' % relationships_submit_data)
        if image_xml:
            image_submit_data = self.submitfeed(image_xml, '_POST_PRODUCT_IMAGE_DATA_')
            logger.error('image_submit_data: %s' % image_submit_data)

        time.sleep(60)

        # 获取刊登结果
        if inventory_xml_data:
            inventory_response_result = self.get_deal_result(inventory_submit_data)
            all_submit_result['_POST_INVENTORY_AVAILABILITY_DATA_'] = self.parse_feed_result(inventory_response_result, seller_sku_list, 'Inventory')
        if price_xml_data:
            price_response_result = self.get_deal_result(price_submit_data)
            all_submit_result['_POST_PRODUCT_PRICING_DATA_'] = self.parse_feed_result(price_response_result, seller_sku_list, 'Price')
        if relationships_xml_data:
            relationships_response_result = self.get_deal_result(relationships_submit_data)
            all_submit_result['_POST_PRODUCT_RELATIONSHIP_DATA_'] = self.parse_feed_result(relationships_response_result, seller_sku_list, 'Relation')
        if image_xml:
            image_response_result = self.get_deal_result(image_submit_data)
            all_submit_result['_POST_PRODUCT_IMAGE_DATA_'] = self.parse_feed_result(image_response_result, seller_sku_list, 'Image')

        # 仅图片上传失败时置is_image_lost为1，插入图片缺失记录
        fail_feed_type = [k for k, v in all_submit_result.items() if v != 'all success']
        is_image_lost = 1 if len(fail_feed_type) == 1 and '_POST_PRODUCT_IMAGE_DATA_' in fail_feed_type else 0

        # 刊登失败时，将同一店铺SKU的失败信息组合到一起
        # error_messages = {sku1: 'Inventory: inventory fail reason; Price: price fail reason ……'，sku2: 'Inventory: inventory fail reason; Price: price fail reason ……'}
        error_messages = dict()
        for i in all_submit_result:
            if all_submit_result[i] != 'all success' and i != '_POST_PRODUCT_DATA_':
                for key, val in all_submit_result[i].items():
                    if key in error_messages:
                        error_messages[key] += ';' + val
                    else:
                        error_messages[key] = val
        # 第一步提交商品信息时就报错的商品SKU 后续图片价格等上传必定失败，仅提供刊登产品信息的失败原因即可
        if all_submit_result['_POST_PRODUCT_DATA_'] != 'all success':
            for product_key, product_val in all_submit_result['_POST_PRODUCT_DATA_'].items():
                if product_key in error_messages:
                    error_messages[product_key] = product_val

        logger.error('Start to update amazon upload result db info')
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 提取刊登成功的upload_id
        all_upload_id_list = [product['amazon_upload_id'] for product in product_list]
        fail_upload_id_list = [product['amazon_upload_id'] for product in product_list for seller_sku in product['seller_sku_list'] if seller_sku in error_messages]
        success_upload_id_list = list(set(all_upload_id_list) - set(fail_upload_id_list))
        # 提取刊登成功的seller_sku列表
        seller_sku_success_list = [sku for product in product_list for sku in product['seller_sku_list'] if product['amazon_upload_id'] in success_upload_id_list]

        if success_upload_id_list:
            for product_id in success_upload_id_list:
                sql = '''UPDATE t_templet_amazon_upload_result 
                            SET updateTime='%s', status='%s', errorMessages='%s'
                            WHERE id='%s';''' % (now, 'SUCCESS', '', product_id)
                self.write_result_to_db(sql)
            try:
                logger.error('Begin refresh data into t_online_info_amazon')
                self.refresh_data_by_seller_sku(seller_sku_success_list)
                logger.error('End refresh data into t_online_info_amazon')
            except Exception as e:
                logger.error('refresh data into t_online_info_amazon failed! %s' % e)
                logger.error('traceback.format_exc():\n%s' % traceback.format_exc())

        if error_messages:
            logger.error('errorMessages is:%s' % str(error_messages))
            logger.error('is_image_lost is:%s' % str(is_image_lost))
            self.update_error_info_to_db(now, error_messages, product_list, is_image_lost)
        logger.error('End to update amazon upload result db info')

    def feed_flow1(self):
        logger.info('this is info')
        logger.debug('this is debug')
        logger.error('this is error')

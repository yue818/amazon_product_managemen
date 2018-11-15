#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import time
import pika
import sys
import requests
import urllib2
import logging
import logging.handlers
import MySQLdb
import datetime
import traceback
import copy
import json


log_formatter = logging.Formatter('%(asctime)s [%(filename)s %(funcName)s:%(lineno)d] %(thread)d %(levelname)s %(message)s')
logFile = 'joom_get_product.log'
my_handler = logging.handlers.RotatingFileHandler(
    logFile,
    mode='a',
    maxBytes=100 * 1024 * 1024,
    backupCount=4,
    encoding=None,
    delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.ERROR)
logger = logging.getLogger('root')
logger.setLevel(logging.ERROR)
logger.addHandler(my_handler)


# Real environment sql connection info
DATABASES = {
    'NAME': 'hq_db',
    'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
    'PORT': '3306',
    'USER': 'by15161458383',
    'PASSWORD': 'K120Esc1'
}

REVIEWSTATECHOICES = {
    'approved': '0',
    'rejected': '1',
    'pending': '2',
}

STATUSCHOICES = {
    'False': '0',
    'True': '1',
}


class Server():

    def __init__(self):
        RABBITMQ = self.get_rabbitmq_info()
        credentials = pika.PlainCredentials(RABBITMQ['username'], RABBITMQ['password'])
        self.parameters = pika.ConnectionParameters(RABBITMQ['hostname'], RABBITMQ['port'], '/', credentials, socket_timeout=3600)
        self.connection = pika.BlockingConnection(self.parameters)
        self.realIP = self.get_out_ip(self.get_real_url())
        # JOOM-0003
        # self.realIP = '114.115.161.21'
        # Joom-0001 Local Account No fixed ip
        # self.realIP = 'joom_1_local_ip'

    def listen_client(self):
        channel = self.connection.channel()
        queue = self.realIP + '_joom_get_product'
        channel.queue_declare(queue=queue, durable=True)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(self.callback,
                              queue=queue,
                              no_ack=False)
        channel.start_consuming()

    def callback(self, ch, method, properties, body):
        print " [x] Received %r" % (body,)
        logger.debug(" [x] Received %r" % (body,))
        ch.basic_ack(delivery_tag=method.delivery_tag)
        datas = eval(body)
        db_conn = MySQLdb.connect(DATABASES['HOST'], DATABASES['USER'], DATABASES['PASSWORD'], DATABASES['NAME'], charset="utf8")
        for data in datas:
            flag = data.get('flag', 0)
            logger.debug('shop info: %s' % data)
            data['IP'] = self.realIP
            self.joom_get_products(data, flag, db_conn)
        print ' [x] Get Joom Products Over, Close DB Connection, Now: %s' % datetime.datetime.now()
        logger.debug(' [x] Get Joom Products Over, Close DB Connection, Now: %s' % datetime.datetime.now())
        db_conn.close()

    def joom_get_products(self, OneCmdRecoreDict, flag, db_conn):
        t_api_scheduleImp = t_api_schedule(None, db_conn)
        if 'CMDID' not in OneCmdRecoreDict.keys() or OneCmdRecoreDict is None or OneCmdRecoreDict['CMDID'] is None:
            logger.debug('OneCmdRecoreDict=%s' % OneCmdRecoreDict)
            return
        for cmdid in OneCmdRecoreDict['CMDID']:
            newOneCmdRecoreDict = copy.deepcopy(OneCmdRecoreDict)
            newOneCmdRecoreDict['CMDID'] = cmdid
            logger.debug('newOneCmdRecoreDict%s' % newOneCmdRecoreDict)
            try:
                product_id = OneCmdRecoreDict.get('productid', '')
                t_api_scheduleImp.getauthByShopName(newOneCmdRecoreDict['ShopName'])
                ShopOnlineInfoImp = ShopOnlineInfo(t_api_scheduleImp, newOneCmdRecoreDict, flag, product_id)
                myresult = ShopOnlineInfoImp.do()
                logger.debug('myresult: %s' % myresult)
                if myresult['record']:
                    # {'start':start,'end':end,'type':type}
                    get_joom_product_order_updatetime_obj = get_joom_product_order_updatetime(db_conn, newOneCmdRecoreDict['ShopName'])
                    get_joom_product_order_updatetime_obj.update_time_or_insert(myresult['record']['start'], myresult['record']['end'], myresult['record']['type'])

                # params = {}
                # params['ShopName'] = myresult['ShopName']
                # params['ShopIP'] = t_api_scheduleImp.auth_info['ShopIP']
                # params['ProductID'] = ''
                # params['dbcnxn'] = db_conn

                # for productid in set(myresult['ProductID']):
                #     params['ProductID'] = productid
                #     if myresult['CMDID'] == 'GetListOrders':
                #         self.refresh_joom_order_sale_run(params)
                #     elif myresult['CMDID'] == 'GetShopSKUInfo':
                #         self.refresh_joom_listing_run(params)

                # time.sleep(1)
            except Exception, ex:
                newOneCmdRecoreDict['Status'] = 'Exception'
                newOneCmdRecoreDict['ActualEndTime'] = datetime.datetime.now()
                errorinfo = '%s  f_GetShopSKUInfo except Exception= %s ex=%s  __LINE__=%s' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), Exception, ex, sys._getframe().f_lineno)
                newOneCmdRecoreDict['errorinfo'] = errorinfo
                t_api_scheduleImp.moveOneCmd(newOneCmdRecoreDict)
                print errorinfo
                print 'traceback.format_exc():\n%s' % traceback.format_exc()
                logger.error(errorinfo)
                logger.error('traceback.format_exc():\n%s' % traceback.format_exc())
                time.sleep(1)

    def refresh_joom_order_sale_run(self, params):
        pass

    def get_out_ip(self, url):
        r = requests.get(url, timeout=30)
        txt = r.text
        ip = txt[txt.find("[") + 1: txt.find("]")]
        print('ip:' + ip)
        return ip

    def get_real_url(self, url=r'http://www.ip138.com/'):
        r = requests.get(url, timeout=30)
        txt = r.text
        soup = BeautifulSoup(txt, "html.parser").iframe
        return soup["src"]

    def write_result_to_db(self, sql, db_conn):
        cursor = db_conn.cursor()
        try:
            logger.debug('write_result_to_db sql: %s' % sql)
            cursor.execute(sql)
            cursor.execute('commit;')
        except Exception as e:
            logger.error('Update product info faild, Execute sql: %s, Error info: %s' % (sql, e))
        cursor.close()

    def execute_db(self, sql, db_conn):
        cursor = db_conn.cursor()
        cursor.execute(sql)
        columns = cursor.description
        result = []
        for value in cursor.fetchall():
            tmp = {}
            for (index, column) in enumerate(value):
                tmp[columns[index][0]] = column
            result.append(tmp)

        cursor.close()
        return result

    def get_rabbitmq_info(self):
        db_conn = MySQLdb.connect(DATABASES['HOST'], DATABASES['USER'], DATABASES['PASSWORD'], DATABASES['NAME'], charset="utf8")
        sql = "SELECT IP, K, V FROM t_config_mq_info WHERE Name='Amazon-RabbitMQ-Server' AND PlatformName='Amazon';"
        logger.debug('get_rabbitmq_info sql: %s' % sql)
        res = self.execute_db(sql, db_conn)
        RABBITMQ = dict()
        for i in res:
            if i.get('K') == 'MQPort':
                RABBITMQ['port'] = i.get('V')
            elif i.get('K') == 'MQUser':
                RABBITMQ['username'] = i.get('V')
            elif i.get('K') == 'MQPassword':
                RABBITMQ['password'] = i.get('V')
            else:
                pass
            RABBITMQ['hostname'] = i.get('IP')
        db_conn.close()
        return RABBITMQ


class t_api_schedule():

    def __init__(self, auth_info, cnxn):
        self.PlatformName = None
        self.ShopName = None
        self.auth_info = auth_info
        if auth_info is not None and 'PlatformName' in auth_info.keys():
            self.PlatformName = auth_info['PlatformName']
        if auth_info is not None and 'ShopName' in auth_info.keys():
            self.ShopName = auth_info['ShopName']
        self.cnxn = cnxn

    def getauthByShopName(self, ShopName):
        cursor = self.cnxn.cursor()
        sql = "SELECT IP,ShopName,K,V FROM t_config_online_joom WHERE ShopName= %s "
        logger.debug('getauthByShopName: %s' % sql)
        cursor.execute(sql, (ShopName.strip(),))
        t_config_online_joom_objs = cursor.fetchall()
        cursor.close()
        auth_info = {}
        auth_info['ShopName'] = ShopName
        for t_config_online_joom_obj in t_config_online_joom_objs:
            auth_info['ShopIP'] = t_config_online_joom_obj[0]
            k = t_config_online_joom_obj[2]
            v = t_config_online_joom_obj[3]
            auth_info[k] = v
        self.auth_info = auth_info
        return auth_info

    def updateOneCmd(self, OneCmdRecoreDict):
        cursor = self.cnxn.cursor()
        sql = "UPDATE t_api_schedule_ing SET ActualBeginTime=%s, TransactionID=%s, ScheduleTime=%s, Status=%s, " \
            "ProcessingStatus=%s, ActualEndTime=%s, Timedelta=%s, RetryCount=%s, pid=%s, cmdtext=%s, errorinfo=%s WHERE id=%s;"
        logger.debug('updateOneCmd sql=%s ' % sql)
        cursor.execute(sql, (OneCmdRecoreDict['ActualBeginTime'], OneCmdRecoreDict['TransactionID'],
                             OneCmdRecoreDict['ScheduleTime'], OneCmdRecoreDict['Status'], OneCmdRecoreDict['ProcessingStatus'],
                             OneCmdRecoreDict['ActualEndTime'], OneCmdRecoreDict['Timedelta'], OneCmdRecoreDict['RetryCount'],
                             OneCmdRecoreDict['pid'], OneCmdRecoreDict['cmdtext'], OneCmdRecoreDict['errorinfo'], OneCmdRecoreDict['id']))
        self.cnxn.commit()

    def moveOneCmd(self, OneCmdRecoreDict):
        self.insertOneCmd(OneCmdRecoreDict)
        self.cnxn.commit()

    def insertOneCmd(self, OneCmdRecoreDict):
        cursor = self.cnxn.cursor()
        sql = "INSERT INTO t_api_schedule_ed (ShopName, PlatformName, CMDID, ScheduleTime, ActualBeginTime, " \
            "ActualEndTime, Status, ProcessingStatus, Processed, Successful, WithError, WithWarning, TransactionID, " \
            "InsertTime, Params, Timedelta, RetryCount, pid, cmdtext, errorinfo) " \
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        logger.debug('insertOneCmd sql= %s' % sql)
        cursor.execute(sql, (OneCmdRecoreDict['ShopName'], OneCmdRecoreDict['PlatformName'], OneCmdRecoreDict['CMDID'], OneCmdRecoreDict['ScheduleTime'],
                       OneCmdRecoreDict['ActualBeginTime'], OneCmdRecoreDict['ActualEndTime'], OneCmdRecoreDict['Status'], OneCmdRecoreDict['ProcessingStatus'], OneCmdRecoreDict['Processed'],
                       OneCmdRecoreDict['Successful'], OneCmdRecoreDict['WithError'], OneCmdRecoreDict['WithWarning'], OneCmdRecoreDict['TransactionID'], OneCmdRecoreDict['InsertTime'],
                       OneCmdRecoreDict['Params'], OneCmdRecoreDict['Timedelta'], OneCmdRecoreDict['RetryCount'], OneCmdRecoreDict['pid'], OneCmdRecoreDict['cmdtext'], OneCmdRecoreDict['errorinfo']))

    def deleteOneCmd(self, OneCmdRecoreDict):
        cursor = self.cnxn.cursor()
        sql = "DELETE FROM t_api_schedule_ing WHERE id=\'%s\'" % (OneCmdRecoreDict['id'])
        logger.debug('deleteOneCmd sql= %s ' % sql)
        cursor.execute(sql)

    # 2倍指数增加
    def refreshScheduleTimeAndTimedelta(self, OneCmdRecoreDict):
        OneCmdRecoreDict['ScheduleTime'] = datetime.datetime.now() + datetime.timedelta(seconds=OneCmdRecoreDict['Timedelta'])
        OneCmdRecoreDict['Timedelta'] = OneCmdRecoreDict['Timedelta'] * 2
        OneCmdRecoreDict['RetryCount'] += 1


class ShopOnlineInfo():
    def __init__(self, t_api_scheduleImp, OneCmdRecoreDict, flag, product_id):
        self.t_api_scheduleImp = t_api_scheduleImp
        self.OneCmdRecoreDict = OneCmdRecoreDict
        self.flag = flag
        self.product_id = product_id

    def do(self):
        result = {}
        if self.OneCmdRecoreDict['CMDID'] == 'UpdateInventory':
            self.UpdateInventory()
            result['CMDID'] = 'UpdateInventory'

        elif self.OneCmdRecoreDict['CMDID'] == 'GetShopSKUInfo':
            result = self.GetShopSKUInfoV2()
            result['CMDID'] = 'GetShopSKUInfo'

        elif self.OneCmdRecoreDict['CMDID'] == 'GetListOrders':
            result = self.GetListOrders2()
            result['CMDID'] = 'GetListOrders'

        else:
            result['CMDID'] = 'Other'
            pass
        return result

    def UpdateInventory(self):
        pass

    def GetShopSKUInfoV2(self):
        refreshdict = {'ShopName': '', 'ProductID': [], 'record': {}}
        record = {}
        pageurl = ''
        datalist = []
        while True:
            if pageurl == '':
                if self.product_id:
                    url_List_all_Products = "https://api-merchant.joom.com/api/v2/product"
                    data = {
                        'access_token': self.t_api_scheduleImp.auth_info['access_token'],
                        'id': self.product_id,
                    }
                else:
                    url_List_all_Products = "https://api-merchant.joom.com/api/v2/product/multi-get"
                    data = {
                        'access_token': self.t_api_scheduleImp.auth_info['access_token'],
                        'limit': '250',
                    }
                if self.flag == 1:
                    record = self.getSinceV2(data, 'Product')
                logger.debug('url_List_all_Products request data = %s' % data)
                dict_ret = requests.get(url_List_all_Products, params=data, timeout=200)
                # _content = eval((dict_ret._content.replace('null', 'None').replace('true', 'True')))
                _content = json.loads(dict_ret._content)
                logger.debug('_content: %s' % str(_content))
                # 刷新一下token  1015 :问令牌过期   4000:权存取 1016:失效
                if _content['code'] == 1000 or _content['code'] == 1015 or _content['code'] == 1016:  # or _content['code']== 4000   or _content['code']== 1017  or _content['code']== 1018  or _content['code']== 9000   :
                    self.RefreshToken()
                    self.OneCmdRecoreDict['ActualEndTime'] = datetime.datetime.now()
                    self.OneCmdRecoreDict['TransactionID'] = ''
                    self.t_api_scheduleImp.refreshScheduleTimeAndTimedelta(self.OneCmdRecoreDict)
                    # self.t_api_scheduleImp.updateOneCmd(self.OneCmdRecoreDict)
                    break
                if dict_ret.status_code == 200 and _content['code'] == 0:
                    if self.product_id:
                        datalist.append(_content['data'])
                        break
                    else:
                        datalist = datalist + _content['data']

                    if 'paging' in _content.keys() and 'next' in _content['paging'].keys():
                        logger.debug("_content['paging']['next']: %s" % _content['paging']['next'])
                        pageurl = _content['paging']['next'].replace('\\u0026', '&')
                        logger.debug("pageurl: %s" % pageurl)
                    else:
                        self.t_api_scheduleImp.cnxn.commit()
                        self.OneCmdRecoreDict['Status'] = '2'
                        self.OneCmdRecoreDict['ActualEndTime'] = datetime.datetime.now()
                        self.t_api_scheduleImp.moveOneCmd(self.OneCmdRecoreDict)
                        break
                else:
                    break
            else:
                logger.debug('pageurl %s' % pageurl)
                paging_bytes = None
                try:
                    paging_req = urllib2.Request(pageurl)
                    paging_bytes = urllib2.urlopen(paging_req, timeout=200).read()
                    # paging_bytes = paging_bytes.replace('null', 'None')
                    logger.debug('paging_bytes: %s' % paging_bytes)
                except Exception, ex:
                    datalist = []
                    record = {}
                    self.OneCmdRecoreDict['Status'] = 'Exception'
                    self.OneCmdRecoreDict['ActualEndTime'] = datetime.datetime.now()
                    errorinfo = '%s  f_GetShopSKUInfo except Exception= %s ex=%s  __LINE__=%s' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), Exception, ex, sys._getframe().f_lineno)
                    self.OneCmdRecoreDict['errorinfo'] = errorinfo
                    self.t_api_scheduleImp.moveOneCmd(self.OneCmdRecoreDict)
                    break

                if paging_bytes is not None:
                    # paging_bytes_dict = eval(paging_bytes)
                    paging_bytes_dict = json.loads(paging_bytes)
                    datalist = datalist + paging_bytes_dict['data']

                    if 'paging' in paging_bytes_dict.keys() and 'next' in paging_bytes_dict['paging'].keys():
                        if len(paging_bytes_dict['paging']['next']) <= 10:
                            break
                        else:
                            logger.debug("paging_bytes_dict['paging']['next']: %s" % paging_bytes_dict['paging']['next'])
                            pageurl = paging_bytes_dict['paging']['next'].replace('\\u0026', '&')
                            logger.debug("pageurl: %s" % pageurl)
                            # TO GET TEST INFO
                            # break
                    else:
                        break
                else:
                    break
        # logger.debug('datalist: %s' % datalist)
        if datalist:
            t_online_info_obj = t_online_info_joom_detail(self.t_api_scheduleImp.auth_info['ShopName'], self.t_api_scheduleImp.auth_info['ShopIP'], self.t_api_scheduleImp.cnxn)
            refreshdict = t_online_info_obj.insertJoomV2(datalist)

            self.t_api_scheduleImp.cnxn.commit()
            self.OneCmdRecoreDict['Status'] = '2'
            self.OneCmdRecoreDict['ActualEndTime'] = datetime.datetime.now()
            self.t_api_scheduleImp.moveOneCmd(self.OneCmdRecoreDict)
        refreshdict['record'] = record
        return refreshdict

    def GetListOrders2(self):
        pass

    def getSinceV2(self, data, stype):
        get_joom_product_order_updatetime_obj = get_joom_product_order_updatetime(self.t_api_scheduleImp.cnxn, self.t_api_scheduleImp.auth_info['ShopName'])
        updatetimeobj = get_joom_product_order_updatetime_obj.get_updatetime(stype)
        end = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        if updatetimeobj:
            start = updatetimeobj[1]  # 上次更新时间
            if stype == 'Product':
                data['since'] = start.split('T')[0]
            else:
                data['since'] = start
            self.OneCmdRecoreDict['cmdtext'] = '[ %s , %s )' % (start, end)
        else:
            start = None
        return {'start': start, 'end': end, 'type': stype}

    def RefreshToken(self):
        params = {
            'client_id': self.t_api_scheduleImp.auth_info['client_id'],
            'client_secret': self.t_api_scheduleImp.auth_info['client_secret'],
            'refresh_token': self.t_api_scheduleImp.auth_info['refresh_token'],
            'grant_type': 'refresh_token',
        }
        refresh_token_ret = requests.post('https://api-merchant.joom.com/api/v2/oauth/refresh_token', params=params, timeout=200)
        logger.debug('refresh_token_ret=%s' % refresh_token_ret.__dict__)
        # _content = eval(refresh_token_ret._content.replace(':null,', ':0,'))
        _content = json.loads(refresh_token_ret._content.replace(':null,', ':0,'))
        logger.debug('RefreshToken ')
        access_token = _content['data']['access_token']
        refresh_token = _content['data']['refresh_token']

        cursor = self.t_api_scheduleImp.cnxn.cursor()
        sql_access_token = 'UPDATE t_config_online_joom SET V= \'%s\' WHERE ShopName =\'%s\' AND K =\'%s\' ' % (access_token, self.OneCmdRecoreDict['ShopName'], 'access_token')
        logger.debug('sql_access_token: %s' % sql_access_token)
        cursor.execute(sql_access_token)
        sql_refresh_token = 'UPDATE t_config_online_joom SET V= \'%s\' WHERE ShopName =\'%s\' AND K =\'%s\' ' % (refresh_token, self.OneCmdRecoreDict['ShopName'], 'refresh_token')
        logger.debug('sql_refresh_token: %s' % sql_refresh_token)
        cursor.execute(sql_refresh_token)

        last_refresh_token_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        select_sql = "SELECT * FROM t_config_online_joom WHERE ShopName=%s AND IP=%s AND K=%s;"
        res = cursor.execute(select_sql, (self.OneCmdRecoreDict['ShopName'], self.OneCmdRecoreDict['IP'], 'last_refresh_token_time'))
        if not res:
            sql_insert = 'INSERT INTO t_config_online_joom (V,ShopName,IP,K) VALUES(%s,%s,%s,%s);'
        else:
            sql_insert = "UPDATE t_config_online_joom SET V=%s WHERE ShopName=%s AND IP=%s AND K=%s;"
        logger.debug('sql_insert: %s' % sql_insert)
        cursor.execute(sql_insert, (last_refresh_token_time, self.OneCmdRecoreDict['ShopName'], self.OneCmdRecoreDict['IP'], 'last_refresh_token_time'))
        self.t_api_scheduleImp.cnxn.commit()
        cursor.close()


class get_joom_product_order_updatetime():
    def __init__(self, db_coon, shopname):
        self.db_coon = db_coon
        self.shopname = shopname

    def get_updatetime(self, stype):
        procur = self.db_coon.cursor()
        sql = "SELECT lastupdatetime, nowupdatetime FROM t_joom_shop_update_time WHERE stype=%s AND shopname=%s ;"
        logger.debug('get_updatetime: %s' % sql)
        procur.execute(sql, (stype, self.shopname,))
        obj = procur.fetchone()
        procur.close()
        return obj

    def update_time_or_insert(self, lastupdatetime, nowupdatetime, stype):
        updcur = self.db_coon.cursor()
        sql = "INSERT INTO t_joom_shop_update_time SET lastupdatetime=%s," \
            "nowupdatetime=%s, stype=%s, shopname=%s " \
            "ON DUPLICATE KEY UPDATE lastupdatetime=%s, nowupdatetime=%s;"
        logger.debug('update_time_or_insert: %s' % sql)
        updcur.execute(sql, (lastupdatetime, nowupdatetime, stype, self.shopname, lastupdatetime, nowupdatetime))
        updcur.execute("commit;")
        updcur.close()


class t_online_info_joom_detail():

    def __init__(self, ShopName, ShopIP, cnxn, redis_conn=None):
        self.cnxn = cnxn
        self.redis_conn = redis_conn
        self.PlatformName = ''  # models.CharField(u'平台',choices=ChoicesPlatformName,max_length=16,blank = True,null = True)
        self.ProductID = ''  # models.CharField(u'ProductID',max_length=32,blank = True,null = True)
        self.ShopIP = ShopIP  # models.CharField(u'URL',max_length=32,blank = True,null = True)
        self.ShopName = ShopName  # models.CharField(u'店铺名称',max_length=32,blank = True,null = True)
        self.Title = ''  # models.CharField(u'Title',max_length=100,blank = True,null = True)
        self.SKU = ''  # models.CharField(u'商品SKU',max_length=32,blank = True,null = True)
        self.ShopSKU = ''  # models.CharField(u'店铺SKU',max_length=32,blank = True,null = True)
        self.Price = ''  # models.CharField(u'价格',max_length=32,blank = True,null = True)
        self.RefreshTime = None  # models.DateTimeField(u'刷新时间',blank = True,null = True)
        self.Image = ''  # models.CharField(u'图片',max_length=200,blank = True,null = True)

    def insertJoomV2(self, data):
        refreshdict = {}
        refreshdict['ShopName'] = ''
        prolist = []
        cursor = self.cnxn.cursor()

        # classlisting_obj = classlisting(self.cnxn)
        classshopsku_obj = classshopsku(self.cnxn)
        classsku_obj = classsku(self.cnxn)
        t_store_configuration_file_obj = t_store_configuration_file(self.cnxn)

        for row in data:
            ProductID = row['Product'].get('id')
            prolist.append(ProductID)

            is_promoted = row['Product'].get('is_promoted', '')
            # classlisting_obj.set_is_promoted_listingid(ProductID,is_promoted)

            JoomExpress = '%s' % row['Product'].get('joom_express_country_codes', '[]')
            # classlisting_obj.set_JoomExpress_listingid(ProductID,JoomExpress)

            ProductName = row['Product'].get('name')
            OfJoomes = row['Product'].get('number_saves')
            OfSales = row['Product'].get('number_sold')
            ParentSKU = row['Product'].get('parent_sku', '').replace('&lt;', '<').replace('&gt;', '>')
            ReviewState = row['Product'].get('review_status')
            ImageURL = row['Product'].get('main_image', '').split(r'?')[0].replace('\\', '')
            DateUploaded = time.strftime("%Y-%m-%d", time.strptime(row['Product'].get('date_uploaded'), "%Y-%m-%dT%H:%M:%SZ"))  # row['Product']['date_uploaded'] 2017-11-11T06:41:33Z
            if row['Product'].get('last_updated'):
                last_update_time = row['Product'].get('last_updated')
            else:
                last_update_time = row['Product'].get('date_uploaded')
            LastUpdated = time.strftime("%Y-%m-%dT%H:%M:%S", time.strptime(last_update_time, "%Y-%m-%dT%H:%M:%SZ"))  # row['Product']['last_updated']  2017-11-11T06:41:33Z
            ExtraImages = row['Product'].get('extra_images', '').replace('\\', '')
            Description = row['Product'].get('description')
            ShopName = self.ShopName.strip()
            refreshdict['ShopName'] = ShopName
            PlatformName = 'Joom'
            Tags_dict = row['Product'].get('tags', '')
            Title = ProductName

            DepartmentID, seller, Published = t_store_configuration_file_obj.getinfobyshopcode(ShopName[:9])  # 获取该店铺的部门 编号 销售员 刊登人
            if Published is None or Published.strip() == '':
                Published = seller

            SKU = None
            MainSKU = None
            RefreshTime = datetime.datetime.now()
            Tags = ''
            for Tag_dict in Tags_dict:
                if Tags == '':
                    Tags = Tag_dict['Tag'].get('name')
                else:
                    Tags = '%s,%s' % (Tags, Tag_dict['Tag'].get('name'))

            shopskulist = []  # 定义ShopSKU列表

            filterdict = {}  # 用于 存放 需要修改的 商品SKU
            for variant in row['Product'].get('variants', [{'Variant': None}]):
                VariationID = variant['Variant'].get('id')
                ShopSKU = variant['Variant'].get('sku').replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
                SKU = classshopsku_obj.getSKU(ShopSKU)  # 商品SKU get
                MainSKU = classsku_obj.get_bemainsku_by_sku(SKU)

                sku_goodsstatus = None
                if SKU is not None and SKU.strip() != '':
                    sku_goodsstatus = classsku_obj.get_goodsstatus_by_sku(SKU)  # 获取商品SKU的商品状态
                logger.debug('sku_goodsstatus: %s' % sku_goodsstatus)
                # 下面是简单的转换
                if sku_goodsstatus == u'正常':
                    sku_goodsstatus = '1'
                elif sku_goodsstatus == u'售完下架':
                    sku_goodsstatus = '2'
                elif sku_goodsstatus == u'临时下架':
                    sku_goodsstatus = '3'
                elif sku_goodsstatus == u'停售':
                    sku_goodsstatus = '4'

                ShopSKUImage = ''
                if 'main_image' in variant['Variant'].keys():
                    ShopSKUImage = variant['Variant'].get('main_image').replace('\\', '')
                # classshopsku_obj.setImage(ShopSKU,ShopSKUImage) # 变体图 set

                Price = variant['Variant'].get('price')
                if Price:
                    Price = float('%.2f' % float(Price))
                # classshopsku_obj.setPrice(ShopSKU,Price)        # 价格 set

                Inventory = variant['Variant'].get('inventory')
                # classshopsku_obj.setQuantity(ShopSKU,Inventory) # 库存 set

                Status = variant['Variant'].get('enabled', '')  # "enabled": "False",
                Statusssss = Status
                # classshopsku_obj.setStatus(ShopSKU,Statusssss)      # 状态 set

                if Statusssss == 'True':
                    filterdict[ShopSKU] = 0

                Shipping = variant['Variant'].get('shipping')
                # classshopsku_obj.setShipping(ShopSKU,Shipping)  # 运费 set

                Color = ''
                if 'color' in variant['Variant'].keys():
                    Color = variant['Variant'].get('color')
                # classshopsku_obj.setColor(ShopSKU,Color)        # 颜色 set

                Size = ''
                if 'size' in variant['Variant'].keys():
                    Size = variant['Variant'].get('size')[:30]
                # classshopsku_obj.setSize(ShopSKU,Size)          # 尺寸 set

                msrp = variant['Variant'].get('msrp')
                # classshopsku_obj.setmsrp(ShopSKU,msrp)           # 标签价 set

                ShippingTime = variant['Variant'].get('shipping_time')
                # classshopsku_obj.setshippingtime(ShopSKU,ShippingTime) # 运输时间 set
                # Quantity = Inventory

                cursor.execute("SELECT COUNT(ProductID) FROM t_online_info_joom_detail WHERE ProductID=%s AND ShopSKU=%s;", (ProductID, ShopSKU,))
                somecount = cursor.fetchone()
                if somecount[0] > 0:
                    oldprice = self.get_old_price(ProductID, ShopSKU)
                    if oldprice != Price:
                        try:
                            self.update_change_price_log(ProductID, ShopSKU, Price)
                        except Exception as e:
                            logger.error('update_change_price_log error: %s' % str(e))

                    sql_update = "UPDATE t_online_info_joom_detail SET ShopIP=%s,Title=%s,Price=%s,Quantity=%s,RefreshTime=%s,Image=%s,Status=%s," \
                                 "ReviewState=%s,OfJoomes=%s,OfSales=%s,LastUpdated=%s,Shipping=%s,Color=%s,`Size`=%s,msrp=%s," \
                                 "ShippingTime=%s,ExtraImages=%s,Description=%s,Tags=%s,ShopSKUImage=%s,is_promoted=%s," \
                                 "JoomExpress=%s,seller=%s,Published=%s,GoodsStatus=%s,SKU=%s,MainSKU=%s WHERE ProductID=%s AND ShopSKU=%s;"
                    logger.debug('sql_update: %s' % sql_update)
                    cursor.execute(sql_update, (self.ShopIP, Title, Price, Inventory, RefreshTime, ImageURL, Statusssss,
                                   ReviewState, OfJoomes, OfSales, LastUpdated, Shipping, Color, Size, msrp,
                                   ShippingTime, ExtraImages, Description, Tags, ShopSKUImage, is_promoted,
                                   JoomExpress, seller, Published, sku_goodsstatus, SKU, MainSKU, ProductID, ShopSKU))
                else:
                    sql_insert = 'INSERT INTO t_online_info_joom_detail (ShopIP,ShopName,PlatformName,ProductID,Title,' \
                                 'SKU,ShopSKU,Price,Quantity,RefreshTime,Image,Status,DateUploaded,ParentSKU,' \
                                 'ReviewState,OfJoomes,OfSales,LastUpdated,Shipping,Color,`Size`,msrp,' \
                                 'ShippingTime,ExtraImages,VariationID,Description,Tags,' \
                                 'MainSKU,ShopSKUImage,is_promoted,JoomExpress,DepartmentID,seller,Published,' \
                                 'GoodsStatus,filtervalue,APIState)' \
                                 ' VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,' \
                                 '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
                    logger.debug('sql_insert: %s' % sql_insert)
                    cursor.execute(sql_insert, (self.ShopIP, ShopName, PlatformName, ProductID, Title, SKU,
                                                ShopSKU, Price, Inventory, RefreshTime, ImageURL, Statusssss, DateUploaded,
                                                ParentSKU, ReviewState, OfJoomes, OfSales, LastUpdated, Shipping, Color,
                                                Size, msrp, ShippingTime, ExtraImages, VariationID, Description, Tags,
                                                MainSKU, ShopSKUImage, is_promoted, JoomExpress, DepartmentID, seller,
                                                Published, sku_goodsstatus, 1, 'nothing'))
                cursor.execute('commit;')

                shopskulist.append(ShopSKU)
            # classlisting_obj.setShopSKUList(ProductID, '|'.join(shopskulist)) # ProductID ShopSKUList

            for k, v in filterdict.items():
                sql = "UPDATE t_online_info_joom_detail SET filtervalue = 0 WHERE ProductID=%s AND ShopSKU=%s;"
                logger.debug('update t_online_info_joom_detail filtervalue sql: %s' % sql)
                cursor.execute(sql, (ProductID, k))
                self.cnxn.commit()

            params = dict()
            params['ShopName'] = ShopName
            params['ShopIP'] = self.ShopIP
            params['ProductID'] = ProductID
            params['Seller'] = seller
            params['dbcnxn'] = self.cnxn
            self.refresh_joom_listing_run(params)

        self.cnxn.commit()
        cursor.close()
        refreshdict['ProductID'] = prolist
        return refreshdict

    def get_old_price(self, product_id, shopsku):
        sql = "SELECT Price FROM t_online_info_joom_detail WHERE ProductID=%s AND ShopSKU=%s"
        sql_params = (product_id, shopsku, )
        cursor = self.cnxn.cursor()
        cursor.execute(sql, sql_params)
        res = cursor.fetchall()
        oldprice = None
        if res:
            oldprice = res[0][0]
            oldprice = float(oldprice)
            oldprice = float('%.2f' % oldprice)
        cursor.close()
        return oldprice

    def update_change_price_log(self, product_id, shopsku, newprice, newshipping=None):
        get_old_sql = "SELECT SKU, Price, Shipping FROM t_online_info_joom_detail WHERE ProductID=%s AND ShopSKU=%s;"
        get_old_sql_params = (product_id, shopsku,)
        cursor = self.cnxn.cursor()
        cursor.execute(get_old_sql, get_old_sql_params)
        detail_info = cursor.fetchall()
        if detail_info:
            sku = detail_info[0][0]
            oldprice = detail_info[0][1]
            oldshipping = detail_info[0][2]
        else:
            return

        update_info_sql = "UPDATE t_online_info_joom SET UpdatePriceFlag=1, UpdatePriceTime=%s WHERE ProductID=%s;"
        udpate_info_sql_params = (datetime.datetime.now(), product_id, )
        cursor.execute(update_info_sql, udpate_info_sql_params)

        if newshipping:
            newsellprice = float(newprice) + float(newshipping)
            oldsellprice = float(oldprice) + float(newshipping)
        else:
            newsellprice = float(newprice) + float(oldshipping)
            oldsellprice = float(oldprice) + float(oldshipping)

        OldProfitrate = self.get_profit_rate_fun(sku, oldsellprice)
        NewProfitrate = self.get_profit_rate_fun(sku, newsellprice)

        update_detail_sql = "UPDATE t_online_info_joom_detail SET Price=%s, OldPrice=%s, OldProfitrate=%s, NewProfitrate=%s, LastUpdatePriceTime=%s " \
                            "WHERE ProductID=%s AND ShopSKU=%s;"
        update_detail_sql_params = (newprice, oldprice, OldProfitrate, NewProfitrate, datetime.datetime.now(), product_id, shopsku)
        cursor.execute(update_detail_sql, update_detail_sql_params)

        cursor.execute("commit;")
        cursor.close()

    def get_profit_rate_fun(self, sku, sellprice):
        try:
            calculate_price_obj = calculate_price(sku, self.cnxn)
            profitrate_info = calculate_price_obj.calculate_profitRate(sellprice)
        except Exception as e:
            print 'get_profit_rate_fun error: %s' % e
            print 'traceback.format_exc():\n%s' % traceback.format_exc()
            profitrate_info = ''
        if profitrate_info:
            Profitrate = '%.2f' % float(profitrate_info['profitRate'])
        else:
            Profitrate = ''

        return Profitrate

    def refresh_joom_listing_run(self, params):
        shopalldata = None

        infodata = self.getshopproductdata(params['ProductID'])
        if infodata['code'] == 0:
            shopalldata = infodata['mydata']

        if shopalldata is not None:
            # t_report_orders1days_objs = t_report_orders1days(params['dbcnxn'])
            # t_store_configuration_file_obj = t_store_configuration_file(params['dbcnxn'])
            # classlisting_obj = classlisting(params['dbcnxn'])
            # classmainsku_obj = classmainsku(params['dbcnxn'])
            t_templet_joom_upload_result_obj = t_templet_joom_upload_result(params['dbcnxn'])
            # classshopsku_obj = classshopsku(params['dbcnxn'])
            t_online_info_joom_obj = t_online_info_joom(params['dbcnxn'])
            t_distribution_product_to_store_result_obj = t_distribution_product_to_store_result(params['dbcnxn'])

            for obj in shopalldata:
                datedict = {}
                datedict['ProductID'] = obj[1]
                datedict['ShopName'] = obj[3]
                datedict['Title'] = obj[4]
                datedict['SKU'] = obj[5]
                datedict['ShopSKU'] = obj[6]
                datedict['Price'] = obj[7]
                datedict['RefreshTime'] = obj[9]

                # yyyymmdd = obj[9].strftime('%Y%m%d')

                # TODO 订单同步做完之后才有
                # datedict['SoldTheDay']    = t_report_orders1days_objs.getSoldTheDay(obj[1],yyyymmdd)
                # datedict['SoldYesterday'] = t_report_orders1days_objs.getSoldYesterday(obj[1],yyyymmdd)
                # datedict['Orders7Days']   = t_report_orders1days_objs.getOrders7Days(obj[1],yyyymmdd)
                # datedict['SoldXXX']       = int(datedict['SoldTheDay']) - int(datedict['SoldYesterday'])
                datedict['SoldTheDay'] = None
                datedict['SoldYesterday'] = None
                datedict['Orders7Days'] = None
                datedict['SoldXXX'] = None

                # classlisting_obj.set_order7days_listingid(datedict['ProductID'],datedict['Orders7Days'])

                datedict['DateOfOrder'] = None
                datedict['Image'] = obj[10]
                # datedict['Status'] = obj[11]
                # datedict['ReviewState'] = obj[14]

                if str(obj[11]) in STATUSCHOICES.keys():
                    datedict['Status'] = STATUSCHOICES[str(obj[11])]
                else:
                    datedict['Status'] = '0'

                if str(obj[14]) in REVIEWSTATECHOICES.keys():
                    datedict['ReviewState'] = REVIEWSTATECHOICES[obj[14]]
                else:
                    datedict['ReviewState'] = '1'

                datedict['DateUploaded'] = obj[12]
                datedict['LastUpdated'] = obj[17]
                datedict['OfSales'] = obj[16]
                datedict['ParentSKU'] = obj[13]

                datedict['is_promoted'] = obj[-3]
                datedict['JoomExpress'] = obj[-2]

                datedict['Seller'] = params['Seller']

                mainskus = obj[18]
                mainsku = list()
                if mainskus:
                    mainskus_list = mainskus.split(',')
                    for i in mainskus_list:
                        if i not in mainsku:
                            mainsku.append(i)
                if mainsku:
                    datedict['MainSKU'] = ','.join(mainsku)
                else:
                    datedict['MainSKU'] = None

                datedict['TortInfo'] = 'N'
                # mainskulist = classlisting_obj.getmainsku(obj[1])
                # if mainskulist:
                #     tortlist = []
                #     for mainsku in mainskulist:
                #         tortsite = classmainsku_obj.get_tort_by_mainsku(mainsku)
                #         if tortsite is not None:
                #             tortlist = tortlist + tortsite
                #     if tortlist:
                #         if 'Wish' in tortlist:
                #             datedict['TortInfo'] = 'WY'
                #         else :
                #             datedict['TortInfo'] = 'Y'

                datedict['DataSources'] = "NORMAL"
                if t_templet_joom_upload_result_obj.get_count_num(obj[13]) >= 1:
                    datedict['DataSources'] = "UPLOAD"
                else:
                    if t_distribution_product_to_store_result_obj.get_count_num(obj[13]) >= 1:
                        datedict['DataSources'] = "UPLOAD"

                datedict['OperationState'] = 'No'
                if obj[11] == 'Disabled':
                    datedict['OperationState'] = 'Yes'
                datedict['Published'] = obj[-1]
                # if obj[6] is not None and obj[6].strip() != '':
                #     datedict['Published'] = classshopsku_obj.getPublished((obj[6].split(',')[0]).strip())

                datedict['market_time'] = None

                refreshresult = t_online_info_joom_obj.refresh_joom_data(datedict)
                print 'refreshresult %s' % refreshresult
                # logger.debug("refreshresult['error']: %s" % refreshresult['error'])

    def getshopproductdata(self, productid):
        result = {}
        try:
            mycur = self.cnxn.cursor()
            sql = "SELECT PlatformName,ProductID,ShopIP,ShopName,Title,group_concat(SKU separator ',') AS SKU, " \
                  "group_concat(ShopSKU separator ',') AS ShopSKU,Price,Quantity,RefreshTime,Image, " \
                  "IF('True' IN (SELECT `Status` FROM t_online_info_joom_detail a WHERE a.ProductID = '%s' ),'True','False') AS `Status`, " \
                  "DateUploaded,ParentSKU,ReviewState,OfJoomes,OfSales,LastUpdated,group_concat(MainSKU separator ',') as MainSKU,is_promoted,JoomExpress,Published " \
                  "FROM t_online_info_joom_detail WHERE ShopName='%s' AND ProductID='%s' GROUP BY ProductID;"
            full_sql = sql % (productid, self.ShopName, productid)
            logger.debug('getshopproductdata full_sql: %s' % full_sql)
            mycur.execute(full_sql)
            objs = mycur.fetchall()
            mycur.close()
            result['code'] = 0
            result['error'] = ''
            result['mydata'] = objs
        except Exception, ex:
            result['code'] = 1
            result['error'] = '%s:%s' % (Exception, ex)
            result['mydata'] = []
        logger.debug('getshopproductdata %s' % str(result))
        return result


class classshopsku():
    def __init__(self, db_conn=None):
        self.db_conn = db_conn

    def getSKU(self, shopsku):
        sku = None
        shopskulist = []
        for shopskutmp in shopsku.split('+'):
            newshopsku = shopskutmp.split('*')[0].split('\\')[0]
            shopskulist.append(newshopsku)
        skulist = []
        for shopskueach in shopskulist:
            if self.db_conn is not None:
                skusor = self.db_conn.cursor()
                sql = "SELECT SKU FROM py_db.b_goodsskulinkshop WHERE ShopSKU=%s;"
                logger.debug('classshopsku getSKU b_goodsskulinkshop sql: %s' % sql)
                skusor.execute(sql, (shopskueach,))
                obj = skusor.fetchone()
                if obj:
                    sku = obj[0]
                else:
                    sql = "SELECT SKU FROM py_db.b_goods WHERE SKU=%s;"
                    logger.debug('classshopsku getSKU b_goods sql: %s' % sql)
                    skusor.execute(sql, (shopskueach,))
                    skuobj = skusor.fetchone()
                    if skuobj:
                        sku = skuobj[0]
                skusor.close()
            else:
                skulist.append(sku)
        if skulist:
            sku = '+'.join(skulist)
        return sku

    # 商品Published
    def getPublished(self, shopsku):
        if self.db_conn is not None:
            persor = self.db_conn.cursor()
            sql = "SELECT PersonCode FROM py_db.b_goodsskulinkshop WHERE ShopSKU=%s;"
            logger.debug('getPublished sql: %s' % sql)
            persor.execute(sql, (shopsku,))
            obj = persor.fetchone()
            persor.close()
            if obj:
                published = obj[0]
            return published
        else:
            return None


class classsku():
    def __init__(self, db_cnxn=None):
        self.db_cnxn = db_cnxn

    def get_goodsstatus_by_sku(self, sku):
        if self.db_cnxn is not None:
            stacur = self.db_cnxn.cursor()
            sql = "SELECT GoodsStatus, used FROM py_db.b_goods WHERE SKU=%s;"
            logger.debug('get_goodsstatus_by_sku sql: %s' % sql)
            stacur.execute(sql, (sku,))
            obj = stacur.fetchone()
            if obj:
                used = obj[1]
                goodsstatus = obj[0]
                if int(used) == 1:
                    goodsstatus = '4'  # 停售
                else:
                    sql = "SELECT statuscode FROM goodsstatus_compare WHERE hq_GoodsStatus=%s;"
                    logger.debug('get_goodsstatus_by_sku goodsstatus_compare sql: %s' % sql)
                    stacur.execute(sql, (goodsstatus,))
                    obj = stacur.fetchone()
                    if obj:
                        goodsstatus = obj[0]
            stacur.close()
        if goodsstatus == u'1' or goodsstatus == u'1-正常':
            goodsstatus = u'正常'
        if goodsstatus == u'2' or goodsstatus == u'2-售完下架':
            goodsstatus = u'售完下架'
        if goodsstatus == u'3' or goodsstatus == u'3-临时下架':
            goodsstatus = u'临时下架'
        if goodsstatus == u'4' or goodsstatus == u'4-停售':
            goodsstatus = u'停售'
        logger.debug(u'get_goodsstatus_by_sku goodsstatus: %s' % goodsstatus)
        return goodsstatus

    def get_bemainsku_by_sku(self, sku):
        if self.db_cnxn is not None:
            becur = self.db_cnxn.cursor()
            sql = "SELECT MainSKU FROM t_product_mainsku_sku WHERE ProductSKU=%s;"
            logger.debug('get_bemainsku_by_sku sql: %s' % sql)
            becur.execute(sql, (sku,))
            obj = becur.fetchone()
            becur.close()
            if obj:
                bemainsku = obj[0]
                return bemainsku
            else:
                return ''
        else:
            return ''


class classlisting():
    def __init__(self, db_conn=None):
        self.db_conn = db_conn

    def getmainsku(self, listingid):
        if self.db_conn is not None:
            maincur = self.db_conn.cursor()
            maincur.execute("select MainSKU from t_online_info WHERE ProductID = %s ;", (listingid,))
            objs = maincur.fetchall()
            maincur.close()
            mainskulist = []
            for obj in objs:
                if obj and obj[0] is not None:
                    mainskulist.append(obj[0])
            return mainskulist
            logger.debug('getmainsku: %s' % mainskulist)
        else:
            return None


class classmainsku():
    def __init__(self, db_cnxn=None, redis_cnxn=None):
        self.db_cnxn = db_cnxn

    # get 侵权站点
    def get_tort_by_mainsku(self, mainsku):
        if self.db_cnxn is not None:
            percur = self.db_cnxn.cursor()
            sql = "SELECT Site FROM t_tort_aliexpress WHERE MainSKU=%s;"
            logger.debug('get_tort_by_mainsku sql: %s' % sql)
            percur.execute(sql, (mainsku,))
            objs = percur.fetchall()
            percur.close()
            tortlist = []
            for obj in objs:
                if obj and obj[0] is not None:
                    tortlist.append(obj[0])
            tortlist = set(tortlist)
            return tortlist
        else:
            return None


class t_store_configuration_file():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def getDepartmentbyshopcode(self, shopcode):
        depcur = self.db_conn.cursor()
        sql = "SELECT Department FROM t_store_configuration_file WHERE ShopName_temp=%s;"
        logger.debug('getDepartmentbyshopcode sql: %s' % sql)
        depcur.execute(sql, (shopcode,))
        objs = depcur.fetchone()
        depcur.close()
        Department = ''
        if objs:
            Department = objs[0]
        return Department

    def getsellerbyshopcode(self, shopcode):
        setcur = self.db_conn.cursor()
        sql = "SELECT Seller FROM t_store_configuration_file WHERE ShopName_temp=%s;"
        logger.debug('getsellerbyshopcode sql: %s' % sql)
        setcur.execute(sql, (shopcode,))
        objs = setcur.fetchone()
        setcur.close()
        seller = ''
        if objs:
            seller = objs[0]
        return seller

    def getPublishedbyshopcode(self, shopcode):
        pubcur = self.db_conn.cursor()
        sql = "SELECT Published FROM t_store_configuration_file WHERE ShopName_temp=%s;"
        logger.debug('getPublishedbyshopcode sql: %s' % sql)
        pubcur.execute(sql, (shopcode,))
        objs = pubcur.fetchone()
        pubcur.close()
        Published = ''
        if objs:
            Published = objs[0]
        return Published

    def getinfobyshopcode(self, shopcode):
        pubcur = self.db_conn.cursor()
        sql = "SELECT Department, Seller, Published FROM t_store_configuration_file WHERE ShopName_temp=%s;"
        logger.debug('getinfobyshopcode sql: %s' % sql)
        pubcur.execute(sql, (shopcode,))
        objs = pubcur.fetchone()
        pubcur.close()
        Published = ''
        Department = ''
        Seller = ''
        if objs:
            Department = objs[0]
            Seller = objs[1]
            Published = objs[2]
        return Department, Seller, Published


class t_report_orders1days():
    def __init__(self, db_cnxn):
        # TODO JOOM订单数表 t_joom_report_orders1days
        self.db_cnxn = db_cnxn

    def getSoldTheDay(self, productid, yyyymmdd):
        nowtime = (datetime.datetime.strptime(yyyymmdd, '%Y%m%d') + datetime.timedelta(days=-1)).strftime('%Y%m%d')
        mycur = self.db_cnxn.cursor()
        sql = "SELECT OrdersLast1Days FROM t_report_orders1days WHERE YYYYMMDD=%s AND ProductID=%s;"
        logger.debug('getSoldTheDay sql: %s' % sql)
        mycur.execute(sql, (nowtime, productid,))
        obj = mycur.fetchone()
        mycur.close()
        order1 = 0
        if obj and obj[0] is not None:
            order1 = obj[0]

        return order1

    def getSoldYesterday(self, productid, yyyymmdd):
        yesttime = (datetime.datetime.strptime(yyyymmdd, '%Y%m%d') + datetime.timedelta(days=-2)).strftime('%Y%m%d')
        mycur = self.db_cnxn.cursor()
        sql = "SELECT OrdersLast1Days FROM t_report_orders1days WHERE YYYYMMDD=%s AND ProductID=%s;"
        logger.debug('getSoldYesterday sql: %s' % sql)
        mycur.execute(sql, (yesttime, productid,))
        obj = mycur.fetchone()
        mycur.close()
        order2 = 0
        if obj and obj[0] is not None:
            order2 = obj[0]

        return order2

    def getOrders7Days(self, productid, yyyymmdd):
        sevtimeq = (datetime.datetime.strptime(yyyymmdd, '%Y%m%d') + datetime.timedelta(days=-7)).strftime('%Y%m%d')
        sevtimej = (datetime.datetime.strptime(yyyymmdd, '%Y%m%d') + datetime.timedelta(days=-1)).strftime('%Y%m%d')
        mycur = self.db_cnxn.cursor()
        sql = "SELECT sum(OrdersLast1Days) AS Orders7Days FROM  t_report_orders1days WHERE YYYYMMDD BETWEEN %s AND %s AND ProductID=%s;"
        logger.debug('getOrders7Days sql: %s' % sql)
        mycur.execute(sql, (sevtimeq, sevtimej, productid,))
        obj = mycur.fetchone()
        mycur.close()
        order7 = 0
        if obj and obj[0] is not None:
            order7 = obj[0]

        return order7


class t_templet_joom_upload_result():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def update_result_status(self, resultstatus, errormessage, resultid):
        updcur = self.db_conn.cursor()
        sql = "UPDATE t_templet_joom_upload_result SET Status=%s, ErrorMessage=%s WHERE id=%s;"
        logger.debug('t_templet_joom_upload_result update_result_status sql: %s' % sql)
        updcur.execute(sql, (resultstatus, errormessage, resultid))
        updcur.execute('commit')
        updcur.close()

    def get_count_num(self, parentsku):
        parcur = self.db_conn.cursor()
        sql = "SELECT COUNT(ParentSKU) FROM t_templet_joom_upload_result WHERE ParentSKU=%s;"
        logger.debug('t_templet_joom_upload_result get_count_num sql: %s' % sql)
        parcur.execute(sql, (parentsku,))
        obj = parcur.fetchone()
        parcur.close()
        num = 0
        if obj:
            num = obj[0]
        return num


class t_online_info_joom():
    def __init__(self, db_cnxn):
        self.db_cnxn = db_cnxn

    def refresh_joom_data(self, params):
        result = {}
        try:
            mycur = self.db_cnxn.cursor()
            sql = "INSERT INTO t_online_info_joom SET " \
                "PlatformName='Joom',ProductID=%s,ShopIP='',ShopName=%s,Title=%s,SKU=%s," \
                "ShopSKU=%s,Price=%s,Quantity=0,SoldYesterday=%s," \
                "SoldTheDay=%s,SoldXXX=%s,DateOfOrder=%s,RefreshTime=%s," \
                "Image=%s,Status=%s,ReviewState=%s,DateUploaded=%s,LastUpdated=%s,OfSales=%s," \
                "ParentSKU=%s,Seller=%s,TortInfo=%s,MainSKU=%s,DataSources=%s,OperationState=%s" \
                ",Published=%s,market_time=%s,is_promoted=%s,JoomExpress=%s ON DUPLICATE KEY UPDATE" \
                " Title=%s,SoldYesterday=%s,SKU=%s," \
                "SoldTheDay=%s,SoldXXX=%s,DateOfOrder=%s,RefreshTime=%s,Status=%s," \
                "ReviewState=%s,DateUploaded=%s,LastUpdated=%s,OfSales=%s,Seller=%s," \
                "TortInfo=%s,MainSKU=%s,DataSources=%s,OperationState=%s,Published=%s," \
                "market_time=%s,ShopSKU=%s,is_promoted=%s,JoomExpress=%s;"
            logger.debug('refresh_joom_data sql: %s' % sql)
            mycur.execute(sql, (params['ProductID'], params['ShopName'], params['Title'], params['SKU'],
                                params['ShopSKU'], params['Price'], params['SoldYesterday'],
                                params['SoldTheDay'], params['SoldXXX'], params['DateOfOrder'], params['RefreshTime'],
                                params['Image'], params['Status'], params['ReviewState'], params['DateUploaded'],
                                params['LastUpdated'], params['OfSales'], params['ParentSKU'], params['Seller'],
                                params['TortInfo'], params['MainSKU'], params['DataSources'], params['OperationState'],
                                params['Published'], params['market_time'], params['is_promoted'], params['JoomExpress'],
                                params['Title'], params['SoldYesterday'], params['SKU'], params['SoldTheDay'],
                                params['SoldXXX'], params['DateOfOrder'], params['RefreshTime'], params['Status'], params['ReviewState'],
                                params['DateUploaded'], params['LastUpdated'], params['OfSales'], params['Seller'],
                                params['TortInfo'], params['MainSKU'], params['DataSources'], params['OperationState'],
                                params['Published'], params['market_time'], params['ShopSKU'], params['is_promoted'], params['JoomExpress'],))
            mycur.execute("commit;")
            mycur.close()
            result['code'] = 0
            result['error'] = ''
        except Exception, ex:
            result['code'] = 1
            result['error'] = '%s:%s' % (Exception, ex)
        # logger.debug('refresh_joom_data result: %s' % str(result))
        return result


class t_distribution_product_to_store_result():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def get_count_num(self, parentsku):
        parcur = self.db_conn.cursor()
        sql = "SELECT COUNT(ParentSKU) FROM t_distribution_product_to_store_result WHERE ParentSKU=%s;"
        logger.debug('t_distribution_product_to_store_result get_count_num sql: %s' % sql)
        parcur.execute(sql, (parentsku,))
        obj = parcur.fetchone()
        parcur.close()
        num = 0
        if obj:
            num = obj[0]
        return num


class calculate_price():
    def __init__(self, SKU, conn):
        self.SKU = SKU
        self.conn = conn
        cur = self.conn.cursor()
        try:
            sql = "SELECT CostPrice,Weight FROM py_db.b_goods WHERE SKU = '%s';" % SKU
            cur.execute(sql)
            row = cur.fetchone()
            self.Money = str(row[0])
            self.Weight = str(row[1])
        except Exception as e:
            print 'calculate_price error: %s' % e
            print 'traceback.format_exc():\n%s' % traceback.format_exc()
            self.Money = None
            self.Weight = None
        cur.close()

    # 计算售价
    # Weight 商品原始克重(g)
    # Money  商品原始成本(人民币)
    # profitRate 利润率 默认0
    # 返回三种不同货币类型的售价,数据类型dic
    def calculate_selling_price(self, profitRate, platformCountryCode='JOOM-RUS', DestinationCountryCode='RUS', Money=None, Weight=None):
        cur = self.conn.cursor()
        try:
            Money = float(self.Money)
            Weight = float(self.Weight)
        except:
            Money = float(Money)
            Weight = float(Weight)
        profitRate = float(profitRate)

        error_info = {'error_code': 200, 'error_info': '信息获取成功!'}
        # 根据页面的目的地国家和平台国家编号去找物流方式编号
        sql = "SELECT logisticwaycode,logisticwaycode_desc,kickback FROM t_cfg_b_emsfare2 WHERE platform_country_code = '%s' AND countrycode = '%s'" % (platformCountryCode, DestinationCountryCode)
        cur.execute(sql)
        row = cur.fetchone()
        logisticwaycode_expression = str(row[0])
        logisticwaycode_desc = str(row[1])
        scope = {'sell_price': 0, 'Weight': Weight}
        exec(logisticwaycode_expression, scope)
        logisticwaycode = scope['waycode']
        # 根据当前平台国家编号获取当前货币编号以及平台扣点
        kickback = float(row[2])
        CURRENCYCODE = None
        basefee = None
        try:
            sql = "SELECT basefee FROM t_cfg_platform_country WHERE platform_country_code = '%s'" % platformCountryCode
            cur.execute(sql)
            row = cur.fetchone()
            basefee = float(row[0])
            sql = "SELECT CURRENCYCODE FROM t_cfg_b_country WHERE country_code = '%s'" % DestinationCountryCode
            cur.execute(sql)
            row = cur.fetchone()
            CURRENCYCODE = str(row[0])
            sql = "SELECT ExchangeRate FROM t_cfg_b_currencycode WHERE CURRENCYCODE = '%s'" % CURRENCYCODE
            cur.execute(sql)
            row = cur.fetchone()
            basefee = basefee * float(row[0])
        except:
            error_info = {'error_code': 2, 'error_info': '平台扣点/目的国家货币名称/ 当中没有配置！'}

        # 计算售价=成本价+运费
        if 1 - profitRate / 100 - kickback / 100 == 0:
            error_info = {'error_code': 7, 'error_info': '利润率和平台扣点有冲突！'}
            return

        # 根据货币编号获取人民币汇率
        ExchangeRate = None
        try:
            sql = "SELECT ExchangeRate FROM t_cfg_b_currencycode WHERE CURRENCYCODE = '%s'" % CURRENCYCODE
            cur.execute(sql)
            row = cur.fetchone()
            ExchangeRate = float(row[0])
        except:
            error_info = {'error_code': 3, 'error_info': '当前货币与人民币汇率 没有配置！'}

        # 获取美元与人民币汇率
        ExchangeRate_USD = None
        try:
            sql = "SELECT ExchangeRate FROM t_cfg_b_currencycode WHERE CURRENCYCODE = 'USD'"
            cur.execute(sql)
            row = cur.fetchone()
            ExchangeRate_USD = float(row[0])
        except:
            error_info = {'error_code': 4, 'error_info': '美元与人民币汇率 没有配置！'}

        # 根据物流方式编号和目的国家编号去查询基本运费计算规则
        try:
            sql = "SELECT getprice,getprice_desc,Bracketid FROM t_cfg_b_emsfare_country2 WHERE country_code = '%s' AND logisticwaycode = '%s'" % (DestinationCountryCode, logisticwaycode)
            cur.execute(sql)
            row = cur.fetchone()
            getprice_expression = str(row[0])
            getprice_desc = str(row[1])
            scope2 = {'Weight': Weight}

            exec(getprice_expression, scope2)
            price_yf = scope2['Price']
            Bracketid = str(row[2])
        except:
            error_info = {'error_code': 5, 'error_info': '基础费用/初始价格/初始重量/增加价格/增加重量 没有配置！'}

        # 根据一次算价的物流方式得到的外键Bracketid获取分档价格
        try:
            sql = "SELECT money,CURRENCYCODE FROM t_cfg_bracket WHERE bracketid = '%s' AND weight >= '%s' ORDER BY weight LIMIT 1" % (Bracketid, Weight)
            cur.execute(sql)
            row = cur.fetchone()
            fd_money = float(row[0])
            CURRENCYCODE = str(row[1])
            sql = "SELECT ExchangeRate FROM t_cfg_b_currencycode WHERE CURRENCYCODE = '%s'" % CURRENCYCODE
            cur.execute(sql)
            row = cur.fetchone()
            ExchangeRate2 = float(row[0])
            fd_money = fd_money * float(ExchangeRate2)
        except:
            fd_money = 0

        # 一次算价,获取对应物流中文名称以及物流折扣
        logisticName = None
        Discount = None
        try:
            sql = "SELECT name,discount FROM t_cfg_b_logisticway WHERE CODE = '%s'" % logisticwaycode
            cur.execute(sql)
            row = cur.fetchone()
            logisticName = str(row[0])
            Discount = float(row[1])
        except:
            error_info = {'error_code': 6, 'error_info': '物流方式名称/物流折扣 没有配置！'}
            print error_info

        # 一次算价得到最终售价
        sellingPrice_destination = ((price_yf + fd_money) * Discount / 100 + Money + basefee) / ExchangeRate / (1 - profitRate / 100 - kickback / 100)
        # 目的国家售价
        sellingPrice_china = sellingPrice_destination * ExchangeRate
        sellingPrice_us = sellingPrice_destination * ExchangeRate / ExchangeRate_USD
        sellingPrice1 = round(sellingPrice_us, 2)
        params_flow1 = {
            'flag': 01, 'logisticwaycode_desc': logisticwaycode_desc, 'getprice_desc': getprice_desc, 'sellingPrice1': sellingPrice1,
            'price_yf': price_yf, 'fd_money': fd_money, 'Discount': Discount, 'Money': Money, 'basefee': basefee, 'ExchangeRate_USD': ExchangeRate_USD,
            'profitRate': profitRate, 'kickback': kickback, 'logisticwaycode_expression': logisticwaycode_expression
        }
        # 二次算价重新给域赋值
        scope3 = {'Weight': Weight, 'sell_price': sellingPrice1}
        exec(logisticwaycode_expression, scope3)
        pricelimit_logisticwaycode = scope3['waycode']
        # 二次算价,获取对应物流中文名称以及平台折扣
        try:
            sql = "SELECT name,discount FROM t_cfg_b_logisticway WHERE CODE = '%s'" % pricelimit_logisticwaycode
            cur.execute(sql)
            row = cur.fetchone()
            logisticName = str(row[0])
            Discount = float(row[1])
        except:
            logisticName = None
            Discount = None
        # 二次算价获取运费
        sql = "SELECT getprice,getprice_desc,Bracketid FROM t_cfg_b_emsfare_country2 WHERE country_code = '%s' AND logisticwaycode = '%s'" % (DestinationCountryCode, pricelimit_logisticwaycode)
        cur.execute(sql)
        row = cur.fetchone()
        getprice_expression = str(row[0])
        getprice_desc = str(row[1])

        scope4 = {'Weight': Weight}
        exec(getprice_expression, scope4)
        price_yf = scope4['Price']
        Bracketid = str(row[2])
        # 二次算价获取分档运费
        try:
            sql = "SELECT money,CURRENCYCODE FROM t_cfg_bracket WHERE bracketid = '%s' AND weight >= '%s' ORDER BY weight LIMIT 1" % (Bracketid, Weight)
            cur.execute(sql)
            row = cur.fetchone()
            fd_money = float(row[0])
            CURRENCYCODE = str(row[1])
            sql = "SELECT ExchangeRate FROM t_cfg_b_currencycode WHERE CURRENCYCODE = '%s'" % CURRENCYCODE
            cur.execute(sql)
            row = cur.fetchone()
            ExchangeRate2 = float(row[0])
            fd_money = fd_money * float(ExchangeRate2)
        except:
            fd_money = 0

        sellingPrice_destination = ((price_yf + fd_money) * Discount / 100 + Money + basefee) / ExchangeRate / (1 - profitRate / 100 - kickback / 100)  # 目的国家售价
        sellingPrice_china = sellingPrice_destination * ExchangeRate
        sellingPrice_us = sellingPrice_destination * ExchangeRate / ExchangeRate_USD
        sellingPrice2 = round(sellingPrice_us, 2)
        params_flow2 = {
            'flag': 02, 'logisticwaycode_desc': logisticwaycode_desc, 'getprice_desc': getprice_desc, 'price_yf': price_yf, 'fd_money': fd_money,
            'Discount': Discount, 'Money': Money, 'basefee': basefee, 'ExchangeRate_USD': ExchangeRate_USD, 'profitRate': profitRate,
            'kickback': kickback, 'logisticwaycode_expression': logisticwaycode_expression
        }

        # 保留俩位小数点
        sellingPrice_destination = round(sellingPrice_destination, 2)
        sellingPrice_china = round(sellingPrice_china, 2)
        sellingPrice_us = round(sellingPrice_us, 2)

        # sellingPrice 最终售价,同时获取 logisticName物流方式,kickback平台扣点,ExchangeRate汇率,Discount物流折扣 以dic形式返回=>
        if sellingPrice1 == sellingPrice2:
            params = {
                'sellingPrice_destination': sellingPrice_destination, 'sellingPrice_china': sellingPrice_china, 'sellingPrice_us': sellingPrice_us,
                'logisticName': logisticName, 'CURRENCYCODE': CURRENCYCODE, 'kickback': kickback, 'ExchangeRate': ExchangeRate, 'Discount': Discount,
                'params_flow': params_flow1
            }
        else:
            params = {
                'sellingPrice_destination': sellingPrice_destination, 'sellingPrice_china': sellingPrice_china, 'sellingPrice_us': sellingPrice_us,
                'logisticName': logisticName, 'CURRENCYCODE': CURRENCYCODE, 'kickback': kickback, 'ExchangeRate': ExchangeRate, 'Discount': Discount,
                'params_flow': params_flow2, 'params_flow1': params_flow1
            }
        cur.close()
        # conn.close()
        return params

    # 计算利润率
    # platformCountryCode=t_cfg_b_emsfare.platform_country_code
    # Weight 商品原始克重(g)
    # Money  商品原始成本(人民币)
    # sellingPrice 售价(人民币，显示的是加入汇率计算)
    # 返回profitRate利润率(百分制,15就是 15%)
    # (成本(￥)+运费(￥))/汇率/(1-利润率-平台扣点比率) = 最终售价(目标币种)
    def calculate_profitRate(self, sellingPrice, platformCountryCode='JOOM-RUS', DestinationCountryCode='RUS', Money=None, Weight=None):
        cur = self.conn.cursor()
        try:
            Money = float(self.Money)
            Weight = float(self.Weight)
        except:
            Money = float(Money)
            Weight = float(Weight)
        try:
            sellingPrice = float(sellingPrice)
        except:
            sellingPrice = -1
        # 获取美元与人民币汇率
        try:
            sql = "SELECT ExchangeRate FROM t_cfg_b_currencycode WHERE CURRENCYCODE = 'USD'"
            cur.execute(sql)
            row = cur.fetchone()
            ExchangeRate_USD = float(row[0])
        except:
            ExchangeRate_USD = None
        # 根据当前平台国家编号获取当前货币编号以及平台扣点
        try:
            sql = "SELECT basefee FROM t_cfg_platform_country WHERE platform_country_code = '%s'" % platformCountryCode
            cur.execute(sql)
            row = cur.fetchone()
            basefee = float(row[0])
            sql = "SELECT kickback FROM t_cfg_b_emsfare2 WHERE platform_country_code = '%s' AND countrycode = '%s'" % (platformCountryCode, DestinationCountryCode)
            cur.execute(sql)
            row = cur.fetchone()
            kickback = float(row[0])
            sql = "SELECT CURRENCYCODE FROM t_cfg_b_country WHERE country_code = '%s'" % DestinationCountryCode
            cur.execute(sql)
            row = cur.fetchone()
            CURRENCYCODE = str(row[0])
            sql = "SELECT ExchangeRate FROM t_cfg_b_currencycode WHERE CURRENCYCODE = '%s'" % CURRENCYCODE
            cur.execute(sql)
            row = cur.fetchone()
            ExchangeRate_basefee = row[0]
            basefee = basefee * float(ExchangeRate_basefee)
        except:
            kickback = None
            CURRENCYCODE = None
            basefee = None
        # 根据货币编号获取人民币汇率
        try:
            sql = "SELECT ExchangeRate FROM t_cfg_b_currencycode WHERE CURRENCYCODE = '%s'" % CURRENCYCODE
            cur.execute(sql)
            row = cur.fetchone()
            ExchangeRate = float(row[0])
        except:
            ExchangeRate = None
        # 根据页面的目的地国家和平台国家编号去找默认物流方式编号，最大价格限制以及超过最大价格后采取的新的物流方式编号
        sql = "SELECT logisticwaycode FROM t_cfg_b_emsfare2 WHERE platform_country_code = '%s' AND countrycode = '%s'" % (platformCountryCode, DestinationCountryCode)
        cur.execute(sql)
        row = cur.fetchone()
        logisticwaycode_expression = str(row[0])
        scope = {'sell_price': sellingPrice, 'Weight': Weight}
        exec(logisticwaycode_expression, scope)
        waycode = scope['waycode']

        try:
            sql = "SELECT name,discount FROM t_cfg_b_logisticway WHERE CODE = '%s'" % waycode
            cur.execute(sql)
            row = cur.fetchone()
            logisticName = row[0]
            Discount = float(row[1])
        except Exception as e:
            print 't_cfg_b_logisticway Discount error: %s' % e
            print 'traceback.format_exc():\n%s' % traceback.format_exc()
            logisticName = None
            Discount = None
        # 根据物流方式编号和目的国家编号去查询基本运费计算规则
        sql = "SELECT getprice,Bracketid FROM t_cfg_b_emsfare_country2 WHERE country_code = '%s' AND logisticwaycode = '%s'" % (DestinationCountryCode, waycode)
        cur.execute(sql)
        row = cur.fetchone()
        getprice_expression = str(row[0])
        scope2 = {'Weight': Weight}
        exec(getprice_expression, scope2)
        price_yf = scope2['Price']
        Bracketid = str(row[1])
        # 二次算价获取分档运费
        try:
            sql = "SELECT money,CURRENCYCODE FROM t_cfg_bracket WHERE bracketid = '%s' AND weight >= '%s' ORDER BY weight LIMIT 1" % (Bracketid, Weight)
            cur.execute(sql)
            row = cur.fetchone()
            fd_money = float(row[0])
            CURRENCYCODE = str(row[1])
            sql = "SELECT ExchangeRate FROM t_cfg_b_currencycode WHERE CURRENCYCODE = '%s'" % CURRENCYCODE
            cur.execute(sql)
            row = cur.fetchone()
            ExchangeRate = row[0]
            fd_money = fd_money * float(ExchangeRate)
        except:
            fd_money = 0
        sum_money = (price_yf + fd_money) * Discount / 100.0 + Money + basefee
        # 计算利润率
        profitRate = (1 - kickback / 100 - sum_money / ExchangeRate_USD / sellingPrice) * 10.0 * 10.0
        if sellingPrice == -1:
            profitRate = 99999
        profitRate = round(profitRate, 2)
        # 获取人民币以及目标国家货币价值
        sellingPrice_china = sellingPrice * ExchangeRate_USD
        sellingPrice_destination = sellingPrice_china / ExchangeRate
        params = {
            'price_yf': price_yf, 'fd_money': fd_money, 'basefee': basefee, 'sellingPrice_destination': sellingPrice_destination,
            'sellingPrice_china': sellingPrice_china, 'logisticName': logisticName, 'CURRENCYCODE': CURRENCYCODE, 'ExchangeRate_USD': ExchangeRate_USD,
            'Discount': Discount, 'Money': Money, 'sum_money': sum_money, 'sellingPrice': sellingPrice, 'kickback': kickback,
            'ExchangeRate': ExchangeRate, 'Discount': Discount, 'profitRate': profitRate
        }
        cur.close()
        return params


def retry_server():
    try:
        c = Server()
        c.listen_client()
    except Exception as e:
        print 'Define server error', e
        print 'traceback.format_exc():\n%s' % traceback.format_exc()
        logger.error('Define server error %s' % e)
        logger.error('traceback.format_exc():\n%s' % traceback.format_exc())
        time.sleep(5)
        retry_server()

if __name__ == '__main__':
    retry_server()

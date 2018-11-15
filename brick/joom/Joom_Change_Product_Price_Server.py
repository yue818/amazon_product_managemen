#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import time
import pika
import requests
import logging
import logging.handlers
import MySQLdb
import datetime
import traceback
# import multiprocessing

# logging.basicConfig(level=logging.DEBUG,format='%(asctime)s [%(filename)s %(funcName)s:%(lineno)d] %(thread)d %(levelname)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S',filename='joom_get_product.log',filemode='a')
# logging.handlers.RotatingFileHandler('joom_get_product.log', maxBytes=100 * 1024 * 1024, backupCount=10)

log_formatter = logging.Formatter('%(asctime)s [%(filename)s %(funcName)s:%(lineno)d] %(thread)d %(levelname)s %(message)s')
logFile = 'joom_change_product_price.log'
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

    def listen_client(self):
        channel = self.connection.channel()
        queue = self.realIP + '_joom_change_product_info'
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
        data = eval(body)
        db_conn = MySQLdb.connect(DATABASES['HOST'], DATABASES['USER'], DATABASES['PASSWORD'], DATABASES['NAME'], charset="utf8")
        logger.debug('shop info: %s' % data)
        try:
            self.joom_change_product_info(data, db_conn)
        except Exception as e:
            print 'traceback.format_exc():\n%s' % traceback.format_exc()
            logger.error(e)
            logger.error('traceback.format_exc():\n%s' % traceback.format_exc())
        print ' [x] Get Joom Products Over, Close DB Connection, Now: %s' % datetime.datetime.now()
        logger.debug(' [x] Get Joom Products Over, Close DB Connection, Now: %s' % datetime.datetime.now())
        db_conn.close()

    def joom_change_product_info(self, data, db_conn):
        t_api_scheduleImp = t_api_schedule(None, db_conn)
        if not data:
            logger.error('Empty Message!')
        t_api_scheduleImp.getauthByShopName(data['ShopName'])
        product_info = data.get('productinfo')
        product_id = data.get('product_id')
        result_list = list()
        res_dict = dict()
        for shopsku in product_info.keys():
            res = self.change_product_price(t_api_scheduleImp, shopsku, product_info[shopsku], product_id, db_conn)
            print '=========res: %s' % res
            # logger.debug('=========res: %s' % res)
            res_dict[shopsku] = {'message': res['mess'], 'result': res['result']}
            result_list.append(res['result'])

        res_data = dict()
        if 'FALIED' in result_list and 'SUCCESS' in result_list:
            res_data['result'] = 'SOME SUCCESS'
        elif 'FALIED' not in result_list and 'SUCCESS' in result_list:
            res_data['result'] = 'ALL SUCCESS'
        elif 'SUCCESS' not in result_list and 'FALIED' in result_list:
            res_data['result'] = 'ALL FALIED'
        else:
            res_data['result'] = 'ERROR'
        res_data['mess'] = str(res_dict).replace('\'', '\\\'')
        res_data['info'] = res_dict

        self.update_result_to_db(res_data, db_conn, data)

    def change_product_price(self, t_api_scheduleImp, shopsku, product_info, product_id, db_conn):
        url_Change_Products = "https://api-merchant.joom.com/api/v2/variant/update"
        data = {
            'access_token': t_api_scheduleImp.auth_info['access_token'],
            'sku': shopsku,
        }

        if product_info.get('color'):
            data['color'] = product_info.get('color')
        if product_info.get('main_image'):
            data['main_image'] = product_info.get('main_image')
        if product_info.get('msrp'):
            data['msrp'] = product_info.get('msrp')
        if product_info.get('price'):
            data['price'] = product_info.get('price')
        if product_info.get('shipping'):
            data['shipping'] = product_info.get('shipping')
        if product_info.get('size'):
            data['size'] = product_info.get('size')
        if product_info.get('inventory'):
            data['inventory'] = product_info.get('inventory')
        if product_info.get('shipping_time'):
            data['shipping_time'] = product_info.get('shipping_time')

        flag = 0
        while True:
            res = {'result': '', 'mess': ''}
            try:
                dict_ret = requests.post(url_Change_Products, params=data, timeout=60)
            except:
                time.sleep(30)
                dict_ret = requests.post(url_Change_Products, params=data, timeout=60)
            _content = eval((dict_ret._content.replace('null', 'None')))
            print '==========_content %s' % _content
            # 刷新一下token  1015 :问令牌过期   4000:权存取 1016:失效
            if _content['code'] == 1015 or _content['code'] == 1016:  # or _content['code']== 4000   or _content['code']== 1017  or _content['code']== 1018  or _content['code']== 9000   :
                self.RefreshToken(t_api_scheduleImp)
                if flag == 0:
                    flag = 1
                    continue
                else:
                    res['result'] = 'FALIED'
                    res['mess'] = 'Shop access_token and refresh_token are not available!'
                    break
            if dict_ret.status_code == 200 and _content['code'] == 0:
                res['result'] = 'SUCCESS'
                res['mess'] = _content.get('data', '')
                if product_info.get('price'):
                    self.update_change_price_log(product_id, shopsku, product_info.get('price'), db_conn, newshipping=product_info.get('shipping'))
                break
            else:
                res['result'] = 'FALIED'
                if _content:
                    res['mess'] = str(_content)
                else:
                    res['mess'] = 'Change Product Price Falied!'
                break
        return res

    def update_change_price_log(self, product_id, shopsku, newprice, db_conn, newshipping=None):
        get_old_sql = "SELECT SKU, Price, Shipping FROM t_online_info_joom_detail WHERE ProductID=%s AND ShopSKU=%s;"
        get_old_sql_params = (product_id, shopsku,)
        cursor = db_conn.cursor()
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

        OldProfitrate = self.get_profit_rate_fun(sku, oldsellprice, db_conn)
        NewProfitrate = self.get_profit_rate_fun(sku, newsellprice, db_conn)

        update_detail_sql = "UPDATE t_online_info_joom_detail SET Price=%s, OldPrice=%s, OldProfitrate=%s, NewProfitrate=%s, LastUpdatePriceTime=%s " \
                            "WHERE ProductID=%s AND ShopSKU=%s;"
        update_detail_sql_params = (newprice, oldprice, OldProfitrate, NewProfitrate, datetime.datetime.now(), product_id, shopsku)
        cursor.execute(update_detail_sql, update_detail_sql_params)

        cursor.execute("commit;")
        cursor.close()

    def get_profit_rate_fun(self, sku, sellprice, db_conn):
        try:
            calculate_price_obj = calculate_price(sku, db_conn)
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

    def update_result_to_db(self, res, db_conn, data):
        params = tuple()
        if data.get('flag') == 'cutprice':
            sql = "UPDATE t_joom_cutprice_log SET SetResult=%s, ResMess=%s WHERE ProductID=%s"
            params = (res['result'], res['mess'], data['product_id'])
        elif data.get('flag') == 'recoverprice':
            sql = "UPDATE t_joom_cutprice_log SET RecoverResult=%s, RecoverMess=%s, Recover_Datetime=%s WHERE ProductID=%s"
            params = (res['result'], res['mess'], datetime.datetime.now(), data['product_id'])
        elif data.get('flag') == 'price_parity':
            self.update_price_parity_resinfo(res, db_conn, data)
            return
        else:
            return
        cursor = db_conn.cursor()
        cursor.execute(sql, params)
        db_conn.commit()
        cursor.close()
        return

    def update_price_parity_resinfo(self, res, db_conn, data):
        cursor = db_conn.cursor()
        product_info = data.get('productinfo')
        for shopsku in product_info.keys():
            log_id = product_info[shopsku]['log_id']
            res_info = res['info'][shopsku]
            if res_info['result'] == 'SUCCESS':
                change_flag = 'True'
            else:
                change_flag = 'False'
            params_log = tuple()
            sql = "UPDATE t_joom_price_parity_log SET ChangeRes=%s, ChangeResMess=%s, ChangeFlag=%s WHERE id=%s;"
            params_log = (res_info['result'], res_info['message'], change_flag, log_id)
            cursor.execute(sql, params_log)
            if change_flag != 'False':
                params_detail = tuple()
                sql_detail = "UPDATE t_online_info_joom_detail SET Price=%s WHERE ProductID=%s AND ShopSKU=%s;"
                params_detail = (product_info[shopsku]['price'], data['product_id'], shopsku)
                cursor.execute(sql_detail, params_detail)
        if res['result'] != 'ALL SUCCESS':
            params_status = tuple()
            sql_1 = "UPDATE t_online_info_joom SET priceParity_Status='4' WHERE ProductID=%s;"
            params_status = (data['product_id'],)
            cursor.execute(sql_1, params_status)
        db_conn.commit()
        cursor.close()
        return

    def RefreshToken(self, t_api_scheduleImp):
        params = {
            'client_id': t_api_scheduleImp.auth_info['client_id'],
            'client_secret': t_api_scheduleImp.auth_info['client_secret'],
            'refresh_token': t_api_scheduleImp.auth_info['refresh_token'],
            'grant_type': 'refresh_token',
        }
        try:
            refresh_token_ret = requests.post('https://api-merchant.joom.com/api/v2/oauth/refresh_token', params=params, timeout=200)
        except:
            time.sleep(10)
            refresh_token_ret = requests.post('https://api-merchant.joom.com/api/v2/oauth/refresh_token', params=params, timeout=200)
        logger.debug('refresh_token_ret=%s' % refresh_token_ret.__dict__)
        _content = eval(refresh_token_ret._content.replace(':null,', ':0,'))
        access_token = _content['data']['access_token']
        refresh_token = _content['data']['refresh_token']

        cursor = t_api_scheduleImp.cnxn.cursor()
        sql_access_token = 'UPDATE t_config_online_joom SET V= \'%s\' WHERE ShopName =\'%s\' AND K =\'%s\' ' % (access_token, t_api_scheduleImp.ShopName, 'access_token')
        logger.debug('sql_access_token: %s' % sql_access_token)
        cursor.execute(sql_access_token)
        sql_refresh_token = 'UPDATE t_config_online_joom SET V= \'%s\' WHERE ShopName =\'%s\' AND K =\'%s\' ' % (refresh_token, t_api_scheduleImp.ShopName, 'refresh_token')
        logger.debug('sql_refresh_token: %s' % sql_refresh_token)
        cursor.execute(sql_refresh_token)

        last_refresh_token_time = datetime.datetime.now()
        select_sql = "SELECT * FROM t_config_online_joom WHERE ShopName=%s AND IP=%s AND K=%s;"
        res = cursor.execute(select_sql, (self.OneCmdRecoreDict['ShopName'], self.realIP, 'last_refresh_token_time'))
        if not res:
            sql_insert = 'INSERT INTO t_config_online_joom (V,ShopName,IP,K) VALUES(%s,%s,%s,%s);'
        else:
            sql_insert = "UPDATE t_config_online_joom SET V=%s WHERE ShopName=%s AND IP=%s AND K=%s;"
        logger.debug('sql_insert: %s' % sql_insert)
        cursor.execute(sql_insert, (last_refresh_token_time, self.OneCmdRecoreDict['ShopName'], self.realIP, 'last_refresh_token_time'))
        self.t_api_scheduleImp.cnxn.commit()
        cursor.close()


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
    # pool = multiprocessing.Pool(processes=1)
    # for i in xrange(1):
    #     pool.apply_async(retry_server)

    # pool.close()
    # pool.join()    # behind close() or terminate()

    retry_server()

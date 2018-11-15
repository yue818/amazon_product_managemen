# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: amazon_auto_load_.py
 @time: 2018/11/8 18:48
"""
import uuid
import pymysql
import redis
# from brick.amazon.product_refresh.get_auth_info import GetAuthInfo
# from brick.amazon.product_refresh.generate_feed_xml import GenerateFeedXml
# from brick.amazon.upload_product.message_to_rabbitmq import MessageToRabbitMq
import json
import datetime
import time
import xml.dom.minidom
import pika
# import chardet


class GetAuthInfo:
    def __init__(self, db_connection, ):
        self.db_connection = db_connection

    def get_name_by_shop_and_site(self, shop_name, site):
        cursor = self.db_connection.cursor()
        sql = "select DISTINCT name from t_config_online_amazon where shop_name = '%s' and site = '%s'" \
              %(shop_name, site)
        cursor.execute(sql)
        name_info = cursor.fetchone()
        cursor.close()
        return name_info[0]

    def get_auth_info_by_shop_name(self, shop_name):
        auth_info = {}
        cursor = self.db_connection.cursor()
        sql_site = "select site from t_config_online_amazon  where name= '%s' limit 1" % shop_name
        print sql_site
        cursor.execute(sql_site)
        auth_info['ShopSite'] = cursor.fetchone()[0]

        sql = "select IP,Name,K,V from t_config_online_amazon  where name= '%s'" % shop_name
        cursor.execute(sql)
        shop_config_info = cursor.fetchall()
        print shop_config_info
        cursor.close()
        auth_info['ShopName'] = shop_name
        for shop_config_info_obj in shop_config_info:
            auth_info['ShopIP'] = shop_config_info_obj[0]
            k = shop_config_info_obj[2]
            v = shop_config_info_obj[3]
            auth_info[k] = v
        return auth_info


class GenerateFeedXml:
    def __init__(self, auth_info):
        self.auth_info = auth_info
        pass

    @staticmethod
    def generate_message_id():
        """
         生成唯一的messageid供feed使用

        """
        #message_id = uuid.uuid4()
        # message_id = 111111111111
        message_id = int(time.time() * 1000)
        return message_id

    def get_inventory_xml(self, product_sku_list, quantity):
        submit_data_inventory = '''<?xml version="1.0" encoding="utf-8" ?>
                      <AmazonEnvelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="amzn-envelope.xsd">
                              <Header>
                                <DocumentVersion>1.01</DocumentVersion>
                                <MerchantIdentifier>SellerId</MerchantIdentifier>
                              </Header>
                              <MessageType>Inventory</MessageType>
                              <PurgeAndReplace>false</PurgeAndReplace>
                              inventory_info_placeholder
                      </AmazonEnvelope>'''

        inventory_xml = '''
                   <Message>
                     <MessageID>feed_message_id</MessageID>
                     <OperationType>Update</OperationType>
                     <Inventory>
                       <SKU>product_sku</SKU>
                       <Quantity>product_quantity</Quantity>
                     </Inventory>
                   </Message>
                   '''
        inventory_xml_all = ''
        for product_sku in product_sku_list:
            time.sleep(0.001)
            message_id = self.generate_message_id()
            inventory_xml_tmp = inventory_xml.replace('feed_message_id', str(message_id))
            inventory_xml_tmp = inventory_xml_tmp.replace('product_sku', product_sku)
            inventory_xml_tmp = inventory_xml_tmp.replace('product_quantity', str(quantity))
            inventory_xml_all = inventory_xml_all + inventory_xml_tmp

        submit_data_inventory = submit_data_inventory.replace('SellerId', self.auth_info['SellerId'])
        submit_data_inventory = submit_data_inventory.replace('inventory_info_placeholder', inventory_xml_all)

        return submit_data_inventory

    def get_price_xml(self, sku, standard_price, currency_type='USD', start_date=None, end_date=None, sale_price=None):
        """
         时间格式：2018-02-06T08:00:00+00:00
        """
        submit_data_price = '''<?xml version="1.0" encoding="utf-8" ?>
        <AmazonEnvelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="amzn-envelope.xsd">
           <Header>
             <DocumentVersion>1.01</DocumentVersion>
             <MerchantIdentifier>SellerId</MerchantIdentifier>
           </Header>
           <MessageType>Price</MessageType>
           <Message>
             <MessageID>feed_message_id</MessageID>
               <Price>
                 <SKU>product_sku</SKU>
                 <StandardPrice currency="Currency_type">standard_price</StandardPrice>
                 sale_info_placeholder
           </Price>
          </Message>
        </AmazonEnvelope>'''

        message_id = self.generate_message_id()

        if sale_price is not None and str(sale_price).strip() != '':
            sale_info = ''' 
            <Sale>
               <StartDate>%s</StartDate>
               <EndDate>%s</EndDate>
               <SalePrice currency="Currency_type">%s</SalePrice>
             </Sale>
             ''' %(start_date, end_date, sale_price)
        else:
            sale_info = ''

        submit_data_price = submit_data_price.replace('SellerId', self.auth_info['SellerId'])
        submit_data_price = submit_data_price.replace('feed_message_id', str(message_id))
        submit_data_price = submit_data_price.replace('product_sku', sku)
        submit_data_price = submit_data_price.replace('sale_info_placeholder', sale_info)
        submit_data_price = submit_data_price.replace('Currency_type', currency_type)
        submit_data_price = submit_data_price.replace('standard_price', standard_price)

        return submit_data_price

    def get_price_xml_multi(self, sku_price_list, currency_type='USD'):
        doc = xml.dom.minidom.Document()
        AmazonEnvelope = doc.createElement('AmazonEnvelope')
        AmazonEnvelope.setAttribute('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")
        AmazonEnvelope.setAttribute('xsi:noNamespaceSchemaLocation', 'amzn-envelope.xsd')
        doc.appendChild(AmazonEnvelope)

        Header = doc.createElement('Header')
        DocumentVersion = doc.createElement('DocumentVersion')
        MerchantIdentifier = doc.createElement('MerchantIdentifier')
        DocumentVersion_text = doc.createTextNode('1.01')
        MerchantIdentifier_text = doc.createTextNode('%s' % self.auth_info['SellerId'])
        DocumentVersion.appendChild(DocumentVersion_text)
        MerchantIdentifier.appendChild(MerchantIdentifier_text)
        Header.appendChild(DocumentVersion)
        Header.appendChild(MerchantIdentifier)
        AmazonEnvelope.appendChild(Header)

        MessageType = doc.createElement('MessageType')
        MessageType_text = doc.createTextNode('Price')
        MessageType.appendChild(MessageType_text)
        AmazonEnvelope.appendChild(MessageType)

        # Message
        for sku_price in sku_price_list:
            for sku, price in sku_price.items():
                time.sleep(0.001)
                timeStamp = int(time.time() * 1000)

                Message = doc.createElement('Message')
                MessageID = doc.createElement('MessageID')
                MessageID_text = doc.createTextNode('%s' % timeStamp)
                MessageID.appendChild(MessageID_text)
                Message.appendChild(MessageID)
                Price = doc.createElement('Price')
                SKU = doc.createElement('SKU')
                SKU_text = doc.createTextNode(sku)
                SKU.appendChild(SKU_text)
                Price.appendChild(SKU)
                StandardPrice = doc.createElement('StandardPrice')
                StandardPrice.setAttribute('currency', currency_type)
                StandardPrice_text = doc.createTextNode(str(price))
                StandardPrice.appendChild(StandardPrice_text)
                Price.appendChild(StandardPrice)
                Message.appendChild(Price)
                AmazonEnvelope.appendChild(Message)

        feed = doc.toxml()
        return feed

    def get_product_xml(self, product_info_dic):
        submit_data_product = '''<?xml version="1.0" encoding="utf-8" ?>
            <AmazonEnvelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="amzn-envelope.xsd">
              <Header>
                <DocumentVersion>1.01</DocumentVersion>
                <MerchantIdentifier>SellerId</MerchantIdentifier>
              </Header>
              <MessageType>Product</MessageType>
              <PurgeAndReplace>false</PurgeAndReplace>
              <Message>
                <MessageID>message_id</MessageID>
                <OperationType>Update</OperationType>
                <Product>
                  <SKU>seller_sku</SKU>
                  <Condition><ConditionType>New</ConditionType></Condition>
                  <DescriptionData>
                          <Title>product_title</Title>
                          <Description>product_description</Description>
                          <BulletPoint>bullet_point1</BulletPoint>
                          <BulletPoint>bullet_point2</BulletPoint>
                          <BulletPoint>bullet_point3</BulletPoint>
                          <BulletPoint>bullet_point4</BulletPoint>
                          <BulletPoint>bullet_point5</BulletPoint>
                          <SearchTerms>generic_keywords1</SearchTerms>
                          <SearchTerms>generic_keywords2</SearchTerms>
                          <SearchTerms>generic_keywords3</SearchTerms>
                          <SearchTerms>generic_keywords4</SearchTerms>
                          <SearchTerms>generic_keywords5</SearchTerms>
                  </DescriptionData>
                    </Product>
              </Message>
             </AmazonEnvelope>'''
        message_id = self.generate_message_id()
        submit_data_product = submit_data_product.replace('SellerId', self.auth_info['SellerId'])
        submit_data_product = submit_data_product.replace('message_id', str(message_id))
        submit_data_product = submit_data_product.replace('seller_sku', product_info_dic['seller_sku'])
        submit_data_product = submit_data_product.replace('product_title', product_info_dic['item_name'])
        submit_data_product = submit_data_product.replace('product_description', product_info_dic['product_description'])
        submit_data_product = submit_data_product.replace('product_title', product_info_dic['item_name'])
        submit_data_product = submit_data_product.replace('bullet_point1', product_info_dic['bullet_point1'])
        submit_data_product = submit_data_product.replace('bullet_point2', product_info_dic['bullet_point2'])
        submit_data_product = submit_data_product.replace('bullet_point3', product_info_dic['bullet_point3'])
        submit_data_product = submit_data_product.replace('bullet_point4', product_info_dic['bullet_point4'])
        submit_data_product = submit_data_product.replace('bullet_point5', product_info_dic['bullet_point5'])
        submit_data_product = submit_data_product.replace('generic_keywords1', product_info_dic['generic_keywords1'])
        submit_data_product = submit_data_product.replace('generic_keywords2', product_info_dic['generic_keywords2'])
        submit_data_product = submit_data_product.replace('generic_keywords3', product_info_dic['generic_keywords3'])
        submit_data_product = submit_data_product.replace('generic_keywords4', product_info_dic['generic_keywords4'])
        submit_data_product = submit_data_product.replace('generic_keywords5', product_info_dic['generic_keywords5'])

        return submit_data_product

    def get_image_xml(self, auth_info_image):
        submit_data_image = '''<?xml version="1.0" encoding="utf-8" ?> 
        <AmazonEnvelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="amzn-envelope.xsd">
            <Header>
              <DocumentVersion>1.01</DocumentVersion> 
              <MerchantIdentifier>SellerId</MerchantIdentifier> 
            </Header>
              <MessageType>ProductImage</MessageType> 
            <Message>
              <MessageID>message_id</MessageID> 
              <OperationType>Update</OperationType> 
                <ProductImage>
                  <SKU>seller_sku</SKU> 
                  <ImageType>Main</ImageType> 
                  <ImageLocation>image_url</ImageLocation> 
              </ProductImage>
            </Message>
        </AmazonEnvelope>'''
        message_id = self.generate_message_id()
        submit_data_image = submit_data_image.replace('SellerId', self.auth_info['SellerId'])
        submit_data_image = submit_data_image.replace('message_id', str(message_id))
        submit_data_image = submit_data_image.replace('seller_sku', self.auth_info['seller_sku'])
        submit_data_image = submit_data_image.replace('image_url', auth_info_image['pic_url'])
        return submit_data_image


class MessageToRabbitMq:
    def __init__(self, auth_info, db_connection):
        self.auth_info = auth_info
        self.db_conn = db_connection

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

    def put_message(self, message_body):
        RABBIT_MQ = self.get_mq_info()
        credentials = pika.PlainCredentials(RABBIT_MQ['MQUser'], RABBIT_MQ['MQPassword'])
        parameters = pika.ConnectionParameters(RABBIT_MQ['hostname'], RABBIT_MQ['MQPort'], '/', credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        queue_name = str(self.auth_info['IP']) + '_amazon_upload_toy'
        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_publish(exchange='',
                              routing_key=queue_name,
                              body=message_body)


class AmazonAutoLoad:
    def __init__(self):
        # self.batch_id = str(uuid.uuid4())
        self.batch_id = '5a0cacaa-8604-478a-b624-94093e91183c'
        self.online_conn = pymysql.connect(user="by15161458383",
                                           passwd="K120Esc1",
                                           host="rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com",
                                           db="hq_db",
                                           port=3306,
                                           charset='utf8')
        self.rd_conn = redis.Redis(host='r-uf6206e9df36e854.redis.rds.aliyuncs.com',
                                   password='K120Esc1',
                                   port=6379,
                                   db=0)
        self.pipe = self.rd_conn.pipeline(transaction=False)

    def close_db_conn(self):
        try:
            if self.online_conn:
                self.online_conn.close()
        except Exception as ex:
            print ex

    def get_operate_records(self):
        record_sql_com = '''insert into t_amazon_auto_load
                                      (batch_id,
                                       shop_name,
                                       seller_sku,
                                       sku_type,
                                       sku,
                                       com_pro_sku,
                                       status,
                                       product_status_detail,
                                       product_sku_status)
                                      select "''' + self.batch_id + '''",
                                             f.shopname,
                                             seller_sku,
                                             2,
                                             sku,
                                             com_pro_sku,
                                             status,
                                             GROUP_CONCAT(product_sku_status_remark) product_status_detail,
                                             min(product_sku_status) product_sku_status
                                        from (select aa.*,
                                                     CONCAT(bb.sku, ':', bb.goodsstatus, ';') product_sku_status_remark,
                                                     CASE
                                                       when bb.goodsstatus is null or bb.goodsstatus = '清仓（合并）' THEN
                                                        -2
                                                       WHEN bb.goodsstatus IN ('正常', '在售') THEN
                                                        1
                                                       when bb.goodsstatus IN
                                                            ('临时下架', '停售', '暂停销售', '清仓') THEN
                                                        -1
                                                       when bb.goodsstatus IN ('售完下架', '处理库尾') THEN
                                                        0
                                                     END product_sku_status
                                                from (select ShopName,
                                                             seller_sku,
                                                             sku,
                                                             com_pro_sku,
                                                             substring_index(substring_index(substring_index(if(com_pro_sku is not null,
                                                                                                                com_pro_sku,
                                                                                                                sku),
                                                                                                             '+',
                                                                                                             b.help_topic_id),
                                                                                             '+',
                                                                                             -1),
                                                                             '*',
                                                                             1) product_sku,
                                                             a.status
                                                        from t_online_info_amazon a, t_amazon_help_topic b
                                                       where b.help_topic_id <=
                                                             (LENGTH(if(com_pro_sku is not null, com_pro_sku, sku)) -
                                                             length(replace(if(com_pro_sku is not null,
                                                                                com_pro_sku,
                                                                                sku),
                                                                             '+',
                                                                             '')) + 1)
                                                         and refresh_status = 0
                                                         and a.is_fba = 0
                                                         and a.shopname in (select ShopName from t_config_shop_alias where ShopStatus = 1)
                                                         and a.shopname = 'AMZ-0033-YJQ-US/PJ'
                                                         and a.status in ('Active', 'Inactive')
                                                         and (a.sku like 'ZH%' or a.sku like '%+%')
                                                         and b.help_topic_id > 0) aa
                                                left join py_db.b_goods bb
                                                  on aa.product_sku = bb.sku) f
                                       group by f.shopname, seller_sku, sku, com_pro_sku, status
                                      having(status = 'Active' and min(product_sku_status) in(0, -1)) or (status = 'Inactive' and min(product_sku_status) = 1) or min(product_sku_status) = -2;'''

        record_sql_single = '''insert into t_amazon_auto_load
                                      (batch_id,
                                       shop_name,
                                       seller_sku,
                                       sku_type,
                                       sku,
                                       com_pro_sku,
                                       status,
                                       product_status_detail,
                                       product_sku_status)
                                      SELECT "''' + self.batch_id + '''",
                                             a.shopname,
                                             a.seller_sku,
                                             1,
                                             a.sku,
                                             a.com_pro_sku,
                                             a.status,
                                             b.goodsstatus product_status_detail,
                                             CASE
                                               when b.goodsstatus is null or b.goodsstatus = '清仓（合并）' THEN
                                                -2
                                               WHEN b.goodsstatus IN ('正常', '在售') THEN
                                                1
                                               when b.goodsstatus IN ('临时下架', '停售', '暂停销售', '清仓') THEN
                                                -1
                                               when b.goodsstatus IN ('售完下架', '处理库尾') THEN
                                                0
                                             END product_sku_status
                                        FROM t_online_info_amazon a, py_db.b_goods b
                                       WHERE a.sku = b.sku
                                         and a.shopname in (select ShopName from t_config_shop_alias where ShopStatus = 1)
                                         and a.shopname = 'AMZ-0033-YJQ-US/PJ'
                                         and refresh_status = 0
                                         and a.is_fba = 0
                                         and a.STATUS IN ('Active', 'Inactive')
                                         and a.sku not like 'ZH%'
                                         and a.sku not like '%+%'
                                         and ((a.status = 'Active' and
                                             b.goodsstatus in ('临时下架',
                                                                 '停售',
                                                                 '售完下架',
                                                                 '处理库尾',
                                                                 '暂停销售',
                                                                 '清仓',
                                                                 '清仓（合并）')) or
                                             (a.status = 'Inactive' and b.goodsstatus in ('在售', '正常')));'''
        sql_upload = "update t_amazon_auto_load set deal_type = 'upload' where batch_id = '%s' and product_sku_status = 1" % self.batch_id
        sql_unload = "update t_amazon_auto_load set deal_type = 'unload' where batch_id = '%s' and product_sku_status = -1 or (product_sku_status = 0 and quantity = 0);" % self.batch_id
        sql_remind = "update t_amazon_auto_load set deal_type = 'remind' where batch_id = '%s' and product_sku_status = -2;" % self.batch_id

        with self.online_conn.cursor() as cursor:
            # char_set = chardet.detect(record_sql_com)['encoding']
            # print char_set
            # record_sql_com = record_sql_com.decode(char_set).encode('utf-8')
            # print record_sql_com
            cursor.execute(record_sql_com)
            cursor.execute(record_sql_single)
            cursor.execute(sql_upload)
            cursor.execute(sql_unload)
            cursor.execute(sql_remind)
            self.online_conn.commit()

    def get_com_sku_quantity(self, com_sku):
        sku_list = com_sku.split('+')

        cnt = 0
        for sku in sku_list:
            print sku.split("*")[0]
            self.pipe.hget(sku.split("*")[0], 'Number')
            self.pipe.hget(sku.split("*")[0], 'ReservationNum')
            cnt += 1
        quantity_result = self.pipe.execute()
        quantity_list = []
        for i in range(cnt):
            quantity_list.append((int(quantity_result[i * 2]) if quantity_result[i * 2] else 0) - (int(quantity_result[i * 2 + 1]) if quantity_result[i * 2 + 1] else 0))

        return min(quantity_list)

    def get_product_sku_quantity(self):
        sql_quantity = "select id, sku, com_pro_sku from t_amazon_auto_load where product_sku_status = 0 and batch_id = '%s'" % self.batch_id
        sql_update = "update t_amazon_auto_load set quantity = %s where id = %s"
        update_list = list()
        with self.online_conn.cursor() as cursor:
            cursor.execute(sql_quantity)
            quantity_obj = cursor.fetchall()
            quantity_record_list = list()
            for obj in quantity_obj:
                quantity_record_list.append((obj[0], obj[1], obj[2]))
                self.pipe.hget(obj[1], 'Number')
                self.pipe.hget(obj[1], 'ReservationNum')
            print quantity_record_list
            quantity_result = self.pipe.execute()

            for ind, id_sku in enumerate(quantity_record_list):
                if id_sku[2]:
                    quantity = self.get_com_sku_quantity(id_sku[2])
                elif id_sku[1] and '+' in id_sku[1]:
                    quantity = self.get_com_sku_quantity(id_sku[1])
                else:
                    quantity = (int(quantity_result[ind * 2]) if quantity_result[ind * 2] else 0) - (int(quantity_result[ind * 2 + 1]) if quantity_result[ind * 2 + 1] else 0)
                update_list.append((quantity, id_sku[0]))
            print update_list
            cursor.executemany(sql_update, update_list)
            self.online_conn.commit()

    def deal_feed_record(self):
        sql_upload = "select shop_name,seller_sku from t_amazon_auto_load where deal_type = 'unload' and batch_id = '%s' and 1=2" % self.batch_id
        sql_unload = "select shop_name,seller_sku from t_amazon_auto_load where  deal_type = 'unload' and deal_result is null and deal_user != 'wuchongxiang' and batch_id = '%s'" % self.batch_id
        print sql_unload

        with self.online_conn.cursor() as cursor_upload:
            cursor_upload.execute(sql_upload)
            print cursor_upload.rowcount
            if cursor_upload.rowcount > 0:
                upload_records = cursor_upload.fetchall()
            else:
                upload_records = None
        self.get_feed_xml(upload_records, 'auto_load_product')

        with self.online_conn.cursor() as cursor_unload:
            cursor_unload.execute(sql_unload)
            print cursor_unload.rowcount
            if cursor_unload.rowcount > 0:
                unload_records = cursor_unload.fetchall()
            else:
                unload_records = None
        self.get_feed_xml(unload_records, 'auto_unload_product')

    def get_feed_xml(self, record_obj, load_type):
        shop_sku = dict()
        if record_obj:
            for record in record_obj:
                shop_name = record[0]
                seller_sku = record[1]
                if shop_name not in shop_sku:
                    shop_sku[shop_name] = [seller_sku]
                else:
                    shop_sku[shop_name].append(seller_sku)

            for key, value in shop_sku.items():
                get_auth_info_ins = GetAuthInfo(self.online_conn)
                auth_info = get_auth_info_ins.get_auth_info_by_shop_name(str(key))
                auth_info['IP'] = auth_info['ShopIP']
                auth_info['table_name'] = 't_online_info_amazon'
                auth_info['update_type'] = load_type
                auth_info['product_list'] = value
                auth_info['batch_id'] = self.batch_id

                if load_type == 'auto_load_product':
                    feed_xml_ins = GenerateFeedXml(auth_info)
                    feed_xml = feed_xml_ins.get_inventory_xml(value, 999)
                elif load_type == 'auto_unload_product':
                    feed_xml_ins = GenerateFeedXml(auth_info)
                    feed_xml = feed_xml_ins.get_inventory_xml(value, 0)
                else:
                    feed_xml = None
                auth_info['feed_xml'] = feed_xml
                print auth_info
                self.put_message_to_mq(auth_info)

    def put_message_to_mq(self, auth_info):
        message_to_rabbit_obj = MessageToRabbitMq(auth_info, self.online_conn)
        auth_info = json.dumps(auth_info)
        message_to_rabbit_obj.put_message(auth_info)

    def auto_start(self):
        self.get_operate_records()
        self.get_product_sku_quantity()
        self.deal_feed_record()


auto_load_obj = AmazonAutoLoad()
print datetime.datetime.now()
auto_load_obj.deal_feed_record()
auto_load_obj.close_db_conn()
print datetime.datetime.now()

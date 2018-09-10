# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: auto_upgrade_refresh.py
 @time: 2018-05-02 17:11
"""  

import oss2
import pika
import pymysql as MySQLdb


ACCESS_KEY_ID = 'LTAIH6IHuMj6Fq2h'
ACCESS_KEY_SECRET = 'N5eWsbw8qBkMfPREkgF2JnTsDASelM'
ENDPOINT_OUT = 'oss-cn-shanghai.aliyuncs.com'
BUCKETNAME_APIVERSION = 'fancyqube-apiversion'


def put_file(oss_file_name, local_file):
    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, ENDPOINT_OUT, BUCKETNAME_APIVERSION)
    bucket.put_object_from_file(oss_file_name, local_file)

# auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
# bucket = oss2.Bucket(auth, ENDPOINT_OUT, BUCKETNAME_APIVERSION)
# bucket.delete_object('fba_refresh-20180906.exe')

class MessageToRabbitMq:
    def __init__(self, db_connection):
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

    def construct_queue_name(self, ip):
        queue_name = 'amazon_' + ip + '_refresh_product_data'  # + str(self.auth_info['ShopName'])
        print 'queue_name is:%s' % queue_name
        return queue_name

    def put_message(self, ip, message_body):
        RABBIT_MQ = self.get_mq_info()
        credentials = pika.PlainCredentials(RABBIT_MQ['MQUser'], RABBIT_MQ['MQPassword'])
        parameters = pika.ConnectionParameters(RABBIT_MQ['hostname'], RABBIT_MQ['MQPort'], '/', credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        queue_name = self.construct_queue_name(ip)
        channel.queue_declare(queue=queue_name)
        channel.basic_publish(exchange='',
                              routing_key=queue_name,
                              body=message_body)

#
# DATABASES = {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'hq_db',
#         'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
#         'PORT': '3306',
#         'USER': 'by15161458383',
#         'PASSWORD': 'K120Esc1'
#             }
#
# ip_list = ['123.57.63.178']


put_file('fba_refresh-20180906a.exe', 'D:\\fba_refresh-20180906a.exe')


# cnxn = MySQLdb.connect(DATABASES['HOST'],DATABASES['USER'],DATABASES['PASSWORD'],DATABASES['NAME'] )
#
# put_message_obj = MessageToRabbitMq(cnxn)
# for ip in ip_list:
#     put_message_obj.put_message(ip, 'auto_upgrade')
#     print '%s auto upgrade message send OK' % ip
# cnxn.close()


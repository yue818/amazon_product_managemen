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
# bucket.delete_object('fba_refresh-20181129a.exe')

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
        queue_name =  ip + '_amazon_upload_toy'  # + str(self.auth_info['ShopName'])
        print 'queue_name is:%s' % queue_name
        return queue_name

    def put_message(self, ip, message_body):
        RABBIT_MQ = self.get_mq_info()
        credentials = pika.PlainCredentials(RABBIT_MQ['MQUser'], RABBIT_MQ['MQPassword'])
        parameters = pika.ConnectionParameters(RABBIT_MQ['hostname'], RABBIT_MQ['MQPort'], '/', credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        queue_name = self.construct_queue_name(ip)
        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_publish(exchange='',
                              routing_key=queue_name,
                              body=message_body)


# DATABASES = {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'hq_db',
#         'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
#         'PORT': '3306',
#         'USER': 'by15161458383',
#         'PASSWORD': 'K120Esc1'
#             }

ip_list = [
'123.57.63.178',
'120.25.161.53',
'120.25.250.235',
'120.25.219.73',
'182.92.70.68',
'121.40.205.92',
'121.43.113.40',
'121.40.106.183',
'123.57.12.60',
'121.199.73.100',
'120.25.124.222',
'120.24.4.219',
'115.159.58.25',
'139.196.27.109',
'121.40.78.237',
'121.199.34.252',
'182.92.66.164',
'120.26.117.203',
'123.207.137.23',
'120.25.172.219',
'114.215.138.107',
'139.196.182.150',
'139.196.180.248',
'123.206.33.96',
'118.89.143.150',
'139.199.162.251',
'123.206.180.50',
'123.206.82.134',
'101.200.76.183',
'123.57.152.243',
'115.28.224.127',
'101.200.136.7',
'118.89.148.166',
'101.200.147.150',
'120.26.207.178',
'120.26.239.49',
'139.196.6.73',
'120.26.241.64',
'112.74.88.69',
'121.41.84.99',
'123.57.206.223',
'139.196.50.143',
'101.200.165.145',
'120.26.199.138',
'139.224.72.107',
'121.41.36.137',
'112.74.205.97',
'139.196.37.27',
'139.129.53.33',
'123.57.137.82',
'120.76.122.51',
'120.24.190.175',
'120.25.235.160',
'101.200.166.190',
'120.24.44.4',
'115.28.233.29',
'120.25.196.3',
'121.41.91.86',
'115.28.149.34',
'120.27.93.217',
'121.43.109.32',
'123.206.94.219',
'118.89.104.191',
'123.206.33.237',
'118.89.244.56',
'139.199.39.221',
'123.207.241.27',
'123.207.235.212',
'123.207.175.230',
'123.207.248.204',
'119.29.175.24',
'118.89.160.203',
'123.206.96.194',
'115.159.213.24',
'115.159.83.93',
'119.29.239.34',
'123.207.252.46',
'123.206.104.230',
'119.29.37.31',
'182.254.247.185',
'123.206.238.111',
'118.89.152.151',
'123.206.208.72',
'123.207.173.162',
'118.89.152.183',
'118.89.17.122',
'123.207.152.32',
'123.206.33.246',
'123.206.228.39',
'139.199.30.51',
'115.159.40.187',
'123.207.8.225',
'115.159.76.185',
'182.254.210.201',
'123.207.159.11',
'123.206.216.81',
'123.206.86.18',
'139.199.24.172',
'123.207.45.143',
'139.199.210.86',
'120.25.120.195',
'118.89.157.227',
'123.206.13.65',
'119.29.234.173',
'119.29.179.99',
'115.159.124.158',
'123.206.46.168',
'139.196.5.231',
'139.199.193.193',
'123.207.159.63',
'118.89.140.74',
'123.206.14.69',
'123.207.181.186',
'123.206.202.191',
'182.92.192.177',
'123.206.23.20',
'119.29.156.65',
'115.159.106.162',
'120.55.127.56',
'139.196.34.111',
'120.24.67.170',
'123.207.141.53',
'182.254.159.176',
'139.199.123.109',
'120.24.203.44',
'139.196.187.233',
'101.200.224.121',
'119.29.158.131',
'120.24.182.39',
'120.77.234.116',
'119.29.185.184',
'115.29.213.5',
'182.254.219.114',
'106.14.97.20',
'120.79.99.118',
'115.159.218.174',
'106.3.143.140',
'119.23.154.96',
'120.55.76.63',
'119.23.146.160',
'101.132.251.238',
'106.3.143.184',
'120.24.45.108',
'123.56.132.64',
'115.159.113.146',
'121.199.12.215',
'118.31.249.132',
'121.43.48.187',
'120.27.251.70',
'121.199.18.164',
'47.96.251.1',
'121.199.10.148',
'121.199.3.227',
'121.199.71.223']


put_file('fba_refresh-20181129a.exe', 'D:\\fba_refresh-20181129a.exe')


# cnxn = MySQLdb.connect(DATABASES['HOST'],DATABASES['USER'],DATABASES['PASSWORD'],DATABASES['NAME'] )
#
# put_message_obj = MessageToRabbitMq(cnxn)
# for ip in ip_list:
#     put_message_obj.put_message(ip, 'auto_upgrade')
#     print '%s auto upgrade message send OK' % ip
# cnxn.close()


# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: auto_upgrade.py
 @time: 2018-04-18 16:31
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
# bucket.delete_object('fba_refresh-20181017a.exe')


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
        queue_name = ip + '_amazon_upload_toy'  # + str(self.auth_info['ShopName'])
        print 'queue_name is:%s' % queue_name
        return queue_name

    def put_message(self, ip, message_body):
        RABBIT_MQ = self.get_mq_info()
        credentials = pika.PlainCredentials(RABBIT_MQ['MQUser'], RABBIT_MQ['MQPassword'])
        parameters = pika.ConnectionParameters(RABBIT_MQ['hostname'], RABBIT_MQ['MQPort'], '/', credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        queue_name = self.construct_queue_name(ip)
        channel.queue_declare(queue=queue_name, durable='True')
        channel.basic_publish(exchange='',
                              routing_key=queue_name,
                              body=message_body)


DATABASES = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hq_db',
        'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
        'PORT': '3306',
        'USER': 'by15161458383',
        'PASSWORD': 'K120Esc1'
            }

ip_list = ['118.89.143.150']

fba_config = {
'AMZ-0001':'123.57.63.178',
'AMZ-0003':'120.25.161.53',
'AMZ-0004':'120.25.250.235',
'AMZ-0005':'120.25.219.73',
'AMZ-0006':'182.92.70.68',
'AMZ-0010':'121.40.205.92',
'AMZ-0011':'121.43.113.40',
'AMZ-0013':'121.40.106.183',
'AMZ-0017':'123.57.12.60',
'AMZ-0022':'121.199.73.100',
'AMZ-0023':'120.25.124.222',
'AMZ-0025':'120.24.4.219',
'AMZ-0026':'115.159.58.25',
'AMZ-0028':'139.196.27.109',
'AMZ-0029':'121.40.78.237',
'AMZ-0031':'121.199.34.252',
'AMZ-0033':'182.92.66.164',
'AMZ-0034':'120.26.117.203',
'AMZ-0042':'123.207.137.23',
'AMZ-0043':'120.25.172.219',
'AMZ-0045':'114.215.138.107',
'AMZ-0048':'139.196.182.150',
'AMZ-0049':'139.196.180.248',
'AMZ-0051':'123.206.33.96',
'AMZ-0052':'118.89.143.150',
'AMZ-0053':'139.199.162.251',
'AMZ-0054':'123.206.180.50',
'AMZ-0055':'123.206.82.134',
'AMZ-0056':'101.200.76.183',
'AMZ-0058':'123.57.152.243',
'AMZ-0059':'115.28.224.127',
'AMZ-0061':'101.200.136.7',
'AMZ-0062':'118.89.148.166',
'AMZ-0063':'101.200.147.150',
'AMZ-0064':'120.26.207.178',
'AMZ-0066':'120.26.239.49',
'AMZ-0069':'139.196.6.73',
'AMZ-0070':'120.26.241.64',
'AMZ-0071':'112.74.88.69',
'AMZ-0075':'121.41.84.99',
'AMZ-0076':'123.57.206.223',
'AMZ-0077':'139.196.50.143',
'AMZ-0078':'101.200.165.145',
'AMZ-0079':'120.26.199.138',
'AMZ-0080':'139.224.72.107',
'AMZ-0081':'121.41.36.137',
'AMZ-0082':'112.74.205.97',
'AMZ-0083':'139.196.37.27',
'AMZ-0084':'139.129.53.33',
'AMZ-0086':'123.57.137.82',
'AMZ-0087':'120.76.122.51',
'AMZ-0090':'120.24.190.175',
'AMZ-0091':'120.25.235.160',
'AMZ-0092':'101.200.166.190',
'AMZ-0094':'120.24.44.4',
'AMZ-0095':'115.28.233.29',
'AMZ-0096':'120.25.196.3',
'AMZ-0097':'121.41.91.86',
'AMZ-0098':'115.28.149.34',
'AMZ-0099':'120.27.93.217',
'AMZ-0100':'121.43.109.32',
'AMZ-0104':'123.206.94.219',
'AMZ-0105':'118.89.104.191',
'AMZ-0113':'123.206.33.237',
'AMZ-0128':'118.89.244.56',
'AMZ-0129':'139.199.39.221',
'AMZ-0133':'123.207.241.27',
'AMZ-0135':'123.207.235.212',
'AMZ-0139':'123.207.175.230',
'AMZ-0140':'123.207.248.204',
'AMZ-0141':'119.29.175.24',
'AMZ-0142':'118.89.160.203',
'AMZ-0143':'123.206.96.194',
'AMZ-0144':'115.159.213.24',
'AMZ-0145':'115.159.83.93',
'AMZ-0147':'119.29.239.34',
'AMZ-0148':'123.207.252.46',
'AMZ-0149':'123.206.104.230',
'AMZ-0150':'119.29.37.31',
'AMZ-0152':'182.254.247.185',
'AMZ-0153':'123.206.238.111',
'AMZ-0154':'118.89.152.151',
'AMZ-0155':'123.206.208.72',
'AMZ-0156':'123.207.173.162',
'AMZ-0157':'118.89.152.183',
'AMZ-0158':'118.89.17.122',
'AMZ-0159':'123.207.152.32',
'AMZ-0161':'123.206.33.246',
'AMZ-0162':'123.206.228.39',
'AMZ-0163':'139.199.30.51',
'AMZ-0165':'115.159.40.187',
'AMZ-0166':'123.207.8.225',
'AMZ-0167':'115.159.76.185',
'AMZ-0168':'182.254.210.201',
'AMZ-0169':'123.207.159.11',
'AMZ-0170':'123.206.216.81',
'AMZ-0171':'123.206.86.18',
'AMZ-0173':'139.199.24.172',
'AMZ-0181':'139.199.210.86',
'AMZ-0182':'120.25.120.195',
'AMZ-0183':'118.89.157.227',
'AMZ-0185':'123.206.13.65',
'AMZ-0186':'119.29.234.173',
'AMZ-0187':'119.29.179.99',
'AMZ-0188':'115.159.124.158',
'AMZ-0190':'123.206.46.168',
'AMZ-0191':'139.196.5.231',
'AMZ-0192':'139.199.193.193',
'AMZ-0194':'123.207.159.63',
'AMZ-0195':'118.89.140.74',
'AMZ-0196':'123.206.14.69',
'AMZ-0197':'123.207.181.186',
'AMZ-0198':'123.206.202.191',
'AMZ-0199':'182.92.192.177',
'AMZ-0200':'123.206.23.20',
'AMZ-0203':'119.29.156.65',
'AMZ-0204':'115.159.106.162',
'AMZ-0205':'120.55.127.56',
'AMZ-0206':'139.196.34.111',
'AMZ-0207':'120.24.67.170',
'AMZ-0208':'123.207.141.53',
'AMZ-0209':'182.254.159.176',
'AMZ-0210':'139.199.123.109',
'AMZ-0211':'120.24.203.44',
'AMZ-0213':'139.196.187.233',
'AMZ-0216':'101.200.224.121',
'AMZ-0217':'119.29.158.131',
'AMZ-0218':'120.24.182.39',
'AMZ-0219':'120.77.234.116',
'AMZ-0222':'119.29.185.184',
'AMZ-0223':'115.29.213.5',
'AMZ-0224':'182.254.219.114',
'AMZ-0225':'106.14.97.20',
'AMZ-0226':'120.79.99.118',
'AMZ-0227':'115.159.218.174',
'AMZ-0228':'106.3.143.140',
'AMZ-0229':'119.23.154.96',
'AMZ-0230':'120.55.76.63',
'AMZ-0231':'119.23.146.160',
'AMZ-0232':'101.132.251.238',
'AMZ-0233':'106.3.143.184',
}

# put_file('amazon_upload_product-20180912.exe','D:\\amazon_upload_product-20180912.exe')
put_file('fba_refresh-20181017a.exe','D:\\fba_refresh-20181017a.exe')

# cnxn = MySQLdb.connect(DATABASES['HOST'],DATABASES['USER'],DATABASES['PASSWORD'],DATABASES['NAME'] )
# put_message_obj = MessageToRabbitMq(cnxn)
# for key in sorted(fba_config.keys()):
#     put_message_obj.put_message(fba_config[key], 'auto_upgrade')
#     print '%s auto upgrade message send OK' % key
# cnxn.close()
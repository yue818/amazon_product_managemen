import pika
import pymysql as MySQLdb
import time

try:
    credentials = pika.PlainCredentials('admin', 'admin')
    parameters = pika.ConnectionParameters('106.14.125.45', '5672', '/', credentials, socket_timeout=999999)
    connection = pika.BlockingConnection(parameters)
    print 'connect rabbitmq ok'
except Exception as e:
    print 'can not  connect rabbitmq'
    print e

DATABASES = {
    'NAME': 'hq_db',
    'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
    'PORT': '3306',
    'USER': 'by15161458383',
    'PASSWORD': 'K120Esc1'
}

try:
    db_conn = MySQLdb.connect(DATABASES['HOST'], DATABASES['USER'], DATABASES['PASSWORD'], DATABASES['NAME'])
    print 'connect db ok'
    db_conn.close()
except Exception as e:
    print 'can not connect db'
    print e

time.sleep(10)

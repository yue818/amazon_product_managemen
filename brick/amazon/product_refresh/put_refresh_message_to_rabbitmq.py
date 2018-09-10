# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: put_refresh_message_to_rabbitmq.py
 @time: 2018-02-12 10:23
"""  
import pika

# RABBIT_MQ = {
#             'hostname': '106.14.125.45',
#             'port': 5672,
#             'username': 'admin',
#             'password': 'admin'}


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

    def construct_queue_name(self):
        queue_name = 'amazon_' + str(self.auth_info['ShopIP']) + '_refresh_product_data'  # + str(self.auth_info['ShopName'])
        return queue_name

    def put_message(self, message_body):
        RABBIT_MQ = self.get_mq_info()
        credentials = pika.PlainCredentials(RABBIT_MQ['MQUser'], RABBIT_MQ['MQPassword'])
        parameters = pika.ConnectionParameters(RABBIT_MQ['hostname'], RABBIT_MQ['MQPort'], '/', credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        queue_name = self.construct_queue_name()
        channel.queue_declare(queue=queue_name)
        channel.basic_publish(exchange='',
                              routing_key=queue_name,
                              body=message_body)


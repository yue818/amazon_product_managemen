#-*-coding:utf-8-*-
import pika
import json
from skuapp.table.t_config_mq_info import t_config_mq_info

class Send_to_MQ():
    # RABBITMQ = {
    #     'hostname': '192.168.105.38',
    #     'port': 5672,
    #     # 'username': 'admin',
    #     # 'password': 'admin',
    #     'username': 'guest',
    #     'password': 'guest',
    # }

    #
    # '''
    # [
    #     {'IP': u'106.14.125.45', 'K': u'MQPort', 'V': u'5672'},
    #     {'IP': u'106.14.125.45', 'K': u'MQUser', 'V': u'admin'},
    #     {'IP': u'106.14.125.45', 'K': u'MQPassword', 'V': u'admin'}
    # ]
    # '''

    def __init__(self):
        t_config_mq_info_objs = t_config_mq_info.objects.filter(Name='Ebay-RabbitMQ-Server').values('IP', 'K', 'V')
        RABBITMQ = {}
        for t_config_mq_info_obj in t_config_mq_info_objs:
            RABBITMQ['IP'] = t_config_mq_info_obj['IP']
            RABBITMQ[t_config_mq_info_obj['K']] = t_config_mq_info_obj['V']
        #新建连接，rabbitmq安装在本地则hostname为'localhost'
        credentials = pika.PlainCredentials(RABBITMQ['MQUser'], RABBITMQ['MQPassword'])
        self.parameters = pika.ConnectionParameters(RABBITMQ['IP'], RABBITMQ['MQPort'], '/', credentials)
        # 创建通道

    def ebay_to_MQ(self,params):

        #result = {'params': params, 'result': ''}
        connection = pika.BlockingConnection(self.parameters)
        channel = connection.channel()
        '''往队列里发送数据'''
        print params
        if params.get('ebay_publish_product'):
            if params['body']:
                body = json.dumps(params['body'])
                channel.queue_declare(queue='ebay_publish_product')
                channel.basic_publish(exchange='',
                                           routing_key=params['ebay_publish_product'],
                                           body=body)
            else:
                pass
        elif params.get('upload_ebayapp_products'):  # 刊登
            if params['body']:
                body = json.dumps(params['body'])
                channel.queue_declare(queue='upload_ebayapp_products')
                channel.basic_publish(exchange='',
                                      routing_key=params['upload_ebayapp_products'],
                                      body=body)
        elif params.get('relist_end_item_ebayapp'): # 上下架
            if params['body']:
                body = json.dumps(params['body'])
                channel.queue_declare(queue='relist_end_item_ebayapp')
                channel.basic_publish(exchange='',
                                      routing_key=params['relist_end_item_ebayapp'],
                                      body=body)
        elif params.get('refresh_syn_ebayapp_shopdata'): # 全量同步
            if params['body']:
                body = json.dumps(params['body'])
                channel.queue_declare(queue='refresh_syn_ebayapp_shopdata')
                channel.basic_publish(exchange='',
                                      routing_key=params['refresh_syn_ebayapp_shopdata'],
                                      body=body)
        connection.close()






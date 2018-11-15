# -*- coding: utf-8 -*-

from brick.db.dbconnect import execute_db
import pika
import uuid


class Rabbit_MQ_Server():

    def __init__(self, db_conn=None, RABBITMQ=None):
        self.cnxn = db_conn
        self.response = None
        self.corr_id = None
        self.credentials = pika.PlainCredentials(RABBITMQ['username'], RABBITMQ['password'])
        self.parameters = pika.ConnectionParameters(RABBITMQ['hostname'],
                                                    RABBITMQ['port'], '/', self.credentials,
                                                    blocked_connection_timeout=0,
                                                    heartbeat=0, socket_timeout=3600)
        self.connection = pika.BlockingConnection(self.parameters)
        # 创建通道
        self.channel = None

    def get_rabbitmq_info(self, Name, PlatformName):
        sql = "SELECT IP, K, V FROM t_config_mq_info WHERE Name='%s' AND PlatformName='%s';" % (Name, PlatformName)
        res = execute_db(sql, self.cnxn, 'select')
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
        return RABBITMQ

    def Send_Mess_To_MQ(self, body, queue):
        # 创建通道
        self.channel = self.connection.channel()
        # 声明一个队列，生产者和消费者都要声明一个相同的队列，用来防止万一某一方挂了，另一方能正常运行
        self.channel.queue_declare(queue=queue, durable=True)
        self.channel.basic_publish(exchange='',
                                   routing_key=queue,
                                   body=body,
                                   properties=pika.BasicProperties(delivery_mode=2,)
                                   )
        print " [x] Sent %s" % body
        self.channel.close()
        # self.connection.close()

    def Send_Mess_To_MQ_With_Callback(self, body, queue):
        # 接收消息
        def on_response(ch, method, props, body):
            # 服务端回应的correlation_id等于请求的id 接收数据
            ch.basic_ack(delivery_tag=method.delivery_tag)
            if self.corr_id == props.correlation_id:
                self.response = body

        # 生成corr_id
        self.corr_id = str(uuid.uuid4())

        # 创建通道
        self.channel = self.connection.channel()
        # 定义专用队列，队列名随机，断开连接时删除队列
        self.channel.queue_declare(queue=queue, durable=True)
        # 接收服务端回应的callback_queue
        self.channel.basic_consume(on_response, no_ack=False,
                                   queue=queue)

        # 发起请求
        self.channel.basic_publish(exchange='',
                                   routing_key=queue,  # 发送至rpc_queue队列
                                   properties=pika.BasicProperties(reply_to=queue,  # 回调队列 #告诉服务端从这个队列回应请求
                                                                   correlation_id=self.corr_id,  # 请求关联corr_id
                                                                   delivery_mode=2,),
                                   body=str(body))  # 消息
        print " [x] Sent %s" % body
        # 监听回应消息
        while self.response is None:
            self.connection.process_data_events()
        # return int(response)
        # self.connection.close()
        print '===========', self.response
        self.channel.close()
        return self.response

    def close_channel(self):
        self.channel.close()

    def close_connection(self):
        self.connection.close()

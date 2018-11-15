#-*-coding:utf-8-*-
import pika
import uuid
import traceback
"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: schedule_to_MQ.py
 @time: 2017/12/22 13:50
"""
class schedule_to_MQ():
    def __init__(self, hostname, portValue, username, pwd):
        user_pwd = pika.PlainCredentials(username, pwd)
        self.parameters = pika.ConnectionParameters(hostname, portValue, "/", user_pwd)
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()

    def on_response(self, ch, method, props, body):
        '''获取命令执行结果的回调函数'''
        # print("验证码核对",self.callback_id,props.correlation_id)
        if self.callback_id == props.correlation_id:  # 验证码核对
            self.response = body
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def get_response_test(self, params):
        result = {'errorcode': 0, 'errortext': '', 'params': params, 'result': ''}
        '''取队列里的值，获取callback_queued的执行结果'''
        # print result
        self.callback_id = params['callback_id']
        self.response = None
        self.channel.basic_consume(self.on_response,  # 只要收到消息就执行on_response
                                   queue=params['callback_queue'])
        self.connection.process_data_events(time_limit=1)
        # while self.response is None:
        #     print '1111111111111'
        #     self.connection.process_data_events()  # 非阻塞版的start_consuming
        result['result'] = {'resultIfo': self.response}
        return result

    def xml_to_MQ(self, params):
        result = {'errorcode': 0, 'errortext': '', 'params': params, 'result': ''}
        '''队列里发送数据'''
        try:
            if params['queueName']:
                if params['body']:
                    result_data = self.channel.queue_declare(exclusive=False,durable=True)  # exclusive=False 必须这样写
                    self.callback_queue = result_data.method.queue
                    self.corr_id = str(uuid.uuid4())
                    # print(self.corr_id)
                    resultIfo = self.channel.basic_publish(exchange='',
                                               routing_key=params['queueName'],
                                               properties=pika.BasicProperties(
                                                   reply_to=self.callback_queue,  # 发送返回信息的队列name
                                                   correlation_id=self.corr_id,  # 发送uuid 相当于验证码
                                                   delivery_mode=2,
                                               ),
                                               body=params['body'])
                    result['result'] = {'resultIfo': resultIfo, 'callback_queue': self.callback_queue, 'callback_id': self.corr_id}
                else:
                    result['errorcode'] = -1
                    result['errortext'] = 'body is null'
            else:
                result['errorcode'] = -1
                result['errortext'] = 'queueName is null'
        except Exception,ex:
            result['errorcode'] = -1
            result['errortext'] = traceback.format_exc()
        return result

    def close_connection(self):
        self.connection.close()
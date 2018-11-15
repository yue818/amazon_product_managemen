#-*-coding:utf-8-*-


"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: py_redis_ali_sku.py
 @time: 2018/6/25 13:47
"""   
from django_redis import get_redis_connection
import json

class py_redis_ali_sku(object):
    def __init__(self):
        self.redis_conn=get_redis_connection("aliexpress_online_info")

    def __private_hset_attr(self,name,data):
        for key,value in data.items():
            if isinstance(value,dict):
                value=json.dumps(value)
            self.redis_conn.hset(name, key,value)

    def __private_hget_attr(self,name,key):
        if self.redis_conn is not None:
            _result=self.redis_conn.hget(name,key)
            try:
                result=json.loads(_result)
            except ValueError:
                return _result
            return result

    def __private_hgetall(self,name):
        return self.redis_conn.hgetall(name)

    def get_data(self,name,key):
        return self.__private_hget_attr(name,key)

    def set_data(self,name,data):
        if isinstance(data,dict):
            return self.__private_hset_attr(name,data)
        raise TypeError('{} must dict'.format(data))

    def hgetall_data(self,name):
        return self.__private_hgetall(name)
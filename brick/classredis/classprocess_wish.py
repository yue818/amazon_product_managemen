#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: classprocess_wish.py
 @time: 2018-05-02 15:06
"""

class classprocess_wish():
    def __init__(self,redisconn = None):
        self.redis_conn = redisconn

    def __private_set_attr(self,name,key,value):
        if self.redis_conn is not None and value is not None:
            return self.redis_conn.hset(name, key,value)

    def __private_get_attr(self,name,key):
        if self.redis_conn is not None:
            return self.redis_conn.hget(name,key)

    def __private_del_attr(self, name):
        if self.redis_conn is not None:
            return self.redis_conn.delete(name)

    def setProcess(self,Name,Key,Val):
        self.__private_set_attr(Name,Key,Val)

    def getProcess(self,Name,Key):
        return self.__private_get_attr(Name,Key)

    def delProcess(self,Name):
        self.__private_del_attr(Name)

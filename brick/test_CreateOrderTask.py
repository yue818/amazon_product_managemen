# -*- coding: utf-8 -*-
from db import dbconnect
from wish import CreateOrderTask

from wish import ShopOnlineInfo

import redis
#这里替换为连接的实例host和port
host = 'r-uf6206e9df36e854.redis.rds.aliyuncs.com'
port = 6379
#这里替换为实例password
pwd = 'K120Esc1'
redis_conn = redis.StrictRedis(host=host, port=port, password=pwd)


params ={}

#连接数据库
result = dbconnect.run(params)

print result


CreateOrderTask_obj = CreateOrderTask.CreateOrderTask(result['db_conn'])

#CreateOnlineinfoTask_obj.CreateTasks()

OneCmdRecoreDict_list = CreateOrderTask_obj.GetTasksV2()

for OneCmdRecoreDict in OneCmdRecoreDict_list:
    print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++OneCmdRecoreDict =%s'%OneCmdRecoreDict
    ShopOnlineInfo.F_EXE_SHOP_ONLINE_INFO.delay(result['db_conn'],redis_conn,OneCmdRecoreDict)

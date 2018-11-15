# -*- coding: utf-8 -*-
from db import dbconnect
from table import b_goodsskulinkshop
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


b_goodsskulinkshop_obj = b_goodsskulinkshop.b_goodsskulinkshop(result['db_conn'],redis_conn)

sku = b_goodsskulinkshop_obj.get_sku_by_shopsku('VFAMNJK8952')
print 'sku=%s' % sku


sku = b_goodsskulinkshop_obj.get_sku_by_shopsku('QTLVKRT6575')
print 'sku=%s' % sku

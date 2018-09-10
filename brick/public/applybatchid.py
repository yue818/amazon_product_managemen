# -*- coding: utf-8 -*-
import datetime
import random
def getbatchid():
    #生成随机标记
    batch_id = '%s.%s'%(datetime.datetime.now(),random.randint(10000, 90000))
    print 'batch_id= %s'%batch_id
    return batchid

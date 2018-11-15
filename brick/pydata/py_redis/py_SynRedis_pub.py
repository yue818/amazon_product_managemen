# coding: utf-8
"""
@author: wangzy
@contact: 15205512335
@site:
@software: PyCharm
@file: py_SynRedis_pub.py
@time: 2018-01-23 15:21
"""

import sys
from datetime import datetime
from redis import Redis
from array import array


#.8 redis连接
from django_redis import get_redis_connection
import os
sys.path.append('/data/djangostack-1.9.7/apps/django/django_projects/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Project.settings')
connRedis = get_redis_connection(alias='product')

'''
#测试环境
connRedis = Redis(host='192.168.105.223', port=6379,db=0)
'''

class py_SynRedis_pub():
    ################################list结构存入redis#################################
    '''单条SUK+list入redis
    参数：sSUK redis唯一字段
          sValue  sSUK 对应redis list值
    返回值：1 成功入redis   -1 其他错误   -2 异常抛出
    '''
    def setToListRedis(self,sSUK,sArray):
        try:
            if connRedis.llen(sSUK) > 0:
               connRedis.delete(sSUK) #删除指定SKU列表
            #判断是否存在指定的SKU
            nLen = len(sArray)
            for i in range(0,nLen):
                connRedis.rpush(sSUK, sArray[i]) #push到redis列表
            return 1
        except Exception as e:
            print('filename={},line={},insert {} redis error:{}'.format(__file__, sys._getframe().f_lineno, sSUK,e.message))
            return -2

    '''单个SUK从redis获取值
    参数：sSUK redis唯一字段
          nIndex 默认-1 返回sSUK对应列所有值
                 非-1 返回sSUK对应index-1列值
    返回值：SUK对应的值   
            -1 其他错误   
            -2 异常抛出
    '''
    def getFromListRedis(self,sSUK,nIndex):
        try:
            if nIndex != -1:
                nLen =  connRedis.llen(sSUK)
                if nLen < nIndex:
                    print('filename={},line={},input index={} not in SUK={}}'.format(__file__, sys._getframe().f_lineno,nIndex, sSUK))
                else:
                    return connRedis.lindex(sSUK,nIndex-1)
            else:
                return connRedis.lrange(sSUK, 0, -1)
        except Exception as e:
            print('filename={},line={},get {}{} redis error:{}}'.format(__file__, sys._getframe().f_lineno,sSUK,nIndex, e.message))

    '''单个SUK从redis删除
       参数：sSUK redis唯一字段
       返回值：1 成功删除指定的SUK在redis存储   -1 找不到指定的SUK索引值   -2异常抛出
    '''
    def delFromListRedis(self, sSUK):
        try:
            if connRedis.llen(sSUK) > 0:
                connRedis.delete(sSUK)  # 删除指定SKU列表
                return 1
            else:
                print('filename={},line={},redis not exist SUK={}}'.format(__file__, sys._getframe().f_lineno, sSUK))
                return -1
        except Exception as e:
            print('filename={},line={},redis delete SUK={} error:{}}'.format(__file__, sys._getframe().f_lineno,sSUK,e.message))
            return  -2

    '''以数组传送多条记录入redis
        参数：sSUK redis唯一字段
              sValue  sSUK 对应redis list值
        返回值：1 成功入redis   -1 找不到指定的key索引值   -2异常抛出
    '''
    def setArrayToListRedis(self, nArray, sTableName,nKeyIndex):
        try:
            nCol = len(nArray[0])
            nRow = len(nArray)
            if nKeyIndex > nCol:
                print('filename={},line={},key={} not exist'.format(__file__, sys._getframe().f_lineno, nKeyIndex))
                return -1
            for i in range(0,nRow):
                sKey = nArray[i][nKeyIndex-1] #查找指定的key值
                sSUK = sTableName + '_' + str(sKey) #拼接SUK
                #self.setToListRedis(sSUK,','.join(str(j) for j in nArray[i]))
                self.setToListRedis(sSUK, nArray[i])
            return  1
        except Exception as e:
            print('filename={},line={}, insert redis error:{}'.format(__file__, sys._getframe().f_lineno, e.message))
            return -2

    '''以数组传送多条记录入redis
            参数：sSUK redis唯一字段
                  sValue  sSUK 对应redis list值
            返回值：批量获取记录   -1 找不到指定的key索引值   -2异常抛出
    '''
    def getArrayToListRedis(self, sArray):
        try:
            nCol = len(sArray)
            sArrayList = []
            for i in range(0,nCol):
                #print('filename={},line={},SUK={}'.format(__file__,sys._getframe().f_lineno ,sSUK))
                sArrayList.append(self.getFromListRedis(sArray[i],-1))
            return sArrayList
        except Exception as e:
            print('filename={},line={},gets redis error：{}'.format(__file__, sys._getframe().f_lineno, e.message))
            return -2

    '''单个SUK从redis删除
           参数：sSUK redis唯一字段
           返回值：1 成功删除指定的SUK在redis存储   -1 找不到指定的SUK索引值   -2异常抛出
    '''

    ################################hash结构存入redis#################################
    '''说明：针对从表里面获取的二维数组进行，并从二维数组获取key
            单条记录以hash入redis
            参数：nNameLoc key值索引
                 nKeyLoc name值索引
                 sArray 入redis值 一维数组
            返回值：1 成功入redis   -1 其他错误   -2 异常抛出
    '''
    def setToHashRedis(self,sTableName,nKeyLoc,nNameLoc ,sArray):
        try:
            nCol = len(sArray)
            if nKeyLoc > nCol or nNameLoc > nCol:
                print('filename={},line={},nKeyLoc={} or nNameLoc={} not exist'.format(__file__, sys._getframe().f_lineno, nKeyLoc,nNameLoc))
                return -1
            # 判断当前name+key值是否存在,存在则删除再insert  hset 可不删除，直接覆盖原有的内容
            sSuk = sTableName + '_' + str(sArray[nKeyLoc - 1])
            if connRedis.hexists(sSuk, sArray[nNameLoc - 1]):
                connRedis.hdel(sSuk, sArray[nNameLoc - 1])
            connRedis.hset(sSuk, sArray[nNameLoc-1], sArray)  # push到redis列表
            return 1
        except Exception as e:
            print('filename={},line={},insert hash in redis error：{}'.format(__file__, sys._getframe().f_lineno, e.message))
            return -2

    '''
    说明：key、name、value 都提供情况，直接插入redis
    参数：
        sTableName：key值
        sName:属性值
        sValue:值
    返回值：1成功   -2处理异常
    '''
    def setToValuesHashRedis(self,sTableName,sName,sValue):
        try:
            # 判断当前name+key值是否存在,存在则删除再insert  hset 可不删除，直接覆盖原有的内容
            sSuk = sTableName
            #if connRedis.hexists(sSuk, sName):
            #   connRedis.hdel(sSuk, sName)
            connRedis.hset(sSuk, sName, sValue)  # push到redis列表
            return 1
        except Exception as e:
            print('filename={},line={},insert hash in redis error：{}'.format(__file__, sys._getframe().f_lineno, e.message))
            return -2


    '''多个条记录以hash入redis
            参数：nNameLoc key值索引
                 nKeyLoc name值索引
                 sArray 按一维数组形式insert redis
            返回值：1 成功入redis   -1 其他错误   -2 异常抛出
    '''
    def setArrayToHashRedis(self, sTableName,nKeyLoc,nNameLoc, sArray):
        try:
            if len(sArray) == 0:
                return 1
            nCol = len(sArray[0])
            nRow = len(sArray)
            if nKeyLoc > nCol or nNameLoc > nCol:
                print('filename={},line={},nKeyLoc={} or nNameLoc={} not exist：{}'.format(__file__, sys._getframe().f_lineno,nKeyLoc, nNameLoc))
                return -1
            for i in range(0, nRow):
                self.setToHashRedis(sTableName,nKeyLoc,nNameLoc,sArray[i])
            return 1
        except Exception as e:
            print('filename={},line={},insert hash in redis error：{}'.format(__file__, sys._getframe().f_lineno, e.message))
            return -2


    '''多个条记录以hash入redis
                参数：nNameLoc key值索引
                     nKeyLoc name值索引
                     sArray 按一维数组形式insert redis
                返回值：1 成功入redis   -1 其他错误   -2 异常抛出
        '''

    def setArrayArgsToHashRedis(self, sTableName, nKeyLoc, sArray, sArgs):
        try:
            if len(sArray) == 0:
                return 1
            nCol = len(sArray[0])
            nRow = len(sArray)
            for sRowArgs in sArgs:
                for sRow in sArray:
                    sSuk = ''
                    if len(sTableName) == 0:
                        sSuk = str(sRow[nKeyLoc - 1])
                    else:
                        if type(nKeyLoc) is type(1):
                            sSuk = sTableName + '_' + str(sRow[nKeyLoc - 1])
                        else:
                            sSuk = sTableName + '_' + str(nKeyLoc)
                    #print('{},{}'.format(sRowArgs[0],sRowArgs[1]))
                    if  type(sRowArgs[0]) is type(1):
                        if connRedis.hexists(sSuk, sRow[sRowArgs[0]-1]):
                            connRedis.hdel(sSuk, sRow[sRowArgs[0]-1])
                        if type(sRowArgs[1]) is type(1):
                            connRedis.hset(sSuk, sRow[sRowArgs[0]-1], sRow[sRowArgs[1]-1])  # push到redis列表
                        else:
                            connRedis.hset(sSuk, sRow[sRowArgs[0] - 1], sRowArgs[1])  # push到redis列表
                    else:
                        if connRedis.hexists(sSuk, sRowArgs[0]):
                            connRedis.hdel(sSuk, sRowArgs[0])
                        if type(sRowArgs[1]) is type(1):
                            connRedis.hset(sSuk, sRowArgs[0], sRow[sRowArgs[1] - 1])  # push到redis列表
                        else:
                            connRedis.hset(sSuk, sRowArgs[0], sRowArgs[1])  # push到redis列表
            return 1
        except Exception as e:
            print('filename={},line={},insert hash in redis error：{}'.format(__file__, sys._getframe().f_lineno,
                                                                             e.message))
            return -2

    '''根据sKey获取所有sName下的sValue值（比如一个商品SUK在不同区域sName存货量）
                参数：sKey（SUK） Redis中hash的name值,可以为空值
                返回值：获取sKey对应所有记录   -1 其他错误   -2 异常抛出
    '''
    def getAllFromHashRedis(self,sTableName, sKey):
        try:
            sSuk = ''
            if sTableName == '':
                sSuk = sKey
            else:
                if sKey == '':
                    sSuk = sTableName
                else:
                    sSuk = sTableName + '_' + str(sKey)
            if connRedis.hlen(sSuk) > 0:
                mName = connRedis.hkeys(sSuk)
                sArray = []
                for sName in mName:
                    strInfo = connRedis.hget(sSuk, sName)
                    strList = []
                    if strInfo[0] == "(" and strInfo[-1] == ")":
                        strList = (strInfo[1:-1]).replace('Decimal', '').replace('u', '').replace(', (', ', ').replace('), ', ',').replace('\'', '').replace(', ', ',').split(',')
                    else:
                        strList = connRedis.hget(sSuk, sName).split('#@#@#@#')
                    sArray.append(strList)
                return sArray
            else:
                return -1
        except Exception as e:
            print('filename={},line={},get redis error：{}'.format(__file__, sys._getframe().f_lineno, e.message))
            return -2

    '''根据sKey+sName 获取sValue值
            参数：sSUK redis唯一字段
                  sValue  sSUK 对应redis list值
            返回值：1 成功入redis   -1 其他错误   -2 异常抛出
    '''
    def getFromHashRedis(self,sTableName, sKey, sName):
        try:
            sSuk = ''
            if len(sTableName) == 0:
                sSuk = str(sKey)
            else:
                if len(sKey) == 0:
                    sSuk = sTableName
                else:
                    sSuk = sTableName + '_' + str(sKey)

            if connRedis.hexists(sSuk,sName):
                strInfo = connRedis.hget(sSuk, sName)
                if len(strInfo) == 0:
                    return []
                strList = []
                if len(str(strInfo)) != 0 and strInfo[0] == "(" and strInfo[-1] == ")":
                    strList = (strInfo[1:-1]).replace('Decimal', '').replace('u', '').replace(', (', ', ').replace('), ', ',').replace('\'', '').replace(', ', ',').split(',')
                elif len(str(strInfo)) != 0 and (strInfo[0] == "(" or strInfo[0] == "["):
                    strList = eval(strInfo)
                else:
                    # 返回单个字段不需要转原有类型envl
                    strList =connRedis.hget(sSuk, sName)
                return strList
            else:
                return -1
        except Exception as e:
            print('filename={},line={},get redis error：{}'.format(__file__, sys._getframe().f_lineno, e.message))
            return -2

    '''根据sKey获取所有sName下的sValue值（比如一个商品SUK在不同区域sName存货量）
                    参数：sKey（SUK） Redis中hash的name值
                    返回值：获取sKey对应所有记录   -1 其他错误   -2 异常抛出
    '''
    def getKeysFromHashRedis(self, sTableName, sKey):
        try:
            sSuk = ''
            if len(sKey) == 0:
                sSuk = sTableName
            else:
                sSuk = sTableName + '_' + str(sKey)
            if connRedis.hlen(sSuk) > 0:
                mName = connRedis.hkeys(sSuk)
                return mName
        except Exception as e:
            print('filename={},line={},get redis error：{}'.format(__file__, sys._getframe().f_lineno, e.message))
            return -2

    '''根据一组sKey+sName 获取一组sValue值
                参数：数组 二维数组（表名+key一行数据）
                      sValue  sSUK 对应redis list值
                返回值：返回批量查询结果（以二维数组形式返回）   -1 其他错误   -2 异常抛出
    '''
    def getBatchFromHashRedis(self, sArray):
        try:
            nRow = len(sArray)
            mArray = []
            for i in range(0,nRow):
                sSuk = sArray[i][0] + '_' + sArray[i][1]
                if len(sArray[i]) == 1:
                    sSuk = sArray[i][0]
                mName = connRedis.hkeys(sSuk)
                for sName in mName:
                    strList = []
                    strInfo = connRedis.hget(sSuk, sName)
                    if strInfo[0] == "(" and strInfo[-1] == ")":
                        strList = (strInfo[1:-1]).replace('Decimal','').replace('u\'','').replace(', (',', ').replace('), ',', ').replace('\'','').replace(', ',',').split(',')
                    else:
                        strList = eval(connRedis.hget(sSuk, sName))
                    mArray.append(strList)
            return mArray
        except Exception as e:
            print('filename={},line={},get redis error：{}'.format(__file__, sys._getframe().f_lineno, e.message))
            return -2
    '''
    说明：获取所有key值
    '''
    def getAllHashKeys(self,patternName):
        return connRedis.keys(patternName)

    '''
    删除匹配模式的key值
    '''
    def DelHashKeys(self,patternName):
        if len(patternName) > 0:
            strDelPattern = patternName + '*'
            delListKeys = connRedis.keys(strDelPattern)
            #print('{},{}'.format(strDelPattern,delListKeys))
            if len(delListKeys) > 0:
                connRedis.delete(*delListKeys)
                #print('delListKeys={}'.format(delListKeys))
        '''
        for sKey in delListKeys:
            if connRedis.exists(sKey):
                hashkey_all = connRedis.hkeys(sKey)
                for i in range(len(hashkey_all)):
                    connRedis.hdel(sKey, hashkey_all[i])
        '''


    '''
    获取匹配patternName数量
    '''
    def GteHashKeysCount(self,patternName):
        try:
            strDelPattern = patternName + '*'
            ListKeys = connRedis.keys(strDelPattern)
            return len(ListKeys)
        except Exception as e:
            print('filename={},line={},get redis error：{}'.format(__file__, sys._getframe().f_lineno, e.message))
            return -2

'''
测试用例
'''


'''
#hash 测试多维插入和获取
tt = py_SynRedis_pub()
nKeyLoc = 1
nNameLoc = 2
sArray = [[347518, 347054, u'TOY3694R', None, None, None, u'\u521b\u610f\u513f\u7ae5\u5361\u901a\u52a8\u7269\u53d1\u6761\u5c0f\u6c7d\u8f66\u73a9\u5177-\u968f\u673a', 575354, u'', 2, None, 2, 2, 2, 44.0, 2.25, 0.00, 2, 2, u'\u6b63\u5e38', '2017-01-24', None, None, None, None, None], [347518, 324355, u'W6179NB-S', None, None, None, u'\u65b0\u6b3e\u9ad8\u9152\u676f\u60c5\u5973\u5f69\u8272\u5370\u82b1\u536b\u8863-\u6df1\u84dd\u8272', 592, u'', 0, None, 0, 0, 0, 280.0, '19.00' ,'0.00', 0, 0, u'\u6b63\u5e38', '2018-01-24', None, None, None, None, None], [324820, 324356, u'W6179NB-XL', None, None, None, u'\u65b0\u6b3e\u9ad8\u9152\u676f\u60c5\u5973\u5f69\u8272\u5370\u82b1\u536b\u8863-\u6df1\u84dd\u8272', 592, u'', 0, None, 0, 0, 0, 310.0,'19.00', '0.00', 0, 0, u'\u6b63\u5e38', '2017-09-11', None, None, None, None, None]]
sArray1 = [2252757, 702296, 247197, 246744, '10.0000', '2.9000', '0.0000', '2.9000', '0.0000', '29.0000', '29.0000', u'', '10.0000', u'', u'', u'', '2.9000', '2.9000', u'', u'', u'']
sArray2=[['t_goods','347518'],['t_orders','347518']]

tt.setToHashRedis('cg_StockOrderD',nKeyLoc,nNameLoc,sArray1)
tt.setArrayToHashRedis('t_goods',nKeyLoc,nNameLoc,sArray)
tt.setArrayToHashRedis('t_orders',nKeyLoc,nNameLoc,sArray)
##tt.setToHashRedis(nNameLoc,nKeyLoc,sArray)
print tt.getFromHashRedis('t_goods','347518','347054')[6]
print tt.getAllFromHashRedis('t_goods','347518')
print tt.getBatchFromHashRedis(sArray2)


tt = py_SynRedis_pub()
tt.DelHashKeys('CG_StockOrderD')
'''



'''
#由单个SUK和对应值入redis测试
sSUK = "test6"
sValue = [1,2,3,,4,5,,,,7,12,13434]
tt.setToListRedis(sSUK,sValue)
testData = tt.getFromListRedis(sSUK,nIndex=-1)
print(testData)
tt.delFromListRedis(sSUK)
testData = tt.getFromListRedis(sSUK,nIndex=-1)
print(testData)

#由多个SUK和对应值入redis测试
sArray = [[1,'sss',3,5],[33,2,3,11],['ttttt',15,16,17],[1456,'wangzy',5444,6788],[555,666,777,'wwwww']]
tt.setArrayToListRedis(sArray,'t_goods',2)

sArray = ['t_goods_2','t_goods_wangzy','t_goods_666']
sArrayInfo = tt.getArrayToListRedis(sArray)
print  sArrayInfo
'''




'''
###连接池
#host = '192.168.105.223'
#port = 6379
#POOL = redis.ConnectionPool(host=host, port=port, db=0)
#my_server = redis.Redis(connection_pool=POOL)

nLen = connRedis.llen(self.sSUK)  #获取指定SKU下面list长度
keys = connRedis.keys()  #获取所有keys
connRedis.dbsize()
print 'dbsize: %s' %  # 查看当前数据库大小
print 'ping %s' % connRedis.ping() # ping查询
'''
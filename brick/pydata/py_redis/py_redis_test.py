from py_SynRedis_pub import py_SynRedis_pub
py_p = py_SynRedis_pub()
from redis import Redis
connRedis = Redis(host='192.168.105.223', port=6379,db=0)
import MySQLdb

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hq',
        'HOST': '192.168.105.111',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'root123'
    },
    'syn': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'py_db',
        'HOST': '192.168.105.111',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'root123',
    }
}
db_conn = MySQLdb.Connect(DATABASES['default']['HOST'], DATABASES['default']['USER'], DATABASES['default']['PASSWORD'],
                          DATABASES['syn']['NAME'], charset='utf8')


def setArrayToRedis( nArray, sTableName, nKeyIndex):
    try:
        nCol = len(nArray[0])
        nRow = len(nArray)
        print nCol, nRow
        if nKeyIndex > nCol:
            return -1

        for i in range(0, nRow):
            sKey = nArray[i][nKeyIndex - 1]
            sSUK = sTableName + '_' + str(sKey)
            print sSUK
            for j in range(0,nCol):
                connRedis.rpush(sSUK,nArray[i][j] )
        return 1
    except Exception as e:
        print('filename={},line={},{}'.format(__file__, sys._getframe().f_lineno, e.message))
        return -2



sqlcursor = db_conn.cursor()
selectsql = "select NID,GoodsID,SKU,property1,property2,property3,SKUName,LocationID," \
            "BmpFileName,SellCount,Remark,SellCount1,SellCount2,SellCount3,Weight,CostPrice,RetailPrice," \
            "MaxNum,MinNum,GoodsSKUStatus,ChangeStatusTime,ASINN,UPC,ModelNum,ChangeCostTime,linkurl " \
            "from b_goodssku limit 10"
sqlcursor.execute(selectsql)
objs = []
objs = sqlcursor.fetchall()
sqlcursor.close()
db_conn.close();

py_p.setArrayToListRedis(objs,'b_goodssku',3)


value = py_p.getArrayToListRedis_1('b_goodssku_NL-0192-MC,b_goodssku_MU-112-Random')

print value
print value [0]
print value [0][0]
print value [0][6]
print value [0][20]

print value [1]

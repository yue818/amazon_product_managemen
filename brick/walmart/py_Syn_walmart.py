#-*-coding:utf-8-*-

import redis
import pymysql
import time

sql_select = u"select id, productsku from t_online_info_walmart; "
sql_update = u"""INSERT INTO t_online_info_walmart(id,UseNumber,SaleDay,pyStatus,Orders7Days,refreshPYtime)
    VALUES %s
    ON DUPLICATE KEY 
    UPDATE UseNumber=VALUES(UseNumber),
    SaleDay=VALUES(SaleDay),
    pyStatus=VALUES(pyStatus),
    Orders7Days=VALUES(Orders7Days),
    refreshPYtime=VALUES(refreshPYtime);"""


def p_update_Syn_Walmart_TortInfo(onlineConn):
    print "[start] p_update_Syn_Walmart_TortInfo"
    result = {'code': 0, 'data': ''}
    try:
        cursor = onlineConn.cursor()
        fn_sql = "CALL p_update_Syn_Walmart_TortInfo()"
        cursor.execute(fn_sql)
        onlineConn.commit()
        cursor.close()
        print "[end] p_update_Syn_Walmart_TortInfo success"
    except Exception, ex:
        result['code'] = -1
        result['data'] = str(repr(ex))
        print "[end] p_update_Syn_Walmart_TortInfo except"
    return result

def format_v(data):
    t = data[1:-1]
    t = t.replace("u'", "'")
    t = t.replace("None", "Null")
    return t


def py_Syn_walmart_main():
    print "[start] main :::"
    onlineConn = pymysql.connect(user="by15161458383", passwd="K120Esc1",
                                 host="rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com",
                                 db="hq_db", port=3306,charset='utf8')

    rdConn = redis.Redis(host='r-uf6206e9df36e854.redis.rds.aliyuncs.com',
                         password='K120Esc1',port=6379, db=0)

    oncursor = onlineConn.cursor()
    rdpipe = rdConn.pipeline(transaction=False)

    p_update_Syn_Walmart_TortInfo(onlineConn=onlineConn)  # 先更新mainsku, productsku 和侵权状态
    oncursor.execute(sql_select)

    if oncursor.rowcount > 0:
        wal_data = []

        ids = []
        objs = oncursor.fetchall()
        for obj in objs:
            ids.append((obj[0],obj[1]))  # id  sku
            rdpipe.hget(obj[1], 'Number')
            rdpipe.hget(obj[1], 'ReservationNum')
            rdpipe.hget(obj[1], 'CanSaleDay')
            rdpipe.hget(obj[1], 'GoodsStatus')
            rdpipe.hget(obj[1], 'UpdateTime')
            rdpipe.hget(obj[1], 'WalMart-0001-VideoGames@#@'+str(obj[1]))
        result = rdpipe.execute()

        for i,dad in enumerate(ids):
            usenumber = (int(result[i * 6]) if result[i * 6] else 0) - (int(result[i * 6 + 1]) if result[i * 6 + 1] else 0)
            saleday = result[i * 6 + 2]
            GoodsStatus = result[i * 6 + 3]
            updateTime = result[i * 6 + 4] if result[i * 6 + 4] else time.strftime("%Y-%m-%d %X")
            Orders7Days = result[i * 6 + 5]

            wal_data.append((dad[0],usenumber,saleday,GoodsStatus,Orders7Days,updateTime,))

        data_str = format_v(str(wal_data))
        oncursor.execute(sql_update % (data_str,))

        onlineConn.commit()

    oncursor.close()
    onlineConn.close()
    print "[end] main :::"



# if __name__ == '__main__':
#     py_Syn_walmart_main()





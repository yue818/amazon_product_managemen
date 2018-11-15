#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_wish_store_oplogs.py
 @time: 2018-05-07 10:45
"""

from django_redis import get_redis_connection
r = get_redis_connection(alias='schedule')


class t_operation_log_online_syn_py():
    def __init__(self,DBConn):
        self.DBConn = DBConn

    def createLog(self,param):
        u'''
        :param param:
        param['OpNum']:操作编号
        param['OpType']:操作类型
        param['OpKey']:操作记录关键字
        param['Status']:操作状态
        param['ErrorInfo']:错误信息
        param['OpPerson']:操作人
        param['OpTime']:操作时间
        param['OpStartTime']:操作开始时间
        param['OpEndTime']:操作结束时间
        param['aNum']:操作总数量
        param['rNum']:操作成功数量
        param['eNum']:操作失败数量
        :return:
        0:插入成功
        -1:插入异常
        '''
        try:
            cursor = self.DBConn.cursor()
            sql = "insert into t_operation_log_online_syn_py (OpNum,OpType,OpKey,Status,ErrorInfo,OpPerson," \
                  "OpTime,OpStartTime,OpEndTime,aNum,rNum,eNum) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"

            parameter = []
            for productid in param['OpKey']:
                parameter.append((
                    param['OpNum'],param['OpType'],productid,param['Status'],param['ErrorInfo'],param['OpPerson'],
                    param['OpTime'], param['OpStartTime'], param['OpEndTime'], param['aNum'], param['rNum'],param['eNum']
                ))
            cursor.executemany(sql,parameter)
            cursor.execute("commit;")
            cursor.close()
            return {'errorcode':0,'errortext':''}
        except Exception,e:
            return {'errorcode':-1,'errortext':'%s:%s' % (Exception,e)}

    def deleteLog(self,opnum):
        try:
            cursor = self.DBConn.cursor()
            cursor.execute("delete from t_operation_log_online_syn_py WHERE OpNum=%s;",(opnum,))
            cursor.execute("commit;")
            cursor.close()
            return {'errorcode':0,'errortext':''}
        except Exception,e:
            return {'errorcode':-1,'errortext':'%s:%s' % (Exception,e)}

    def update_error(self,opnum,elogs):
        try:
            cursor = self.DBConn.cursor()
            cursor.execute("update t_operation_log_online_syn_py set Status='error',ErrorInfo=%s WHERE OpNum=%s;",(elogs, opnum,))
            cursor.execute("commit;")
            cursor.close()
            return {'errorcode':0,'errortext':''}
        except Exception,e:
            return {'errorcode':-1,'errortext':'%s:%s' % (Exception,e)}

    def update_success(self,opnum,elogs,rNum,eNum):
        try:
            cursor = self.DBConn.cursor()
            cursor.execute("update t_operation_log_online_syn_py set Status='over',ErrorInfo=%s,rNum=%s,eNum=%s WHERE OpNum=%s;",(elogs, rNum,eNum,opnum,))
            cursor.execute("commit;")
            cursor.close()
            return {'errorcode':0,'errortext':''}
        except Exception,e:
            return {'errorcode':-1,'errortext':'%s:%s' % (Exception,e)}


    def updateStatusP(self,opnum,opkey,status,elogs=''):
        try:
            cursor = self.DBConn.cursor()
            cursor.execute(
                "update t_operation_log_online_syn_py set Status=%s,ErrorInfo=%s WHERE OpNum=%s and OpKey=%s;",
                (status,elogs,opnum,opkey)
            )

            if status == 'over':
                cursor.execute("update t_operation_log_online_syn_py set rNum=rNum+1,OpEndTime=now() WHERE OpNum=%s;", (opnum,))
            if status == 'error':
                cursor.execute("update t_operation_log_online_syn_py set eNum=eNum+1,OpEndTime=now() WHERE OpNum=%s;", (opnum,))

            cursor.execute("commit;")
            cursor.close()
            return {'errorcode':0,'errortext':''}
        except Exception,e:
            return {'errorcode':-1,'errortext':'%s:%s' % (Exception,e)}

    def selectLogs(self,opnum):
        try:
            cursor = self.DBConn.cursor()
            cursor.execute(
                "select OpNum,OpType,OpKey,Status,ErrorInfo,OpPerson,OpTime,OpStartTime,OpEndTime,aNum,rNum,eNum "
                "from t_operation_log_online_syn_py WHERE OpNum=%s AND `Status`='error';", (opnum,)
            )
            error_objs = cursor.fetchall()
            if error_objs:
                opobjs = error_objs
            else:
                cursor.execute(
                    "select OpNum,OpType,OpKey,Status,ErrorInfo,OpPerson,OpTime,OpStartTime,OpEndTime,aNum,rNum,eNum "
                    "from t_operation_log_online_syn_py WHERE OpNum=%s limit 1;",(opnum,)
                )
                opobjs = cursor.fetchall()
            cursor.close()
            return {'errorcode': 0, 'errortext': '','OpLogs':opobjs}
        except Exception, e:
            return {'errorcode': -1, 'errortext': '%s:%s' % (Exception, e)}

    def DoneOrNot(self,opnum):
        try:
            cursor = self.DBConn.cursor()
            cursor.execute("select count(*) from t_operation_log_online_syn_py WHERE OpNum=%s and Status='runing';",(opnum,))
            count = cursor.fetchone()
            cursor.close()
            return {'errorcode': 0, 'errortext': '','count':count[0]}
        except Exception, e:
            return {'errorcode': -1, 'errortext': '%s:%s' % (Exception, e)}


    def selectLogsByIDError(self,opkey):
        try:
            cursor = self.DBConn.cursor()
            cursor.execute(
                "select OpNum,OpType,OpKey,Status,ErrorInfo,OpPerson,OpTime,OpStartTime,OpEndTime,aNum,rNum,eNum "
                "from t_operation_log_online_syn_py WHERE OpKey=%s and Status='error';",(opkey,)
            )
            opobjs = cursor.fetchall()
            cursor.close()
            einfor = []
            for opinfo in opobjs:
                einfor.append(u'%s'%opinfo[4])  # 错误信息
            return {'errorcode': 0, 'errortext': '','einfors':set(einfor)}
        except Exception, e:
            return {'errorcode': -1, 'errortext': '%s:%s' % (Exception, e)}


    def update_sku(self, opnum, sku, main_sku):
        try:
            cursor = self.DBConn.cursor()
            cursor.execute("update t_operation_log_online_syn_py set SKU=%s WHERE OpNum=%s AND OpKey=%s;",(sku, opnum, main_sku))
            cursor.execute("commit;")
            cursor.close()
            return {'errorcode':0,'errortext':''}
        except Exception,e:
            return {'errorcode':-1,'errortext':'%s:%s' % (Exception,e)}


    def search_banding_schedule(self, opnum):
        StartTime = r.hget(opnum, 'StartTime')
        EndTime = r.hget(opnum, 'EndTime')
        aNum = r.hget(opnum, 'aNum')
        rNum = r.hget(opnum, 'rNum')
        eNum = r.hget(opnum, 'eNum')
        etype = r.hget(opnum, 'etype')
        downinfo = r.hget(opnum, 'downinfo')
        endFlag = r.hget(opnum, 'endFlag')
        result = {
            'StartTime': StartTime, 'EndTime': EndTime, 'aNum': aNum, 'rNum': rNum, 'eNum': eNum,
            'etype': etype, 'downinfo': downinfo, 'endFlag': endFlag
        }
        return result


    def update_banding_schedue(self, opnum, start_time, end_time, aNum, rNum, eNum, endFlag=0 ):
        r.hset(opnum, 'StartTime', start_time)
        r.hset(opnum, 'EndTime', end_time)
        r.hset(opnum, 'aNum', aNum)
        r.hset(opnum, 'rNum', rNum)
        r.hset(opnum, 'eNum', eNum)
        r.hset(opnum, 'etype', 'add_binding')
        r.hset(opnum, 'downinfo', '')
        r.hset(opnum, 'endFlag', endFlag)



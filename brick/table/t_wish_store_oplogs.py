#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_wish_store_oplogs.py
 @time: 2018-05-07 10:45
"""

class t_wish_store_oplogs():
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
            sql = "insert into t_wish_store_oplogs (OpNum,OpType,OpKey,Status,ErrorInfo,OpPerson," \
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
            cursor.execute("delete from t_wish_store_oplogs WHERE OpNum=%s;",(opnum,))
            cursor.execute("commit;")
            cursor.close()
            return {'errorcode':0,'errortext':''}
        except Exception,e:
            return {'errorcode':-1,'errortext':'%s:%s' % (Exception,e)}

    def update_error(self,opnum,elogs):
        try:
            cursor = self.DBConn.cursor()
            cursor.execute("update t_wish_store_oplogs set Status='error',ErrorInfo=%s WHERE OpNum=%s;",(elogs, opnum,))
            cursor.execute("commit;")
            cursor.close()
            return {'errorcode':0,'errortext':''}
        except Exception,e:
            return {'errorcode':-1,'errortext':'%s:%s' % (Exception,e)}


    def updateStatusP(self,opnum,opkey,status,elogs=''):
        try:
            cursor = self.DBConn.cursor()
            cursor.execute(
                "update t_wish_store_oplogs set Status=%s,ErrorInfo=%s WHERE OpNum=%s and OpKey=%s;",
                (status,elogs,opnum,opkey)
            )

            if status == 'over':
                cursor.execute("update t_wish_store_oplogs set rNum=rNum+1,OpEndTime=now() WHERE OpNum=%s;", (opnum,))
            if status == 'error':
                cursor.execute("update t_wish_store_oplogs set eNum=eNum+1,OpEndTime=now() WHERE OpNum=%s;", (opnum,))

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
                "from t_wish_store_oplogs WHERE OpNum=%s ;",(opnum,)
            )
            opobjs = cursor.fetchall()
            cursor.close()
            return {'errorcode': 0, 'errortext': '','OpLogs':opobjs}
        except Exception, e:
            return {'errorcode': -1, 'errortext': '%s:%s' % (Exception, e)}

    def DoneOrNot(self,opnum):
        try:
            cursor = self.DBConn.cursor()
            cursor.execute("select count(*) from t_wish_store_oplogs WHERE OpNum=%s and Status='runing';",(opnum,))
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
                "from t_wish_store_oplogs WHERE OpKey=%s and Status='error' ORDER by id DESC limit 1;",(opkey,)
            )
            opobjs = cursor.fetchall()
            cursor.close()
            einfor = []
            for opinfo in opobjs:
                einfor.append((u'%s'%opinfo[4]).replace('<','&lt;').replace('>','&gt;'))  # 错误信息
            return {'errorcode': 0, 'errortext': '','einfors':set(einfor)}
        except Exception, e:
            return {'errorcode': -1, 'errortext': '%s:%s' % (Exception, e)}







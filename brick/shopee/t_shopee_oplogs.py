#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: 张浩  
 @site: 
 @software: sublime Text
 @file: t_shopee_oplogs.py
"""

class t_shopee_oplogs():
    def __init__(self, DBConn):
        self.DBConn = DBConn

    def createLog(self,param):
        '''
        :param param:
        param['OpId']:操作编号
        param['OpType']:操作类型
        param['OpObject']:操作对象
        param['OpStatus']:操作状态
        param['OpErrInfo']:错误信息
        param['OpPerson']:操作人
        param['OpTime']:操作时间
        param['OpStartTime']:操作开始时间
        param['OpEndTime']:操作结束时间
        param['OpNum']:操作总数量
        param['OpSuccess']:操作成功数量
        param['OpError']:操作失败数量
        :return:
        0:插入成功
        -1:插入异常
        '''
        try:
            cursor = self.DBConn.cursor()
            sql = "insert into t_shopee_online_info_log (OpID,OpType,OpObject,OpStatus,OpErrInfo,OpPerson," \
                  "OpTime,OpStartTime,OpEndTime,OpNum,OpSuccess,OpError) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"

            parameter = []
            for productid in param['OpObject']:
                parameter.append((
                    param['OpID'],param['OpType'],productid,param['OpStatus'],param['OpErrInfo'],param['OpPerson'],
                    param['OpTime'], param['OpStartTime'], param['OpEndTime'], param['OpNum'], param['OpSuccess'],param['OpError']
                ))
            cursor.executemany(sql,parameter)
            cursor.execute("commit;")
            cursor.close()
            return {'errorcode':0,'errortext':''}
        except Exception,e:
            return {'errorcode':-1,'errortext':'%s:%s' % (Exception,e)}

    def deleteLog(self,opid):
        try:
            cursor = self.DBConn.cursor()
            cursor.execute("delete from t_shopee_online_info_log WHERE OpID=%s;",(opid,))
            cursor.execute("commit;")
            cursor.close()
            return {'errorcode':0,'errortext':''}
        except Exception,e:
            return {'errorcode':-1,'errortext':'%s:%s' % (Exception,e)}

    def update_error(self,opid,elogs):
        try:
            cursor = self.DBConn.cursor()
            cursor.execute("update t_shopee_online_info_log set OpStatus='error',OpErrInfo=%s WHERE OpID=%s;",(elogs, opid,))
            cursor.execute("commit;")
            cursor.close()
            return {'errorcode':0,'errortext':''}
        except Exception,e:
            return {'errorcode':-1,'errortext':'%s:%s' % (Exception,e)}

    def updateStatusP(self,opid,opobject,status,elogs=''):
        try:
            cursor = self.DBConn.cursor()
            cursor.execute(
                "update t_shopee_online_info_log set OpStatus=%s,OpErrInfo=%s WHERE OpID=%s and OpObject=%s;",
                (status,elogs,opid,opobject)
            )

            if status == 'over':
                cursor.execute("update t_shopee_online_info_log set OpSuccess=OpSuccess+1,OpEndTime=now() WHERE OpID=%s;", (opid,))
            if status == 'error':
                cursor.execute("update t_shopee_online_info_log set OpError=OpError+1,OpEndTime=now() WHERE OpID=%s;", (opid,))

            cursor.execute("commit;")
            cursor.close()
            return {'errorcode':0,'errortext':''}
        except Exception,e:
            return {'errorcode':-1,'errortext':'%s:%s' % (Exception,e)}

    def selectLogs(self,opid):
        try:
            cursor = self.DBConn.cursor()
            cursor.execute(
                "select OpID,OpType,OpObject,OpStatus,OpErrInfo,OpPerson,OpTime,OpStartTime,OpEndTime,OpNum,OpSuccess,OpError "
                "from t_shopee_online_info_log WHERE OpID=%s ;",(opid,)
            )
            opobjs = cursor.fetchall()
            cursor.close()
            return {'errorcode': 0, 'errortext': '','OpLogs':opobjs}
        except Exception, e:
            return {'errorcode': -1, 'errortext': '%s:%s' % (Exception, e)}

    def DoneOrNot(self,opid):
        try:
            cursor = self.DBConn.cursor()
            cursor.execute("select count(*) from t_shopee_online_info_log WHERE OpID=%s and OpStatus='runing';",(opid,))
            count = cursor.fetchone()
            cursor.close()
            return {'errorcode': 0, 'errortext': '','count':count[0]}
        except Exception, e:
            return {'errorcode': -1, 'errortext': '%s:%s' % (Exception, e)}

    def selectLogsByIDError(self,opobject):
        try:
            cursor = self.DBConn.cursor()
            cursor.execute(
                "select OpID,OpType,OpObject,OpStatus,OpErrorInfo,OpPerson,OpTime,OpStartTime,OpEndTime,OpNum,OpSuccess,OpError "
                "from t_shopee_online_info_log WHERE OpObject=%s and OpStatus='error' ORDER by id DESC limit 1;",(opobject,)
            )
            opobjs = cursor.fetchall()
            cursor.close()
            einfor = []
            for opinfo in opobjs:
                einfor.append((u'%s'%opinfo[4]).replace('<','&lt;').replace('>','&gt;'))  # 错误信息
            return {'errorcode': 0, 'errortext': '','einfors':set(einfor)}
        except Exception, e:
            return {'errorcode': -1, 'errortext': '%s:%s' % (Exception, e)}

    def MoreselectLogs(self, opid):
        # 针对全量及增量同步操作，只存在一条日志记录
        try:
            cursor = self.DBConn.cursor()
            cursor.execute("select OpStatus, OpNum, OpSuccess, OpError, OpErrInfo from t_shopee_online_info_log WHERE OpID=%s and OpStatus='runing';",(opid,))
            opobjs = cursor.fetchone()
            cursor.close()
            return {'errorcode': 0, 'errortext': '', 'OpLogs':opobjs}
        except Exception, e:
            return {'errorcode': -1, 'errortext': '%s:%s' % (Exception, e)}
    
    def MoreupdateNum(self, opid, erlogs=''):
        # 针对全量及增量同步操作，只存在一条日志记录
        try:
            cursor = self.DBConn.cursor()
            if erlogs:
                cursor.execute("UPDATE t_shopee_online_info_log set OpErrInfo=%s, OpStatus='error', OpEndTime=now() WHERE OpID=%s;",
                    (opid, erlogs))
            else:
                cursor.execute("UPDATE t_shopee_online_info_log set OpSuccess=OpSuccess+100 WHERE OpID=%s;", (opid, ))
            cursor.execute("commit;")
            cursor.close()
            return {'errorcode': 0, 'errortext': ''}
        except Exception, e:
            return {'errorcode': -1, 'errortext': '%s:%s' % (Exception, e)}

    def MoreupdateStatus(self, opid, status):
        # 针对全量及增量同步操作，只存在一条日志记录
        try:
            cursor = self.DBConn.cursor()
            cursor.execute("UPDATE t_shopee_online_info_log set OpStatus=%s WHERE OpID=%s;", (status, opid))
            cursor.execute("commit;")
            cursor.close()
            return {'errorcode': 0, 'errortext': ''}
        except Exception, e:
            return {'errorcode': -1, 'errortext':'%s:%s' % (Exception,e)}

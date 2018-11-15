# -*- coding: utf-8 -*-

import sys
import datetime


'''if flow_id is not None and params.has_key('db_conn') and params.has_key('flow_id'):
CREATE TABLE `t_flow_logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `flow_id` int(11) NOT NULL COMMENT '流程id',
  `seq` smallint(2) NOT NULL COMMENT '函数seq',
  `function_id` int(11) NOT NULL COMMENT '函数id',
  `begin_time` datetime DEFAULT NULL COMMENT '开始时间',
  `end_time` datetime DEFAULT NULL COMMENT '结束时间',
  `errorcode` varchar(16) DEFAULT NULL COMMENT '执行结果',
  `errortext` varchar(32) DEFAULT NULL COMMENT '错误描述',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
'''
class t_flow_logs():
    def __init__(self,db_conn):
        self.db_conn   = db_conn
    def insert_begin(self,params):
        try:
            cursor =self.db_conn.cursor()
            begin_time= datetime.datetime.now()
            sql = 'insert into t_flow_logs(flow_id,seq,function_id,begin_time,batch_id) VALUES(%s,%s,%s,%s,%s) ;'
            cursor.execute(sql,(params['flow_id'],params['seq'],params['function_id'],begin_time,params['batch_id']))
            self.db_conn.commit()
            cursor.close()
        except Exception,ex:
            print 'insert_begin Exception = %s ex=%s  __LINE__=%s'%(Exception,ex,sys._getframe().f_lineno)
            pass
    def insert_end(self,params):
        try:
            cursor =self.db_conn.cursor()
            end_time= datetime.datetime.now()
            sql = 'insert into t_flow_logs(flow_id,seq,function_id,end_time,errorcode,errortext,batch_id) VALUES(%s,%s,%s,%s,%s,%s,%s) ;'
            cursor.execute(sql,(params['flow_id'],params['seq'],params['function_id'],end_time,params['errorcode'],params['errortext'],params['batch_id']))
            self.db_conn.commit()
            cursor.close()
        except Exception,ex:
            print 'insert_end Exception = %s ex=%s  __LINE__=%s'%(Exception,ex,sys._getframe().f_lineno)
            pass


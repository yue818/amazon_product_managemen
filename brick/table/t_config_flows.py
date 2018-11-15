# -*- coding: utf-8 -*-

import sys


'''if flow_id is not None and params.has_key('db_conn') and params.has_key('flow_id'):
CREATE TABLE `t_config_flows` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `flow_id` int(11) NOT NULL COMMENT '流程id',
  `flow_name` varchar(32) NOT NULL COMMENT '流程描述名字',
  `flow_name2` varchar(32) NOT NULL COMMENT '中文描述',
  `create_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  `create_staff` varchar(32) DEFAULT NULL COMMENT '创建人',
  `status` smallint(2) unsigned NOT NULL DEFAULT '1' COMMENT '1-启用\n0-废弃',
  `seq` int(11) DEFAULT NULL COMMENT '功能函数的顺序小到大',
  `function_id` int(11) DEFAULT NULL COMMENT '功能函数id',
  PRIMARY KEY (`id`),
  KEY `idx_t_config_flows_1` (`flow_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8
'''

class t_config_flows_main():
    def __init__(self,db_conn):
        self.db_conn   = db_conn
    def get_flows_by_flow_id(self,flow_id):
        try:
            print 'input flow_id =%s'%flow_id
            if flow_id is not None :
                cursor =self.db_conn.cursor()
                sql = 'select flow_id,flow_name from t_config_flows_main where flow_id = %s and status = 1 '
                cursor.execute(sql,(flow_id,))
                t_config_flows_main_objs=cursor.fetchall()
                cursor.close()
                print t_config_flows_main_objs
                return len(t_config_flows_main_objs)
        except Exception,ex:
            print 'Exception = %s ex=%s  __LINE__=%s'%(Exception,ex,sys._getframe().f_lineno)
            return 0


class t_config_flows():
    def __init__(self,db_conn):
        self.db_conn   = db_conn
    def get_functions_by_flow_id(self,flow_id):
        try:
            print 'input flow_id =%s'%flow_id
            if flow_id is not None :
                cursor =self.db_conn.cursor()
                sql = 'select flow_id,seq,function_id from t_config_flows where flow_id = %s order by seq'
                cursor.execute(sql,(flow_id,))
                t_config_flows_objs=cursor.fetchall()
                cursor.close()
                print t_config_flows_objs
                return t_config_flows_objs
        except Exception,ex:
            print 'Exception = %s ex=%s  __LINE__=%s'%(Exception,ex,sys._getframe().f_lineno)
            pass

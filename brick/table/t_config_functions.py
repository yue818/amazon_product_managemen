# -*- coding: utf-8 -*-

import sys


'''if flow_id is not None and params.has_key('db_conn') and params.has_key('flow_id'):
CREATE TABLE `t_config_functions` (
  `function_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '功能函数id',
  `function_name` varchar(32) NOT NULL COMMENT '功能描述名字',
  `function_name2` varchar(32) NOT NULL COMMENT '中文描述',
  `create_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  `create_staff` varchar(32) DEFAULT NULL COMMENT '创建人',
  `status` smallint(2) unsigned NOT NULL DEFAULT '1' COMMENT '1-启用\n0-废弃',
  `function_path` varchar(64) DEFAULT NULL COMMENT '功能函数路径例如： wish.getdata',
  PRIMARY KEY (`function_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
'''
class t_config_functions():
    def __init__(self,db_conn):
        self.db_conn   = db_conn
    def getobj_by_function_id(self,function_id):
        try:
            print 'input function_id =%s'%function_id
            if function_id is not None :
                cursor =self.db_conn.cursor()
                sql = 'select function_id,function_name,function_path from t_config_functions where function_id = %s and status = 1 '
                cursor.execute(sql,(function_id,))
                t_config_functions_obj=cursor.fetchone()
                cursor.close()
                print t_config_functions_obj
                return t_config_functions_obj
        except Exception,ex:
            print 'Exception = %s ex=%s  __LINE__=%s'%(Exception,ex,sys._getframe().f_lineno)
            pass

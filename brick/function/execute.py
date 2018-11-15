# -*- coding: utf-8 -*-
import sys
import importlib
from table.t_config_functions import *

#result =  {'errorcode':1,'errortext':'aaaaaaaaaaaaaaaaaaaa','params':params}
#params         :   params 字典

#字典定义通用取值,不能超出这个范围，所有模块统一通用名字
# db_conn        :   数据库连接
# errorcode      :   错误码  0-成功  -1失败  其它具体错误原因
# errortext      :   错误描述
# todo ...


def execute(params):

    try:
        t_config_functions_obj = t_config_functions(params['db_conn'])
        function_path = t_config_functions_obj.getobj_by_function_id(params['function_id'])
        print 'function_path =%s'%function_path[2]
        module = importlib.import_module(function_path[2])
        result ={}
        result = module.run(params)
        params['errorcode'] = 0
        params['errortext'] = 0
    except Exception,ex:
        result['errorcode'] = -1
        result['errortext'] = 'Exception = %s ex=%s  __LINE__=%s'%(Exception,ex,sys._getframe().f_lineno)
        print 'module.run Exception = %s ex=%s  __LINE__=%s'%(Exception,ex,sys._getframe().f_lineno)
        params['errorcode'] = result['errorcode']
        params['errortext'] = result['errortext']
    print result

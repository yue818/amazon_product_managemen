#-*-coding:utf-8-*-
"""  
 @desc:  自定义异常类,标准化我们自己的错误代码
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: MyException.py
 @time: 2018-05-12 15:53
"""

from exceptions import Exception
from skuapp.table.t_sys_error_code import t_sys_error_code

class MyException(Exception):
    def __init__(self, error_code, attach_value=''):
        attach_value = '' if attach_value == '' else ' (定位值:%s)' % attach_value
        obj = t_sys_error_code.objects.filter(error_code=error_code)
        if obj.count() > 0:
            err = obj[0].error_text+attach_value
            Exception.__init__(self, err)
            self.todo = obj[0].possible_reason
        else:
            err = u'未知异常::>_<:: '+attach_value
            Exception.__init__(self, err)
            self.todo = u'请维护error_code:%s'%error_code


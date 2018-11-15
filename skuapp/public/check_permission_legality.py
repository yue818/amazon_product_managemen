#-*-coding:utf-8-*-
u"""
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: check_permission_legality.py
 @time: 2018/8/9 15:45
 权限校验
"""

import inspect

def check_permission_legality(self):
    """
    :param self:
    :return:
    """
    funcName = inspect.stack()[1][3]
    permname = '{}.Can_{}_{}'.format(self.model._meta.app_label, self.model._meta.model_name, funcName)
    if self.request.user.is_superuser or self.request.user.has_perm(permname):
        return True
    return False


# -*- coding: utf-8 -*-
class t_sys_department_Admin(object):
    list_display=('id','DepartmentID','DepartmentName', )
    readonly_fields = list_display
# -*- coding: utf-8 -*-
class t_sys_department_staff_Admin(object):
    list_display=('id','StaffID','DepartmentID',)
    readonly_fields = ('id',)
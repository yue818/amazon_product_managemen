# -*- coding: utf-8 -*-
class t_sys_param_Admin(object):
    list_display=('id','Type','TypeDesc','TypeName','V','VDesc','UpdateTime',)
    list_filter=('Type','TypeDesc','TypeName','V','VDesc','UpdateTime',)
    search_fields=('id','Type','TypeDesc','TypeName','V','VDesc',)

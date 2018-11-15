# -*- coding: utf-8 -*-
import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView
from django.template import loader
from skuapp.table.t_sys_department_staff import t_sys_department_staff


class enter_ed_user_Plugin(BaseAdminPlugin):
    enter_ed_user_flag = False
    def init_request(self, *args, **kwargs):
        return bool(self.enter_ed_user_flag)
    def block_search_cata_nav(self, context, nodes):
        models_objs = (u'%s'%context['request']).split('/')
        if models_objs[1] == 'Project' and models_objs[2] == 'admin':
            app_name = str(models_objs[4])
        elif models_objs[1] == 'xadmin':
            app_name = str(models_objs[3])
        username = self.request.user.username
        try:
            DepartmentID = str(t_sys_department_staff.objects.get(StaffID=username).DepartmentID)
        except:
            DepartmentID = 'none'
        if self.request.user.is_superuser or DepartmentID == '2':
            flag = 1
        else:
            flag = 0
        nodes.append(loader.render_to_string('enter_ed_user.html',{'app_name':app_name,'flag':flag}))

xadmin.site.register_plugin(enter_ed_user_Plugin, ListAdminView)


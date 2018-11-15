# -*- coding: utf-8 -*-
import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView
from django.template import loader


class depart_get_user_Plugin(BaseAdminPlugin):
    depart_get_user_flag = False
    def init_request(self, *args, **kwargs):
        return bool(self.depart_get_user_flag)
    def block_search_cata_nav(self, context, nodes):
        models_objs = (u'%s'%context['request']).split('/')
        if models_objs[1] == 'Project' and models_objs[2] == 'admin':
            app_name = str(models_objs[4])
        elif models_objs[1] == 'xadmin':
            app_name = str(models_objs[3])
        nodes.append(loader.render_to_string('depart_get_user.html',{'app_name':app_name}))

xadmin.site.register_plugin(depart_get_user_Plugin, ListAdminView)


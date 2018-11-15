# -*- coding: utf-8 -*-
import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from django.template import loader

class t_stocking_check_reportPlugin(BaseAdminPlugin):
    check_report_plugin = False
    def init_request(self, *args, **kwargs):
        return bool(self.check_report_plugin)
    def block_luru(self, context, nodes):
        nodes.append(loader.render_to_string('t_stocking_check_report.html',))
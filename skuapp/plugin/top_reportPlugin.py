# -*- coding: utf-8 -*-
import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from django.template import loader
import time

from skuapp.table.t_yearweek import *
from skuapp.table.t_report_week import *
#增加图片

class top_reportPlugin(BaseAdminPlugin):
    show_report = False
    def init_request(self, *args, **kwargs):
        return bool(self.show_report)
    def block_top_report(self, context, nodes):

        if context['user'].is_superuser:
            t_yearweek_objs = t_yearweek.objects.filter(yearweek=time.strftime("%Y%W"))[0:1]
            if not t_yearweek_objs.exists():
                t_yearweek_obj = [0]
            else:
                t_yearweek_obj = t_yearweek_objs[0]

            nodes.append(loader.render_to_string('top_report_super.html',{'t_yearweek_obj':t_yearweek_obj}))
        else:
            kf_objs  = t_report_week.objects.filter(YearWeek=time.strftime("%Y%W"),StaffName=context['user'].first_name,StepID='KF')
            jzl_objs = t_report_week.objects.filter(YearWeek=time.strftime("%Y%W"),StaffName=context['user'].first_name,StepID='JZL')

            if not kf_objs.exists():
                user_kf_objs = [0]
            else:
                user_kf_objs = kf_objs[0]

            if not jzl_objs.exists():
                user_jzl_objs = [0]
            else:
                user_jzl_objs = jzl_objs[0]

            nodes.append(loader.render_to_string('top_report.html',{'user_kf_objs':user_kf_objs,'user_jzl_objs':user_jzl_objs}))


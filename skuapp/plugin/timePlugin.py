# -*- coding: utf-8 -*-

import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
import time

from django.utils.safestring import mark_safe
from django.template import loader
class timePlugin(BaseAdminPlugin):
    show_time = True
    def init_request(self, *args, **kwargs):
        return bool(self.show_time)
    def block_time(self, context, nodes):

        import datetime
        day = int(time.strftime("%w"))-1
        deltaday = datetime.timedelta(days=day)
        timeday = datetime.datetime.now()-deltaday
        date_from = datetime.datetime(timeday.year, timeday.month, timeday.day)
        site_title = mark_safe('我的任务(%s)'%time.strftime("第%W周"))

        nodes.append(loader.render_to_string('time.html',{'site_title':site_title}))


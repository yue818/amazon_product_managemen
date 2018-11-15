# -*- coding: utf-8 -*-
import os
import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from django.template import loader

from skuapp.table.public import getChoices,ChoiceIp
class t_helpPlugin(BaseAdminPlugin):
    to_help = True
    def init_request(self, *args, **kwargs):
        return bool(self.to_help)
    def block_help(self, context, nodes):
        IP = ''
        ServerIP = os.popen(
            "ifconfig | grep 'inet addr:' | grep -v '127.0.0.1' | cut -d: -f2 | awk '{print $1}' | head -1").read()
        GetIPs = getChoices(ChoiceIp)
        for GetIP in GetIPs:
            if GetIP[0] == ServerIP.strip():  # （75--测试环境）
                IP = u'%s' % GetIP[1]

        siteIP = u'%s' % (IP)

        help_name = u'帮助'
        history_name=u'最近访问记录'

        #logger = logging.getLogger('sourceDns.webdns.views')
        #logger.error("context=%s ,opts= %s "%(context,context['opts']))

        nodes.append(loader.render_to_string('t_help.html', {'help_name':help_name,'history_name':history_name,'siteIP':siteIP}))


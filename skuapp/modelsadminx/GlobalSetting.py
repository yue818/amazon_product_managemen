# -*- coding: utf-8 -*-
import os
import socket, fcntl, struct
import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from skuapp.table.public import *
import logging

class GlobalSetting(object):
    #设置base_site.html的Title
    #import datetime
    #day = int(time.strftime("%w"))-1
    #deltaday = datetime.timedelta(days=day)
    #timeday = datetime.datetime.now()-deltaday
    #date_from = datetime.datetime(timeday.year, timeday.month, timeday.day)
    logger = logging.getLogger('sourceDns.webdns.views')
    IP = ''
    #site_title = mark_safe('功能首页  (%s) <br> %s-%s '%(time.strftime("%Y年第%W周"),date_from,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    #设置base_site.html的Footer
    ServerIP = os.popen("ifconfig | grep 'inet addr:' | grep -v '127.0.0.1' | cut -d: -f2 | awk '{print $1}' | head -1").read() 
    GetIPs = getChoices(ChoiceIp)
    for GetIP in GetIPs:
        if GetIP[0] == ServerIP.strip(): #（75--测试环境）
            IP = u'--%s'%GetIP[1]
            
    site_footer  = u'fancyqube%s'%(IP)
    #menu_style = 'accordion'
xadmin.site.register(CommAdminView, GlobalSetting)

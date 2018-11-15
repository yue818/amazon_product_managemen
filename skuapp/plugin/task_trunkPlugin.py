# coding=utf-8

from xadmin.views import BaseAdminPlugin
from django.template import loader
from skuapp.table.t_online_info_wish import *
from django.db.models import Q
from django.contrib import messages
import logging
from urllib import unquote


class task_trunkPlugin(BaseAdminPlugin):
    task_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.task_flag)

    def get_media(self, media):
        media.add_js([self.static('xadmin/js/xadmin.plugin.button.color.js')])
        return media

    def block_search_cata_nav(self, context, nodes):
        sourceURL = str(context['request']).split("'")[1]

        paramList = ['&status=mycreate&Flow_Status=TC,SH,CL,NYZ,YZ','&status=mytask&Flow_Status=TC,SH,CL,NYZ,YZ','&status=myjoin&Flow_Status=TC,SH,CL,NYZ,YZ','&status=taskout&Flow_Status=TC,SH,CL,NYZ,YZ','&status=all&Flow_Status=TC,SH,CL,NYZ,YZ',
                     'Flow_Status=TC,SH,CL,NYZ,YZ&status=mycreate&','Flow_Status=TC,SH,CL,NYZ,YZ&status=mytask&','Flow_Status=TC,SH,CL,NYZ,YZ&status=myjoin&','Flow_Status=TC,SH,CL,NYZ,YZ&status=taskout&','status=all&Flow_Status=TC,SH,CL,NYZ,YZ&',
                     'status=mycreate&Flow_Status=TC,SH,CL,NYZ,YZ','status=mytask&Flow_Status=TC,SH,CL,NYZ,YZ','status=myjoin&Flow_Status=TC,SH,CL,NYZ,YZ','status=taskout&Flow_Status=TC,SH,CL,NYZ,YZ','status=all&Flow_Status=TC,SH,CL,NYZ,YZ',]

        if 'status=mycreate' in sourceURL:
            flag = 1
        elif 'status=mytask' in sourceURL:
            flag = 2
        elif 'status=myjoin' in sourceURL:
            flag = 3
        elif 'status=taskout' in sourceURL:
            flag = 4
        elif 'status=all' in sourceURL:
            flag = 5
        else:
            flag = 0

        oldUrl = sourceURL
        #messages.error(context['request'],oldUrl.split('?')[1][0:23])
        #messages.error(context['request'],oldUrl.replace('Flow_Status=TC,SH,CL,NYZ,YZ&',''))
        if '?' in oldUrl:
            newFlag = True
            for param in paramList:
                if param in oldUrl:
                    oldUrl = oldUrl.replace(param,'')
                    newFlag = False
                    if oldUrl.split('?')[1] == '':
                        oldUrl = oldUrl
                    #elif oldUrl.split('?')[1][0:23] == 'Flow_Status=TC,SH,CL,NYZ,YZ':
                        #oldUrl = oldUrl.replace('Flow_Status=TC,SH,CL,NYZ,YZ&','')
                        #messages.error(context['request'],oldUrl)
                    else:
                        oldUrl = oldUrl + '&'
            if(newFlag):
                oldUrl = oldUrl + '&'
        else:
            oldUrl = oldUrl + '?'
        request = self.request    
        username = request.user.username  

        nodes.append(loader.render_to_string('task_trunk.html',
                                             {'url':oldUrl, 'flag':flag,'username':username}))
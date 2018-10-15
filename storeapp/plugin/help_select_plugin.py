# -*- coding: utf-8 -*-
from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.template import RequestContext
import logging
import json
from urllib import urlencode
from django.contrib import messages

class help_select_plugin(BaseAdminPlugin):
    help_select = False

    def init_request(self, *args, **kwargs):
        return bool(self.help_select)

    def block_search_loaction_after(self, context, nodes):
        activeflag = self.request.GET.get('EXPRESS', 'STANDARD')
        nodes.append(
            loader.render_to_string(
                'help_select_content.html',{'activeflag':activeflag}, context_instance=RequestContext(self.request)
            )
        )



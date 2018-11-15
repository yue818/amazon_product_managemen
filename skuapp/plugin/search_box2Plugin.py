# -*- coding: utf-8 -*-

from xadmin.views import BaseAdminPlugin
from django.template import loader
from urllib import unquote
#from django.template import RequestContext
from skuapp.table.search_box_plugin import *
from Project.settings import *
from django.contrib import messages
from skuapp.table.t_cfg_category_info import *


class search_box2Plugin(BaseAdminPlugin):
    search_box2_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.search_box2_flag)

    def block_search_cata_nav(self, context, nodes):
        CategoryName_objs = t_cfg_category_info.objects.filter(CategoryId=None).values('id','CategoryName').order_by('CategoryName')
        nodes.append(loader.render_to_string('search_box2_plugin.html',{'id':id,'CategoryName_objs':CategoryName_objs}))
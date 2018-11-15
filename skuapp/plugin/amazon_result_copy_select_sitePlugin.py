#-*-coding:utf-8-*-
from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.contrib import messages

"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: amazon_result_copy_select_sitePlugin.py
 @time: 2018/7/23 17:04
"""   
class amazon_result_copy_select_sitePlugin(BaseAdminPlugin):
    amazon_result_copy_select_site_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.amazon_result_copy_select_site_flag)

    def block_search_cata_nav(self, context, nodes):
        nodes.append(loader.render_to_string('amazon_result_copy_select_site_plugin.html',{}))
#-*-coding:utf-8-*-
from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.template import RequestContext

"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_product_upc_id_Plugin.py
 @time: 2018/3/26 17:43
"""   
class t_product_upc_id_amazon_Plugin(BaseAdminPlugin):
    product_upc_amazon_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.product_upc_amazon_flag)

    def block_before_fieldsets(self, context, nodes):
        nodes.append(loader.render_to_string('t_product_upc_id_amazon_Plugin.html',context_instance=RequestContext(self.request)))



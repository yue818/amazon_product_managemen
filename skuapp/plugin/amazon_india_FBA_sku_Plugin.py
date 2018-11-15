#-*-coding:utf-8-*-
from xadmin.views import BaseAdminPlugin
from django.template import loader

"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: amazon_india_FBA_sku_Plugin.py
 @time: 2018/6/11 20:24
"""   
class amazon_india_FBA_sku_Plugin(BaseAdminPlugin):
    amazon_india_FBA_sku_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.amazon_india_FBA_sku_flag)

    def block_search_cata_nav(self, context, nodes):
        source_path = self.request.get_full_path()
        fba_sku = self.request.GET.get('fba_sku', '')
        sku = self.request.GET.get('mrp_sku', '')
        source_fba_path = source_path.split('?')[0] + 'generate_fba_price_pdf/?' + source_path.split('?')[1]
        source_mrp_path = source_path.split('?')[0] + 'generate_mrp_price_india/?' + source_path.split('?')[1]

        nodes.append(loader.render_to_string('amazon_india_FBA_sku.html',
                                             {'source_url': source_fba_path, 'fba_sku': fba_sku, 'source_mrp_path': source_mrp_path, 'sku': sku}))
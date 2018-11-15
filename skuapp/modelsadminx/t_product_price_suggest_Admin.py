#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_product_price_suggest_Admin.py
 @time: 2018-08-08 14:57
"""

from django.utils.safestring import mark_safe
from django.contrib import messages
import re

class t_product_price_suggest_Admin(object):
    category_flag = True

    pp = re.compile('http.+?(?=;)')

    def LinkDetail(self, obj):

        rt = ''
        if obj.LinkUrl is None or obj.LinkUrl.strip() == '':
            pass
        else:
            data = self.pp.findall(obj.LinkUrl)
            for i, linkurl in enumerate(data, 1):
                rt += '<a href=%s target="_blank">核价链接_%s</a></br>'%(linkurl, i)

        rt = '''%s<br /><form id="form4_%s" method="post" action="/button_Plugin/">
              <input type="hidden" name="GoodsSKU" value="%s" /> 
              <a onclick="document.getElementById('form4_%s').submit();">进行修改</a>
              </form>''' % (rt, obj.id, obj.SKU, obj.id)

        return mark_safe(rt)
    LinkDetail.short_description = mark_safe('<p style="color:#428bca;text-align:center">操作</p>')

    list_display_links = ('id',)
    list_display = ('SKU', 'GoodsName', 'GoodsStatus', 'StoreName', 'SupplierName', 'SalerName2', 'Purchaser',
                    'CreateDate', 'Number', 'SellCount1', 'SellCount2', 'SellCount3', 'UseNumber', 'CostPrice',
                    'LinkDetail')
    list_filter = ( 'CreateDate', 'Number', 'SellCount1', 'SellCount2', 'SellCount3', 'UseNumber',)
    search_fields = ('SKU', 'GoodsName', 'SupplierName', 'SalerName2', 'Purchaser', )
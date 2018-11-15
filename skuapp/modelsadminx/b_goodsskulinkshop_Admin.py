# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from skuapp.table.b_goodsskulinkshop import *
from django.db import transaction,connection
from .t_product_Admin import *
class b_goodsskulinkshop_Admin(object):
    list_display=('NID','SKU','ShopSKU','Memo','PersonCode')
    search_fields =None
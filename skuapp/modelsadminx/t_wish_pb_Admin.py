# -*- coding: utf-8 -*-
from .t_product_Admin import *
from skuapp.table.t_store_configuration_file import *

class t_wish_pb_Admin(object):
    def show_pic(self,obj) :
        picUrl =  obj.Pic
        rt =  '<img src="%s"  width="150" height="150"  alt = "%s"  title="%s"  />  '%(picUrl,picUrl,picUrl)
        return mark_safe(rt)
    show_pic.short_description = u'产品图片'
    list_display  =('id','ShopName','ActivityName','ActivityStatus','ActivityID',
                    'Duration','show_pic','ProductID','ProductName','PbKey','PbCharge',
                    'PbFee','PbData','PbOrder','PbCount','updateTime',)
    search_fields =('id','ShopName','ActivityName','ActivityStatus','ActivityID',
                    'Duration','ProductID','ProductName','PbKey','PbCharge',
                    'PbFee','PbData','PbOrder','PbCount',)
    
   
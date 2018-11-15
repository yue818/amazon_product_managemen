# -*- coding: utf-8 -*-
from .t_product_Admin import *
from skuapp.table.t_store_configuration_file import *

class v_wish_pb_Admin(object):
    def show_Activity(self,obj):
        rt='<br><input type="button" value="查看广告详情" onclick="window.open(\'/Project/admin/skuapp/t_wish_pb/?_p_ActivityID=%s\')" <br>'%(obj.ActivityID)
        return mark_safe(rt)
    show_Activity.short_description = u'查看广告详情'
    list_display  =('ShopName','ActivityName','ActivityStatus', 'ActivityID','Duration' ,'Budget' ,'EnrollFee', 'TotalFee',
                    'ProductNum', 'ActivityFee', 'ActivityFlow', 'ProductOrder', 'ActivityAmount','FeeDivAmount','show_Activity')
    list_filter   =('ShopName','ActivityName','ActivityStatus', 'ActivityID','Duration' ,'Budget' ,'EnrollFee', 'TotalFee',
                    'ProductNum', 'ActivityFee', 'ActivityFlow', 'ProductOrder', 'ActivityAmount','FeeDivAmount',)
    search_fields =('ShopName','ActivityName','ActivityStatus', 'ActivityID','Duration' ,'Budget' ,'EnrollFee', 'TotalFee',
                    'ProductNum', 'ActivityFee', 'ActivityFlow', 'ProductOrder', 'ActivityAmount','FeeDivAmount',)
    
   
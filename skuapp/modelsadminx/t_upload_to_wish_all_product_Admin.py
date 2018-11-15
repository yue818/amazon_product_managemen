# -*- coding: utf-8 -*-
from django.forms import TextInput, Textarea
from skuapp.modelsadminx.t_online_info_wish_Admin import t_online_info_wish_Admin
from skuapp.table.t_upload_shopname import t_upload_shopname

class t_upload_to_wish_all_product_Admin(t_online_info_wish_Admin):
    
    #list_display = ('id','show_Picture','show_tortInfo','show_remarks','Remarks','show_ShopName_Seller','Orders7Days','OfSales','show_Title_ProductID','show_SKU_list','show_status','show_time','show_orders7days',)
    #list_editable = ('Remarks')
    #list_filter = ('Seller','Orders7Days','RefreshTime','Status','ReviewState','DateUploaded','LastUpdated','TortInfo','DataSources','OperationState',)
    #search_fields = ('id','PlatformName','ProductID','ShopIP','ShopName','Title','SKU','Orders7Days','Status','ReviewState','ParentSKU','Seller','DataSources','OperationState',)
    search_fields =None    
    def get_list_queryset(self):
        request = self.request
        qs = super(t_upload_to_wish_all_product_Admin, self).get_list_queryset()
        
        return qs.filter(DataSources='UPLOAD')
# -*- coding: utf-8 -*-
from datetime import datetime

import requests
from skuapp.table.t_config_online_amazon import t_config_online_amazon
from django.contrib import messages
from django.utils.safestring import mark_safe
from skuapp.table.t_tort_aliexpress import t_tort_aliexpress
from skuapp.table.t_sensitive_word_info import t_sensitive_word_info
from skuapp.table.t_sensitive_sku_info import t_sensitive_sku_info
from skuapp.table.t_tort_shelve_wish import t_tort_shelve_wish

class t_tort_shelve_wish_Admin(object):
    search_box_flag = True
    show_tort_wish = True
    
    def show_Picture(self,obj) :
        url = u'https://contestimg.wish.com/api/webimage/%s-medium.jpg'%str(obj.ProductID)
        rt =  '<img src="%s"  width="120" height="120"  alt = "%s"  title="%s"  />  '%(url,url,url)
        return mark_safe(rt)
    show_Picture.short_description = u'图片'
    
    def show_ShopName_Seller(self,obj) :
        rt = u'卖家简称:<br>%s<br>店长/销售员:<br>%s'%(obj.ShopName,obj.Seller)
        return mark_safe(rt)
    show_ShopName_Seller.short_description = u'卖家简称/店长/销售员'
    
    def show_Title(self,obj):
        s_objs = t_sensitive_word_info.objects.values_list('sensitive_words',flat=True)
        rt = obj.Title
        for s_obj in s_objs:
            if s_obj in obj.Title:
                middle_var = '<font color="red">'+s_obj+'</font>'
                rt = rt.replace(s_obj,middle_var)
        return mark_safe(rt)
    show_Title.short_description = u'标题'

    

    
    list_display = ('PlatformName','show_Picture','onemark','RemarkReason','ShopIP','show_ShopName_Seller','ProductID','show_Title','SKU','ShopSKU','Orders7Days','OfSales','Price','Quantity','Status','DateUploaded','ParentSKU','MainSKU','OperationState','OperationTime','OperationMan','ShelveTime')
    list_editable= ('RemarkReason','onemark')
    search_fields = (
        'PlatformName', 'ProductID', 'ShopIP', 'ShopName', 'Seller', 'Title', 'SKU', 'ShopSKU', 'Price', 'Quantity',
        'Image', 'Status', 'DateUploaded', 'ParentSKU', 'ReviewState', 'OfWishes', 'OfSales', 'LastUpdated', 'Shipping',
        'Color', 'Size', 'msrp', 'ShippingTime', 'ExtraImages', 'VariationID', 'Description', 'Tags', 'MainSKU',
        'MainShopSKU', 'OperationState',)
    list_filter  = ('PlatformName','Status','ReviewState','OperationState','Orders7Days','OfSales',)
    
    actions=['do_tort_shelve_wish']

    # 添加权限，使超级用户可以使用一键下架功能
    
    def do_tort_shelve_wish(self, request, objs):

        list_id = []
        list_id_l = []
    
        if request.user.is_superuser:
            self.actions.append('do_tort_shelve_wish')

            for obj in objs:
        
                t_config_online_amazon_objs = t_config_online_amazon.objects.filter(Name=obj.ShopName)
                if t_config_online_amazon_objs.exists():
                
                    access_token_value = ''
                    for t_config_online_amazon_obj in t_config_online_amazon_objs:
                        if t_config_online_amazon_obj.K == 'access_token':
                            access_token_value = t_config_online_amazon_obj.V
                    url = 'https://merchant.wish.com/api/v2/product/disable'
                    data = {
                        'access_token': access_token_value,
                        'format': 'json',
                        'id':obj.ProductID,
                        'parent_sku': obj.ParentSKU,
                    }
                    r = requests.post(url,data=data)
                    _content = eval(r._content)
                    #messages.error(request,u'_content:%s'%(_content))
                    if r.status_code == 200 and _content['code'] == 0:
                        list_id.append(obj.id)
                    else:
                        list_id_l.append(obj.id)
                
                else:
                    messages.error(request,u'请联系相关人员，添加该店铺:%s的token信息'%(obj.ShopName))

            objs.filter(id__in = list_id).update(OperationState = 'Yes',Status = 'Disabled')
            objs.filter(id__in = list_id_l).update(OperationState = 'Error')
        else:
            messages.error(request,'你没有足够的权限来进行一键下架！！！')
    do_tort_shelve_wish.short_description = u'仿品_一键下架'
    
    def get_list_queryset(self):
        request = self.request

        qs = super(t_tort_shelve_wish_Admin, self).get_list_queryset()
        
        
        Status = request.GET.get('Status', '')                      #状态
        ReviewState = request.GET.get('ReviewState', '')            #Wish查看状态
        OperationState = request.GET.get('OperationState', '')      #api执行状态

        OfSalesStart = request.GET.get('OfSalesStart', '')          #订单量
        OfSalesEnd = request.GET.get('OfSalesEnd', '')
        
        Orders7DaysStart = request.GET.get('Orders7DaysStart', '')  #7天order数
        Orders7DaysEnd = request.GET.get('Orders7DaysEnd', '')
        ss = request.GET.get('ss','')

        searchList = {'Status__exact': Status,
                      'ReviewState__exact': ReviewState,
                      'OperationState__exact': OperationState,

                      'Orders7Days__gte': Orders7DaysStart, 'Orders7Days__lt': Orders7DaysEnd,
                      'OfSales__gte': OfSalesStart, 'OfSales__lt': OfSalesEnd,
                      }
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    # if k == 'ShopName__exact':
                    #  v = 'Wish-' + v.zfill(4)
                    # messages.error(request, v)
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')
        
        if request.user.is_superuser:
            if ss == 'sku':
                sensitive_sku_objs = t_sensitive_sku_info.objects.values_list('sensitive_sku',flat=True)
                return qs.filter(SKU__in = sensitive_sku_objs)
            elif ss == 'words':
                sensitive_words_objs = t_sensitive_word_info.objects.values_list('sensitive_words',flat=True)

                id_list = []
                objs = t_tort_shelve_wish.objects.values('id', 'Title')  
                id_title_dict = {}
                for obj in objs:
                    id_title_dict[obj['id']] = obj['Title']
                for k, v in id_title_dict.items():
                    for sensitive_words_obj in sensitive_words_objs:
                        if sensitive_words_obj in v:
                            id_list.append(k)
                #messages.error(request,'---1---%s'%id_list)
                #messages.error(request,'---2---%s'%id_title_dict)
                for sensitive_words_obj in sensitive_words_objs:
                    return qs.filter(id__in = id_list)
            else:
                return qs
        return qs.filter(Seller = request.user.first_name)
    
    
    
    
    
    

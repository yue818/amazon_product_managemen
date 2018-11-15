# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from skuapp.table.t_online_info import *
import logging
from django.forms import TextInput, Textarea
from skuapp.table.t_online_info_wish import *
from skuapp.table.t_store_configuration_file import *


class t_online_info_wish_Admin(object):

    def show_Picture(self,obj) :
        url = u'https://contestimg.wish.com/api/webimage/%s-medium.jpg'%str(obj.ProductID)
        rt =  '<img src="%s"  width="120" height="120"  alt = "%s"  title="%s"  />  '%(url,url,url)
        return mark_safe(rt)
    show_Picture.short_description = u'图片'
    
    def get_product_ID_link(self,obj) :
        return mark_safe('<a href=https://www.amazon.com/dp/%s>%s</a>'%(obj.ProductID,obj.ProductID))
    get_product_ID_link.short_description = u'产品ID'
    
    def show_ShopName_Seller(self,obj) :
        rt=''
        rt = u'%s卖家简称:<br>%s<br>店长/销售员:<br>%s'%(rt,obj.ShopName,obj.Seller)
        return mark_safe(rt)
    show_ShopName_Seller.short_description = u'卖家简称/店长/销售员'
    
    def show_Title_ProductID(self,obj) :
        l = obj.Title.split(' ')
        aa = len(l)
        ll = ''
        rt=''
        logger = logging.getLogger('sourceDns.webdns.views')
        #
        if aa <= 6:
            rt = u'%s标题: %s<br>产品ID: <a href=" https://www.wish.com/c/%s" target="_blank">%s</a>'%(rt,obj.Title,obj.ProductID,obj.ProductID)
        elif aa > 6:
            newe_Title_list = []
            for i in range(0, len(l), 6):
                min_list = ''
                for a in l[i:i+6]:
                    min_list = u'%s%s '%(min_list,a)
                newe_Title_list.append(min_list)
                #logger.error("newe_Title_list===================xxxxxxxxxxxxxxx=%s "%(newe_Title_list))
            for newe_Title  in newe_Title_list:
                ll = u'%s%s<br>'%(ll,newe_Title)
            rt = u'%s标题:<br>%s产品ID:<br><a href=" https://www.wish.com/c/%s" target="_blank">%s</a>'%(rt,ll,obj.ProductID,obj.ProductID)
        return mark_safe(rt)
    show_Title_ProductID.short_description = u'标题/产品ID'
    
    def show_time(self,obj) :
        rt=''
        rt = u'%s刷新时间:<br>%s <br>上架时间:<br>%s <br>最近更新时间:<br>%s'%(rt,obj.RefreshTime,obj.DateUploaded,obj.LastUpdated)
        return mark_safe(rt)
    show_time.short_description = u'时间'
    
    def show_SKU_list(self,obj) :
        rt='<table   style="text-align:center;" border="1" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1"><tr bgcolor="#C00"><th style="text-align:center">子SKU</th><th style="text-align:center">店铺SKU</th><th style="text-align:center">库存量</th><th style="text-align:center">价格</th></tr>'
        t_online_info_wish_objs = t_online_info.objects.values('SKU','ShopSKU','Quantity','Price').filter(ProductID=obj.ProductID).distinct()
        i = 0
        for t_online_info_wish_obj in t_online_info_wish_objs:
            if i < 5:
                rt = '%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> '%(rt,t_online_info_wish_obj['SKU'],t_online_info_wish_obj['ShopSKU'],t_online_info_wish_obj['Quantity'],t_online_info_wish_obj['Price'])
                i = i + 1
        if len(t_online_info_wish_objs)>5:
            rt = '%s<tr><td><a id="link_id_%s">查看更多</a></td></tr>'%(rt,obj.id)
        else:
            rt = rt
        rt = "%s</table><script>$('#link_id_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['500px','500px'],content:'/t_online_info_wish/SKU/?abc=%s',});});</script>"%(rt,obj.id,obj.ProductID)
        return mark_safe(rt)
    show_SKU_list.short_description = mark_safe('<p align="center"> 子SKU</p>')
    
    def show_orders7days(self,obj) :

        rt =  u"<a id=show_orderlist_%s>日销量</a><script>$('#show_orderlist_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['1000px','600px'],content:'/t_online_info_wish/order1day/?aID=%s',});});</script>"%(obj.id,obj.id,obj.ProductID)
        rt =  u"%s<br><a id=show_distribution_%s>铺货</a><script>$('#show_distribution_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'进行铺货',fix:false,shadeClose: true,maxmin:true,area:['600px','400px'],content:'/t_online_info_wish/t_distribution_product_to_store/?PID=%s',});});</script>"%(rt,obj.id,obj.id,obj.ProductID)
        
        return mark_safe(rt)
        
    show_orders7days.short_description = u'操作'
    
    list_display = ('id','show_Picture','Remarks','show_ShopName_Seller','Orders7Days','OfSales','show_Title_ProductID','show_SKU_list','Status','show_time','show_orders7days',)
    list_editable = ('Remarks',)
    list_filter = ('Seller','Orders7Days','RefreshTime','Status','ReviewState','DateUploaded','LastUpdated',)
    search_fields = ('id','PlatformName','ProductID','ShopIP','ShopName','Title','SKU','Orders7Days','Status','ReviewState','ParentSKU','Seller',)
    
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':5, 'cols':50})},
        }
    
    
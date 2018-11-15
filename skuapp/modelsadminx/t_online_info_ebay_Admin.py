# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from skuapp.table.t_online_info import *
import logging
from django.forms import TextInput, Textarea
from skuapp.table.t_online_info_ebay import *
from skuapp.table.t_store_configuration_file import *
from skuapp.table.t_online_info_ebay_subsku import *


class t_online_info_ebay_Admin(object):

    def show_Picture(self,obj) :
        url = u'%s'%(obj.img)
        rt =  '<img src="%s"  width="150" height="150"  alt = "%s"  title="%s"  />  '%(url,url,url)
        return mark_safe(rt)
    show_Picture.short_description = u'图片'
    
    def show_ShopName_Seller(self,obj) :
        rt=''
        t_store_configuration_file_objs=t_store_configuration_file.objects.filter(ShopName=obj.ShopName)
        if t_store_configuration_file_objs.exists():
            for t_store_configuration_file_obj in  t_store_configuration_file_objs:
                rt = u'%s卖家简称:<br>%s<br>店长/销售员:<br>%s'%(rt,t_store_configuration_file_obj.ShopName,t_store_configuration_file_obj.Seller)
        return mark_safe(rt)
    show_ShopName_Seller.short_description = u'卖家简称/店长/销售员'
    
    def show_SKU_list(self,obj) :
        rt='<table   style="text-align:center;" border="1" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1"><tr bgcolor="#C00"><th style="text-align:center">子SKU</th><th style="text-align:center">价格</th></tr>'
        t_online_info_ebay_subsku_objs = t_online_info_ebay_subsku.objects.filter(itemid=obj.itemid)
        i = 0
        for t_online_info_ebay_subsku_obj in t_online_info_ebay_subsku_objs:
            if i < 5:
                rt = '%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td></tr> '%(rt,t_online_info_ebay_subsku_obj.subSKU,t_online_info_ebay_subsku_obj.startprice)
                i = i + 1
        if len(t_online_info_ebay_subsku_objs)>5:
            rt = '%s<tr><td><a id="link_id_%s">查看更多</a></td></tr>'%(rt,obj.id)
        else:
            rt = rt
        rt = "%s</table><script>$('#link_id_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['500px','500px'],content:'/t_online_info_ebay/ebay_SKU/?abc=%s',});});</script>"%(rt,obj.id,obj.itemid)
        return mark_safe(rt)
    show_SKU_list.short_description = mark_safe('<p align="center"> 子SKU</p>')
    
    def show_Title(self,obj) :
        l = obj.title.split(' ')
        aa = len(l)
        ll = ''
        rt=''
        #logger = logging.getLogger('sourceDns.webdns.views')
        #
        if aa <= 6:
            rt = u'%s标题:<br>%s'%(rt,obj.title)
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
            rt = u'%s标题:<br>%s'%(rt,ll)
        return mark_safe(rt)
    show_Title.short_description = u'标题'
    
    def show_time(self,obj) :
        rt=''
        rt = u'%s上架时间:<br>%s <br>下架时间:<br>%s '%(rt,obj.starttime,obj.endtime)
        return mark_safe(rt)
    show_time.short_description = u'时间'
    
    def show_orders7days(self,obj) :
        rt =  "<a id=show_orderlist_%s>日销量</a><script>$('#show_orderlist_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['1000px','600px'],content:'/t_online_info_ebay/ebay_order1day/?ID=%s',});});</script>"%(obj.id,obj.id,obj.itemid)
        return mark_safe(rt)
    show_orders7days.short_description = u'操作'

    list_display = ('id','show_Picture','Remarks','show_ShopName_Seller','Orders7Days','sold','show_Title','status','show_time','show_SKU_list','show_orders7days',)
    list_editable = ('Remarks',)
    list_filter = ('Orders7Days','starttime',)
    search_fields = ('id','itemid','title','Orders7Days',)
    
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':5, 'cols':50})},
        }
    
    
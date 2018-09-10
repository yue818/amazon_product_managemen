# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from .models import *
from django.db import transaction,connection
from django import forms
import xadmin
from django.utils.safestring import mark_safe
from Project.settings import *
from django.contrib import messages  
from django.shortcuts import render_to_response,RequestContext  
from django.template import Context  
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db import models
from xadmin.sites import site
from xadmin.views import BaseAdminPlugin, ListAdminView
from pyapp.models import *
from skuapp.table.t_shopsku_information_binding import t_shopsku_information_binding
from datetime import datetime as ddtime
from pyapp.models import b_goodsskulinkshop as py_b_goodsskulinkshop
from pyapp.models import b_goodssku as py_b_goodssku
import csv
from pyapp.plugin.syn_b_goods_plugin import syn_b_goods_plugin
from skuapp.table.t_product_mainsku_sku import *
from pyapp.modelsadminx.t_cloth_factory_dispatch_apply_Admin import t_cloth_factory_dispatch_apply_Admin
from brick.classredis.classshopsku import classshopsku
from skuapp.table.t_online_info import t_online_info
from django_redis import get_redis_connection
redis_coon = get_redis_connection(alias='product')
classshopsku_obj = classshopsku(db_conn=None,redis_conn=redis_coon)
from pyapp.table.t_cloth_factory_dispatch_apply import t_cloth_factory_dispatch_apply
xadmin.site.register(t_cloth_factory_dispatch_apply,t_cloth_factory_dispatch_apply_Admin)
from pyapp.table.kc_currentstock_sku import kc_currentstock_sku

class t_stockorderm_refund_Admin(object):
    orderm_tree_menu = True
    search_box_flag = True
    
    def show_handle_archive(self, obj):
        rt = '<script>{function update_cg_archive_%s(){var cgcheck =  document.getElementById("cg_%s");'\
            'if(cgcheck.checked==1){$.ajax({url:"/shift_to_archive/",type:"GET",'\
            'contentType:"application/x-www-form-urlencoded:charset=UTF-8",datatype:"json",data:{"index":1,"id":%s},'\
            'success:function(data,textStatus,jqXHR){if(data.status==0)document.getElementById("cgt_id_ts_%s").innerHTML="已归档!";},error:function(data){alert("failed");}})}'\
            'else{$.ajax({url:"/shift_to_archive/",type:"GET",'\
            'contentType:"application/x-www-form-urlencoded:charset=UTF-8",datatype:"json",data:{"index":2,"id":%s},'\
            'success:function(data,textStatus,jqXHR){if(data.status==0)document.getElementById("cgt_id_ts_%s").innerHTML="已取消归档!";},error:function(){alert("failed");}})}}}</script>'\
            '<div><input type="checkbox" id="cg_%s" onclick="update_cg_archive_%s()">'\
            '<span id="cgt_id_ts_%s" style="color:#F00"><span></div>' %(obj.NID,obj.NID,obj.stockordermID,obj.NID,obj.stockordermID,obj.NID,obj.NID,obj.NID,obj.NID)
            
        return mark_safe(rt)
    show_handle_archive.short_description = mark_safe('<p style="width:60px;color:#428bca;">归档</p>')
    
    list_display_links = ('NID',)
    list_display = ('billNumber','refundWay','tradeWay','purchaser','alibabaRefundNumber','refundMoney','transferNumber','refundReason','processer','note','refundDate','show_handle_archive')

    def get_list_queryset(self,):
        request = self.request
        qs = super(t_stockorderm_refund_Admin, self).get_list_queryset()

        refundDateStart = request.GET.get('refundDateStart','')
        refundDateEnd = request.GET.get('refundDateEnd','')
        BillNumber = request.GET.get('BillNumber','')
        BillNumber = [ gs for gs in BillNumber.split(',') if gs ]
        processer = request.GET.get('processer','')
        processer = [ gs for gs in processer.split(',') if gs ]
        Purchaser = request.GET.get('Purchaser','')
        Purchaser = [ gs for gs in Purchaser.split(',') if gs ]
        
        searchList = {'BillNumber__in':BillNumber,'purchaser__in': Purchaser,
                    'processer__in': processer,
                    'MakeDate__gte': refundDateStart, 'MakeDate__lt': refundDateEnd}
            
        sl = {}
        for k,v in searchList.items():
            if isinstance(v,list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception,ex:
                messages.error(request,u'输入的查询数据有问题！')
    
        return qs.filter(refundStatus='A')
xadmin.site.register(t_stockorderm_refund,t_stockorderm_refund_Admin)

class t_stockorderm_refund_track_Admin(object):
    orderm_tree_menu = True
    search_box_flag = True
    
    def show_handle_refund(self, obj):
        rt = '<script>{function update_cg_archive_%s(){var cgcheck =  document.getElementById("cg_%s");'\
            'if(cgcheck.checked==1){$.ajax({url:"/shift_to_archive/",type:"GET",'\
            'contentType:"application/x-www-form-urlencoded:charset=UTF-8",datatype:"json",data:{"index":3,"id":%s},'\
            'success:function(data,textStatus,jqXHR){if(data.status==0)document.getElementById("cgt_id_ts_%s").innerHTML="退款成功!";},error:function(data){alert("failed");}})}'\
            'else{$.ajax({url:"/shift_to_archive/",type:"GET",'\
            'contentType:"application/x-www-form-urlencoded:charset=UTF-8",datatype:"json",data:{"index":4,"id":%s},'\
            'success:function(data,textStatus,jqXHR){if(data.status==0)document.getElementById("cgt_id_ts_%s").innerHTML="已取消退款成功!";},error:function(){alert("failed");}})}}}</script>'\
            '<div><input type="checkbox" id="cg_%s" onclick="update_cg_archive_%s()">'\
            '<span id="cgt_id_ts_%s" style="color:#F00"><span></div>' %(obj.NID,obj.NID,obj.stockordermID,obj.NID,obj.stockordermID,obj.NID,obj.NID,obj.NID,obj.NID)
            
        return mark_safe(rt)
    show_handle_refund.short_description = mark_safe('<p style="width:80px;color:#428bca;">退款成功</p>')

    list_display_links = ('NID',)
    list_display = ('billNumber','refundWay','tradeWay','purchaser','alibabaRefundNumber','refundMoney','transferNumber','refundReason','processer','note','refundDate','show_handle_refund')

    def get_list_queryset(self,):
        request = self.request
        qs = super(t_stockorderm_refund_track_Admin, self).get_list_queryset()

        refundDateStart = request.GET.get('refundDateStart','')
        refundDateEnd = request.GET.get('refundDateEnd','')
        BillNumber = request.GET.get('BillNumber','')
        BillNumber = [ gs for gs in BillNumber.split(',') if gs ]
        processer = request.GET.get('processer','')
        processer = [ gs for gs in processer.split(',') if gs ]
        Purchaser = request.GET.get('Purchaser','')
        Purchaser = [ gs for gs in Purchaser.split(',') if gs ]
        
        searchList = {'BillNumber__in':BillNumber,'purchaser__in': Purchaser,
                    'processer__in': processer,
                    'MakeDate__gte': refundDateStart, 'MakeDate__lt': refundDateEnd}
            
        sl = {}
        for k,v in searchList.items():
            if isinstance(v,list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception,ex:
                messages.error(request,u'输入的查询数据有问题！')
    
        return qs.filter(refundStatus='B')
xadmin.site.register(t_stockorderm_refund_track,t_stockorderm_refund_track_Admin)

class b_supplier_money_Admin(object):
    list_display = ('NID')
xadmin.site.register(b_supplier_money,b_supplier_money_Admin)

class t_stockorderd_Admin(object):

    list_display = ('NID','StockOrderNID','GoodsID')
xadmin.site.register(t_stockorderd, t_stockorderd_Admin)

class t_stockorderm_Admin(object):
    show_warning = True
    search_box_flag = True
    
    def show_SKU_list(self,obj) :
        rt='<table   style="text-align:center;" border="1" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1"><tr bgcolor="#C00"><th style="width:80px;text-align:center">商品SKU</th><th style="width:80px;text-align:center">预计可用库存</th><th style="width:80px;text-align:center">已入库数量</th><th style="width:80px;text-align:center">未入库数量</th></tr>'
        GoodsID_objs = t_stockorderd.objects.filter(StockOrderNID=obj.NID)
        try:
            skulist = []
            if GoodsID_objs:
                #messages.error(self.request,'GoodsID_objs = %s'%GoodsID_objs)       
                for GoodsID_obj in GoodsID_objs:
                    skudict = {}
                        
                    sku_objs = kc_currentstock_sku.objects.filter(GoodsID=GoodsID_obj.GoodsID)
                    if sku_objs:
                        skudict['SKU'] = sku_objs[0].SKU
                        skudict['hopeUseNum'] = sku_objs[0].hopeUseNum
                        skudict['InAmount'] = GoodsID_obj.InAmount
                        skudict['NotInAmount'] = GoodsID_obj.Amount - GoodsID_obj.InAmount
                        skulist.append(skudict)
        except Exception,e:
            messages.error(self.request,'---%s'%repr(e))
        #messages.error(self.request,'-----------%s'%skulist)
        if skulist:
            i = 0
            for skuinfo in skulist:
                if i < 5:
                    rt = '%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> '%(rt,skuinfo['SKU'],skuinfo['hopeUseNum'],skuinfo['InAmount'],skuinfo['NotInAmount'])
                    i = i + 1
            if len(skulist)>5:
                rt = '%s<tr><td><a id="link_id_%s">查看更多</a></td></tr>'%(rt,obj.NID)

        rt = "%s</table><script>$('#link_id_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['500px','500px'],content:'/t_stockorderm_track/t_stockorderm_sku/?track=%s',});});</script>"%(rt,obj.NID,obj.NID)
        return mark_safe(rt)
    show_SKU_list.short_description = mark_safe('<p align="center" style="width:320px;color:#428bca;"> 订单商品</p>')
    
    def show_NotInAmount(self,obj):
        number = round(obj.OrderAmount - obj.InAmount,1)
        return mark_safe(number)
    show_NotInAmount.short_description = mark_safe('<p align="center" style="width:60px;color:#428bca;">未入库数量</p>')
    
    def showStoreName(self,obj):
        rt = ''
        storeName_objs = b_store.objects.filter(NID=obj.StoreID).values()
        if storeName_objs:
            rt = storeName_objs[0]['StoreName']
            
        return mark_safe(rt)
    showStoreName.short_description = mark_safe('<p align="center" style="width:60px;color:#428bca;">采购仓库</p>')
        
    list_display = ('NID','MakeDate','BillNumber','alibabasellername','Recorder','ExpressName','LogisticOrderNo','Note','Memo','showStoreName','OrderAmount','InAmount','show_NotInAmount','SKUCount','show_SKU_list','logisticsStatus','packagestate',)
    #list_editable = ('WarningFlag',)
    #list_filter = ('MakeDate','BillNumber','alibabasellername','Recorder','ExpressName','LogisticOrderNo','Note','Memo','StoreID','ExpressFee','OrderAmount','OrderMoney','InMoney','SKUCount','alibabaorderid','alibabamoney','packagestate','WarningFlag',)
    #search_fields = ('MakeDate','BillNumber','alibabasellername','Recorder','ExpressName','LogisticOrderNo','Note','Memo','StoreID','ExpressFee','OrderAmount','OrderMoney','InMoney','SKUCount','alibabaorderid','alibabamoney','packagestate','WarningFlag',)
    
    def get_list_queryset(self,):
        request = self.request
        qs = super(t_stockorderm_Admin, self).get_list_queryset()

        MakeDateStart = request.GET.get('MakeDateStart','')
        MakeDateEnd = request.GET.get('MakeDateEnd','')
        BillNumber = request.GET.get('BillNumber','')
        alibabasellername = request.GET.get('alibabasellername','')
        Purchaser = request.GET.get('Purchaser','')
        Purchaser = [ gs for gs in Purchaser.split(',') if gs ]
        ExpressName = request.GET.get('ExpressName','')
        
        searchList = {'BillNumber__exact':BillNumber,'Recorder__in': Purchaser,
                    'alibabasellername__exact': alibabasellername,'ExpressName__exact': ExpressName,
                    'MakeDate__gte': MakeDateStart, 'MakeDate__lt': MakeDateEnd}
            
        sl = {}
        for k,v in searchList.items():
            if isinstance(v,list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    #if k == 'ShopName__exact':
                      #  v = 'Wish-' + v.zfill(4)
                        # messages.error(request, v)
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception,ex:
                messages.error(request,u'输入的查询数据有问题！')
    
        return qs    
xadmin.site.register(t_stockorderm, t_stockorderm_Admin)

class b_goodsskulinkshop_Admin(object):
    search_box_flag = True
    list_display=('NID','SKU','ShopSKU','Memo','PersonCode')
    search_fields=('NID','SKU','ShopSKU','Memo','PersonCode')
    
    fields = ('Filename',)

    form_layout = (
        Fieldset(u'请导入解绑文件-格式为"CSV"',
                    Row('Filename'),
                    css_class = 'unsort '
                ),
                  )
    
    actions = ['to_delete',]
    
    def to_delete(self, request, queryset):
        for querysetid in queryset.all():
            t_shopsku_information_binding_objs            = t_shopsku_information_binding()
            t_shopsku_information_binding_objs.SKU        = querysetid.SKU
            t_shopsku_information_binding_objs.ShopSKU    = querysetid.ShopSKU
            t_shopsku_information_binding_objs.Memo       = querysetid.Memo
            t_shopsku_information_binding_objs.PersonCode = querysetid.PersonCode
            t_shopsku_information_binding_objs.Submitter     = request.user.first_name
            t_shopsku_information_binding_objs.SubmitTime    = ddtime.now()
            t_shopsku_information_binding_objs.BindingStatus = u'Unbind'#解绑
            t_shopsku_information_binding_objs.save()

            if len(querysetid.Memo)>=9:
                shopcode = querysetid.Memo[0:9]
            else:
                shopcode = querysetid.Memo

            t_online_info.objects.filter(ShopSKU=querysetid.ShopSKU,ShopName=shopcode).update(SKU=None,MainSKU=None) # 清除online绑定关系

            classshopsku_obj.delsku(querysetid.ShopSKU) # 删除redis数据
            querysetid.delete()

    to_delete.short_description = u'解绑删除'
    
    
    def save_models(self):
        obj     = self.new_obj
        request = self.request

        logger  = logging.getLogger('sourceDns.webdns.views')

        try :
            if obj.Filename is not None and str(obj.Filename).strip() !='' :
                i = 0
                for row in csv.reader(obj.Filename):#obj.Status本身就是16进制字节流，直接reader
                    if i < 1:
                        i = i + 1
                        continue
                    i = i + 1

                    b_goodsskulinkshop_objs = py_b_goodsskulinkshop.objects.filter(SKU = row[0].decode("GBK"),ShopSKU = row[1].decode("GBK"))
                    
                    if b_goodsskulinkshop_objs.exists() :

                        ShopSKU = row[1].decode("GBK")
                        classshopsku_obj.delsku(ShopSKU) # 删除redis中店铺SKU和商品SKU的对应关系

                        if len(row[2].decode("GBK")) >= 9:
                            shopcode = (row[2].decode("GBK"))[0:9]
                        else:
                            shopcode = row[2].decode("GBK")

                        t_online_info.objects.filter(ShopSKU=ShopSKU, ShopName=shopcode).update(SKU=None,MainSKU=None)

                        b_goodsskulinkshop_objs.delete()

                        t_shopsku_information_binding_objs = t_shopsku_information_binding()
                        t_shopsku_information_binding_objs.SKU                 = row[0].decode("GBK") #
                        t_shopsku_information_binding_objs.ShopSKU             = ShopSKU
                        t_shopsku_information_binding_objs.Memo                = row[2].decode("GBK") #/
                        t_shopsku_information_binding_objs.PersonCode          = row[3].decode("GBK") #
                        t_shopsku_information_binding_objs.Filename            = obj.Filename
                        t_shopsku_information_binding_objs.Submitter           = request.user.first_name
                        t_shopsku_information_binding_objs.SubmitTime          = ddtime.now()
                        t_shopsku_information_binding_objs.BindingStatus       = u'Unbind'#解除绑定
                        
                        t_shopsku_information_binding_objs.save()

        except Exception,ex :
            logger.error('%s============================%s'%(Exception,ex))
            messages.error(request,'%s============================%s'%(Exception,ex))
            
    def get_list_queryset(self,):
        request = self.request
        qs = super(b_goodsskulinkshop_Admin, self).get_list_queryset()

        sku = request.GET.get('sku','')
        sku_list=sku.split(',')
        sku_list2=[]
        for sku_l in  sku_list:
            for s in t_product_mainsku_sku.objects.filter(MainSKU=sku_l).values_list('ProductSKU',flat=True):
                sku_list2.append(s)
        for s in  sku_list:
            sku_list2.append(s)

        shopSKU = request.GET.get('shopSKU','')
        shopSKU_list=shopSKU.split(',')
        shopSKU_list2=[]
        for s in shopSKU_list:
            shopSKU_list2.append(s.decode('utf-8'))

        memo = request.GET.get('memo','')
        personCode = request.GET.get('personCode','')
        if(sku==''and shopSKU!=''):
            searchList = {'ShopSKU__in': shopSKU_list2,
                          'Memo__exact':memo, 'PersonCode__exact': personCode,
                          }
        elif(shopSKU==''and  sku!=''):
            searchList = {'SKU__in': sku_list2,
                          'Memo__exact':memo, 'PersonCode__exact': personCode,
                          }
        elif(sku==''and shopSKU==''):
            searchList = {
                      'Memo__exact':memo, 'PersonCode__exact': personCode,
                      }
        else:
            searchList = {'SKU__in': sku_list2,'ShopSKU__in': shopSKU_list2,
                'Memo__exact':memo, 'PersonCode__exact': personCode,
            }
        sl = {}
        for k,v in searchList.items():
            if isinstance(v,list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    #if k == 'ShopName__exact':
                      #  v = 'Wish-' + v.zfill(4)
                        # messages.error(request, v)
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception,ex:
                messages.error(request,u'输入的查询数据有问题！')
    
        return qs    
    
# xadmin.site.register(b_goodsskulinkshop,b_goodsskulinkshop_Admin)
class t_syn_tables_Admin(object):
    list_display=('id','TableName','AllCount','BeginTime','EndTime')
    search_fields=('id','TableName','AllCount','BeginTime','EndTime')
xadmin.site.register(t_syn_tables,t_syn_tables_Admin)
"""
class b_packinfo_Admin(object):
    list_display=('NID','PackCode','PackName','CostPrice','Used','Remark','Weight','BarCode',)
    search_fields=('NID','PackCode','PackName','CostPrice','Used','Remark','Weight','BarCode',)
xadmin.site.register(xxxb_packinfo,b_packinfo_Admin)
"""
class b_goods_Admin(object):
    py_search_flag = True
    actions = ['get_pic']
    def get_pic(self, request, queryset):
        logger = logging.getLogger('sourceDns.webdns.views')
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_PY)
        for querysetid in queryset.all():
            SKU = querysetid.SKU
            SKU = SKU.replace('OAS-','').replace('FBA-','')
            oss_pic = '%s.jpg'%SKU
            exist = bucket.object_exists(oss_pic)
            if exist:
                messages.error(request,"%s :exist"%(SKU))
                logger.error("%s :exist"%(SKU))
                continue
            picurls = 'http://fancyqube.net:89/ShopElf/images/%s.jpg'%(SKU)
            image_bytes = None
            if  picurls is not None :
                try:
                    req = urllib2.Request(picurls)
                    image_bytes = urllib2.urlopen(req, timeout = 15).read()
                except urllib2.HTTPError, e:
                    messages.error(request,e.reason)
                    logger.error("%s :error"%(SKU))
                    continue
                except urllib2.URLError, e:
                    messages.error(request,e.reason)
                    logger.error("%s :error"%(SKU))
                    continue
                if image_bytes is not None:
                    bucket.put_object(u'%s.jpg'%(SKU),image_bytes)
    get_pic.short_description = u'获取普源图片'
    def show_BmpUrl(self,obj) :
        SKU = obj.SKU
        SKU = SKU.replace('OAS-','').replace('FBA-','')
        picurls = 'http://fancyqube.net:89/ShopElf/images/%s.jpg'%(SKU)
        #BmpUrl = u'%s%s.%s/%s.jpg'%(PREFIX,BUCKETNAME_PY,ENDPOINT_OUT,SKU)
        rt =  '<img src="%s"  width="80" height="80"  alt = "%s"  title="%s"  />  '%(picurls,picurls,picurls)
        return mark_safe(rt)
    show_BmpUrl.short_description = u'普源图'
    list_export =()
    list_per_page=50
    show_detail_fields  =  [ 'NID',]
    list_display= ('NID','show_BmpUrl','GoodsCategoryID','CategoryCode','GoodsCode','GoodsName','GoodsStatus','SKU','Material','Class',
                    'Unit','Quantity','SalePrice','CostPrice','GoodsStatus','SalerName','SalerName2','Purchaser','possessMan2','Notes',)
    list_filter = ('GoodsStatus','GoodsCategoryID',) #'SalerName','SalerName2','Purchaser','possessMan2',)
    readonly_fields = ('NID','GoodsCategoryID','CategoryCode','GoodsCode','GoodsName','ShopTitle','SKU','BarCode','FitCode','MultiStyle','Material','Class','Model',
                    'Unit','Style','Brand','LocationID','Quantity','SalePrice','CostPrice','AliasCnName','AliasEnName','Weight','DeclaredValue','OriginCountry','OriginCountryCode',
                    'ExpressID','Used','BmpFileName','BmpUrl','MaxNum','MinNum','GoodsCount','SupplierID','SupplierName','Notes','SampleFlag','SampleCount','SampleMemo','CreateDate','GroupFlag','SalerName',
                    'SellCount','SellDays','PackFee','PackName','GoodsStatus','DevDate','SalerName2','BatchPrice','MaxSalePrice','RetailPrice','MarketPrice','PackageCount','ChangeStatusTime',
                    'StockDays','StoreID','Purchaser','LinkUrl','LinkUrl2','LinkUrl3','StockMinAmount','MinPrice','HSCODE','ViewUser','InLong','InWide','InHigh','InGrossweight','InNetweight',
                    'OutLong','OutWide','OutHigh','OutGrossweight','OutNetweight','ShopCarryCost','ExchangeRate','WebCost','PackWeight','LogisticsCost','GrossRate','CalSalePrice','CalYunFei',
                    'CalSaleAllPrice','PackMsg','ItemUrl','IsCharged','DelInFile','Season','IsPowder','IsLiquid','possessMan1','possessMan2','LinkUrl4','LinkUrl5','LinkUrl6','isMagnetism',
                    'NoSalesDate',)
    search_fields = ('NID','GoodsCategoryID','CategoryCode','GoodsCode','GoodsName','ShopTitle','SKU','BarCode','FitCode','MultiStyle','Material','Class','Model',
                    'Unit','Style','Brand','LocationID','Quantity','SalePrice','CostPrice','AliasCnName','AliasEnName','Weight','DeclaredValue','OriginCountry','OriginCountryCode',
                    'ExpressID','Used','BmpFileName','BmpUrl','MaxNum','MinNum','GoodsCount','SupplierID','SupplierName','Notes','SampleFlag','SampleCount','SampleMemo','GroupFlag','SalerName',
                    'SellCount','SellDays','PackFee','PackName','GoodsStatus','SalerName2','BatchPrice','MaxSalePrice','RetailPrice','MarketPrice','PackageCount',
                    'StockDays','StoreID','Purchaser','LinkUrl','LinkUrl2','LinkUrl3','StockMinAmount','MinPrice','HSCODE','ViewUser','InLong','InWide','InHigh','InGrossweight','InNetweight',
                    'OutLong','OutWide','OutHigh','OutGrossweight','OutNetweight','ShopCarryCost','ExchangeRate','WebCost','PackWeight','LogisticsCost','GrossRate','CalSalePrice','CalYunFei',
                    'CalSaleAllPrice','PackMsg','ItemUrl','IsCharged','DelInFile','Season','IsPowder','IsLiquid','possessMan1','possessMan2','LinkUrl4','LinkUrl5','LinkUrl6','isMagnetism',
                    )

    def get_list_queryset(self):
        request = self.request
        qs = super(b_goods_Admin, self).get_list_queryset()
        GET = request.GET
        SKU = GET.get('sku','')
        GoodsName = GET.get('name','')
        GoodsStatus = GET.get('state','')
        Cate1 = GET.get('cate1','')
        Cate2 = GET.get('cate2','')

        if Cate1 != '':
            if Cate2 != '':
                qs = qs.filter(CategoryCode=Cate2)
            else:
                qs = qs.filter(CategoryCode=Cate1)

        if SKU != '':
            SKU = SKU.replace(' ','')
            if ',' in SKU:
                skuList = SKU.split(',')
            else:
                skuList = SKU.split('，')
            qs = qs.filter(SKU__in=skuList)

        if GoodsStatus != '':
            qs = qs.filter(GoodsStatus__in=GoodsStatus.split(','))

        if GoodsName != '':
            qs = qs.filter(GoodsName__contains=GoodsName)

        return qs



xadmin.site.register(b_goods, b_goods_Admin)
'''
class t_product_B_SupplierAdmin(admin.ModelAdmin):
    list_display = ('id','NID','SupplierName')
    fields=(('id','NID','SupplierName',),)
    list_display_links = ('id',)
    readonly_fields =('id',)
    
adminx.site.register(t_product_B_Supplier, t_product_B_SupplierAdmin)
'''
from skuapp.plugin.py_searchPlugin import *
from skuapp.plugin.t_stockordermPlugin import *
xadmin.site.register_plugin(py_searchPlugin, ListAdminView)
xadmin.site.register_plugin(t_stockordermPlugin, ListAdminView)

from pyapp.plugin.create_cg_data_Plugin import *
xadmin.site.register_plugin(create_cg_data_Plugin, BaseAdminView)
from pyapp.table.t_product_b_goods import *
from pyapp.modelsadminx.t_product_b_goods_all_productsku_Admin import *
xadmin.site.register(t_product_b_goods, t_product_b_goods_all_productsku_Admin)
xadmin.site.register_plugin(syn_b_goods_plugin,ListAdminView)

from pyapp.table.kc_currentstock_sku import *
from pyapp.modelsadminx.kc_currentstock_sku_Admin import *
xadmin.site.register(kc_currentstock_sku, kc_currentstock_sku_Admin)
from pyapp.plugin.kc_downloadcsv_Plugin import *
xadmin.site.register_plugin(kc_downloadcsv_Plugin,ListAdminView)
from pyapp.plugin.search_purchaser_Plugin import *
xadmin.site.register_plugin(search_purchaser_Plugin,ListAdminView)
from pyapp.plugin.site_left_menu_Plugin_kc import *
xadmin.site.register_plugin(site_left_menu_Plugin_kc,BaseAdminView)

from pyapp.table.kc_currentstock_sku_log import *
from pyapp.modelsadminx.kc_currentstock_sku_log_Admin import *
xadmin.site.register(kc_currentstock_sku_log, kc_currentstock_sku_log_Admin)
from pyapp.plugin.purchaser_handle_Plugin import *
xadmin.site.register_plugin(purchaser_handle_Plugin,BaseAdminView)

from pyapp.table.kc_currentstock_sku_log_check import *
from pyapp.modelsadminx.kc_currentstock_sku_log_check_Admin import *
xadmin.site.register(kc_currentstock_sku_log_check, kc_currentstock_sku_log_check_Admin)
from pyapp.plugin.update_purchaserData_Plugin import *
xadmin.site.register_plugin(update_purchaserData_Plugin,BaseAdminView)
from pyapp.plugin.site_left_menu_Plugin_sh import *
xadmin.site.register_plugin(site_left_menu_Plugin_sh,BaseAdminView)
from pyapp.plugin.check_Remark_Plugin import *
xadmin.site.register_plugin(check_Remark_Plugin,BaseAdminView)

from pyapp.plugin.show_dataflag_Plugin import *
xadmin.site.register_plugin(show_dataflag_Plugin,BaseAdminView)

from pyapp.table.kc_currentstock_sku_log_realtime import *
from pyapp.modelsadminx.kc_currentstock_sku_log_realtime_Admin import *
xadmin.site.register(kc_currentstock_sku_log_realtime, kc_currentstock_sku_log_realtime_Admin)

from pyapp.table.kc_currentstock_sku_log_ed import *
from pyapp.modelsadminx.kc_currentstock_sku_log_ed_Admin import *
xadmin.site.register(kc_currentstock_sku_log_ed, kc_currentstock_sku_log_ed_Admin)

from pyapp.table.kc_currentstock_sku_log_ignore import *
from pyapp.modelsadminx.kc_currentstock_sku_log_ignore_Admin import *
xadmin.site.register(kc_currentstock_sku_log_ignore, kc_currentstock_sku_log_ignore_Admin)

from pyapp.table.kc_currentstock_sku_log_abnormal import *
from pyapp.modelsadminx.kc_currentstock_sku_log_abnormal_Admin import *
xadmin.site.register(kc_currentstock_sku_log_abnormal, kc_currentstock_sku_log_abnormal_Admin)

from pyapp.table.kc_currentstock_sku_log_check_abnormal import *
from pyapp.modelsadminx.kc_currentstock_sku_log_check_abnormal_Admin import *
xadmin.site.register(kc_currentstock_sku_log_check_abnormal, kc_currentstock_sku_log_check_abnormal_Admin)

from pyapp.table.kc_currentstock_sku_statistics import *
from pyapp.modelsadminx.kc_currentstock_sku_statistics_Admin import *
from pyapp.plugin.kc_currentstock_sku_statistics_plugin import *
xadmin.site.register(kc_currentstock_sku_statistics, kc_currentstock_sku_statistics_Admin)
xadmin.site.register_plugin(kc_currentstock_sku_statistics_plugin, ListAdminView)
from pyapp.table.kc_currentstock_sku_log_history import *
from pyapp.modelsadminx.kc_currentstock_sku_log_history_Admin import *
xadmin.site.register(kc_currentstock_sku_log_history, kc_currentstock_sku_log_history_Admin)

from pyapp.table.kc_currentstock_cg_purchaser import *
from pyapp.modelsadminx.kc_currentstock_cg_purchaser_Admin import *
xadmin.site.register(kc_currentstock_cg_purchaser,kc_currentstock_cg_purchaser_Admin)

from pyapp.table.kc_currentstock_sku_notsuggest import *
from pyapp.modelsadminx.kc_currentstock_sku_notsuggest_Admin import *
xadmin.site.register(kc_currentstock_sku_notsuggest,kc_currentstock_sku_notsuggest_Admin)

from pyapp.table.kc_currentstock_sku_log_check_error import *
from pyapp.modelsadminx.kc_currentstock_sku_log_check_error_Admin import *
xadmin.site.register(kc_currentstock_sku_log_check_error,kc_currentstock_sku_log_check_error_Admin)

from pyapp.table.kc_currentstock_sku_log_frequent import *
from pyapp.modelsadminx.kc_currentstock_sku_log_frequent_Admin import *
xadmin.site.register(kc_currentstock_sku_log_frequent,kc_currentstock_sku_log_frequent_Admin)

from pyapp.table.kc_currentstock_sku_sales import *
from pyapp.modelsadminx.kc_currentstock_sku_sales_Admin import *
xadmin.site.register(kc_currentstock_sku_sales,kc_currentstock_sku_sales_Admin)
from pyapp.models import b_goodsskulinkshop
from pyapp.modelsadminx.b_goodsskulinkshop_v2_Admin import b_goodsskulinkshop_v2_Admin
xadmin.site.register(b_goodsskulinkshop,b_goodsskulinkshop_v2_Admin)


from pyapp.models import t_log_sku_shopsku_apply
from pyapp.modelsadminx.t_log_sku_shopsku_apply_Admin import t_log_sku_shopsku_apply_Admin
xadmin.site.register(t_log_sku_shopsku_apply, t_log_sku_shopsku_apply_Admin)


from pyapp.models import t_log_sku_shopsku_change
from pyapp.modelsadminx.t_log_sku_shopsku_change_Admin import t_log_sku_shopsku_change_Admin
xadmin.site.register(t_log_sku_shopsku_change, t_log_sku_shopsku_change_Admin)


from xadmin.views import BaseAdminView
from pyapp.plugin.sku_apply_change_Plugin import sku_apply_change_Plugin
xadmin.site.register_plugin(sku_apply_change_Plugin,BaseAdminView)

from xadmin.views import BaseAdminView
from pyapp.plugin.sku_apply_change_hide_original_button_Plugin import sku_apply_change_hide_original_button_Plugin
xadmin.site.register_plugin(sku_apply_change_hide_original_button_Plugin, BaseAdminView)

from pyapp.plugin.oscode_explain_Plugin import oscode_explain_Plugin
xadmin.site.register_plugin(oscode_explain_Plugin,ListAdminView)

from pyapp.table.t_product_b_goods_supplier_modify import t_product_b_goods_supplier_modify
from pyapp.modelsadminx.t_product_b_goods_supplier_modify_Admin import t_product_b_goods_supplier_modify_Admin
xadmin.site.register(t_product_b_goods_supplier_modify,t_product_b_goods_supplier_modify_Admin)

from pyapp.plugin.modify_b_goods_supplier_Plugin import modify_b_goods_supplier_Plugin
xadmin.site.register_plugin(modify_b_goods_supplier_Plugin,ListAdminView)

from pyapp.table.kc_unsalable_dispose import kc_unsalable_dispose
from pyapp.modelsadminx.kc_unsalable_dispose_Admin import kc_unsalable_dispose_Admin
xadmin.site.register(kc_unsalable_dispose, kc_unsalable_dispose_Admin)

from pyapp.plugin.kc_unsalable_dispose_tree_Plugin import kc_unsalable_dispose_tree_Plugin
xadmin.site.register_plugin(kc_unsalable_dispose_tree_Plugin, ListAdminView)
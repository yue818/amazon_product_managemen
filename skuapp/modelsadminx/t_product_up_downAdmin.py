# -*- coding: utf-8 -*-
from .t_product_Admin import *
from skuapp.table.t_config_ip_ext import *
from django.utils.safestring import mark_safe
from skuapp.table.t_sys_param import *
from django.contrib import messages
from django.db.models import Q
from pyapp.models import b_goods as py_b_goods
from pyapp.models import B_Supplier as sku_b_supplier
from skuapp.table.t_product_up_down import *
import time,datetime
from skuapp.table.t_product_information_modify import *
from brick.classredis.classsku import classsku
from django_redis import get_redis_connection
redis_coon = get_redis_connection(alias='product')
classsku_obj = classsku(db_cnxn=connection, redis_cnxn=redis_coon)



class t_product_up_downAdmin(object):
    show_search_sku = True
    show_type_product = True
    
    def show_url(self,obj):
        #messages.info(self.request,obj.Supplier_url)
        self.show_supplier(obj)
        rt = ''
        if obj.Supplier_url == 'None' or obj.Supplier_url == '' or obj.Supplier_url is None:
            rt = ''
        else:
            urls = re.sub(r'[^\x00-\x7f]', ' ', obj.Supplier_url)
            n=1
            url_objs = urls.split(';')
            for url_obj in url_objs:
                if url_obj != '' and url_obj is not None:
                    rt = '%s<a href="%s" target="_blank">供应商%s</a><br/>'%(rt,url_obj,n)
                    n+=1
        return mark_safe(rt)
    show_url.short_description = u'供应商链接'
    
    def delay_out(self,obj):
        rt = '<input type="button" value="延期" id="cc_%s"></input>'%(obj.id)
        rt = "%s<script>$('#cc_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'延期(填写整数)',fix:false,shadeClose: true,maxmin:true,area:['300px','100px'],content:'/t_product_up_down/delay/?id=%s&add_date=%s&SKU=%s',end:function(){location.reload();}});});</script>"%(rt,obj.id,obj.id,obj.Add_Date,obj.SKU) 
        return mark_safe(rt)
    delay_out.short_description = u'延期操作'

    def show_supplier(self,obj):
        try:
            sn = sku_b_supplier.objects.filter(NID=obj.SupplierID).values_list('SupplierName')[0][0]
        except:
            sn = ''
        t_product_up_down.objects.filter(SupplierID=obj.SupplierID).update(Supplier=sn)
        #messages.info(self.request,sn)
    def show_Add_Date(self,obj):
        if '%s'%obj.Add_Date <= datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S') and obj.Goods_Status == '0':
            rt = u'<div style="width:100px;height:30px;background-color:red">%s</div>'%(obj.Add_Date.strftime('%Y年%m月%d日'))
        else:
            rt = u'%s'%(obj.Add_Date.strftime('%Y年%m月%d日'))
        return mark_safe(rt)
    show_Add_Date.short_description = u'截止日期'
    
    #def Goods_off(self, request, queryset):
    #    for qs in queryset.all():
    #        xgms = '备注：%s<br>%s天后<br>%s重新上架'%(qs.Remark,qs.day_obj,qs.Add_Date.strftime('%Y年%m月%d日'))
    #        t_obj = t_product_information_modify.objects.filter(SKU=qs.SKU).values('MainSKU','Name2','DevDate','SourcePicPath2','InputBox',)
    #        if len(list(t_obj)) != 0:
    #            t_product_information_modify.objects.create(Mstatus='DLQ',SQTimeing=qs.Request_date,SKU=qs.SKU,MainSKU=t_obj[0]['MainSKU'],Name2=t_obj[0]['Name2'],SourcePicPath2=t_obj[0]['SourcePicPath2'],InputBox=t_obj[0]['InputBox'],DevDate=t_obj[0]['DevDate'],Select='2',SQStaffNameing=qs.Request_man,XGcontext=xgms)
    #        else:
    #            t_product_information_modify.objects.create(Mstatus='DLQ',SQTimeing=qs.Request_date,SKU=qs.SKU,Select='2',SQStaffNameing=qs.Request_man,XGcontext=xgms)
    #Goods_off.short_description = u'临时下架'

    def base_func(self, queryset, select, goods_status, target, Mstatus):
        import datetime
        input_box = []
        details = {}
        goods_name = ''
        dev_date = None
        main_sku = ''
        pic = ''
        sku = ''

        for qs in queryset.all():
            sku = str(qs.SKU)
            if target == u'清仓下架(需审核)':
                xgms = u'备注：原供应商没货，找不到可替代供应商，申请清仓下架'
            elif target == u'售完下架(需审核)':
                xgms = u'备注：原供应商没货，找不到可替代供应商，申请售完下架'
            else:
                xgms = u'备注：%s;供应正常' % (qs.Remark)
            temp_main_sku = classsku_obj.get_bemainsku_by_sku(sku=sku)
            current_status = classsku_obj.get_goodsstatus_by_sku(sku=sku)
            input_box.append(sku)

            if main_sku != '':
                if main_sku != temp_main_sku:
                    t_product_information_modify.objects.create(
                        Mstatus=Mstatus, SQTimeing=datetime.datetime.now(), SKU=sku, MainSKU=main_sku,
                        Name2=goods_name, SourcePicPath2=pic, InputBox=','.join(input_box), Details=details,
                        DevDate=dev_date, Select=select, SQStaffNameing=qs.Request_man, XGcontext='')

                    details = {}
                    input_box = []
                    main_sku = temp_main_sku
                    pic = u'http://fancyqube.net:89/ShopElf/images/%s.jpg' % sku.replace('OAS-', '').replace('FBA-', '')
                    details[sku] = {'GoodsStatus': [u'当前状态', current_status, target, xgms, target]}
                    py_b_goods_obj = py_b_goods.objects.filter(SKU=sku).values('GoodsName', 'CreateDate')
                    if py_b_goods_obj.exists():
                        goods_name = py_b_goods_obj[0]['GoodsName']
                        dev_date = py_b_goods_obj[0]['CreateDate']
                else:
                    details[sku] = {'GoodsStatus': [u'当前状态', current_status, target, xgms, target]}
            else:
                main_sku = temp_main_sku
                details[sku] = {'GoodsStatus': [u'当前状态', current_status, target, xgms, target]}
                py_b_goods_obj = py_b_goods.objects.filter(SKU=sku).values('GoodsName', 'CreateDate')
                pic = u'http://fancyqube.net:89/ShopElf/images/%s.jpg' % sku.replace('OAS-', '').replace('FBA-', '')
                if py_b_goods_obj.exists():
                    goods_name = py_b_goods_obj[0]['GoodsName']
                    dev_date = py_b_goods_obj[0]['CreateDate']
        t_product_information_modify.objects.create(
            Mstatus=Mstatus, SQTimeing=datetime.datetime.now(), SKU=sku, MainSKU=main_sku,
            Name2=goods_name, SourcePicPath2=pic, InputBox=','.join(input_box), Details=details,
            DevDate=dev_date, Select=select, SQStaffNameing=qs.Request_man, XGcontext='')

        queryset.update(Goods_Status=goods_status)
    
    def Goods_on(self, request, queryset):
        self.base_func(queryset=queryset, select='8', goods_status='1', target=u'重新上架', Mstatus='DLQ')

        # import datetime
        # for qs in queryset.all():
        #     xgms = '备注：%s<br>供应正常' % (qs.Remark)
        #     t_obj = t_product_information_modify.objects.filter(SKU=qs.SKU)
        #     pic = u'http://fancyqube.net:89/ShopElf/images/%s.jpg' % qs.SKU.replace('OAS-', '').replace('FBA-', '')
        #     if t_obj:
        #         t_obj = t_obj.values('MainSKU', 'Name2', 'DevDate', 'SourcePicPath2', 'InputBox', )
        #         t_product_information_modify.objects.create(Mstatus='DLQ', SQTimeing=datetime.datetime.now(),
        #                                                     SKU=qs.SKU, MainSKU=t_obj[0]['MainSKU'],
        #                                                     Name2=t_obj[0]['Name2'],
        #                                                     SourcePicPath2=t_obj[0]['SourcePicPath2'], InputBox=qs.SKU,
        #                                                     DevDate=t_obj[0]['DevDate'], Select='8',
        #                                                     SQStaffNameing=qs.Request_man, XGcontext=xgms)
        #     else:
        #         t_product_information_modify.objects.create(Mstatus='DLQ', SQTimeing=datetime.datetime.now(),
        #                                                     SKU=qs.SKU, InputBox=qs.SKU, Select='8',
        #                                                     SQStaffNameing=qs.Request_man, XGcontext=xgms,
        #                                                     SourcePicPath2=pic)
        #     t_product_up_down.objects.filter(SKU=qs.SKU).update(Goods_Status='1')
    Goods_on.short_description = u'重新上架'
    
    def Goods_qcxj(self,request,queryset):
        self.base_func(queryset=queryset, select='5', goods_status='2', target=u'清仓下架(需审核)', Mstatus='DSH')

        # import datetime
        # for qs in queryset.all():
        #     xgms = '备注：原供应商没货，找不到可替代供应商，申请清仓下架'
        #     t_obj = t_product_information_modify.objects.filter(SKU=qs.SKU)
        #     pic = u'http://fancyqube.net:89/ShopElf/images/%s.jpg'%qs.SKU.replace('OAS-','').replace('FBA-','')
        #     if t_obj:
        #         t_obj = t_obj.values('MainSKU','Name2','DevDate','SourcePicPath2','InputBox',)
        #         t_product_modify_review.objects.create(Mstatus='DSH',SQTimeing=datetime.datetime.now(),SKU=qs.SKU,MainSKU=t_obj[0]['MainSKU'],Name2=t_obj[0]['Name2'],SourcePicPath2=t_obj[0]['SourcePicPath2'],InputBox=qs.SKU,DevDate=t_obj[0]['DevDate'],Select='5',SQStaffNameing=qs.Request_man,XGcontext=xgms)
        #     else:
        #         t_product_modify_review.objects.create(Mstatus='DSH',SQTimeing=datetime.datetime.now(),SKU=qs.SKU,InputBox=qs.SKU,Select='5',SQStaffNameing=qs.Request_man,XGcontext=xgms,SourcePicPath2=pic)
        #     t_product_up_down.objects.filter(SKU=qs.SKU).update(Goods_Status='2')
    Goods_qcxj.short_description = u'清仓下架'
    
    def Goods_swxj(self,request,queryset):
        self.base_func(queryset=queryset, select='9', goods_status='3', target=u'售完下架(需审核)', Mstatus='DSH')

        # import datetime
        # for qs in queryset.all():
        #     xgms = '备注：原供应商没货，找不到可替代供应商，申请售完下架'
        #     t_obj = t_product_information_modify.objects.filter(SKU=qs.SKU)
        #     pic = u'http://fancyqube.net:89/ShopElf/images/%s.jpg'%qs.SKU.replace('OAS-','').replace('FBA-','')
        #     if t_obj:
        #         t_obj = t_obj.values('MainSKU','Name2','DevDate','SourcePicPath2','InputBox',)
        #         t_product_modify_review.objects.create(Mstatus='DSH',SQTimeing=datetime.datetime.now(),SKU=qs.SKU,MainSKU=t_obj[0]['MainSKU'],Name2=t_obj[0]['Name2'],SourcePicPath2=t_obj[0]['SourcePicPath2'],InputBox=qs.SKU,DevDate=t_obj[0]['DevDate'],Select='9',SQStaffNameing=qs.Request_man,XGcontext=xgms)
        #     else:
        #         t_product_modify_review.objects.create(Mstatus='DSH',SQTimeing=datetime.datetime.now(),SKU=qs.SKU,InputBox=qs.SKU,Select='9',SQStaffNameing=qs.Request_man,XGcontext=xgms,SourcePicPath2=pic)
        #     t_product_up_down.objects.filter(SKU=qs.SKU).update(Goods_Status='3')
    Goods_swxj.short_description = u'售完下架'
    
    actions = ['Goods_on','Goods_qcxj','Goods_swxj']
             
    list_display= ('SKU','Goods_Name','Goods_Status','Purchase_man','Producer','Supplier','show_url','Goodsbirth','Request_man','Request_date','sum','Remark','delay_out','show_Add_Date',)
    list_editable = ('Remark',)

    fields = ('SKU',)

    list_filter = ('SKU','Goods_Name','Goods_Status','Purchase_man','Producer','Supplier','Supplier_url','Request_man','Remark','Add_Date')

    search_fields = ('SKU','Goods_Name','Goods_Status','Purchase_man','Producer','Supplier','Supplier_url','Request_man','Remark')

    #readonly_fields = ()

    show_detail_fields = ['id']
    
    def get_list_queryset(self,):
        from skuapp.table.t_sys_staff_auth import t_sys_staff_auth
        request = self.request
        flag = 0
        try:
            flag = t_sys_staff_auth.objects.filter(StaffID=request.user.username,urltable="t_product_up_down").count()
        except:
            pass
        qs = super(t_product_up_downAdmin, self).get_list_queryset()        
        status = request.GET.get('status', '') 
        if status == 'down':
            qs = qs.filter(Goods_Status__in='0')
        elif status == 'up':
            qs = qs.filter(Goods_Status__in='1')
        elif status == 'cleardown':
            qs = qs.filter(Goods_Status__in='2')   
        elif status == 'selldown':
            qs = qs.filter(Goods_Status__in='3')            
        else:
            qs = qs
        if request.user.is_superuser or flag != 0:
            return qs
        else:
            return qs.filter(Q(Purchase_man=request.user.first_name)|Q(Producer=request.user.first_name)|Q(Request_man=request.user.first_name))




            
            
            
            
            
            
            
            
# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from skuapp.table.t_product_inventory_warnning import t_product_inventory_warnning
from django.contrib import messages
import requests,oss2,math
from Project.settings import *
from django.http import HttpResponseRedirect
#from brick.pydata.py_redis.py_SynRedis_pub import py_SynRedis_pub
from brick.classredis.classsku import classsku
from brick.classredis.classmainsku import classmainsku
from django.db import connection
from datetime import datetime
from .t_product_Admin import *
from django_redis import get_redis_connection
redis_conn = get_redis_connection(alias='product')
classmainsku_obj = classmainsku(connection,redis_conn)
#py_SynRedis_obj = py_SynRedis_pub()
classsku_obj = classsku(connection,redis_conn)
from pyapp.table.t_product_b_goods import t_product_b_goods

def get_ontheWayNumber(MainSKU,storeName):
    number = 0.0
    if storeName == '浦江仓库':
        mainsku_list = classmainsku_obj.get_sku_by_mainsku(MainSKU)  
        if mainsku_list:
            for sku in mainsku_list:
                 #notInNumber = py_SynRedis_obj.getFromHashRedis('',sku,'19')
                notInNumber = classsku_obj.get_uninstore_by_sku(sku)
                if notInNumber == -1 or notInNumber == -2 or notInNumber is None:
                    number = 0.0
                    continue
                number += float(notInNumber)
    return number
class t_product_inventory_warnning_Admin(object):
    search_box_flag = True
    show_kc_refresh = True
    #kc_flag = True
    downloadxls = True
    kc_jump = True
    #show_kc = True
    actions = ['to_export_kc_kurent','to_apply_Handle','to_apply_Ignore']
    
    def to_export_kc_kurent(self,request,queryset):
        from xlwt import *
        
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s'%(MEDIA_ROOT + 'download_xls'))
        
        mkdir_p(path)
        os.popen('chmod 777 %s'%(path))
        
        w = Workbook()
        sheet = w.add_sheet(u'库存预警')
        
        sheet.write(0,0,u'id')
        sheet.write(0,1,u'主sku')
        sheet.write(0,2,u'状态')
        sheet.write(0,3,u'侵权站点')
        sheet.write(0,4,u'商品名称')
        sheet.write(0,5,u'业绩归属人2')
        sheet.write(0,6,u'采购员')
        sheet.write(0,7,u'7天销量')
        sheet.write(0,8,u'15天销量')
        sheet.write(0,9,u'30天销量')
        sheet.write(0,10,u'可用数量')
        sheet.write(0,11,u'库存数量')
        sheet.write(0,12,u'采购未入库')
        sheet.write(0,13,u'可售天数')
        sheet.write(0,14,u'商品创建时间')
        sheet.write(0,15,u'网址6')
        sheet.write(0,16,u'商品成本单价')
        sheet.write(0,17,u'商品重量')
        sheet.write(0,18,u'库存金额')
        sheet.write(0,19,u'仓库')
        sheet.write(0,20,u'商品类型')
        sheet.write(0,21,u'销售总金额')
        sheet.write(0,22,u'首次预警')
        sheet.write(0,23,u'突变系数')
        sheet.write(0,24,u'处理时间')
        sheet.write(0,25,u'处理状态')
        sheet.write(0,26,u'处理人')
        sheet.write(0,27,u'处理结果1')
        sheet.write(0,28,u'处理结果2')
        sheet.write(0,29,u'数据同步时间')
        
        row = 0
        for qs in queryset:
            row = row + 1
            column = 0
            sheet.write(row,column,qs.id)
                        
            column = column + 1
            sheet.write(row,column,qs.MainSKU)
                        
            column = column + 1
            sheet.write(row,column,qs.Status)
                        
            column = column + 1
            sheet.write(row,column,qs.tortinfo)
                        
            column = column + 1
            sheet.write(row,column,qs.ProductName)
                        
            column = column + 1
            sheet.write(row,column,qs.SalerName)
                        
            column = column + 1
            sheet.write(row,column,qs.Purchaser)
                        
            column = column + 1
            sheet.write(row,column,qs.order7daysAll)
                        
            column = column + 1
            sheet.write(row,column,qs.order15daysAll)
                        
            column = column + 1
            sheet.write(row,column,qs.order30daysAll)
                        
            column = column + 1
            sheet.write(row,column,qs.AllAvailableNumber)
                        
            column = column + 1
            sheet.write(row,column,qs.Number)
                        
            number = get_ontheWayNumber(qs.MainSKU,qs.storeName)
            column = column + 1
            sheet.write(row,column,number)
                        
            column = column + 1
            sheet.write(row,column,qs.SaleDate)
                        
            column = column + 1
            sheet.write(row,column,str(qs.CreateTime))
                        
            column = column + 1
            sheet.write(row,column,qs.ItemUrl)
                        
            column = column + 1
            sheet.write(row,column,qs.UnitPrice)
                        
            column = column + 1
            sheet.write(row,column,qs.Weight)
                        
            column = column + 1
            sheet.write(row,column,qs.Money)
                        
            column = column + 1
            sheet.write(row,column,qs.storeName)
                        
            column = column + 1
            sheet.write(row,column,qs.CategoryCode)
                        
            column = column + 1
            sheet.write(row,column,qs.AllMoney)
                        
            column = column + 1
            sheet.write(row,column,str(qs.firstWarnningTime))
                        
            column = column + 1
            sheet.write(row,column,qs.radio)
                        
            column = column + 1
            sheet.write(row,column,str(qs.HandleTime))
                        
            column = column + 1
            if qs.HandleResults == 'Y':
                sheet.write(row,column,u'已处理')
            elif qs.HandleResults == 'W':
                sheet.write(row,column,u'未处理')
            elif qs.HandleResults == 'H':
                sheet.write(row,column,u'忽略')
                        
            column = column + 1
            sheet.write(row,column,qs.HandleMan)
                        
            column = column + 1
            sheet.write(row,column,qs.Remark1)
                        
            column = column + 1
            sheet.write(row,column,qs.Remark2)
                        
            column = column + 1
            sheet.write(row,column,str(qs.insertTime))
                        
        filename = request.user.username + '_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
        w.save(path + '/' +  filename)
        os.popen(r'chmod 777 %s'%(path + '/' +  filename))

        #上传oss对象
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_XLS)
        bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
        #删除现有的
        for  object_info in oss2.ObjectIterator(bucket,prefix='%s/%s_'%(request.user.username,request.user.username)):
            bucket.delete_object(object_info.key)
        bucket.put_object(u'%s/%s'%(request.user.username,filename),open(path + '/' +  filename))

        messages.error(request,u'%s%s.%s/%s/%s'%(PREFIX,BUCKETNAME_XLS,ENDPOINT_OUT,request.user.username,filename) + u':成功导出,可点击Download下载到本地............................。' )
    to_export_kc_kurent.short_description = u'导出EXCEL'  
    
    def show_Picture(self,obj):
        rt = u'<style>img{cursor:pointer;transition:all 0.6s;}img:hover{transform:scale(4) translateX(20px);}</style>' \
             u'<img src="%s"  width="120" height="120"><br><br>' % obj.image_url
                 
        return mark_safe(rt)
    show_Picture.short_description = mark_safe('<p style="width:80px;color:#428bca;">图片</p>')
    
    def show_linkurl(self,obj):
        rt = ''
        link_obj = t_product_b_goods.objects.filter(MainSKU=obj.MainSKU).values('LinkUrl')
        if link_obj:
            rt = '<a href=%s target="_blank">供应商链接</a>'%(link_obj[0]['LinkUrl'])
        return mark_safe(rt)
        
    show_linkurl.short_description = mark_safe('<p style="width:80px;color:#428bca;">供应商链接</p>')
    
    '''def show_AvailableNumber(self,obj):
        rt = ''
        if obj.AllAvailableNumber <=0 :
            rt = '<div class="box" style="width: 80px;height: 30px;background-color: #FFCC33;text-align: center;line-height: 30px;border-radius: 4px">%s</div>'%(obj.AllAvailableNumber)
        else :
            rt = '%s'%(obj.AllAvailableNumber)
        return mark_safe(rt)
    show_AvailableNumber.short_description = u'可用数量'
    

    def show_Money(self,obj):
        rt = ''
        if obj.Money <= 0:
            rt = '<div class="box" style="width: 80px;height: 30px;background-color: #66FF66;text-align: center;line-height: 30px;border-radius: 4px">%s</div>'%(obj.Money)
        else:
            rt = '%s'%(obj.Money)
        return mark_safe(rt)
    show_Money.short_description=u'库存金额' 
    '''
    def show_MainSKU(self,obj):
        from urllib import urlencode
        
        rt = ''
        if obj.radio <= 0.8:
            rt = u'<a href = "/Project/admin/pyapp/kc_currentstock_sku/?%s"><font color="red">%s</a>'%(urlencode({'_p_MainSKU__exact':obj.MainSKU}),obj.MainSKU)       
            #rt = '<div class="box" style="width: 80px;height: 30px;background-color: #FF3333;text-align: center;line-height: 30px;border-radius: 4px">%s</div>'%(obj.MainSKU)
        else:
            rt = u'<a href = "/Project/admin/pyapp/kc_currentstock_sku/?%s">%s</a>'%(urlencode({'_p_MainSKU__exact':obj.MainSKU}),obj.MainSKU)       
            #rt = '<div class="box" style="width: 80px;height: 30px;text-align: center;line-height: 30px;border-radius: 4px">%s</div>'%(obj.MainSKU)
        return mark_safe(rt)
    show_MainSKU.short_description = mark_safe('<p style="width:80px;color:#428bca;">主SKU</p>')
    
    def show_tortInfo(self,obj) :
        rt = ''
        if obj.tortinfo == '未侵权':
            rt = '%s'%(obj.tortinfo)
        else:
            if ',' in obj.tortinfo:
                tortinfo_list = (obj.tortinfo).split(',')
                rt = '<div><class="box" style="width: 80px;height: 30px;background-color: #66FF66;text-align: center;line-height: 0px;border-radius: 4px">'
                for tortinfo in tortinfo_list:
                    rt += '<font size="2">%s </font>'%(tortinfo)
                rt += '</div>'
            else:
                rt = '<div class="box" style="width: 80px;height: 30px;background-color: #66FF66;text-align: center;line-height: 30px;border-radius: 4px">%s</div>'%(obj.tortinfo)
        return mark_safe(rt)
    show_tortInfo.short_description = mark_safe('<p style="width:80px;color:#428bca;">侵权站点</p>')
    
    def show_ontheWayNumber(self,obj):
        number = get_ontheWayNumber(obj.MainSKU,obj.storeName)
        return mark_safe(number)
    show_ontheWayNumber.short_description = mark_safe('<p style="width:80px;color:#428bca;">采购未入库</p>')
    
    def to_apply_Handle(self, request, queryset):
        for querysetid in queryset.all():
            if querysetid.HandleResults is None or querysetid.HandleResults == 'W' or querysetid.HandleResults == 'H':
                if request.user.has_perm('skuapp.change_t_product_inventory_warnning'):
                    t_product_inventory_warnning.objects.filter(id=querysetid.id).update(HandleResults = 'Y',HandleTime = datetime.datetime.now(),HandleMan = request.user.first_name )
                else:
                    messages.error(request, '对不起！您没有处理的权限！ ID：%s'%querysetid.id)
    to_apply_Handle.short_description = u'处理'
    
    def to_apply_Ignore(self, request, queryset):
        for querysetid in queryset.all():
            if querysetid.HandleResults is None or querysetid.HandleResults == 'W':
                if request.user.has_perm('skuapp.change_t_product_inventory_warnning'):
                    t_product_inventory_warnning.objects.filter(id=querysetid.id).update(HandleResults = 'H',HandleTime = datetime.datetime.now(),HandleMan = request.user.first_name )
                else:
                    messages.error(request, '对不起！您没有处理的权限！ ID：%s'%querysetid.id)
    to_apply_Ignore.short_description = u'忽略'
    
    list_display_links = ('NID',)
    list_display = ('show_Picture','show_MainSKU','show_tortInfo','Status','Purchaser','SalerName','order7daysAll','order15daysAll','order30daysAll','AllAvailableNumber','show_ontheWayNumber','SaleDate','CostPrice','UnitPrice','Weight','radio','CreateTime','show_linkurl','HandleResults','HandleMan','Remark1','Remark2',)
    list_editable = ('Remark1','Remark2')
    #readonly_fields = ('handleTime','Discount','SupperCycle')
    
    def get_list_queryset(self,):
        from django.db.models import Q
        request = self.request
        qs = super(t_product_inventory_warnning_Admin, self).get_list_queryset()
        MainSKU = request.GET.get('MainSKU','')     
        AllAvailableNumberStart = request.GET.get('AllAvailableNumberStart','')
        AllAvailableNumberEnd = request.GET.get('AllAvailableNumberEnd','')
        Purchaser = request.GET.get('Purchaser','')
        Purchaser = Purchaser.split(',')
        if '' in Purchaser:
            Purchaser = ''
        radio = request.GET.get('radio','')
        tortinfo = request.GET.get('tortinfo','')
        tortinfoflag = request.GET.get('tortinfoflag','')
        storeName = request.GET.get('storeName','')
        storeName = storeName.split(',')
        if '' in storeName:
            storeName = ''
        SalerName = request.GET.get('SalerName','')
        SalerName1 = request.GET.get('SalerName1','')
        SalerName1 = [ gs for gs in SalerName1.split(',') if gs ]
        SaleDay = request.GET.get('SaleDate','')
        SaleDayStart = request.GET.get('SaleDayStart','')
        SaleDayEnd = request.GET.get('SaleDayEnd','')
        handleResults = request.GET.get('handleResults','')
        orders7DaysStart = request.GET.get('orders7DaysStart','')
        orders7DaysEnd = request.GET.get('orders7DaysEnd','')
        orders15DaysStart = request.GET.get('orders15DaysStart','')
        orders15DaysEnd = request.GET.get('orders15DaysEnd','')
        orders30DaysStart = request.GET.get('orders30DaysStart','')
        orders30DaysEnd = request.GET.get('orders30DaysEnd','')
        LargeCategory = request.GET.get('LargeCategory','')
        GoodsStatus = request.GET.get('GoodsStatus','')
        CreateTimeStart = request.GET.get('CreateTimeStart','')
        CreateTimeEnd = request.GET.get('CreateTimeEnd','')
        
        searchList = {'MainSKU__exact': MainSKU,'Purchaser__in': Purchaser,
                        'SalerName1__in': SalerName1,
                        'radio__lte': radio,'SalerName__exact': SalerName,
                        'storeName__in': storeName,'CategoryCode__exact': LargeCategory,
                        'tortinfo__icontains': tortinfo,'Status__icontains': GoodsStatus,
                        'SaleDate__gte': SaleDayStart, 'SaleDate__lt': SaleDayEnd,
                        'CreateTime__gte': CreateTimeStart, 'CreateTime__lt': CreateTimeEnd,
                        'AllAvailableNumber__gte': AllAvailableNumberStart, 'AllAvailableNumber__lt': AllAvailableNumberEnd,
                        'order7daysAll__gte': orders7DaysStart, 'order7daysAll__lt': orders7DaysEnd,
                        'order15daysAll__gte': orders15DaysStart, 'order15daysAll__lt': orders15DaysEnd,
                        'order30daysAll__gte': orders30DaysStart, 'order30daysAll__lt': orders30DaysEnd,}
        if tortinfoflag:
            if tortinfoflag == '0':
                qs = qs.exclude(tortinfo='未侵权')
            else:
                qs = qs.filter(tortinfo='未侵权')       
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
                
        if handleResults == 'Y':
            return qs.filter(HandleResults='Y')
        elif handleResults == 'W':
            return qs.filter(HandleResults='W')
        elif handleResults == 'H':
            return qs.filter(HandleResults='H')
        else:
            if storeName != '':
                return qs.filter(Q(storeName='其他仓库')|Q(storeName='浦江仓库')|Q(storeName='海外仓仓库')|Q(storeName='亚马逊仓库'))
            else:
                return qs.filter(storeName='浦江仓库')


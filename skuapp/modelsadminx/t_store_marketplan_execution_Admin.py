# -*- coding: utf-8 -*-
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from skuapp.table.t_online_info_wish import t_online_info_wish
from skuapp.table.t_sys_department_staff import t_sys_department_staff
from skuapp.table.t_store_status import t_store_status
from skuapp.table.t_store_marketplan_execution import t_store_marketplan_execution
from skuapp.table.t_store_marketplan_execution_log import t_store_marketplan_execution_log
import math
import logging
from django.contrib import messages
from django.utils.safestring import mark_safe
from Project.settings import *
from .t_product_Admin import *
import logging
from django.contrib import messages
from django.db.models import Count
from datetime import datetime


class t_store_marketplan_execution_Admin(object):

    search_box_flag = True

    downloadxls = True
    def show_Demand(self,obj):
        rt = ''
        if obj.Demand == obj.Quantity:
            rt = '<div style="text-align:center;width:60px;height:20px;background:#33FF00";display:block>%s</div>'%obj.Demand
        else:
            rt = '<div style="text-align:center;width:60px;height:20px;background:#CCCCCC";display:block>%s</div>'%obj.Demand
        return mark_safe(rt)
    show_Demand.short_description='总需求数量'
    
    def add_remarks(self,obj):
        dic={}
        Exetime_objs = t_store_marketplan_execution_log.objects.filter(ProductID=obj.ProductID,Result='成功').values('Exetime').annotate(count=Count('Exetime')).values('Exetime','count')
        #messages.error(self.request,'%s'%Exetime_objs)
        for Exetime_obj in Exetime_objs:            
            dic.setdefault(Exetime_obj['Exetime'].strftime("%Y-%m-%d"),Exetime_obj['count'])
            #messages.error(self.request,'%s:%s'%(Exetime_obj['Exetime'],Exetime_obj['count']))
        
        #messages.error(self.request,'%s'%str(dic))
        if len(Exetime_objs)>0:
            aa = Exetime_objs[0]['Exetime']
            #bb = Exetime_objs[0]['count']
            #messages.error(self.request,'%s--%s'%(aa,bb))
            t_online_info_wish.objects.filter(ProductID=obj.ProductID).update(market_time=aa)
        t_store_marketplan_execution.objects.filter(ProductID=obj.ProductID).update(Remarks=dic)
    
    def show_Quantity(self,obj):
        self.add_remarks(obj)
        rt = ''
        if obj.Demand == obj.Quantity:
            rt = '<div style="text-align:center;width:60px;height:20px;background:#33FF00";display:block>%s(已完成)</div>'%obj.Quantity
        else:
            rt = '<div style="text-align:center;width:60px;height:20px;background:#CCCCCC";display:block>%s</div>'%obj.Quantity
        return mark_safe(rt)
    show_Quantity.short_description='营销数量'
    

    
    actions = ('to_excel',)  
    list_display =('id','ShopName','ShopAccount','ProductID','ParentSKU','Price','show_Demand','show_Quantity','CreateStaffName','CreateTime')
    search_fields = ('id','ShopName','ShopAccount','ProductID','ParentSKU','Price','Demand','Quantity','BrushPerson','CreateStaffName',)
    list_filter =('DepartmentID','ShopName','BuyerAccountLocalmachineinfo','VpnInfo','BuyerAccount','ShopNumber','BrushPerson','BrushTime','CutPerson','CutTime',)
    list_display_links = ('id')
    list_editable = ('DepartmentID','ShopName','ShopAccount','ProductID','ParentSKU','Price','Demand','Quantity','BuyerAccountLocalmachineinfo','VpnInfo','BuyerAccount','ShopNumber','BrushPerson','BrushTime','CutPerson','CutTime',)
    

    fields = ('ShopName','ShopAccount','ProductID','ParentSKU','Price','Demand',)
              
    readonly_fields = ()
             
    def to_excel(self, request, queryset):
        from xlwt import *
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        #if not os.path.exists(path):
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s'%(MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s'%(path))

        w = Workbook()
        sheet = w.add_sheet('information_deal')
        
        sheet.write(0,0,u'ID')
        sheet.write(0,1,u'卖家简称')
        sheet.write(0,2,u'店铺账号')
        sheet.write(0,3,u'产品ID')
        sheet.write(0,4,u'商品价格')
        sheet.write(0,5,u'总需求数量')
        sheet.write(0,6,u'营销数量')
        sheet.write(0,7,u'提交人')
        sheet.write(0,8,u'提交时间')


        logger = logging.getLogger('sourceDns.webdns.views')
        #写数据
        row = 0
        for qs in queryset:
            row = row + 1
            column = 0
            sheet.write(row,column,qs.id)
                    
            column = column + 1
            sheet.write(row,column,qs.ShopName)
                    
            column = column + 1
            sheet.write(row,column,qs.ShopAccount)
            
            column = column + 1
            sheet.write(row,column,qs.ProductID)
            
            column = column + 1
            sheet.write(row,column,qs.Price)

            column = column + 1
            sheet.write(row,column,qs.Demand)

            column = column + 1
            sheet.write(row,column,qs.Quantity)

            column = column + 1
            sheet.write(row,column,qs.CreateStaffName)

            column = column + 1
            sheet.write(row,column,qs.CreateTime.strftime('%Y-%m-%d'))

        filename = request.user.username + '_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
        w.save(path + '/' +  filename)
        os.popen(r'chmod 777 %s'%(path + '/' +  filename))
        #queryset.update(DealStatus=Dealstatus_obj[0].V,DealStaffID=request.user.username,DealTime=datetime.now())

        #上传oss对象
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_XLS)
        bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
        #删除现有的
        for  object_info in oss2.ObjectIterator(bucket,prefix='%s/%s_'%(request.user.username,request.user.username)):
            bucket.delete_object(object_info.key)
        bucket.put_object(u'%s/%s'%(request.user.username,filename),open(path + '/' +  filename))

        messages.error(request,u'%s%s.%s/%s/%s'%(PREFIX,BUCKETNAME_XLS,ENDPOINT_OUT,request.user.username,filename) + u':成功导出,可点击Download下载到本地~~~~~~' )
    to_excel.short_description = u'导出Excel'
                  

    def save_models(self):
        obj = self.new_obj
        request = self.request
        obj.save()
        t_store_marketplan_execution.objects.filter(id=obj.id).update(CreateStaffName=request.user.first_name)



    def get_list_queryset(self, ):
        request = self.request
        qs = super(t_store_marketplan_execution_Admin, self).get_list_queryset()
        departmentID = request.GET.get('DepartmentID', '')
        shopName = request.GET.get('ShopName', '')
        shopAccount = request.GET.get('ShopAccount', '')
        productID = request.GET.get('ProductID', '')
        parentSKU = request.GET.get('ParentSKU', '')
        price = request.GET.get('Price', '')
        buyerAccount = request.GET.get('BuyerAccount', '')
        remarks = request.GET.get('Remarks', '')
        createStaffName = request.GET.get('CreateStaffName', '')
        createTimeStart = request.GET.get('CreateTimeStart', '')
        createTimeEnd = request.GET.get('CreateTimeEnd', '')

        searchList = {'DepartmentID__exact': departmentID, 'ShopName__contains': shopName,
                      'ShopAccount__contains': shopAccount, 'ProductID__exact': productID,
                      'ParentSKU__contains': parentSKU, 'Price__exact': price,
                      'BuyerAccount__contains': buyerAccount, 'Remarks__contains': remarks,
                      'CreateStaffName__exact': createStaffName, 'CreateTime__gte': createTimeStart, 'CreateTime__lt': createTimeEnd
                      }

        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    if k == 'Price__exact':
                        if '.00' in v:
                            v = v
                        else:
                            v += '.00'
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')
        return qs




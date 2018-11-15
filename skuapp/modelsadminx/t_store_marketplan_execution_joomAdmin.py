# -*- coding: utf-8 -*-
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
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


class t_store_marketplan_execution_joomAdmin(object):

    downloadxls = True
    actions = ('to_excel',)
    list_display = ('id','createtime','createman','shopname','productid','ParentSKU','pySKU','colorsize','money','remark','lp_time','price','route_name','vpn','buyer_account','buyer_id','pp_account','yx_man_time','tracenumber','order_id','jd_status')
    list_editable = ('shopname','productid','ParentSKU','pySKU','money','colorsize','remark','createman','createtime','lp_time','price','route_name','vpn','buyer_account','buyer_id','pp_account','yx_man_time','tracenumber','order_id','jd_status')
    list_filter = ('shopname','productid','ParentSKU','pySKU','money','colorsize','remark','createman','createtime','lp_time','price','route_name','vpn','buyer_account','buyer_id','pp_account','yx_man_time','tracenumber','order_id','jd_status')
    def save_models(self):
        obj = self.new_obj
        obj.createtime = datetime.now()
        if obj.createman is None or obj.createman == '':
            obj.createman = self.request.user.first_name
        obj.save()
        
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
        sheet.write(0,1,u'提交时间')
        sheet.write(0,2,u'提交人')
        sheet.write(0,3,u'店铺名称')
        sheet.write(0,4,u'产品ID')
        sheet.write(0,5,u'ParentSKU')
        sheet.write(0,6,u'普源SKU')
        sheet.write(0,7,u'颜色/尺码')
        sheet.write(0,8,u'价格($)')
        sheet.write(0,9,u'备注')
        sheet.write(0,10,u'留评时间')               
        sheet.write(0,11,u'金额($)')
        sheet.write(0,12,u'线路名称')
        sheet.write(0,13,u'VPN信息')
        sheet.write(0,14,u'买家账号(facebook)')
        sheet.write(0,15,u'买家ID')
        sheet.write(0,16,u'PP账号')
        sheet.write(0,17,u'营销人/营销时间')
        sheet.write(0,18,u'跟踪号')
        sheet.write(0,19,u'Order ID')
        sheet.write(0,20,u'是否截单')
                
        
        logger = logging.getLogger('sourceDns.webdns.views')
        #写数据
        row = 0
        for qs in queryset:
            row = row + 1
            column = 0
            sheet.write(row,column,qs.id)       
                    
            column = column + 1
            sheet.write(row,column,qs.createtime.strftime('%Y-%m-%d %H:%M:%S'))
                    
            column = column + 1
            sheet.write(row,column,qs.createman) 
            
            column = column + 1
            sheet.write(row,column,qs.shopname)
            
            column = column + 1
            sheet.write(row,column,qs.productid)

            column = column + 1
            sheet.write(row,column,qs.ParentSKU)

            column = column + 1
            sheet.write(row,column,qs.pySKU)

            column = column + 1
            sheet.write(row,column,qs.colorsize)

            column = column + 1
            sheet.write(row,column,qs.money)

            column = column + 1
            sheet.write(row,column,qs.remark)
            
            column = column + 1
            try:
                va = qs.lp_time.strftime('%Y-%m-%d %H:%M:%S')
            except:
                va = ''
            sheet.write(row,column,va)
            
            column = column + 1
            sheet.write(row,column,qs.price)
            
            column = column + 1
            sheet.write(row,column,qs.route_name)
            
            column = column + 1
            sheet.write(row,column,qs.vpn)
            
            column = column + 1
            sheet.write(row,column,qs.buyer_account)
            
            column = column + 1
            sheet.write(row,column,qs.buyer_id)
            
            column = column + 1
            sheet.write(row,column,qs.pp_account)
            
            column = column + 1
            sheet.write(row,column,qs.yx_man_time)
            
            column = column + 1
            sheet.write(row,column,qs.tracenumber)
            
            column = column + 1
            sheet.write(row,column,qs.order_id)
            
            column = column + 1
            sheet.write(row,column,qs.jd_status)
            
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






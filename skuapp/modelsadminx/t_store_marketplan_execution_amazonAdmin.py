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


class t_store_marketplan_execution_amazonAdmin(object):
    downloadxls = True
    list_display = ('id','createtime','createman','shopaccount','country','SKU','ProductTitle','money','colorsize','evaluate_type','count','buyer_machine','ip','buyer_account','shopnumber','sd_man','sd_time','jd_man','mark1','mark2','wl_tracenumber','lp_info','cs_refund')
    list_editable = ('shopaccount','country','SKU','ProductTitle','money','colorsize','evaluate_type','count','createman','createtime','buyer_machine','ip','buyer_account','shopnumber','sd_man','sd_time','jd_man','mark1','mark2','wl_tracenumber','lp_info','cs_refund')
    list_filter = ('shopaccount','country','SKU','ProductTitle','money','colorsize','evaluate_type','count','createman','createtime','buyer_machine','ip','buyer_account','shopnumber','sd_man','sd_time','jd_man','mark1','mark2','wl_tracenumber','lp_info','cs_refund')
    actions = ('to_excel',)

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
        sheet.write(0,1,u'提交日期')
        sheet.write(0,2,u'填写人')
        sheet.write(0,3,u'卖家账号')
        sheet.write(0,4,u'国家')
        sheet.write(0,5,u'物品SKU')
        sheet.write(0,6,u'产品标题')
        sheet.write(0,7,u'单笔金额+')
        sheet.write(0,8,u'颜色尺寸')
        sheet.write(0,9,u'留评类型')
        sheet.write(0,10,u'数量')               
        sheet.write(0,11,u'买家账号本地机器信息')
        sheet.write(0,12,u'IP地址')
        sheet.write(0,13,u'对应买家账号')
        sheet.write(0,14,u'店铺单号')
        sheet.write(0,15,u'刷单人员')
        sheet.write(0,16,u'刷单时间')
        sheet.write(0,17,u'截单人员')
        sheet.write(0,18,u'备注1')
        sheet.write(0,19,u'备注2')
        sheet.write(0,20,u'物流和跟踪号')
        sheet.write(0,21,u'确认收货/留评')
        sheet.write(0,22,u'测试单退款')

                
        
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
            sheet.write(row,column,qs.shopaccount)
            
            column = column + 1
            sheet.write(row,column,qs.country)

            column = column + 1
            sheet.write(row,column,qs.SKU)

            column = column + 1
            sheet.write(row,column,qs.ProductTitle)

            column = column + 1
            sheet.write(row,column,qs.money)

            column = column + 1
            sheet.write(row,column,qs.colorsize)

            column = column + 1
            sheet.write(row,column,qs.evaluate_type)
            
            column = column + 1
            sheet.write(row,column,qs.count)
            
            column = column + 1
            sheet.write(row,column,qs.buyer_machine)
            
            column = column + 1
            sheet.write(row,column,qs.ip)
            
            column = column + 1
            sheet.write(row,column,qs.buyer_account)
            
            column = column + 1
            sheet.write(row,column,qs.shopnumber)
            
            column = column + 1
            sheet.write(row,column,qs.sd_man)
            
            column = column + 1
            try:
                tt = qs.sd_time.strftime('%Y-%m-%d')
            except:
                tt = ''
            sheet.write(row,column,tt)
            
            column = column + 1
            sheet.write(row,column,qs.jd_man)
            
            column = column + 1
            sheet.write(row,column,qs.mark1)
            
            column = column + 1
            sheet.write(row,column,qs.mark2)
            
            column = column + 1
            sheet.write(row,column,qs.wl_tracenumber)
            
            column = column + 1
            sheet.write(row,column,qs.lp_info)
            
            column = column + 1
            sheet.write(row,column,qs.cs_refund)

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






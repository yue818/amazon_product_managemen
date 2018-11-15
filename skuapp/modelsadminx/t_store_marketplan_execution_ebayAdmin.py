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


class t_store_marketplan_execution_ebayAdmin(object):
    show_cc_flag = False
    downloadxls = True
    actions = ('to_excel',)
    list_display = ('id','create_time','createman','shop_account','platform','product_code','product_sku','execution_count','buyer_machine','vpn','buyer_account','status','execution_man','execution_time','execution_money','jd_status','jd_man','lp_man','lp_time','remark')
    list_editable = ('execution_time','platform','shop_account','product_code','product_sku','execution_count','buyer_machine','vpn','buyer_account','status','execution_man','execution_money','jd_status','jd_man','lp_man','lp_time','remark')
    list_filter = ('execution_time','platform','shop_account','product_code','product_sku','execution_count','buyer_machine','vpn','buyer_account','status','execution_man','execution_money','jd_status','jd_man','lp_man','lp_time','remark')
    '''
    def show_seller_input(self,obj):
        rt = '<table id="table-7" border="1" align="center"  style="text-align:center;padding:10px">' 
        rt = '%s<tr><td>卖家账号</td><td>平台</td><td>物品编号</td><td>物品SKU</td><td>营销数量</td><td>提交人</td><td>提交时间</td></tr>'%rt
        rt = '%s<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr></table>'%(rt,obj.shop_account,obj.platform,obj.product_code,obj.product_sku,obj.execution_count,obj.createman,obj.create_time,)
        return mark_safe(rt)
    show_seller_input.short_description = u'销售人员填写信息'
    
    def show_shuadan_input(self,obj):
        rt = '<table id="table-7" border="1" align="center" style="text-align:center;padding:10px;"><tr><td>买家账号本地机器</td><td>vpn信息</td><td>对应买家账号</td><td>完成进度</td><td>刷单人员</td><td>刷单日期</td><td>执行金额($)</td><td>是否已截单</td><td>截单人</td><td>留评人</td><td>留评日期</td><td>备注</td></tr>'
        rt = '%s<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr></table>'%(rt,obj.buyer_machine,obj.vpn,obj.buyer_account,obj.status,obj.execution_man,obj.execution_time,obj.execution_money,obj.jd_status,obj.jd_man,obj.lp_man,obj.lp_time,obj.remark)
        return mark_safe(rt)
    show_shuadan_input.short_description = u'营销人员填写信息'
    '''
    
    fields = ('platform','shop_account','product_code','product_sku','execution_count','buyer_machine','vpn','buyer_account','status','execution_man','execution_money','execution_time','jd_status','jd_man','lp_man','lp_time','remark')
    form_layout = (
        Fieldset(u'销售人员填写以下内容',
                Row('platform','shop_account'),
                Row('product_code','product_sku'),
                Row('execution_count',),
                css_class = 'unsort '
        ),
        Fieldset(u'营销人员填写以下内容',
                Row('buyer_machine','vpn','buyer_account'),
                Row('execution_man','status','execution_money'),
                Row('jd_status','jd_man','lp_man'),
                Row('remark'),
                Row('execution_time','lp_time'),
                css_class = 'unsort '
        ),
    )
    def save_models(self):
        obj = self.new_obj
        obj.create_time = datetime.now()
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
        sheet.write(0,3,u'卖家账号')
        sheet.write(0,4,u'平台名称')
        sheet.write(0,5,u'物品编号')
        sheet.write(0,6,u'物品SKU')
        sheet.write(0,7,u'营销数量')
        sheet.write(0,8,u'买家账号本地机器')
        sheet.write(0,9,u'vpn信息')
        sheet.write(0,10,u'对应买家账号')               
        sheet.write(0,11,u'完成进度')
        sheet.write(0,12,u'营销人员')
        sheet.write(0,13,u'营销时间')
        sheet.write(0,14,u'执行金额($)')
        sheet.write(0,15,u'是否已截单')
        sheet.write(0,16,u'截单人')
        sheet.write(0,17,u'留评人')
        sheet.write(0,18,u'留评时间')
        sheet.write(0,19,u'备注')

                
        
        logger = logging.getLogger('sourceDns.webdns.views')
        #写数据
        row = 0
        for qs in queryset:
            row = row + 1
            column = 0
            sheet.write(row,column,qs.id)        
                    
            column = column + 1
            sheet.write(row,column,qs.create_time.strftime('%Y-%m-%d %H:%M:%S'))
                    
            column = column + 1
            sheet.write(row,column,qs.createman) 
            
            column = column + 1
            sheet.write(row,column,qs.shop_account)
            
            column = column + 1
            sheet.write(row,column,qs.platform)

            column = column + 1
            sheet.write(row,column,qs.product_code)

            column = column + 1
            sheet.write(row,column,qs.product_sku)

            column = column + 1
            sheet.write(row,column,qs.execution_count)

            column = column + 1
            sheet.write(row,column,qs.buyer_machine)

            column = column + 1
            sheet.write(row,column,qs.vpn)
            
            column = column + 1
            sheet.write(row,column,qs.buyer_account)
            
            column = column + 1
            sheet.write(row,column,qs.status)
            
            column = column + 1
            sheet.write(row,column,qs.execution_man)
            
            column = column + 1
            try:
                va = qs.execution_time.strftime('%Y-%m-%d')
            except:
                va = ''
            sheet.write(row,column,va)
            
            column = column + 1
            sheet.write(row,column,qs.execution_money)
            
            column = column + 1
            sheet.write(row,column,qs.jd_status)
            
            column = column + 1
            sheet.write(row,column,qs.jd_man)
            
            column = column + 1
            sheet.write(row,column,qs.lp_man)
            
            column = column + 1
            try:
                vb = qs.lp_time.strftime('%Y-%m-%d')
            except:
                vb = ''
            sheet.write(row,column,vb)
            
            column = column + 1
            sheet.write(row,column,qs.remark)
            
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






#-*-coding:utf-8-*-
from django.utils.safestring import mark_safe
from django.contrib import messages
import logging,json, re, time
import xadmin
import datetime,oss2
from aliapp.models import *
from Project.settings import *
from brick.public.create_dir import mkdir_p
class t_erp_aliexpress_shop_link_daily_Admin(object):
    #site_left_menu_tree_flag_ali = True
    downloadxls = True
    search_box_flag = True
    actions = ['to_export_aliexpress_link']
    
    def show_accountName(self, obj):
        rt = '<a href="/Project/admin/aliapp/t_erp_aliexpress_online_info/?accountName=%s">%s</a>'%(obj.accountName,obj.accountName)
        return  mark_safe(rt)
    show_accountName.short_description = mark_safe(u'<p align="center"style="color:#428bca;width:120px">店铺账号</p>')
    
    def to_export_aliexpress_link(self,request,queryset):
        from xlwt import *
        
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s'%(MEDIA_ROOT + 'download_xls'))
        
        mkdir_p(path)
        os.popen('chmod 777 %s'%(path))
        
        w = Workbook()

        sheet = w.add_sheet(u'Aliexpress链接统计')
        sheet.write(0,0,u'账号店铺ALI')
        sheet.write(0,1,u'账号名称')
        sheet.write(0,2,u'销售员(中文)')
        sheet.write(0,3,u'刊登人')
        sheet.write(0,4,u'统计数量')
        sheet.write(0,5,u'统计日期')
        
        row = 0
        for qs in queryset: 
            row = row + 1
            column = 0                    
            sheet.write(row,column,qs.shopName)
                
            column = column + 1
            sheet.write(row,column,qs.accountName)
                
            column = column + 1
            sheet.write(row,column,qs.seller_zh)
                
            column = column + 1
            sheet.write(row,column,qs.submitter)
                    
            column = column + 1
            sheet.write(row,column,qs.link_number)
                
            column = column + 1
            sheet.write(row,column,qs.gmt_create)
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
    to_export_aliexpress_link.short_description = u'导出Aliexpress链接统计'
    
    list_display = ('shopName', 'show_accountName', 'seller_zh', 'submitter', 'link_number', 'gmt_create')

    list_display_links = ('shopName',)

    def get_list_queryset(self,):
        """显示可显示的，自己本人的"""
        from skuapp.table.t_sys_staff_auth import t_sys_staff_auth
        flag = 0
        try:
            flag = t_sys_staff_auth.objects.filter(StaffID=self.request.user.username,urltable="t_erp_aliexpress_online_info").count()
        except:
            pass
        request = self.request
        qs = super(t_erp_aliexpress_shop_link_daily_Admin, self).get_list_queryset()
        if self.request.user.is_superuser or flag != 0:
            pass
        else:
            print self.request.user.first_name
            qs = qs.filter(seller_zh=self.request.user.first_name)
        shopName = request.GET.get('shopName', '')
        submitter = request.GET.get('submitter', '')
        accountName = request.GET.get('accountName', '')
        seller_zh = request.GET.get('seller_zh', '')
        link_numberStart = request.GET.get('link_numberStart', '')
        link_numberEnd = request.GET.get('link_numberEnd', '')
        gmt_createStart = request.GET.get('gmt_createStart', '')
        gmt_createEnd = request.GET.get('gmt_createEnd', '')
        searchList = {'shopName__contains': shopName, 'accountName__exact': accountName,
                      'seller_zh__exact': seller_zh,'submitter__exact': submitter,
                      'gmt_create__gte': gmt_createStart, 'gmt_create__lt': gmt_createEnd,
                      'link_number__gte': link_numberStart, 'link_number__lt': link_numberEnd,
                      }
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    sl[k] = v
        if sl is not None:
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')
        return qs
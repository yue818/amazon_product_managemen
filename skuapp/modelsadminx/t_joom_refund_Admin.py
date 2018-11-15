# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from datetime import datetime
from Project.settings import *
from .t_product_Admin import *
import logging
from datetime import datetime


class t_joom_refund_Admin(object):
    joom_refund_flag = True
    downloadxls = True
    actions = ('to_excel',)
    list_filter = ('ShopNum','nid','SKU','RefundPrice', 'RefundReason','UploadMan','UploadTime')
    search_fields = ('ShopNum','nid','SKU', 'RefundPrice', 'RefundReason')
    list_display = ('id','ShopNum','nid','SKU','RefundPrice', 'RefundReason','UploadMan','UploadTime','UpdateTime')

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
        sheet.write(0,1,u'店铺单号')
        sheet.write(0,2,u'SKU')
        sheet.write(0,3,u'订单编号')
        sheet.write(0,4,u'退款金额')
        sheet.write(0,5,u'退款原因')
        sheet.write(0,6,u'上传人')
        sheet.write(0,7,u'更新时间')

                
        
        logger = logging.getLogger('sourceDns.webdns.views')
        #写数据
        row = 0
        for qs in queryset:
            row = row + 1
            column = 0
            sheet.write(row,column,qs.id)       
                    
            column = column + 1
            sheet.write(row,column,qs.ShopNum)
                    
            column = column + 1
            sheet.write(row,column,qs.SKU) 
            
            column = column + 1
            sheet.write(row,column,qs.nid)
            
            column = column + 1
            sheet.write(row,column,qs.RefundPrice)

            column = column + 1
            sheet.write(row,column,qs.RefundReason)

            column = column + 1
            sheet.write(row,column,qs.UploadMan)

            column = column + 1
            sheet.write(row,column,qs.UpdateTime.strftime('%Y-%m-%d %H:%M:%S'))

            
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





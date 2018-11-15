# -*- coding: utf-8 -*-
from skuapp.table.t_shopsku_information_binding import t_shopsku_information_binding
from .t_product_Admin import *
from datetime import datetime


class t_help_banding_sku_to_ali_Admin(object):
    downloadxls = True
    list_display  =('id','SKU','ShopSKU','Memo','PersonCode','Filename','Submitter','SubmitTime','BindingStatus',)
    # list_editable =('SKU','ShopSKU','Memo','PersonCode','BindingStatus',)
    list_filter   =('ShopSKU','Memo','PersonCode','Filename','Submitter','SubmitTime','BindingStatus',)
    search_fields =('id','SKU','ShopSKU','Memo','PersonCode','Filename','Submitter','BindingStatus',)
    
    fields = ('id',)

    actions = ['t_help_banding_sku_to_ali_excel','to_banding']
    
    def t_help_banding_sku_to_ali_excel(self,request,queryset):
        from xlwt import *
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        #if not os.path.exists(path):
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s'%(MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s'%(path))

        w = Workbook()
        sheet = w.add_sheet(u'店铺SKU信息绑定')

        sheet.write(0,0,u'商品SKU')
        sheet.write(0,1,u'店铺SKU')
        sheet.write(0,2,u'店铺名')
        sheet.write(0,3,u'销售员')

        #写数据
        row = 0
        for qs in queryset:

            row = row + 1
            column = 0
            sheet.write(row,column,qs.SKU)

            column = column + 1
            sheet.write(row,column,qs.ShopSKU)

            column = column + 1
            sheet.write(row,column,qs.Memo)

            column = column + 1
            sheet.write(row,column,qs.PersonCode)

            if row > 50000:
                break

        filename = request.user.username + '_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
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
    t_help_banding_sku_to_ali_excel.short_description = u'导出SKU信息绑定'

            
    def to_banding(self,request,objs):
        insertinto = []
        for obj in objs:
            if obj.BindingStatus == 'no':
                insertinto.append(t_shopsku_information_binding(
                    SKU = obj.SKU, ShopSKU = obj.ShopSKU, Memo = obj.Memo, PersonCode = obj.PersonCode,
                    Filename = obj.Filename,Submitter = request.user.first_name, SubmitTime = datetime.now(), 
                    BindingStatus = 'wait'
                ))
                obj.BindingStatus = 'yes'
                obj.save()
        t_shopsku_information_binding.objects.bulk_create(insertinto)
    to_banding.short_description = u'确认绑定'
            
            
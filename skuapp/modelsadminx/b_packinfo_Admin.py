# -*- coding: utf-8 -*-
from .t_product_Admin import *
from datetime import datetime


class b_packinfo_Admin(object):
    downloadxls = True
    list_display = ('NID','PackCode','PackName','CostPrice','Used','Remark','Weight','BarCode',)
    list_editable= ('PackCode','PackName','CostPrice','Used','Remark','Weight','BarCode',)
    search_fields= ('NID','PackCode','PackName','CostPrice','Used','Remark','Weight','BarCode',)
    list_filter  = ('PackCode','PackName','CostPrice','Used','Remark','Weight','BarCode',)
    
    actions = ['to_b_packinfo_excel',]
    fields = ('PackCode','PackName','CostPrice','Used','Remark','Weight','BarCode',)

    form_layout = (
        Fieldset(u'包装规格',
                    Row('PackCode','PackName','CostPrice',),
                    Row('Used','Remark','Weight'),
                    Row('BarCode'),
                    css_class = 'unsort '
                ),
                  )
    
    def to_b_packinfo_excel(self, request, queryset):
        from xlwt import *
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        #if not os.path.exists(path):
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s'%(MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s'%(path))

        w = Workbook()
        sheet = w.add_sheet(u'包装规格配置')

        sheet.write(0,0,u'包装规格代码')
        sheet.write(0,1,u'包装规格名称')
        sheet.write(0,2,u'成本单价')
        sheet.write(0,3,u'停用')
        sheet.write(0,4,u'备注')
        sheet.write(0,5,u'重量（g）')
        sheet.write(0,6,u'条码号')

        #写数据
        row = 0
        for qs in queryset:

            row = row + 1
            column = 0
            sheet.write(row,column,qs.PackCode)

            column = column + 1
            sheet.write(row,column,qs.PackName)

            column = column + 1
            sheet.write(row,column,qs.CostPrice)

            column = column + 1
            sheet.write(row,column,qs.Used)

            column = column + 1
            sheet.write(row,column,qs.Remark)

            column = column + 1
            sheet.write(row,column,qs.Weight)
            
            column = column + 1
            sheet.write(row,column,qs.BarCode)
            
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
    to_b_packinfo_excel.short_description = u'导出包装规格'

    
    
    
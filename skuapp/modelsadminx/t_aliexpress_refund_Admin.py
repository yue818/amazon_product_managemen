# -*- coding: utf-8 -*-
from skuapp.table.t_aliexpress_refund import * 
from Project.settings import *
import oss2,errno,sys
from django.contrib import messages
from django.utils.safestring import mark_safe
import logging


WISH_URL    = 'wish.'
AMAZON_URL  = 'amazon.'
WWW1688_URL = '1688.'
EBAY_URL = 'ebay.'
ALIEXPRESS_URL = 'aliexpress.'
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5 (except OSError, exc: for Python <2.5)
        if exc.errno == errno.EEXIST and os.path.isdir(path): 
            pass
        else:
            raise


class t_aliexpress_refund_Admin(object):
    downloadxls = True
    importfile_plugin1 = True
    search_box_flag = True


    fields = None
    list_display = ('ShopOrderNumber','CorrespondingSalesNumber','RefundsType','AfterSaleType',
                    'MainTableRemark','ShopSKU','SKU','QuantityOfGoods',
                    'AmountOfMoney','FineMeterRemark','RedirectCustomerServiceReason',
                    'ImportTime','ExportState','ExportTime','ImportPerson',)




    actions = [ 'to_excel', ]
    
    



    def to_excel(self, request, queryset):
        
        from datetime import datetime
        from xlwt import *
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        #if not os.path.exists(path):
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s'%(MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s'%(path))

        w = Workbook()
        sheet = w.add_sheet('Aliex_Refund_record')

        sheet.write(0, 0, u'店铺单号')
        sheet.write(0, 1, u'对应销售单号')
        sheet.write(0, 2, u'退款类型')
        sheet.write(0, 3, u'售后类型')
        sheet.write(0, 4, u'主表备注')
        sheet.write(0, 5, u'ShopSku')
        sheet.write(0, 6, u'SKU')
        sheet.write(0, 7, u'数量')
        sheet.write(0, 8, u'金额')
        sheet.write(0, 9, u'细表备注')
        sheet.write(0, 10, u'重寄售后原因')


        # 写数据
        row = 0
        for qs in queryset:
            row = row+1
            column = 0
            sheet.write(row, column, qs.ShopOrderNumber)  # 店铺单号

            column = column + 1
            sheet.write(row, column, qs.CorrespondingSalesNumber)

            column = column + 1
            sheet.write(row, column, qs.RefundsType)

            column = column + 1
            sheet.write(row, column, qs.AfterSaleType)

            column = column + 1
            sheet.write(row, column, qs.MainTableRemark)

            column = column + 1
            sheet.write(row, column, qs.ShopSKU)

            column = column + 1
            sheet.write(row, column, qs.SKU)

            column = column + 1
            sheet.write(row, column, qs.QuantityOfGoods)

            column = column + 1
            sheet.write(row, column, qs.AmountOfMoney)

            column = column + 1
            sheet.write(row, column, qs.FineMeterRemark)

            column = column + 1
            sheet.write(row, column, qs.RedirectCustomerServiceReason)

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

        messages.success(request,u'%s%s.%s/%s/%s'%(PREFIX,BUCKETNAME_XLS,ENDPOINT_OUT,request.user.username,filename) + u':成功导出,可点击Download下载到本地............................。' )

        queryset.update(ExportState=u'已导出',ExportTime=datetime.now())
        
    to_excel.short_description = u'导出EXCEL'

    def get_list_queryset(self):
        request = self.request
        qs = super(t_aliexpress_refund_Admin, self).get_list_queryset()

        ShopName = request.GET.get('ShopName', '')
        ShopOrderNumber = request.GET.get('ShopOrderNumber', '')
        SKU = request.GET.get('SKU', '')
        ImportPerson = request.GET.get('ImportPerson', '')

        ExportState = request.GET.get('ExportState', '')

        ImportTimeStart = request.GET.get('ImportTimeStart', '')
        ImportTimeEnd = request.GET.get('ImportTimeEnd', '')

        ExportTimeStart = request.GET.get('ExportTimeStart', '')
        ExportTimeEnd = request.GET.get('ExportTimeEnd', '')



        searchList = {'ShopName__exact': ShopName, 'ShopOrderNumber__exact': ShopOrderNumber,
                      'SKU__exact': SKU,'ExportState__exact': ExportState,
                      'ImportPerson__exact': ImportPerson,

                      'ImportTime__gte': ImportTimeStart, 'ImportTime__lt': ImportTimeEnd,
                      'ExportTime__gte': ExportTimeStart, 'ExportTime__lt': ExportTimeEnd,
                      }
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    # if k == 'ShopName__exact':
                    #  v = 'Wish-' + v.zfill(4)
                    # messages.error(request, v)
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')
                
        if request.user.is_superuser ==1 :              
            qs = qs
        else:
            qs =  qs.filter(ImportPerson=request.user.username)
        return qs



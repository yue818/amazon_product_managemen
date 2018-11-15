#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_wish_pb_finance_rep_Admin.py
 @time: 2018-07-14 13:42
"""
from django.contrib import messages

class t_wish_pb_finance_rep_Admin(object):
    t_wish_pb_left_menu = True
    search_box_flag = True
    downloadxls = True

    actions = ['to_export_excel', ]

    def to_export_excel(self, request, queryset):
        from xlwt import *
        from datetime import datetime
        from skuapp.modelsadminx.t_product_Admin import MEDIA_ROOT, mkdir_p, os, oss2, ACCESS_KEY_ID, ACCESS_KEY_SECRET, \
            ENDPOINT, BUCKETNAME_XLS, PREFIX, ENDPOINT_OUT

        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s' % (path))

        w = Workbook()

        sheet = w.add_sheet(u'WISH广告财务报表')
        sheet.write(0, 0, u'店铺名称')
        sheet.write(0, 1, u'广告创建人')
        sheet.write(0, 2, u'仓库名称')
        sheet.write(0, 3, u'日期')
        sheet.write(0, 4, u'总曝光量')
        sheet.write(0, 5, u'付费曝光量')
        sheet.write(0, 6, u'花费')
        sheet.write(0, 7, u'订单数')
        sheet.write(0, 8, u'销售额')

        row = 0
        for qs in queryset:
            row = row + 1
            column = 0
            sheet.write(row, column, qs.shopname)

            column = column + 1
            sheet.write(row, column, qs.createuser)

            column = column + 1
            sheet.write(row, column, qs.storename)

            column = column + 1
            sheet.write(row, column, str(qs.p_date))

            column = column + 1
            sheet.write(row, column, qs.impressions)

            column = column + 1
            sheet.write(row, column, qs.paid_impressions)

            column = column + 1
            sheet.write(row, column, qs.spend)

            column = column + 1
            sheet.write(row, column, qs.sales)

            column = column + 1
            sheet.write(row, column, qs.gmv)

        filename = request.user.username + '_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
        w.save(path + '/' + filename)
        os.popen(r'chmod 777 %s' % (path + '/' + filename))

        # 上传oss对象
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT, BUCKETNAME_XLS)
        bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
        # 删除现有的
        for object_info in oss2.ObjectIterator(bucket,
                                               prefix='%s/%s_' % (request.user.username, request.user.username)):
            bucket.delete_object(object_info.key)
        bucket.put_object(u'%s/%s' % (request.user.username, filename), open(path + '/' + filename))

        messages.success(request, u'%s%s.%s/%s/%s' % (PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, request.user.username,
                                                      filename) + u':成功导出,可点击Download下载到本地............................。')

    to_export_excel.short_description = u'导出到Excel'

    list_display_links = ('id',)

    list_display = ('shopname', 'createuser', 'storename', 'p_date', 'impressions', 'paid_impressions', 'spend', 'sales', 'gmv', )


    def get_list_queryset(self):
        request = self.request
        qs = super(t_wish_pb_finance_rep_Admin, self).get_list_queryset()

        shopname = request.GET.get('shopname', '')
        createuser = request.GET.get('createuser', '')
        storename = request.GET.get('storename', '')
        p_date_start = request.GET.get('p_date_start', '')
        p_date_end = request.GET.get('p_date_end', '')

        searchList = {'shopname__exact': shopname,
                      'createuser__exact': createuser,
                      'storename__exact': storename,
                      'p_date__gte': p_date_start,
                      'p_date__lt': p_date_end
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
                messages.error(request, u'输入的查询数据有误！')

        return qs
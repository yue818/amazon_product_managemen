# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_fba_inventory_age_Admin.py
 @time: 2018/11/21 17:14
"""
from django.contrib import messages
from Project.settings import *
from xlwt import *
import errno
import datetime
import oss2
from django.db.models import Q


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5 (except OSError, exc: for Python <2.5)
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


class t_amazon_fba_inventory_age_Admin(object):
    amazon_site_left_menu_tree_flag = True
    # search_box_flag = True
    downloadxls = True
    list_display = ('shop_name','seller','snapshot_date', 'sku', 'asin', 'qty_to_be_charged_ltsf_6_mo', 'projected_ltsf_6_mo',
                    'qty_to_be_charged_ltsf_12_mo', 'projected_ltsf_12_mo', 'refresh_time',)
    list_filter = ('shop_name', 'seller', 'sku', 'qty_to_be_charged_ltsf_6_mo', 'qty_to_be_charged_ltsf_12_mo')
    search_fields = ('shop_name', 'seller', 'sku', 'qty_to_be_charged_ltsf_6_mo', 'qty_to_be_charged_ltsf_12_mo')
    list_display_links = ('',)
    actions = ['to_excel']

    def to_excel(self, request, queryset):
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))
        mkdir_p(path)
        os.popen('chmod 777 %s' % path)

        w = Workbook()
        sheet = w.add_sheet('amazon_inventory_age')
        sheet.write(0, 0, u'店铺')
        sheet.write(0, 1, u'销售员')
        sheet.write(0, 2, u'报告时间')
        sheet.write(0, 3, u'店铺SKU')
        sheet.write(0, 4, u'ASIN')
        sheet.write(0, 5, u'库龄超6个月')
        sheet.write(0, 6, u'仓储费(6个月)')
        sheet.write(0, 7, u'库龄超12个月')
        sheet.write(0, 8, u'仓储费(12个月)')
        sheet.write(0, 9, u'刷新时间')

        # 写数据
        row = 0
        for qs in queryset:
            row = row + 1
            snapshot_date = qs.snapshot_date.strftime('%Y-%m-%d %H:%M')
            refresh_time = qs.refresh_time.strftime('%Y-%m-%d %H:%M')

            excel_content_list = (qs.shop_name, qs.seller, snapshot_date, qs.sku, qs.asin, qs.qty_to_be_charged_ltsf_6_mo,
                                  qs.projected_ltsf_6_mo, qs.qty_to_be_charged_ltsf_12_mo, qs.projected_ltsf_12_mo,refresh_time)
            column = 0
            for content in excel_content_list:
                sheet.write(row, column, content)
                column += 1
        filename = request.user.username + '_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
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
        messages.success(request, u'%s%s.%s/%s/%s' % (PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, request.user.username, filename) + u':成功导出,可点击Download下载到本地............................。')

    to_excel.short_description = u'导出数据'

    def get_list_queryset(self, ):
        qs = super(t_amazon_fba_inventory_age_Admin, self).get_list_queryset()
        qs = qs.filter(Q(qty_to_be_charged_ltsf_6_mo__gt=0)
                       | Q(qty_to_be_charged_ltsf_12_mo__gt=0))
        return qs

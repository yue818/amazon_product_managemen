# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_removal_order_detail_Admin.py
 @time: 2018/8/23 11:00
"""
from django.utils.safestring import mark_safe
from django.contrib import messages
from Project.settings import *
from xlwt import *
import errno
import datetime
import oss2
import os


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5 (except OSError, exc: for Python <2.5)
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


class t_amazon_removal_order_detail_Admin(object):
    amazon_site_left_menu_tree_flag = True
    search_box_flag = True
    downloadxls = True

    def show_disposed_quantity(self, obj):
        disposed_cnt = obj.disposed_quantity + obj.shipped_quantity
        return mark_safe(disposed_cnt)
    show_disposed_quantity.short_description = u'<span style="color:#428BCA">已完成</span>'

    list_display = ('shop_name', 'sku', 'request_date', 'order_id','order_type','order_status', 'requested_quantity', 'show_disposed_quantity','cancelled_quantity','in_process_quantity','refresh_time')

    actions = ['to_excel']

    def to_excel(self, request, queryset):
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))
        mkdir_p(path)
        os.popen('chmod 777 %s' % path)

        w = Workbook()
        sheet = w.add_sheet('remove order')
        sheet.write(0, 0, u'店铺名')
        sheet.write(0, 1, u'店铺SKU')
        sheet.write(0, 2, u'日期')
        sheet.write(0, 3, u'订单编号')
        sheet.write(0, 4, u'订单类型')
        sheet.write(0, 5, u'订单状态')
        sheet.write(0, 6, u'请求移除')
        sheet.write(0, 7, u'已完成')
        sheet.write(0, 8, u'取消移除')
        sheet.write(0, 9, u'处理中')
        sheet.write(0, 10, u'更新时间')

        # 写数据
        row = 0
        for qs in queryset:
            row = row + 1
            request_date = qs.request_date.strftime('%Y-%m-%d %H:%M')
            refresh_time = qs.refresh_time.strftime('%Y-%m-%d %H:%M')
            disposed_quantity = qs.disposed_quantity + qs.shipped_quantity
            excel_content_list = [qs.shop_name, qs.sku, request_date, qs.order_id, qs.order_type, qs.order_status, qs.requested_quantity, disposed_quantity, qs.cancelled_quantity, qs.in_process_quantity, refresh_time]
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
        request = self.request
        qs = super(t_amazon_removal_order_detail_Admin, self).get_list_queryset()

        shop_name = request.GET.get('shop_name', '')
        sku = request.GET.get('sku', '')
        sku = '' if sku == '' else sku.strip().replace(' ', '+').split(',')
        order_id = request.GET.get('order_id', '')
        order_id = '' if order_id == '' else order_id.split(',')
        order_type = request.GET.get('order_type', '')
        order_status = request.GET.get('order_status', '')
        requested_quantity_start = request.GET.get('requested_quantity_start', '')
        requested_quantity_end = request.GET.get('requested_quantity_end', '')
        disposed_quantity_start = request.GET.get('disposed_quantity_start', '')
        disposed_quantity_end = request.GET.get('disposed_quantity_end', '')
        cancelled_quantity_start = request.GET.get('cancelled_quantity_start', '')
        cancelled_quantity_end = request.GET.get('cancelled_quantity_end', '')
        in_process_quantity_start = request.GET.get('in_process_quantity_start', '')
        in_process_quantity_end = request.GET.get('in_process_quantity_end', '')
        request_date_start = request.GET.get('request_date_start', '')
        request_date_end = request.GET.get('request_date_end', '')

        search_list ={'shop_name__contains': shop_name,
                      'sku__in': sku,
                      'order_id__in': order_id,
                      'order_type__exact': order_type,
                      'order_status__exact': order_status,
                      'request_date__gte': request_date_start,
                      'request_date__lte': request_date_end,
                      'requested_quantity__gte': requested_quantity_start,
                      'requested_quantity__lte': requested_quantity_end,
                      'disposed_quantity__gte': disposed_quantity_start,
                      'disposed_quantity__lte': disposed_quantity_end,
                      'cancelled_quantity__gte': cancelled_quantity_start,
                      'cancelled_quantity__lte': cancelled_quantity_end,
                      'in_process_quantity__gte': in_process_quantity_start,
                      'in_process_quantity__lte': in_process_quantity_end,
                      }
        sl = {}
        for k, v in search_list.items():
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
                # messages.error(request, ex)
                messages.error(request, u'Please enter the correct content!')
        return qs
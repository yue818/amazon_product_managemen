# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_actionable_order_data_Admin.py
 @time: 2018/10/17 9:51
"""
from django.contrib import messages
from Project.settings import *
from xlwt import *
import errno
import datetime
import oss2


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5 (except OSError, exc: for Python <2.5)
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


class t_amazon_actionable_order_data_Admin(object):
    amazon_site_left_menu_tree_flag = True
    search_box_flag = True
    downloadxls = True
    list_display = ('shop_name', 'sku', 'order_id', 'purchase_date', 'payments_date', 'promise_date','days_past_promise','quantity_purchased',
                    'quantity_shipped','quantity_to_ship','ship_service_level', 'refresh_time')

    actions = ['to_excel']

    def to_excel(self, request, queryset):
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))
        mkdir_p(path)
        os.popen('chmod 777 %s' % path)

        w = Workbook()
        sheet = w.add_sheet('actionable_order')
        sheet.write(0, 0, u'店铺')
        sheet.write(0, 1, u'店铺SKU')
        sheet.write(0, 2, u'订单编号')
        sheet.write(0, 3, u'购买日期')
        sheet.write(0, 4, u'付款日期')
        sheet.write(0, 5, u'承诺日期')
        sheet.write(0, 6, u'超出承诺日期的天数')
        sheet.write(0, 7, u'购买的数量')
        sheet.write(0, 8, u'已配送数量')
        sheet.write(0, 9, u'待配送数量')
        sheet.write(0, 10, u'运输方式	')
        sheet.write(0, 11, u'更新时间')

        # 写数据
        row = 0
        for qs in queryset:
            row = row + 1
            purchase_date = qs.purchase_date.strftime('%Y-%m-%d %H:%M')
            payments_date = qs.payments_date.strftime('%Y-%m-%d %H:%M')
            promise_date = qs.promise_date.strftime('%Y-%m-%d %H:%M')
            refresh_time = qs.refresh_time.strftime('%Y-%m-%d %H:%M')
            excel_content_list = (qs.shop_name, qs.sku, qs.order_id, purchase_date, payments_date, promise_date, qs.days_past_promise, qs.quantity_purchased, qs.quantity_shipped, qs.quantity_to_ship, qs.ship_service_level, refresh_time )
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
        shop_name = request.GET.get('shop_name', '')
        sku = request.GET.get('sku', '')
        sku = '' if sku == '' else sku.strip().replace(' ', '+').split(',')
        order_id = request.GET.get('order_id', '')
        order_id = '' if order_id == '' else order_id.strip().split(',')
        payments_date_start = request.GET.get('payments_date_start', '')
        payments_date_end = request.GET.get('payments_date_end', '')
        promise_date_start = request.GET.get('promise_date_start', '')
        promise_date_end = request.GET.get('promise_date_end', '')
        refresh_time_start = request.GET.get('refresh_time_start', '')
        refresh_time_end = request.GET.get('refresh_time_end', '')
        days_past_promise = request.GET.get('days_past_promise', '')
        # days_past_promise_end = request.GET.get('days_past_promise_end', '')

        qs = super(t_amazon_actionable_order_data_Admin, self).get_list_queryset()

        search_list = {
                      'shop_name__icontains':  shop_name,
                      'sku__in': sku,
                      'order_id__in': order_id,
                      'payments_date__gte': payments_date_start,
                      'payments_date__lte': payments_date_end,
                      'promise_date__gte': promise_date_start,
                      'promise_date__lte': promise_date_end,
                      'refresh_time__gte': refresh_time_start,
                      'refresh_time__lte': refresh_time_end,
                      'days_past_promise__gte': days_past_promise,
                      }
        sl = {}
        for k, v in search_list.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and str(v).strip() != '':
                    sl[k] = v
        if sl is not None:
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'Please enter the correct content!')
        return qs

# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_all_orders_data_Admin.py
 @time: 2018/8/24 17:49
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


class t_amazon_all_orders_data_Admin(object):
    amazon_site_left_menu_tree_flag = True
    search_box_flag = True
    downloadxls = True
    list_display = ('shop_name', 'sku', 'asin', 'amazon_order_id', 'purchase_date', 'last_updated_date', 'order_status','fulfillment_channel','sales_channel',
                    'item_status','quantity','currency', 'item_price', 'item_tax','shipping_price','shipping_tax','ship_country',
                    'ship_city', 'ship_state', 'ship_postal_code', 'refresh_time',)

    actions = ['to_excel']

    def to_excel(self, request, queryset):
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))
        mkdir_p(path)
        os.popen('chmod 777 %s' % path)

        w = Workbook()
        sheet = w.add_sheet('product_sku')
        sheet.write(0, 0, u'店铺')
        sheet.write(0, 1, u'店铺SKU')
        sheet.write(0, 2, u'ASIN')
        sheet.write(0, 3, u'订单号')
        sheet.write(0, 4, u'下单日期')
        sheet.write(0, 5, u'订单更新日期')
        sheet.write(0, 6, u'订单状态')
        sheet.write(0, 7, u'配送方式')
        sheet.write(0, 8, u'订单渠道')
        sheet.write(0, 9, u'订单商品状态')
        sheet.write(0, 10, u'商品数量')
        sheet.write(0, 11, u'货币')
        sheet.write(0, 12, u'总金额')
        sheet.write(0, 13, u'税')
        sheet.write(0, 14, u'运费')
        sheet.write(0, 15, u'运费税')
        sheet.write(0, 16, u'国家')
        sheet.write(0, 17, u'城市')
        sheet.write(0, 18, u'地区')
        sheet.write(0, 19, u'邮编')
        sheet.write(0, 20, u'更新时间')

        # 写数据
        row = 0
        for qs in queryset:
            row = row + 1
            purchase_date = qs.purchase_date.strftime('%Y-%m-%d %H:%M')
            last_updated_date = qs.last_updated_date.strftime('%Y-%m-%d %H:%M')
            refresh_time = qs.refresh_time.strftime('%Y-%m-%d %H:%M')
            excel_content_list = (qs.shop_name,  qs.sku,  qs.asin,  qs.amazon_order_id,  purchase_date,  last_updated_date,  qs.order_status, qs.fulfillment_channel, qs.sales_channel,
                    qs.item_status, qs.quantity, qs.currency,  qs.item_price,  qs.item_tax, qs.shipping_price, qs.shipping_tax, qs.ship_country,
                    qs.ship_city,  qs.ship_state,  qs.ship_postal_code,  refresh_time, )
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
        asin = request.GET.get('asin', '')
        asin = '' if asin == '' else asin.strip().split(',')
        order_id = request.GET.get('order_id', '')
        order_id = '' if order_id == '' else order_id.strip().split(',')
        purchase_date_start = request.GET.get('purchase_date_start', '')
        purchase_date_end = request.GET.get('purchase_date_end', '')

        qs = super(t_amazon_all_orders_data_Admin, self).get_list_queryset()

        search_list = {
                      'shop_name__icontains':  shop_name,
                      'sku__in': sku,
                      'asin__in': asin,
                      'order_id__in': order_id,
                      'purchase_date__gte': purchase_date_start,
                      'purchase_date__lte': purchase_date_end,
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

# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_orders_by_receive_day_total_Admin.py
 @time: 2018/9/11 11:17
"""  
from django.utils.safestring import mark_safe
from django.contrib import messages
from Project.settings import *
from xlwt import *
import errno
import datetime
import oss2
from skuapp.table.t_amazon_orders_by_receive_day_info import t_amazon_orders_by_receive_day_info


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5 (except OSError, exc: for Python <2.5)
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


class t_amazon_orders_by_receive_day_total_Admin(object):
    amazon_site_left_menu_tree_flag = True
    downloadxls = True
    amazon_product_cost_refresh_plugin = True
    order_type_plugin = True

    def show_seller_detail(self, obj):
        seller_detail = '<p id="seller_detail_%s"><font  color="blue">%s</font><p/>' % (obj.id, obj.seller)
        seller_detail += '''
                   <script>
                       a = screen.width
                       b = screen.height*0.4
                        $("#seller_detail_%s").on("click", function(){
                         layer.open({
                          type: 2,
                          skin: "layui-layer-lan",
                          title: "出单详情",
                          fix: false,
                          shadeClose: true,
                          maxmin: true,
                          area: [a+'px', b+'px'],
                          content: "/show_seller_detail/?seller=%s&site=%s&order_type=%s",
                          btn: ["关闭页面"],
                          });
                      })
                  </script>
                  ''' % (obj.id, obj.seller, obj.site, obj.order_type)
        return mark_safe(seller_detail)
    show_seller_detail.short_description = mark_safe('<p style="color:#428BCA" align="center">销售员</p>')

    list_display = ('id', 'show_seller_detail', 'site', 'order_type', 'has_order','no_order','time_span', 'refresh_time')

    actions = ['to_excel']

    def to_excel(self, request, queryset):
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))
        mkdir_p(path)
        os.popen('chmod 777 %s' % path)

        w = Workbook()
        sheet = w.add_sheet('product_sku')
        sheet.write(0, 0, u'销售员')
        sheet.write(0, 1, u'站点')
        sheet.write(0, 2, u'订单类型')
        sheet.write(0, 3, u'出单')
        sheet.write(0, 4, u'未出单')
        sheet.write(0, 5, u'到货时间范围')
        sheet.write(0, 6, u'刷新时间')

        sheet_detail = w.add_sheet('product_sku_detail')
        sheet_detail.write(0, 0, u'销售员')
        sheet_detail.write(0, 1, u'店铺')
        sheet_detail.write(0, 2, u'站点')
        sheet_detail.write(0, 3, u'订单类型')
        sheet_detail.write(0, 4, u'商品SKU')
        sheet_detail.write(0, 5, u'店铺SKU')
        sheet_detail.write(0, 6, u'ASIN')
        sheet_detail.write(0, 7, u'到货时间')
        sheet_detail.write(0, 8, u'主SKU')
        sheet_detail.write(0, 9, u'品类')
        sheet_detail.write(0, 10, u'订单数')
        sheet_detail.write(0, 11, u'到货时间范围')
        sheet_detail.write(0, 12, u'刷新时间')

        # 写数据
        row = 0
        row_detail = 0
        for qs in queryset:
            row = row + 1
            refresh_time = qs.refresh_time.strftime('%Y-%m-%d %H:%M')
            excel_content_list = [qs.seller, qs.site, qs.order_type, qs.has_order, qs.no_order, qs.time_span, refresh_time]
            column = 0
            for content in excel_content_list:
                sheet.write(row, column, content)
                column += 1

            sku_order_detail = t_amazon_orders_by_receive_day_info.objects.filter(seller=qs.seller, site=qs.site, order_type=qs.order_type).order_by('-orders_after_14days')
            for detail in sku_order_detail:
                row_detail += 1
                sheet_detail.write(row_detail, 0, detail.seller)
                sheet_detail.write(row_detail, 1, detail.shopname)
                sheet_detail.write(row_detail, 2, detail.site)
                sheet_detail.write(row_detail, 3, detail.order_type)
                sheet_detail.write(row_detail, 4, detail.sku)
                sheet_detail.write(row_detail, 5, detail.seller_sku)
                sheet_detail.write(row_detail, 6, detail.asin)
                sheet_detail.write(row_detail, 7, detail.received_date.strftime('%Y-%m-%d %H:%M'))
                sheet_detail.write(row_detail, 8, detail.mainsku)
                sheet_detail.write(row_detail, 9, detail.categorycode)
                sheet_detail.write(row_detail, 10, detail.orders_after_14days)
                sheet_detail.write(row_detail, 11, detail.time_span)
                sheet_detail.write(row_detail, 12, detail.refresh_time.strftime('%Y-%m-%d %H:%M'))

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


# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_product_remove_cost_Admin.py
 @time: 2018/9/5 17:02
"""  
from django.utils.safestring import mark_safe
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


class t_amazon_product_remove_cost_Admin(object):
    amazon_site_left_menu_tree_flag = True
    search_box_flag = True
    downloadxls = True
    amazon_product_cost_refresh_plugin = True

    def show_sku_detail(self, obj):
        sku_price_detail = '<p id="remove_detail_%s"><font  color="blue">%s</font><p/>' % (obj.id, obj.product_sku)
        sku_price_detail += '''
                   <script>
                       a = screen.width
                       b = screen.height*0.5
                        $("#remove_detail_%s").on("click", function(){
                         layer.open({
                          type: 2,
                          skin: "layui-layer-lan",
                          title: "移除详情",
                          fix: false,
                          shadeClose: true,
                          maxmin: true,
                          area: [a+'px', b+'px'],
                          content: "/show_sku_remove_detail/?product_sku=%s",
                          btn: ["关闭页面"],
                          });
                      })
                  </script>
                  ''' % (obj.id, obj.product_sku)
        return mark_safe(sku_price_detail)
    show_sku_detail.short_description = mark_safe('<p style="color:#428BCA" align="center">商品SKU</p>')

    list_display = ('id', 'show_sku_detail', 'sku_unit_price', 'quantity','total_price','time_span', 'refresh_time')

    actions = ['to_excel']

    def to_excel(self, request, queryset):
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))
        mkdir_p(path)
        os.popen('chmod 777 %s' % path)

        w = Workbook()
        sheet = w.add_sheet('remove')
        sheet.write(0, 0, u'商品SKU')
        sheet.write(0, 1, u'商品单价')
        sheet.write(0, 2, u'移除增量')
        sheet.write(0, 3, u'总成本')
        sheet.write(0, 4, u'时间跨度')
        sheet.write(0, 5, u'更新时间')

        # 写数据
        row = 0
        for qs in queryset:
            row = row + 1
            refresh_time = qs.refresh_time.strftime('%Y-%m-%d %H:%M')
            excel_content_list = [qs.product_sku, qs.sku_unit_price, qs.quantity, qs.total_price, qs.time_span, refresh_time]
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

        product_sku = request.GET.get('product_sku', '')
        product_sku = '' if product_sku == '' else product_sku.strip().replace(' ', '+').split(',')

        sku_unit_price_start = request.GET.get('sku_unit_price_start', '')
        sku_unit_price_end = request.GET.get('sku_unit_price_end', '')
        quantity_start = request.GET.get('quantity_start', '')
        quantity_end = request.GET.get('quantity_end', '')
        total_price_start = request.GET.get('total_price_start', '')
        total_price_end = request.GET.get('total_price_end', '')

        qs = super(t_amazon_product_remove_cost_Admin, self).get_list_queryset()

        search_list = {
                      'product_sku__in': product_sku,
                      'sku_unit_price__gte': sku_unit_price_start,
                      'sku_unit_price__lte': sku_unit_price_end,
                      'quantity__gte': quantity_start,
                      'quantity__lte': quantity_end,
                      'total_price__gte': total_price_start,
                      'total_price__lte': total_price_end,
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

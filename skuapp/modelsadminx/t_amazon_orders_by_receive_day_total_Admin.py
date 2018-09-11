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
    search_box_flag = True
    downloadxls = True
    amazon_product_cost_refresh_plugin = True

    def show_seller_detail(self, obj):
        seller_detail = '<p id="seller_detail_%s"><font  color="blue">%s</font><p/>' % (obj.id, obj.product_sku)
        seller_detail += '''
                   <script>
                       a = screen.width*0.8
                       b = screen.height*0.3
                        $("#seller_detail_%s").on("click", function(){
                         layer.open({
                          type: 2,
                          skin: "layui-layer-lan",
                          title: "成本详情",
                          fix: false,
                          shadeClose: true,
                          maxmin: true,
                          area: [a+'px', b+'px'],
                          content: "/show_seller_detail/?seller=%s",
                          btn: ["关闭页面"],
                          });
                      })
                  </script>
                  ''' % (obj.id, obj.seller)
        return mark_safe(seller_detail)
    show_seller_detail.short_description = mark_safe('<p style="color:#428BCA" align="center">销售员</p>')

    list_display = ('id', 'show_seller_detail', 'site', 'has_order','no_order','time_span', 'refresh_time')

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
        sheet.write(0, 2, u'出单')
        sheet.write(0, 3, u'未出单')
        sheet.write(0, 4, u'到货时间范围')
        sheet.write(0, 5, u'刷新时间')

        # 写数据
        row = 0
        for qs in queryset:
            row = row + 1
            refresh_time = qs.refresh_time.strftime('%Y-%m-%d %H:%M')
            excel_content_list = [qs.seller, qs.site, qs.has_order, qs.no_order, qs.time_span, refresh_time]
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


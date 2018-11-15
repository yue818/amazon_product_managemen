# -*- coding: utf-8 -*-
from django.db import connection as conn
from skuapp.modelsadminx.t_product_Admin import *
from skuapp.table.b_goods_sales_count import b_goods_sales_count
from django.contrib import messages
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from django.utils.safestring import mark_safe
from Project.settings import *
import oss2
from xlwt import *
from .t_product_Admin import *
from datetime import datetime as confirmDate

class b_goods_sales_count_Admin(object):
    sales_count_left_flag = True
    # search_sales_count_flag = True
    list_display= ('sku','show_product_pic','goodsname','goodsstatus','devdate','purchaser','salername', )
    search_box_flag = True
    downloadxls = True

    def show_product_pic(self,obj):
        imag_url = 'http://122.226.216.10:89/ShopElf/images/'
        rt = u'<img src="%s%s.jpg" widht="120"  height="120" alt="picture" />' % (imag_url,obj.sku)

        return mark_safe(rt)
    show_product_pic.short_description = u'<span style="color:#428bca;">商品图片</span>'

    actions = ['to_import_execl']

    def to_import_execl(self, request, objs):
        try:
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
            # 写入execl
            path = MEDIA_ROOT + 'download_xls/' + request.user.username
            # if not os.path.exists(path):
            mkdir_p(MEDIA_ROOT + 'download_xls')
            os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))
            mkdir_p(path)
            os.popen('chmod 777 %s' % (path))
            w = Workbook()
            row = 0
            sheet = w.add_sheet(u'SKU统计')

            sheet.write(0, 0, u'商品sku', )  # 商品sku
            sheet.write(0, 1, u'商品名称', )  # 商品名称
            sheet.write(0, 2, u'商品状态', )  # 商品状态
            sheet.write(0, 3, u'开发时间', )  # 开发时间
            sheet.write(0, 4, u'采购员', )  # 采购员
            sheet.write(0, 5, u'销售员', )  # 销售员

            for obj in objs:
                row = row + 1
                excel_content_list = [obj.sku, obj.goodsname, obj.goodsstatus, obj.devdate, obj.salername, obj.purchaser]
                column = 0
                for content in excel_content_list:
                    sheet.write(row, column, content)
                    column += 1

            filename = request.user.username + '_' + confirmDate.now().strftime('%Y%m%d%H%M%S') + '.xls'
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
        except Exception as e:
            messages.info(self.request,"导出数据到execl报错:%s，请联系开发人员"%(str(e)))
    to_import_execl.short_description = u'导出数据到execl'

    def get_list_queryset(self):
        request = self.request
        qs = super(b_goods_sales_count_Admin, self).get_list_queryset()

        inter_val = request.GET.get('pub', '')
        if inter_val != '':
            qs = qs.filter(inter_val=inter_val)
        else:
            qs = qs.all()
        SKU = request.GET.get('sku', '')  # 商品SKU
        salername = request.GET.get('salername', '')
        # devdate = request.GET.get('devdate', '')
        begin_time_start = request.GET.get('begin_time_start', '')
        begin_time_end = request.GET.get('begin_time_end', '')
        purchaser = request.GET.get('purchaser', '')

        # deal_result = request.GET.get('deal_result', '')
        searchList = {}
        searchList = {
            'sku__exact':SKU,
            'salername__exact':salername,
            # 'devdate_exact':devdate,
            'devdate__gte': begin_time_start,
            'devdate__lt': begin_time_end,
            'purchaser__exact':purchaser
            # 'deal_result__exact': deal_result,
        }

        sl = {}
        for k, v in searchList.items():
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

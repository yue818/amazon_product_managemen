# encoding: utf-8
'''
@author: zhangyu
@contact: 292724306@qq.com
@software: pycharm
@file: wish_processed_order_Admin.py
@time: 2018-06-04 10:56
'''
import logging
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.db import connection
from brick.table.t_config_mstsc_log import t_config_mstsc_log
from datetime import datetime
import oss2
from Project.settings import *
from xlwt import *
from brick.public.create_dir import mkdir_p

logger = logging.getLogger('sourceDns.webdns.views')
t_config_mstsc_log_obj = t_config_mstsc_log(connection)


class wish_processed_order_Admin(object):
    wish_processed_order = True
    wish_site_tree = True

    downloadxls = True
    list_display_links = ("",)
    list_display = ['last_updated', 'order_id', 'show_days_to_fulfill', 'show_pic', 'show_order_size', 'show_price',
                    'show_cost', 'show_shipping', 'show_shipping_cost', 'quantity', 'show_order_total', 'show_customer',
                    'shopName', 'Operators', 'updateTime'
                    ]

    def show_pic(self, obj):
        rt = '<img src="%s" width="60" height="60"><p>{}</p><p>({})</p>'.format(obj.product_id,
                                                                                obj.sku) % obj.product_image_url
        if obj.country == 'RU':
            if float(obj.price) + float(obj.shipping) >= 3.0:
                rt = "{}<span style='background-color: #f7decf'>&nbsp;&nbsp;需要确认妥投&nbsp;&nbsp;</span>".format(rt)
        elif obj.country == 'IT':
            if float(obj.price) + float(obj.shipping) >= 7.0:
                rt = "{}<span style='background-color: #f7decf'>&nbsp;&nbsp;需要确认妥投&nbsp;&nbsp;</span>".format(rt)
        elif obj.country in ['FR', 'DE', 'CA', 'ES', 'DK', 'CL', 'AR', 'MX', 'CO', 'CR', 'SA', 'US', 'GB']:
            if float(obj.price) + float(obj.shipping) >= 10.0:
                rt = "{}<span style='background-color: #f7decf'>&nbsp;&nbsp;需要确认妥投&nbsp;&nbsp;</span>".format(rt)

        if obj.is_wish_express == 'True':
            rt = "{}<span style='background-color: #80b8f7'>&nbsp;&nbsp;Wish Express&nbsp;&nbsp;</span>".format(rt)
        return mark_safe(rt)

    show_pic.short_description = mark_safe("<p align='center' style='color:#428BCA'>查看商品</p>")

    def show_days_to_fulfill(self, obj):
        font_color = 'white'
        if obj.days_to_fulfill == 5:
            back_color = 'green'
        elif obj.days_to_fulfill == 4:
            back_color = 'yellow'
            font_color = 'black'
        else:
            back_color = 'red'
        rt = "<div style='background:{}; width:100%'>\
        <p align='center' style='color:{};font-weight:bold'>{}</p></div>".format(back_color, font_color, obj.days_to_fulfill)
        return mark_safe(rt)

    show_days_to_fulfill.short_description = mark_safe("<p align='center' style='color:#428BCA'>履行的天数</p>")

    def show_order_size(self, obj):
        rt = "<p>{}，{}</p>".format('size:{}'.format(obj.order_size) if obj.order_size else '',
                                   'color:{}'.format(obj.color) if obj.color else '')
        return mark_safe(rt)

    show_order_size.short_description = mark_safe("<p align='center' style='color:#428BCA'>变量</p>")

    def show_price(self, obj):
        rt = "<p>${}</p>".format(obj.price)
        return mark_safe(rt)

    show_price.short_description = mark_safe("<p align='center' style='color:#428BCA'>价格</p>")

    def show_cost(self, obj):
        rt = "<p>${}</p>".format(obj.cost)
        return mark_safe(rt)

    show_cost.short_description = mark_safe("<p align='center' style='color:#428BCA'>成本</p>")

    def show_shipping(self, obj):
        rt = "<p>${}</p>".format(obj.shipping)
        return mark_safe(rt)

    show_shipping.short_description = mark_safe("<p align='center' style='color:#428BCA'>配送</p>")

    def show_shipping_cost(self, obj):
        rt = "<p>${}</p>".format(obj.shipping_cost)
        return mark_safe(rt)

    show_shipping_cost.short_description = mark_safe("<p align='center' style='color:#428BCA'>配送费</p>")

    def show_order_total(self, obj):
        rt = "<p>${}</p>".format(obj.order_total)
        return mark_safe(rt)

    show_order_total.short_description = mark_safe("<p align='center' style='color:#428BCA'>总成本</p>")

    def show_customer(self, obj):
        rt = "<a id=show_customer%s>查看</a><script>$('#show_customer%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'收货地址',fix:false,shadeClose: true,maxmin:true,area:['400px','400px'],content:'/wish_processed_order/show_customer/?id=%s',});});</script>" % (
            obj.id, obj.id, obj.id)
        return mark_safe(rt)

    show_customer.short_description = mark_safe("<p align='center' style='color:#428BCA'>配送至</p>")


    actions = ['to_excel']

    def to_excel(self, request, queryset):
        try:
            path = MEDIA_ROOT + 'download_xls/' + request.user.username
            # if not os.path.exists(path):
            mkdir_p(MEDIA_ROOT + 'download_xls')
            os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))

            mkdir_p(path)
            os.popen('chmod 777 %s' % (path))

            w = Workbook()
            sheet = w.add_sheet('order')

            FIELDS = [u'订单ID', u'履行天数', u'店铺名称', u'运营人']

            for index, item in enumerate(FIELDS):
                sheet.write(0, index, item)

            # 写数据
            row = 0

            for qs in queryset:
                row = row + 1
                column = 0
                sheet.write(row, column, qs.order_id)  # A 订单ID

                column = column + 1
                sheet.write(row, column, qs.days_to_fulfill)  # B 履行天数

                column = column + 1
                sheet.write(row, column, qs.shopName)  # C 店铺名称

                column = column + 1
                sheet.write(row, column, qs.Operators)  # D 运营人

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

            messages.error(request, u'%s%s.%s/%s/%s' % (PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, request.user.username,
                                                        filename) + u':成功导出,可点击Download下载到本地............................。')
        except Exception as error:
            messages.error(request, u'{}'.format(error))
    to_excel.short_description = u'导出表格'

    def save_models(self):
        pass

    def get_list_queryset(self, ):
        # logger = logging.getLogger('sourceDns.webdns.views')
        request = self.request
        Operators = ''
        # 超级用户和金玉玲可以看到所有运营店铺
        if self.request.user.is_superuser or self.request.user.username == 'jinyuling' or self.request.user.username == 'meidandan':
            Operators = ''
        else:
            Operators = self.request.user.first_name
        qs = super(wish_processed_order_Admin, self).get_list_queryset()
        shopname = request.GET.get('shopname', '')
        status = request.GET.get('status', '')
        errorShop = request.GET.get('errorShop', '')
        list_errorShop = []
        list_errorShop_tmp = ''
        if errorShop == 'yes':
            # import redis
            # r = redis.Redis(host='localhost', port=6379, decode_responses=True)
            from django_redis import get_redis_connection
            r = get_redis_connection(alias='product')
            errorShopName1 = r.get('{}_errorShopName_1'.format(request.user.username))
            errorShopName2 = r.get('{}_errorShopName_2'.format(request.user.username))
            errorShopName3 = r.get('{}_errorShopName_3'.format(request.user.username))
            errorShopName = "{}{}{}".format(errorShopName1, errorShopName2, errorShopName3)
            list_errorShop_tmp = errorShopName.replace('[', '').replace(']', '').replace('u', '').replace("'",
                                                                                                          "") if errorShopName else ''
            list_errorShop = list_errorShop_tmp.split(',')
            for i in range(len(list_errorShop)):
                list_errorShop[i] = 'Wish-' + list_errorShop[i]
        days = []
        if status == '1':
            days = [1, 2, 3]
        elif status == '2':
            days = [4]
        elif status == '3':
            days = [5]
        searchList = {'shopName': shopname, 'days_to_fulfill__in': days, 'shopName__in': list_errorShop, 'Operators': Operators}
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
                messages.error(request, u'输入的查询数据有问题！')
        return qs

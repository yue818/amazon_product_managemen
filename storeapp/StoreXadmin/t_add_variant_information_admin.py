#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_add_variant_information_admin.py
 @time: 2018-04-08 17:51
"""
import json
from django.utils.safestring import mark_safe
from django.contrib import messages

from storeapp.models import t_online_info_wish_store

class t_add_variant_information_admin(object):
    change_shipping_flage = True

    def show_Infomartion(self, obj):
        Infostmp = json.loads(obj.Information)
        rt = u'<table class="table table-condensed"><tr><th>国家代码</th><th>最高变量价格</th><th>原运费</th><th>预改运费</th></tr>'
        for country in Infostmp.get('country_mo',[]):
            if Infostmp.get(country):
                rt = u'%s<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%\
                     (rt,country,Infostmp[country]['MaxVariablePrice'],
                      Infostmp[country]['Shipping'],Infostmp[country]['NewShpping'])
        rt = rt + '</table>'
        return mark_safe(rt)
    show_Infomartion.short_description = mark_safe(u'<p align="center"style="color:#428bca;">详细信息</p>')

    def show_Picture(self, obj):
        wish_store_objs = t_online_info_wish_store.objects.filter(ProductID=obj.ProductID).values('is_promoted','WishExpress')
        is_promoted = ''
        WishExpress = '[]'
        if wish_store_objs.exists():
            is_promoted = wish_store_objs[0]['is_promoted']
            WishExpress = wish_store_objs[0]['WishExpress']

        url = u'https://contestimg.wish.com/api/webimage/%s-medium.jpg' % str(obj.ProductID)
        rt = '<div><img src="%s" width="120" height="120"/></div>' % (url,)
        z_url = u'http://fancyqube-wish.oss-cn-shanghai.aliyuncs.com/Wish_Diamonds_pic%5Chuangzuan.png'
        h_url = u'http://main.cdn.wish.com/4fe4c5486817/img/product_badges/express_shipping/badge.png?v=13'
        if is_promoted == 'True':
            rt = rt + '<div style="float:left"><img src="%s"  width="20" height="20"  alt = "%s"  title="%s" /></div>' % (
            z_url, z_url, is_promoted)
        if WishExpress is not None and WishExpress != '[]':
            rt = rt + '<div style="float:left"><img src="%s"  width="20" height="20"  alt = "%s"  title="%s" /></div>' % (
            h_url, h_url, WishExpress)
        rt = rt
        return mark_safe(rt)

    show_Picture.short_description = mark_safe(u'<p align="center"style="color:#428bca;">图片</p>')

    list_display = ('show_Picture','ProductID', 'show_Infomartion','Sresult',)
    list_display_links = ('',)
    search_fields=('id','ProductID','Sresult','Information')
    list_filter = ('Sresult',)
    fields = ('id',)

    actions = ['to_get_shipping','to_change_shipping',]

    def to_get_shipping(self, request, objs):
        from app_djcelery.tasks import wish_change_shipping_to_country
        for i, obj in enumerate(objs.filter(Sresult__isnull=True)):
            if i >= 50:
                break
            if obj.Sresult is None:
                wish_change_shipping_to_country.delay([obj.id])
        messages.success(request, u'正在刷新，请稍后刷新页面。。。')

    to_get_shipping.short_description = u'点击刷新'

    def to_change_shipping(self, request, objs):
        from app_djcelery.tasks import will_change_shipping
        for obj in objs.filter(Sresult='0'):
            will_change_shipping.delay(obj.id)
        messages.success(request, u'正在修改，请稍后刷新页面。。。')

    to_change_shipping.short_description = u'点击修改国际运费'



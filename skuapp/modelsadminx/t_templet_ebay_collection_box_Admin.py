# -*- coding: utf-8 -*-

# import oss2
# from skuapp.table.t_templet_ebay_collection_box import *
# from skuapp.table.t_templet_ebay_variations import *

import logging
from datetime import datetime

from django.utils.safestring import mark_safe
from django.contrib import messages

from skuapp.table.t_templet_public_ebay import t_templet_public_ebay
from ebayapp.table.t_config_site_ebay import t_config_site_ebay

logger = logging.getLogger('django.skuapp.modelsadminx')
# PREFIX = 'http://'
# ACCESS_KEY_ID = 'LTAIH6IHuMj6Fq2h'
# ACCESS_KEY_SECRET = 'N5eWsbw8qBkMfPREkgF2JnTsDASelM'
# ENDPOINT = 'vpc100-oss-cn-shanghai.aliyuncs.com'
# ENDPOINT_OUT = 'oss-cn-shanghai.aliyuncs.com'
# BUCKETNAME = 'fancyqube-upload-xls'


class t_templet_ebay_collection_box_Admin(object):
    # plateform_distribution_navigation = True
    site_left_menu_flag_ebay = True
    search_box_flag = True

    list_display = ('id', 'show_image', 'show_site', 'Selleruserid', 'sku', 'Title', 'show_variation', 'CoreWords', 'show_info')

    list_display_links = ('',)

    fields = ('ExcelFile',)

    list_editable = ('CoreWords',)

    actions = ['to_public_templet']

    def show_image(self, obj):
        imageUrl = obj.Images.split(',')[0]  # .split('?')[0]
        # imageUrl = imageUrl.replace('https://i.ebayimg.com','http://fancyqube-ebaypic.oss-cn-shanghai.aliyuncs.com')
        rt = '<a href="/show_ebay_image/?myId=%s" target="_blank"><img src="%s" style="width:150px;height:150px"></a>' % (obj.id, imageUrl)
        return mark_safe(rt)
    show_image.short_description = u'<p align="center"style="color:#428bca;">主图</p>'

    def show_site(self, obj):
        try:
            rt = t_config_site_ebay.objects.get(siteID=obj.Site).siteName
        except:
            rt = str(obj.Site)

        return mark_safe(rt)

    show_site.short_description = u'<p align="center"style="color:#428bca;">站点</p>'

    def show_variation(self, obj):
        """展示修改变体信息"""
        rt = u'<table   style="text-align:center;" border="1" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1">' \
             u'<tr bgcolor="#C00"><th style="text-align:center">SKU</th><th style="text-align:center">价格</th>' \
             u'<th style="text-align:center">数量</th><th style="text-align:center">颜色</th>' \
             u'<th style="text-align:center">尺寸</th>'

        if obj.Variation:
            variation_list = eval(obj.Variation).get("Variation", '')
            if variation_list != '':
                i = 0
                for variation in variation_list:
                    if i < 5:
                        sku = variation.get('SKU', '')
                        price = variation.get('StartPrice', '')
                        quantity = variation.get('Quantity', '')

                        color = ''
                        size = ''
                        VariationSpecifics = variation.get('VariationSpecifics', '')
                        if VariationSpecifics != '':
                            NameValueList = VariationSpecifics.get('NameValueList', '')
                            if NameValueList != '':
                                for each in NameValueList:
                                    if 'Color' in each.values():
                                        color = each.get('Value', '')
                                    if 'Size' in each.values():
                                        size = each.get('Value', '')

                        rt = u'%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> ' % \
                             (rt, sku, price, quantity, color, size)
                    else:
                        break
                    i += 1
        else:
            sku = obj.sku
            price = obj.StartPrice
            quantity = obj.Quantity
            color = ''
            size = ''
            rt = u'%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> ' % \
                (rt, sku, price, quantity, color, size)

        rt = u'%s<tr><td><a id="link_id_%s">点击查看</a></td></tr>' % (rt, obj.id)
        rt = u"%s</table><script>$('#link_id_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan'," \
             u"title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['1200px','700px']," \
             u"content:'/show_ebay_variation/?box=%s&flag=ebay',btn:['关闭页面'],end:function()" \
             u"{location.reload();}});});</script>" % (rt, obj.id, obj.id)

        return mark_safe(rt)

    show_variation.short_description = u'<p align="center"style="color:#428bca;">变体信息</p>'

    def show_info(self, obj):
        """展示时间、人员信息"""
        st = ''
        if obj.Status == 'OPEN':
            st = u'<font color="#FFCC33">正在处理</font>'
        elif obj.Status == 'YES':
            st = u'<font color="#FF3333">已提交</font>'
        elif obj.Status == 'NO':
            st = u'<font color="#00BB00">未提交</font>'
        rt = u'创建人:%s<br>创建时间:<br>%s<br>更新人:%s<br>更新时间:<br>%s<br>提交状态:%s<br>上传文件:<br>%s' \
             % (obj.CreateStaff, obj.CreateTime, obj.UpdateStaff, obj.UpdateTime, st, obj.ExcelFile)
        return mark_safe(rt)

    show_info.short_description = u'<p align="center"style="color:#428bca;">采集信息</p>'

    def save_models(self):
        request = self.request
        file_obj = request.FILES.get('ExcelFile')
        now_time = datetime.now()
        first_name = request.user.first_name
        from app_djcelery.tasks import ebay_open
        ebay_open.delay(file_obj, now_time, first_name)
        messages.info(request, '表格正在处理中…………')

    def to_public_templet(self, request, queryset):
        time = datetime.now()
        user = request.user.first_name
        for obj in queryset:
            if obj.Status == 'YES':
                messages.error(request, u'ID是%s已经提交为公共模板，请勿重复提交！' % obj.id)
            elif obj.Flag == 100:
                messages.error(request, u'ID是%s的商品自定义属性错误，请修改后提交！' % obj.id)
            else:
                t_templet_public_ebay_obj = t_templet_public_ebay()
                t_templet_public_ebay_obj.__dict__ = obj.__dict__
                t_templet_public_ebay_obj.CreateTime = time
                t_templet_public_ebay_obj.CreateStaffName = user
                t_templet_public_ebay_obj.UpdateTime = time
                t_templet_public_ebay_obj.UpdateStaff = user
                t_templet_public_ebay_obj.Status = ''
                t_templet_public_ebay_obj.UsedNum = 0
                t_templet_public_ebay_obj.save()
                obj.Status = 'YES'
                obj.save()
    to_public_templet.short_description = u'转为公共模板'

    def get_list_queryset(self, ):
        request = self.request
        qs = super(t_templet_ebay_collection_box_Admin, self).get_list_queryset()
        id = request.GET.get('id', '')
        Title = request.GET.get('Title', '')
        Site = request.GET.get('Site', '')
        Selleruserid = request.GET.get('Selleruserid', '')

        Status = request.GET.get('Status', '')
        sku = request.GET.get('sku', '')
        CreateStaff = request.GET.get('CreateStaff', '')
        UpdateStaff = request.GET.get('UpdateStaff', '')

        CreateTime_Start = request.GET.get('CreateTime_Start', '')
        CreateTime_End = request.GET.get('CreateTime_End', '')
        UpdateTime_Start = request.GET.get('UpdateTime_Start', '')
        UpdateTime_End = request.GET.get('UpdateTime_End', '')

        searchList = {'id__exact': id, 'Title__contains': Title, 'Site__exact': Site, 'Selleruserid__exact': Selleruserid,
                      'Status__exact': Status, 'sku__exact': sku,
                      'CreateStaff__exact': CreateStaff, 'UpdateStaff__exact': UpdateStaff,
                      'CreateTime__gte': CreateTime_Start, 'CreateTime__lt': CreateTime_End,
                      'UpdateTime__gte': UpdateTime_Start, 'UpdateTime__lt': UpdateTime_End,
                      }
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
            except Exception:
                messages.error(request, u'输入的查询数据有问题！')

        if not request.user.is_superuser:
            qs = qs.filter(CreateStaff=request.user.first_name)
        return qs

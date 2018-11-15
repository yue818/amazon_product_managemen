# -*- coding: utf-8 -*-

# import oss2
# from datetime import datetime
# from skuapp.table.t_templet_ebay_collection_box import t_templet_ebay_collection_box
# from skuapp.table.t_templet_ebay_upload_result import t_templet_ebay_upload_result
# from skuapp.table.t_templet_public_ebay import t_templet_public_ebay
# from skuapp.table.t_templet_ebay_variations import t_templet_ebay_variations
# from skuapp.table.public import public

from django.contrib import messages
from django.utils.safestring import mark_safe
from ebayapp.table.t_config_site_ebay import t_config_site_ebay

# PREFIX = 'http://'
# ACCESS_KEY_ID = 'LTAIH6IHuMj6Fq2h'
# ACCESS_KEY_SECRET = 'N5eWsbw8qBkMfPREkgF2JnTsDASelM'
# ENDPOINT = 'vpc100-oss-cn-shanghai.aliyuncs.com'
# ENDPOINT_OUT = 'oss-cn-shanghai.aliyuncs.com'
# BUCKETNAME = 'fancyqube-upload-xls'


class t_templet_ebay_upload_result_Admin(object):
    # plateform_distribution_navigation = True
    site_left_menu_flag_ebay = True
    search_box_flag = True

    list_display = ('id', 'show_image', 'show_site', 'Selleruserid', 'ShopName', 'show_SKU_list', 'Title', 'taskid', 'Status', 'ErrorMessage',)

    def show_image(self, obj):
        imageUrl = obj.Images.split(',')[0]  # .split('?')[0]
        # imageUrl = imageUrl.replace('https://i.ebayimg.com','http://fancyqube-ebaypic.oss-cn-shanghai.aliyuncs.com')
        rt = '<a href="/show_ebay_image/?myId=%s" target="_blank"><img src="%s" style="width:150px;height:150px"></a>' % (obj.id, imageUrl)
        return mark_safe(rt)

    show_image.short_description = u'<p align="center"style="color:#428bca;">主图</p>'

    def show_SKU_list(self, obj):
        rt = '<table   style="text-align:center;" border="1" cellpadding="2" cellspacing="1" bgcolor="#c1c1c1"><tr bgcolor="#C00"><th style="text-align:center">商品SKU</th><th style="text-align:center">店铺SKU</th></tr>'
        sku = eval(obj.product_sku.replace("`", "'"))
        shop_sku = eval(obj.shopsku.replace("`", "'"))
        for i in range(len(sku)):
            if i < 5:
                rt = '%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td></tr> ' % (rt, sku[i], shop_sku[i])
            else:
                break
            i += 1
        if len(sku) > 3:
            rt = '%s<tr><td><a id="link_id_%s">查看更多</a></td></tr>' % (rt, obj.id)
        else:
            rt = rt
        rt = "%s</table><script>$('#link_id_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['500px','500px'],content:'/t_templet_ebay_upload_result/ebay_result_SKU/?abc=%s',});});</script>" % (rt, obj.id, obj.id)
        return mark_safe(rt)

    show_SKU_list.short_description = u'<p align="center"style="color:#428bca;">子SKU</p>'

    def show_site(self, obj):
        try:
            rt = t_config_site_ebay.objects.get(siteID=obj.Site).siteName
        except:
            rt = str(obj.Site)

        return mark_safe(rt)

    show_site.short_description = u'<p align="center"style="color:#428bca;">站点</p>'

    def get_list_queryset(self, ):
        request = self.request
        qs = super(t_templet_ebay_upload_result_Admin, self).get_list_queryset()
        id = request.GET.get('id', '')
        Title = request.GET.get('Title', '')
        Site = request.GET.get('Site', '')
        Selleruserid = request.GET.get('Selleruserid', '')
        Status = request.GET.get('Status', '')
        productSKU = request.GET.get('productSKU', '')
        shopSKU = request.GET.get('shopSKU', '')
        taskid = request.GET.get('taskid', '')
        ShopName = request.GET.get('ShopName', '')
        PayPalEmailAddress = request.GET.get('PayPalEmailAddress', '')
        CreateStaff = request.GET.get('CreateStaff', '')
        UpdateStaff = request.GET.get('UpdateStaff', '')

        CreateTime_Start = request.GET.get('CreateTime_Start', '')
        CreateTime_End = request.GET.get('CreateTime_End', '')
        UpdateTime_Start = request.GET.get('UpdateTime_Start', '')
        UpdateTime_End = request.GET.get('UpdateTime_End', '')

        searchList = {'id__exact': id, 'Title__contains': Title, 'Site__exact': Site, 'Selleruserid__exact': Selleruserid,
                      'Status__exact': Status, 'product_sku__contains': productSKU, 'shopsku__contains': shopSKU,
                      'taskid__exact': taskid, 'ShopName__exact': ShopName, 'PayPalEmailAddress__exact': PayPalEmailAddress,
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
        return qs

# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from skuapp.table.t_online_info_amazon import *
from skuapp.table.t_online_amazon_fba_inventory import *
from django.contrib import messages


class t_online_amazon_fba_inventory_Admin(object):
    search_box_flag = True
    def show_product(self,obj) :
        site_url_dict = {'US': 'https://www.amazon.com/',
                         'UK': 'https://www.amazon.co.uk/',
                         'JP': 'https://www.amazon.co.jp/',
                         'DE': 'https://www.amazon.de/',
                         'FR': 'https://www.amazon.fr/',
                         'AU': 'https://www.amazon.com.au/'}

        if obj.ShopName and obj.ShopName.split('-')[-1].split('/')[0] in site_url_dict:
            site_url = site_url_dict[obj.ShopName.split('-')[-1].split('/')[0]]
        else:
            site_url = 'https://www.amazon.com/'

        rt ='%s<br><b>ASIN: </b><a href="%sdp/%s" target="_blank">%s</a><br><b>FNSKU: </b>%s<br><b>ShopSKU: </b>%s<br><b>店铺: </b>%s'%(obj.product_name,site_url, obj.asin, obj.asin, obj.fnsku, obj.sku, obj.ShopName)
        return mark_safe(rt)
    show_product.short_description = mark_safe(u'<p style="color:#428BCA" align="center">商品名称</p>')

    
    def show_Picture(self,obj) :
        t_online_info_amazon_objs = t_online_info_amazon.objects.filter(asin1=obj.asin,seller_sku=obj.sku, ShopName=obj.ShopName).values_list('image_url','SKU')
        rt = ''
        for t_online_info_amazon_obj in t_online_info_amazon_objs:
            rt ='%s<img src="%s"  width="120" height="120"  alt = "%s"  title="%s"  />'%(rt,t_online_info_amazon_obj[0],t_online_info_amazon_obj[0],t_online_info_amazon_obj[0])
        return mark_safe(rt)
    show_Picture.short_description = mark_safe(u'<p style="color:#428BCA" align="center">图片信息</p>')
    
    def show_afn_warehouse_quantity(self,obj):
        if obj.afn_warehouse_quantity < 10:
            rt = u'<font color="red"><b>%s</b></font>'%(obj.afn_warehouse_quantity)
        else:
            rt = u'%s'%(obj.afn_warehouse_quantity)
        return mark_safe(rt)
    show_afn_warehouse_quantity.short_description = mark_safe(u'<p style="color:#428BCA" align="center">FBA库存</p>')

    def get_list_queryset(self):
        request = self.request
        qs = super(t_online_amazon_fba_inventory_Admin, self).get_list_queryset()

        shopname = request.GET.get('ShopName', '')
        SKU = request.GET.get('SKU', '')
        SKU = '' if SKU == '' else SKU.strip().replace(' ','+').split(',')
        # messages.success(request, 'sku is:%s' %SKU)
        ASIN = request.GET.get('ASIN', '')
        ASIN = '' if ASIN == '' else ASIN.split(',')

        afn_fulfillable_quantity_start = request.GET.get('afn_fulfillable_quantity_start', '')
        afn_fulfillable_quantity_end = request.GET.get('afn_fulfillable_quantity_end', '')
        afn_unsellable_quantity_start = request.GET.get('afn_unsellable_quantity_start', '')
        afn_reserved_quantity_start = request.GET.get('afn_reserved_quantity_start', '')
        afn_total_quantity_start = request.GET.get('afn_total_quantity_start', '')
        mfn_fulfillable_quantity_start = request.GET.get('mfn_fulfillable_quantity_start', '')
        afn_warehouse_quantity_start = request.GET.get('afn_warehouse_quantity_start', '')
        afn_unsellable_quantity_end = request.GET.get('afn_unsellable_quantity_end', '')
        afn_reserved_quantity_end = request.GET.get('afn_reserved_quantity_end', '')
        afn_total_quantity_end = request.GET.get('afn_total_quantity_end', '')
        mfn_fulfillable_quantity_end = request.GET.get('mfn_fulfillable_quantity_end', '')
        afn_warehouse_quantity_end = request.GET.get('afn_warehouse_quantity_end', '')

        searchList = {'ShopName__icontains': shopname,
                      'sku__in': SKU,
                      'asin__in': ASIN,

                      'afn_fulfillable_quantity__gte': afn_fulfillable_quantity_start,
                      'afn_fulfillable_quantity__lte': afn_fulfillable_quantity_end,

                      'afn_unsellable_quantity__gte': afn_unsellable_quantity_start,
                      'afn_unsellable_quantity__lte': afn_unsellable_quantity_end,

                      'afn_reserved_quantity__gte': afn_reserved_quantity_start,
                      'afn_reserved_quantity__lte': afn_reserved_quantity_end,

                      'afn_total_quantity__gte': afn_total_quantity_start,
                      'afn_total_quantity__lte': afn_total_quantity_end,

                      'mfn_fulfillable_quantity__gte': mfn_fulfillable_quantity_start,
                      'mfn_fulfillable_quantity__lte': mfn_fulfillable_quantity_end,

                      'afn_warehouse_quantity__gte': afn_warehouse_quantity_start,
                      'afn_warehouse_quantity__lte': afn_warehouse_quantity_end,

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
            except Exception, ex:
                messages.error(request, u'输入的查询数据有误！')
        return qs.exclude(condition_a='Unknown')
        # return qs.filter(afn_listing_exists='Yes')
    
    list_display = ('id','show_Picture','show_product','order3days','order7days','condition_a','your_price','mfn_listing_exists','mfn_fulfillable_quantity','afn_listing_exists','show_afn_warehouse_quantity','afn_fulfillable_quantity','afn_unsellable_quantity','afn_reserved_quantity','afn_total_quantity','per_unit_volume','afn_inbound_working_quantity','afn_inbound_shipped_quantity','afn_inbound_receiving_quantity','RefreshTime',)
    # list_filter = ('afn_inbound_working_quantity','afn_inbound_shipped_quantity','afn_inbound_receiving_quantity','RefreshTime','afn_warehouse_quantity','ShopName')
    search_fields = ('id','sku','asin','fnsku','ShopName')
    
    
    
    

# -*- coding: utf-8 -*-
from django.contrib import messages
from django.utils.safestring import mark_safe
from skuapp.table.t_tort_aliexpress import t_tort_aliexpress
from pyapp.models import kc_currentstock,b_goods as py_b_goods
from datetime import datetime
from django.db.models import Q


class t_goods_shelves_dis_upload_Admin(object):
    search_box_flag = True
    shelves_search = False
    list_per_page=30
    def show_Picture(self,obj) :
        url = u'https://contestimg.wish.com/api/webimage/%s-medium.jpg'%str(obj.ProductID)
        rt =  '<img src="%s"  width="120" height="120"  alt = "%s"  title="%s"  />  '%(url,url,url)
        return mark_safe(rt)
    show_Picture.short_description = u'图片'
    
    def show_ShopName_Seller(self,obj) :
        rt = u'卖家简称:<br>%s<br>店长/销售员:<br>%s'%(obj.ShopName,obj.Seller)
        return mark_safe(rt)
    show_ShopName_Seller.short_description = u'卖家简称/店长/销售员'

    def show_tort_status(self,obj):
        count = t_tort_aliexpress.objects.filter(MainSKU=obj.MainSKU,Site='Wish')[:1]
        if count.exists():
            rt = u'<div class="box" style="width: 80px;height: 30px;background-color: #FF3333;text-align: center;line-height: 30px;border-radius: 4px">Wish仿品</div>'
        else:
            rt = u'<div class="box" style="width: 80px;height: 30px;background-color: #66FF66;text-align: center;line-height: 30px;border-radius: 4px">未侵权</div>'
        return mark_safe(rt)
    show_tort_status.short_description = u'侵权状态'

    # def Show_KC(self,obj):
    #     rt = ''
    #     b_goods_objs = py_b_goods.objects.filter(SKU=obj.SKU)
    #     if b_goods_objs.exists() :
    #         kc_currentstock_objs = kc_currentstock.objects.filter(GoodsID = b_goods_objs[0].NID)
    #         if kc_currentstock_objs.exists() :
    #             for kc_currentstock_obj in kc_currentstock_objs:
    #                 rt = u'%s'%(kc_currentstock_obj.Number-kc_currentstock_obj.ReservationNum)
    #     return mark_safe(rt)
    # Show_KC.short_description = u'可用库存'
    
    list_display = ('PlatformName','show_Picture','show_tort_status','show_ShopName_Seller','ProductID','Title','SKU','ShopSKU','AvailableStock_SKU','Orders7Days','OfSales','Price','Quantity','Status','DateUploaded','GoodsStatus','APIState',)

    actions = ['do_tort_shelve_wish']
    
    def do_tort_shelve_wish(self,request,objs):
        from app_djcelery.tasks import product_and_bottom_shelf_func
        user_name = request.user.first_name
        i = 0
        for obj in objs:
            i = i + 1
            if i >= 5000:
                break

            obj.APIState = 'wait'
            obj.save()

            record_id = [obj.id, obj.ShopName, obj.ShopSKU,obj.SKU]
            product_and_bottom_shelf_func.delay([record_id,], user_name, 'enshopsku')

        messages.success(request, u'数据已经提交，请稍等。。正在处理。。。')
    do_tort_shelve_wish.short_description = u'产品上架'
    
    def get_list_queryset(self):
        request = self.request
        qs = super(t_goods_shelves_dis_upload_Admin, self).get_list_queryset().filter(~Q(ReviewState = 'rejected' )).filter(filtervalue=1,GoodsStatus='1',Status = 'Disabled')

        ProductID = request.GET.get('ProductID', '')                #产品ID
        ShopName = request.GET.get('ShopName', '')                  #店铺名称
        MainSKU = request.GET.get('MainSKU', '')                    #主SKU
        SKU = request.GET.get('SKU', '')                            #商品SKU
        ShopSKU = request.GET.get('ShopSKU', '')                    #店铺SKU
        
        GoodsStatus = request.GET.get('GoodsStatus', '')            #商品状态
        APIState = request.GET.get('APIState', '')                  #api执行状态

        OfSalesStart = request.GET.get('OfSalesStart', '')          #订单量
        OfSalesEnd = request.GET.get('OfSalesEnd', '')
        
        Orders7DaysStart = request.GET.get('Orders7DaysStart', '')  #7天order数
        Orders7DaysEnd = request.GET.get('Orders7DaysEnd', '')

        searchList = {'ProductID__exact': ProductID,
                      'ShopName__exact': ShopName,
                      'MainSKU__exact': MainSKU,
                      'SKU__exact': SKU,
                      'ShopSKU__exact': ShopSKU,
                      
                      'GoodsStatus__exact': GoodsStatus,
                      'APIState__exact': APIState,

                      'Orders7Days__gte': Orders7DaysStart, 'Orders7Days__lt': Orders7DaysEnd,
                      'OfSales__gte': OfSalesStart, 'OfSales__lt': OfSalesEnd,
                      }
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    # if k == 'ShopName__exact':
                    #  v = 'Wish-' + v.zfill(4)
                    # messages.error(request, v)
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')

        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(Seller = request.user.first_name)

      
       
    

    
    
    
    
    
    

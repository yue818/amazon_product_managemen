# coding=utf-8

"""
wish、joom铺货admin公共函数
"""
import re
from urllib import urlencode
from skuapp.table.t_product_image_modify import t_product_image_modify
from skuapp.table.t_tort_aliexpress import  t_tort_aliexpress
from django.db import connection
from django_redis import get_redis_connection
redis_coon = get_redis_connection(alias='product')
from brick.classredis.classsku import classsku
from brick.pricelist.calculate_price import calculate_price
classsku_obj = classsku(connection, redis_coon)


# def show_variants(obj, plateform, page, url):
#     rt = u'<table  class="table table-condensed" >' \
#          u'<tr bgcolor="#C00"><th>子SKU</th><th>店铺SKU</th><th>库存量</th><th>价格</th><th>运费</th>' \
#          u'<th>利润率</th><th>状态</th><th style="text-align:center">普源状态</th></tr>'
#     # shopskulist = listingobjs.getShopSKUList(obj.SrcProductID)
#     try:
#         variantsList = eval(obj.Variants)
#     except:
#         variantsList = []
#     num = 0
#     for variant in variantsList:
#         productSKU = variant['Variant']['productSKU']
#         shopSKU = variant['Variant']['sku']
#         inventory = variant['Variant']['inventory']
#         price = variant['Variant']['price']
#         shipping = variant['Variant']['shipping']
#         enabled = variant['Variant']['enabled']
#         profit_id = str(productSKU) + str(num)
#         num += 1
#         if enabled == True:
#             listing_state = 'Enabled'
#         else:
#             listing_state = 'Disabled'
#         goodsStatus = classsku_obj.get_goodsstatus_by_sku(productSKU)
#         cost_price = classsku_obj.get_price_by_sku(productSKU)
#         weight = classsku_obj.get_weight_by_sku(productSKU)
#         try:
#             sellingPrice = float(price) + float(shipping)
#             calculate_price_obj = calculate_price(productSKU, float(cost_price), float(weight))
#             profitrate_info = calculate_price_obj.calculate_profitRate(sellingPrice, platformCountryCode='WISH-US', DestinationCountryCode='US')
#             profitrate = profitrate_info['profitRate']
#         except:
#             sellingPrice = ''
#             profitrate = ''
#         rt = '%s<tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' \
#              '<td><a><span id="%s">%s%%</span></a></td><td>%s</td><td>%s</td></tr> ' \
#              % (rt, productSKU, shopSKU, inventory, price, shipping, profit_id, profitrate, listing_state, goodsStatus)
#         rt = u"%s<script>$('#%s').on('click',function()" \
#              u"{layer.open({type:2,skin:'layui-layer-lan',title:'算价表'," \
#              u"fix:false,shadeClose: true,maxmin:true,area:['1300px','900px']," \
#              u"content:'/price_list/?SKU=%s&sellingPrice=%s&platformCountryCode=%s&DestinationCountryCode=%s',});});</script>" \
#              % (rt, profit_id, productSKU, sellingPrice, 'WISH-US', 'US')
#     rt = u'%s<tr><td><a id="link_id_%s">点击修改</a></td></tr>' % (rt, obj.id)
#     rt = u"%s</table><input type='hidden' id='getValue' name='getValue' value='0' />" \
#          u"<script>$('#link_id_%s').on('click',function()" \
#          u"{var refresh=document.getElementById('getValue').value;" \
#          u"layer.open({type:2,skin:'layui-layer-lan',title:'查看全部'," \
#          u"fix:false,shadeClose: true,maxmin:true,area:['1200px','700px']," \
#          u"content:'/show_wish_variant/?id=%s&plateform=%s&page=%s&current_url=%s'," \
#          u"end:function(){if (refresh=='1'){location.reload()};}});});</script>" % (
#              rt, obj.id, obj.id, plateform, page, url)
#     return rt


def show_variants(obj, plateform, page):
    rt = u'<table  class="table table-condensed" >' \
         u'<tr bgcolor="#C00"><th>子SKU</th><th>店铺SKU</th><th>库存量</th><th>价格</th><th>运费</th>' \
         u'<th>利润率</th><th>状态</th><th style="text-align:center">普源状态</th></tr>'
    try:
        variantsList = eval(obj.Variants)
    except:
        variantsList = []
    num = 0
    for variant in variantsList:
        try:
            productSKU = re.findall('([A-Z0-9-]+)', str(variant['Variant']['productSKU']))[0]
        except:
            productSKU = variant['Variant']['productSKU']
        shopSKU = variant['Variant']['sku']
        inventory = variant['Variant']['inventory']
        price = variant['Variant']['price']
        shipping = variant['Variant']['shipping']
        enabled = variant['Variant']['enabled']
        profit_id = str(productSKU) + str(num) + str(obj.id)
        num += 1
        if enabled == True:
            listing_state = 'Enabled'
        else:
            listing_state = 'Disabled'
        goodsStatus = classsku_obj.get_goodsstatus_by_sku(productSKU)
        cost_price = classsku_obj.get_price_by_sku(productSKU)
        weight = classsku_obj.get_weight_by_sku(productSKU)
        try:
            sellingPrice = float(price) + float(shipping)
            calculate_price_obj = calculate_price(productSKU, float(cost_price), float(weight))
            profitrate_info = calculate_price_obj.calculate_profitRate(sellingPrice, platformCountryCode='WISH-US', DestinationCountryCode='US')
            profitrate = profitrate_info['profitRate']
        except:
            sellingPrice = ''
            profitrate = ''
        rt = '%s<tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' \
             '<td><a><span id="%s">%s%%</span></a></td><td>%s</td><td>%s</td></tr> ' \
             % (rt,  variant['Variant']['productSKU'], shopSKU, inventory, price, shipping, profit_id, profitrate, listing_state, goodsStatus)
        rt = u"%s<script>$('#%s').on('click',function()" \
             u"{layer.open({type:2,skin:'layui-layer-lan',title:'算价表'," \
             u"fix:false,shadeClose: true,maxmin:true,area:['1300px','900px']," \
             u"content:'/price_list/?SKU=%s&sellingPrice=%s&platformCountryCode=%s&DestinationCountryCode=%s',});});</script>" \
             % (rt, profit_id, productSKU, sellingPrice, 'WISH-US', 'US')
    rt = u'%s<tr><td><a id="link_id_%s">点击修改</a></td></tr>' % (rt, obj.id)
    rt = u"%s</table><script>$('#link_id_%s').on('click',function(){" \
         u"layer.open({type:2,skin:'layui-layer-lan',title:'查看全部'," \
         u"fix:false,shadeClose: true,maxmin:true,area:['1650px','800px']," \
         u"content:'/show_wish_variant/?id=%s&plateform=%s&page=%s'," \
         u"end:function(){location.reload();}});});</script>" % (
             rt, obj.id, obj.id, plateform, page)
    return rt


def show_picture(obj, plateform='wish') :
    """展示主图"""
    manin_image = obj.MainImage
    if manin_image:
        if 'fancyqube' in manin_image:
            rt = '<img src="%s" width="120" height="120"></a>' % manin_image
        else:
            url = manin_image.replace('-original', '-medium')
            data = {'_p_MainSKU__in': obj.MainSKU, 'plateform': plateform}
            param = urlencode(data)
            image_modify_obj = t_product_image_modify.objects.filter(MainSKU=obj.MainSKU)
            if image_modify_obj.exists():
                if image_modify_obj[0].UpdateFlag == 1:
                    rr = '<br><span style="color:blue;">有新的图片<span>'
                else:
                    rr = ''
            else:
                rr = '<br><span style="color:red;">无备用主图<span>'
            rt = '<a href="/Project/admin/skuapp/t_product_image_modify/?%s" target="_blank" id="pic_id_%s">' \
                 '<img src="%s" width="120" height="120"></a>%s' % (param, obj.id, url, rr)
    else:
        rt = '<img src="%s" width="120" height="120"></a>' % ''
    return rt


def show_tortInfo(obj):
    try:
        ret = t_tort_aliexpress.objects.filter(MainSKU=obj.MainSKU).values('Site')
    except t_tort_aliexpress.DoesNotExist:
        ret = None
    if not ret:
        rt = u"<span style='color: green; font-weight: bold;'>未侵权</span>"
    else:
        rets = list()
        for i in ret:
            if not i['Site']:
                if u'未知' not in rets:
                    rets.append(u'未知')
            else:
                if i['Site'] not in rets:
                    rets.append(i['Site'])
        rt = u"<span style='color: red; font-weight: bold;'>%s  侵权</span>" % (','.join(rets))
    return rt


def show_id(obj):
    product_id = obj.SrcProductID
    plateform = obj.PlateForm
    if plateform == 'Wish':
        rt = u'Wish<br><a href=" https://www.wish.com/c/%s" target="_blank">%s</a>' % (product_id, product_id)
    elif plateform == 'AliExpress':
        rt = u'AliExpress<br><a href="https://www.aliexpress.com/item/c/%s.html" target="_blank">%s</a>' % (product_id, product_id)
    else:
        rt = u'Wish<br><a href=" https://www.wish.com/c/%s" target="_blank">%s</a>' % (product_id, product_id)
    return rt


def show_mainsku(obj):
    main_sku = obj.MainSKU
    main_sku_str = u''
    if main_sku:
        main_sku_list = main_sku.split(',')
    else:
        main_sku_list = []

    if len(main_sku_list) == 1:
        main_sku_str = main_sku
    elif len(main_sku_list) == 2:
        main_sku_str = ','.join(main_sku_list)
    else:
        for i in range(len(main_sku_list)):
            if (i + 1) % 2 == 0:
                main_sku_str = u'%s<span>%s<span><br>' % (main_sku_str, main_sku_list[i])
            else:
                main_sku_str = u'%s<span>%s,<span>' % (main_sku_str, main_sku_list[i])
    return main_sku_str
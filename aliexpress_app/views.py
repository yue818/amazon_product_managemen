#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from brick.pricelist.calculate_price import calculate_price
from brick.aliexpress.aliexpress_compare_price import get_product_info
from aliexpress_app.table.t_aliexpress_price_parity_log import t_aliexpress_price_parity_log
from aliexpress_app.table.t_aliexpress_online_info import t_aliexpress_online_info
from aliexpress_app.table.t_aliexpress_online_info_detail import t_aliexpress_online_info_detail
from aliexpress_app.table.t_aliexpress_competitor_product_info import t_aliexpress_competitor_product_info


# 比价设置价格
@csrf_exempt
def aliexpress_price_parity(request):
    productid = request.POST.get('productid', '')
    ShopSKU = request.POST.get('ShopSKU', '')
    newprice = request.POST.get('newprice', '')
    oldprice = request.POST.get('oldprice', '')
    person = request.POST.get('person', '')
    SKU = request.POST.get('SKU', '')

    sRes = {'resultCode': '0', 'messages': ''}
    # source_price = t_aliexpress_online_info_detail.objects.get(ProductID=productid, ShopSKU=ShopSKU).Price
    # if newprice == source_price:
    #     sRes['resultCode'] = '-2'
    #     return JsonResponse(sRes)
    try:
        if newprice != '':
            float(newprice)
    except Exception:
        sRes['resultCode'] = '-1'
        sRes['messages'] = '%s is illegal price' % newprice
        return JsonResponse(sRes)
    pp_log_changeflags = t_aliexpress_price_parity_log.objects.filter(ProductID=productid, ShopSKU=ShopSKU).values('ChangeFlag')
    if pp_log_changeflags:
        changes = list(map(lambda x: x['ChangeFlag'], pp_log_changeflags))
        if 'False' in changes:
            res = udpate_aliexpress_price_parity_log(productid, ShopSKU, newprice, oldprice, person, 'update')
        else:
            res = udpate_aliexpress_price_parity_log(productid, ShopSKU, newprice, oldprice, person, 'insert')
    else:
        res = udpate_aliexpress_price_parity_log(productid, ShopSKU, newprice, oldprice, person, 'insert')

    profitrate = ''
    if res['code'] == 0:
        update_aliexpress_online_price_parity(productid, person)
        try:
            calculate_price_obj = calculate_price(str(SKU))
            sellprice = float(newprice)
            profitrate_info = calculate_price_obj.calculate_profitRate(sellprice, platformCountryCode='ALIEXPRESS-RUS', DestinationCountryCode='RUS')
            if profitrate_info:
                profitrate = profitrate_info['profitRate']
        except Exception:
            profitrate = 'Get profitRate Error'
    else:
        sRes['resultCode'] = '-1'
        sRes['messages'] = res['message']

    sRes['profitrate'] = profitrate

    return JsonResponse(sRes)


def update_aliexpress_online_price_parity(productid, person, priceParity_Status=None):
    try:
        joom_info = t_aliexpress_online_info.objects.get(ProductID=productid)
        if priceParity_Status:
            joom_info.priceParity_Status = priceParity_Status
        joom_info.priceParity_Person = person
        joom_info.save()
    except Exception as e:
        print 'update_aliexpress_online_price_parity error %s' % e


def udpate_aliexpress_price_parity_log(productid, ShopSKU, newprice, oldprice, person, option):
    res = {'code': 0, 'message': ''}
    if option == 'insert':
        try:
            pplog = t_aliexpress_price_parity_log(
                ProductID=productid,
                ShopSKU=ShopSKU,
                OldPrice=oldprice,
                NewPrice=newprice,
                ChangePriceDatetime=datetime.datetime.now(),
                priceParity_Person=person,
                ChangeFlag='False',
            )
            pplog.save()
        except Exception as e:
            res['code'] = -1
            res['message'] = str(e)
    elif option == 'update':
        try:
            pplog = t_aliexpress_price_parity_log.objects.get(ProductID=productid, ShopSKU=ShopSKU, ChangeFlag='False')
            pplog.OldPrice = oldprice
            pplog.NewPrice = newprice
            pplog.priceParity_Person = person
            pplog.ChangePriceDatetime = datetime.datetime.now()
            pplog.save()
        except Exception as e:
            res['code'] = -1
            res['message'] = str(e)
    else:
        res['code'] = -1
        res['message'] = 'Please choice an option'
    return res


# 获取/更新对手信息
def get_aliexpress_competitor_product_info(request):
    product_id = request.GET.get('product_id', '')
    competitor_product_id = t_aliexpress_online_info.objects.get(ProductID=product_id).competitor_ProductID
    sRes = {'resultCode': '0', 'messages': u''}
    if competitor_product_id:
        sRes = get_aliexpress_competitor_product_by_request(competitor_product_id, product_id)
    else:
        sRes['resultCode'] = '-1'
        sRes['messages'] = 'Please input competitor product id'
    return JsonResponse(sRes)


def get_aliexpress_competitor_product_by_request(competitor_product_id, product_id):
    main_image, title, unit, price, orders, ratingvalue = get_product_info(competitor_product_id)
    sRes = {'resultCode': '0', 'messages': 'SUCCESS'}
    price_range = price.split('-')
    if len(price_range) == 1:
        price_range.append(price)
    # profitrate_range = get_aliexpress_competitor_profit_range(product_id, price_range)
    try:
        competitor_product = t_aliexpress_competitor_product_info.objects.get(ProductID=competitor_product_id)
        if main_image:
            competitor_product.Image = main_image
        if title:
            competitor_product.Title = title
        # if unit:
        #     competitor_product.Unit = unit
        # if orders:
        #     competitor_product.Orders = int(orders)
        # if price_range[0]:
        #     competitor_product.minPrice = price_range[0]
        # if price_range[-1]:
        #     competitor_product.maxPrice = price_range[-1]
        # if profitrate_range[0]:
        #     competitor_product.minProfitRate = profitrate_range[0]
        # if profitrate_range[-1]:
        #     competitor_product.maxProfitRate = profitrate_range[-1]
        if ratingvalue:
            competitor_product.ratingValue = ratingvalue
        competitor_product.LastRefreshDate = competitor_product.RefreshDate
        competitor_product.RefreshDate = datetime.datetime.now()
        competitor_product.RefreshStatus = "Refresh Over"
        competitor_product.save()
    except t_aliexpress_competitor_product_info.DoesNotExist:
        competitor_product = t_aliexpress_competitor_product_info(
            ProductID=competitor_product_id,
            Image=main_image,
            Title=title,
            # Unit=unit,
            # Orders=int(orders),
            # minPrice=price_range[0],
            # maxPrice=price_range[-1],
            # minProfitRate=profitrate_range[0],
            # maxProfitRate=profitrate_range[-1],
            ratingValue=ratingvalue,
            RefreshStatus="Refresh Over",
            RefreshDate=datetime.datetime.now()
        )
        competitor_product.save()
    sRes['resultCode'] = '0'
    sRes['messages'] = 'SUCCESS'

    return sRes


def get_aliexpress_competitor_profit_range(product_id, price_range):
    pro_info = t_aliexpress_online_info_detail.objects.filter(ProductID=product_id).values('SKU', 'Price')
    pro_dict = dict()
    pro_dict = {'max': {'SKU': '', 'price': ''}, 'min': {'SKU': '', 'price': ''}}
    max_price = None
    min_price = None

    for i in pro_info:
        if not i['SKU']:
            continue

        price_now = float(i['Price'])

        if not max_price:
            max_price = price_now
            pro_dict['max'] = {'SKU': i['SKU'], 'price': max_price}
        elif max_price < price_now:
            max_price = price_now
            pro_dict['max'] = {'SKU': i['SKU'], 'price': max_price}

        if not min_price:
            min_price = min_price
            pro_dict['min'] = {'SKU': i['SKU'], 'price': min_price}
        elif min_price > price_now:
            max_price = price_now
            pro_dict['min'] = {'SKU': i['SKU'], 'price': max_price}

    if price_range[0]:
        try:
            min_profit_obj = calculate_price(pro_dict['min']['SKU'])
            min_profit_rate = min_profit_obj.calculate_profitRate(price_range[0], platformCountryCode='ALIEXPRESS-RUS', DestinationCountryCode='RUS')
            min_profit_rate = '%.2f' % float(min_profit_rate['profitRate'])
        except:
            min_profit_rate = ''
    else:
        min_profit_rate = ''
    if price_range[-1]:
        try:
            max_profit_obj = calculate_price(pro_dict['max']['SKU'])
            max_profit_rate = max_profit_obj.calculate_profitRate(price_range[-1], platformCountryCode='ALIEXPRESS-RUS', DestinationCountryCode='RUS')
            max_profit_rate = '%.2f' % float(max_profit_rate['profitRate'])
        except:
            max_profit_rate = ''
    else:
        max_profit_rate = ''

    profitrate_range = [min_profit_rate, max_profit_rate]

    return profitrate_range


def get_aliexpress_product_ratingvalue_by_request(product_id):
    main_image, title, unit, price, orders, ratingValue = get_product_info(product_id)
    sRes = {'resultCode': '0', 'messages': 'SUCCESS'}
    if ratingValue:
        ratingValue = int(float(ratingValue) * 10 * 10)
    else:
        ratingValue = None
    try:
        joom_opt = t_aliexpress_online_info.objects.get(ProductID=product_id)
        joom_opt.ratingValue = ratingValue
        joom_opt.save()
        sRes['messages'] = 'SUCCESS'
    except Exception as e:
        sRes['resultCode'] = '-1'
        sRes['messages'] = e
    return (sRes)


@csrf_exempt
def aliexpress_realprice_update(request):
    productid = request.POST.get('productid', '')
    ShopSKU = request.POST.get('ShopSKU', '')
    realprice = request.POST.get('realprice', '')
    SKU = request.POST.get('SKU', '')

    sRes = {'resultCode': '0', 'messages': ''}
    try:
        if realprice != '':
            rp = float(realprice)
            print rp
    except Exception as e:
        sRes['resultCode'] = '-1'
        sRes['messages'] = '%s is illegal price' % realprice
        return JsonResponse(sRes)

    try:
        ali_detail_obj = t_aliexpress_online_info_detail.objects.get(ProductID=productid, ShopSKU=ShopSKU)
        ali_detail_obj.RealPrice = realprice
        ali_detail_obj.save()
    except Exception as e:
        sRes['resultCode'] = '-1'
        sRes['messages'] = str(e)
        return JsonResponse(sRes)

    profitrate = ''
    try:
        calculate_price_obj = calculate_price(str(SKU))
        sellprice = float(realprice)
        profitrate_info = calculate_price_obj.calculate_profitRate(sellprice, platformCountryCode='ALIEXPRESS-RUS', DestinationCountryCode='RUS')
        if profitrate_info:
            profitrate = profitrate_info['profitRate']
    except:
        profitrate = ''

    sRes['profitrate'] = profitrate
    return JsonResponse(sRes)


@csrf_exempt
def aliexpress_competitor_update(request):
    competitor_productid = request.POST.get('competitor_productid', '')
    product_id = request.POST.get('productid', '')
    minprice = request.POST.get('minprice', '')
    maxprice = request.POST.get('maxprice', '')
    sevenorders = request.POST.get('sevenorders', '')

    sRes = {'resultCode': '0', 'messages': ''}

    sku_range = get_aliexpress_price_range_of_sku(product_id)

    profitrate = ''
    try:
        ali_competitor_obj = t_aliexpress_competitor_product_info.objects.get(ProductID=competitor_productid)
        if minprice:
            ali_competitor_obj.minPrice = minprice
            profitrate = get_profit_by_sku(sku_range['min']['SKU'], float(minprice))
            ali_competitor_obj.minProfitRate = profitrate
        if maxprice:
            ali_competitor_obj.maxPrice = maxprice
            profitrate = get_profit_by_sku(sku_range['max']['SKU'], float(maxprice))
            ali_competitor_obj.maxProfitRate = profitrate
        if sevenorders:
            ali_competitor_obj.Orders7Days = sevenorders
        ali_competitor_obj.save()
    except Exception as e:
        sRes['resultCode'] = '-1'
        sRes['messages'] = str(e)
        return JsonResponse(sRes)

    sRes['profitrate'] = profitrate
    return JsonResponse(sRes)


def get_profit_by_sku(sku, sellprice):
    profitrate = ''
    try:
        calculate_price_obj = calculate_price(str(sku))
        profitrate_info = calculate_price_obj.calculate_profitRate(sellprice, platformCountryCode='ALIEXPRESS-RUS', DestinationCountryCode='RUS')
        if profitrate_info:
            profitrate = profitrate_info['profitRate']
    except:
        pass
    return profitrate


def get_aliexpress_price_range_of_sku(product_id):
    pro_info = t_aliexpress_online_info_detail.objects.filter(ProductID=product_id).values('SKU', 'Price', 'RealPrice')
    pro_dict = dict()
    pro_dict = {'max': {'SKU': '', 'price': ''}, 'min': {'SKU': '', 'price': ''}}
    max_price = None
    min_price = None

    for i in pro_info:
        if not i['SKU']:
            continue

        price_now = 0
        if i['Price']:
            price_now = float(i['Price'])
        elif i['RealPrice']:
            price_now = float(i['RealPrice'])

        if not max_price:
            max_price = price_now
            pro_dict['max'] = {'SKU': i['SKU'], 'price': max_price}
        elif max_price < price_now:
            max_price = price_now
            pro_dict['max'] = {'SKU': i['SKU'], 'price': max_price}

        if not min_price:
            min_price = min_price
            pro_dict['min'] = {'SKU': i['SKU'], 'price': min_price}
        elif min_price > price_now:
            max_price = price_now
            pro_dict['min'] = {'SKU': i['SKU'], 'price': max_price}

    return pro_dict

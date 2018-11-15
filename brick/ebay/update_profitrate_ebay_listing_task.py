# -*- coding: utf-8 -*-
from brick.pricelist.calculate_price import calculate_price
from ebayapp.table.t_online_info_ebay_listing import t_online_info_ebay_listing
from skuapp.table.t_online_info_ebay_subsku import t_online_info_ebay_subsku
from pyapp.models import b_goods

ZSHWCL = ['Ottendorf-Okrilla', 'Rowland Heights,CA/Dayton,NJ', 'Rowland Heights, California', 'Dayton, New Jersey','Dandenong', 'Walsall', 'Leicestershire']
SITE_COUNTRY_CODE = {'0':'US','2':'CA','3':'UK','15':'AUS','71':'FRA','77':'GER','100':'US','101':'FRA','186':'FRA'}


def get_calculate_profitrate(pSKU, currentprice, COUNTRY_CODE, Country, Location, currency):
    profitrate = ''
    try:
        calculate_price_obj = calculate_price(str(pSKU))
        if Country and Country != u'CN' and Location not in ZSHWCL:
            t_cfg_platform_country = u'EBAYXNHWC'
        elif Country and Country != u'CN' and Location in ZSHWCL:
            t_cfg_platform_country = u'EBAYZSHWC'
        else:
            b_goods_objs = b_goods.objects.filter(SKU=str(pSKU)).values('AttributeName')
            if len(b_goods_objs) > 0:
                AttributeName = b_goods_objs[0]['AttributeName']
                if AttributeName:
                    if u'特货' in AttributeName:
                        t_cfg_platform_country = u'EBAYGNZFTH'
                    else:
                        t_cfg_platform_country = u'EBAYGNZF'
                else:
                    t_cfg_platform_country = u'EBAYGNZF'
            else:
                t_cfg_platform_country = u'EBAYGNZF'
        profitrate_info = calculate_price_obj.calculate_profitRate(sellingPrice=currentprice,
                                                                   platformCountryCode=t_cfg_platform_country,
                                                                   DestinationCountryCode=COUNTRY_CODE,
                                                                   price_des=currentprice,
                                                                   currencycode=currency)
        profitrate = profitrate_info['profitRate']
    except:
        profitrate = ''
    return profitrate

"""全量更新"""
def update_profitrate_ebay_listing_task():
    print 'ssssssssssssssssssss'
    try:
        t_online_info_ebay_listing_objs = t_online_info_ebay_listing.objects.exclude(itemid='')
        isNOs = [t_online_info_ebay_listing_obj for t_online_info_ebay_listing_obj in t_online_info_ebay_listing_objs if t_online_info_ebay_listing_obj.isVariations == 'NO']
        a = 0
        b = len(isNOs)
        for isNO in isNOs:
            a += 1
            print 'isNO --- ' , a,'--',b
            try:
                pSKU = isNO.Productsku
                profitrate = get_calculate_profitrate(pSKU=pSKU,
                                                           currentprice=isNO.currentprice,
                                                           COUNTRY_CODE=SITE_COUNTRY_CODE[isNO.site],
                                                           Country=isNO.Country,
                                                           Location=isNO.Location,
                                                           currency=isNO.currency)
                t_online_info_ebay_listing.objects.filter(id=isNO.id).update(profitrate=profitrate)
            except Exception,ex:
                print 'isNO except',str(repr(ex))
                continue

        isYESs = [t_online_info_ebay_listing_obj for t_online_info_ebay_listing_obj in t_online_info_ebay_listing_objs if t_online_info_ebay_listing_obj.isVariations == 'YES']
        c = 0
        d = len(isYESs)
        for isYes in isYESs:
            c += 1
            print 'isYes --- ', c, '--', d
            try:
                t_online_info_ebay_subsku_objs = t_online_info_ebay_subsku.objects.filter(itemid=isYes.itemid)
                for t_online_info_ebay_subsku_obj in t_online_info_ebay_subsku_objs:
                    try:
                        pSKU = t_online_info_ebay_subsku_obj.productsku
                        profitrate = get_calculate_profitrate(pSKU=pSKU,
                                                              currentprice=t_online_info_ebay_subsku_obj.startprice,
                                                              COUNTRY_CODE=SITE_COUNTRY_CODE[isYes.site],
                                                              Country=isYes.Country,
                                                              Location=isYes.Location,
                                                              currency=isYes.currency)
                        t_online_info_ebay_subsku.objects.filter(id=t_online_info_ebay_subsku_obj.id).update(profitrate=profitrate)
                    except Exception,ex:
                        print 'subsku except',str(repr(ex))
            except Exception,ex:
                print 'isYes except',str(repr(ex))

    except Exception,ex:
        print str(repr(ex))

"""更新新增"""
def update_profitrate_ebay_listing_task2():
    print 'ssssssssssssssssssss'
    try:
        t_online_info_ebay_listing_objs = t_online_info_ebay_listing.objects.exclude(itemid='').filter(profitrate__in = [None,''])
        isNOs = [t_online_info_ebay_listing_obj for t_online_info_ebay_listing_obj in t_online_info_ebay_listing_objs if t_online_info_ebay_listing_obj.isVariations == 'NO']
        a = 0
        b = len(isNOs)
        for isNO in isNOs:
            a += 1
            print 'isNO --- ', a, '--', b
            try:
                pSKU = isNO.Productsku
                profitrate = get_calculate_profitrate(pSKU=pSKU,
                                                      currentprice=isNO.currentprice,
                                                      COUNTRY_CODE=SITE_COUNTRY_CODE[isNO.site],
                                                      Country=isNO.Country,
                                                      Location=isNO.Location,
                                                      currency=isNO.currency)
                t_online_info_ebay_listing.objects.filter(id=isNO.id).update(profitrate=profitrate)
            except Exception, ex:
                print 'isNO except', str(repr(ex))
                continue

        isYESs = [t_online_info_ebay_listing_obj for t_online_info_ebay_listing_obj in t_online_info_ebay_listing_objs if t_online_info_ebay_listing_obj.isVariations == 'YES']
        c = 0
        d = len(isYESs)
        for isYes in isYESs:
            c += 1
            print 'isYes --- ', c, '--', d
            try:
                t_online_info_ebay_subsku_objs = t_online_info_ebay_subsku.objects.filter(itemid=isYes.itemid,profitrate__in = [None,''])
                if len(t_online_info_ebay_subsku_objs) < 1:
                    continue
                for t_online_info_ebay_subsku_obj in t_online_info_ebay_subsku_objs:
                    try:
                        pSKU = t_online_info_ebay_subsku_obj.productsku
                        profitrate = get_calculate_profitrate(pSKU=pSKU,
                                                              currentprice=t_online_info_ebay_subsku_obj.startprice,
                                                              COUNTRY_CODE=SITE_COUNTRY_CODE[isYes.site],
                                                              Country=isYes.Country,
                                                              Location=isYes.Location,
                                                              currency=isYes.currency)
                        t_online_info_ebay_subsku.objects.filter(id=t_online_info_ebay_subsku_obj.id).update(profitrate=profitrate)
                    except Exception, ex:
                        print 'subsku except', str(repr(ex))
            except Exception, ex:
                print 'isYes except', str(repr(ex))

    except Exception,ex:
        print str(repr(ex))


# if __name__ == '__main__':
#     print 'sssssssssssssssss==========='
#     update_profitrate_ebay_listing_task()


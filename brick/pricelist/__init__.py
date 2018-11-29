# -*- coding:utf-8 -*-
from skuapp.table.t_cfg_b_currencycode import t_cfg_b_currencycode
cfg_b_currencycode={}
cfg_b_currencycode['ExchangeRate_USD'] = float(t_cfg_b_currencycode.objects.get(CURRENCYCODE='USD').ExchangeRate)
t_cfg_b_currencycode_objs = t_cfg_b_currencycode.objects.all()
for t_cfg_b_currencycode_obj in t_cfg_b_currencycode_objs:
    cfg_b_currencycode[t_cfg_b_currencycode_obj.CURRENCYCODE] = t_cfg_b_currencycode_obj.ExchangeRate

from skuapp.table.t_cfg_b_emsfare2 import t_cfg_b_emsfare2
cfg_b_emsfare2 = {}
t_cfg_b_emsfare2_objs = t_cfg_b_emsfare2.objects.all()
for t_cfg_b_emsfare2_obj in t_cfg_b_emsfare2_objs:
    cfg_b_emsfare2[t_cfg_b_emsfare2_obj.platform_country_code + '_' + t_cfg_b_emsfare2_obj.countrycode + '_logisticway'] = t_cfg_b_emsfare2_obj.logisticwaycode
    cfg_b_emsfare2[t_cfg_b_emsfare2_obj.platform_country_code + '_' + t_cfg_b_emsfare2_obj.countrycode + '_kickback'] = t_cfg_b_emsfare2_obj.kickback
    cfg_b_emsfare2[t_cfg_b_emsfare2_obj.platform_country_code + '_' + t_cfg_b_emsfare2_obj.countrycode + '_category_id'] = t_cfg_b_emsfare2_obj.category_id
    cfg_b_emsfare2[t_cfg_b_emsfare2_obj.platform_country_code + '_' + t_cfg_b_emsfare2_obj.countrycode + '_extra_id'] = t_cfg_b_emsfare2_obj.extra_id
    cfg_b_emsfare2[t_cfg_b_emsfare2_obj.platform_country_code + '_' + t_cfg_b_emsfare2_obj.countrycode + '_logisticway_desc'] = t_cfg_b_emsfare2_obj.logisticwaycode_desc
    cfg_b_emsfare2[t_cfg_b_emsfare2_obj.platform_country_code + '_' + t_cfg_b_emsfare2_obj.countrycode + '_standard_id'] = t_cfg_b_emsfare2_obj.standard_id
    cfg_b_emsfare2[t_cfg_b_emsfare2_obj.platform_country_code + '_' + t_cfg_b_emsfare2_obj.countrycode + '_price_point'] = t_cfg_b_emsfare2_obj.price_point
from skuapp.table.t_cfg_category import t_cfg_category
cfg_category = {}
t_cfg_category_objs = t_cfg_category.objects.all()
for t_cfg_category_obj in t_cfg_category_objs:
    cfg_category[str(t_cfg_category_obj.category_id) + '_' + t_cfg_category_obj.category_code] = t_cfg_category_obj.logisticwaycode
    cfg_category[str(t_cfg_category_obj.category_id) + '_' + t_cfg_category_obj.category_code+'_desc'] = t_cfg_category_obj.logisticwaycode_desc

from skuapp.table.t_cfg_platform_country import t_cfg_platform_country
cfg_platform_country = {}
t_cfg_platform_country_objs = t_cfg_platform_country.objects.all()
for t_cfg_platform_country_obj in t_cfg_platform_country_objs:
    cfg_platform_country[t_cfg_platform_country_obj.platform_country_code] = t_cfg_platform_country_obj.basefee

from skuapp.table.t_cfg_b_country import t_cfg_b_country
cfg_b_country={}
t_cfg_b_country_objs = t_cfg_b_country.objects.all()
for t_cfg_b_country_obj in t_cfg_b_country_objs:
    cfg_b_country[t_cfg_b_country_obj.country_code] = t_cfg_b_country_obj.CURRENCYCODE

from skuapp.table.t_cfg_b_logisticway import t_cfg_b_logisticway
cfg_b_logisticway={}
t_cfg_b_logisticway_objs = t_cfg_b_logisticway.objects.all()
for t_cfg_b_logisticway_obj in t_cfg_b_logisticway_objs:
    cfg_b_logisticway[t_cfg_b_logisticway_obj.code + '_name'] = t_cfg_b_logisticway_obj.name
    cfg_b_logisticway[t_cfg_b_logisticway_obj.code + '_Discount'] = t_cfg_b_logisticway_obj.Discount

from skuapp.table.t_cfg_b_emsfare_country2 import t_cfg_b_emsfare_country2
cfg_b_emsfare_country2 = {}
t_cfg_b_emsfare_country2_objs = t_cfg_b_emsfare_country2.objects.all()
for t_cfg_b_emsfare_country2_obj in t_cfg_b_emsfare_country2_objs:
    cfg_b_emsfare_country2[t_cfg_b_emsfare_country2_obj.country_code+'_'+t_cfg_b_emsfare_country2_obj.logisticwaycode+'_getprice'] = t_cfg_b_emsfare_country2_obj.getprice
    cfg_b_emsfare_country2[t_cfg_b_emsfare_country2_obj.country_code+'_'+t_cfg_b_emsfare_country2_obj.logisticwaycode+'_getprice_desc'] = t_cfg_b_emsfare_country2_obj.getprice_desc
    cfg_b_emsfare_country2[t_cfg_b_emsfare_country2_obj.country_code+'_'+t_cfg_b_emsfare_country2_obj.logisticwaycode+'_bracketid'] = t_cfg_b_emsfare_country2_obj.Bracketid
    
from skuapp.table.t_cfg_extra_fee import t_cfg_extra_fee
cfg_extra_fee = {}
t_cfg_extra_fee_objs = t_cfg_extra_fee.objects.all()
for t_cfg_extra_fee_obj in t_cfg_extra_fee_objs:
    cfg_extra_fee[str(t_cfg_extra_fee_obj.id)+'_get_fba_price'] = t_cfg_extra_fee_obj.get_fba_price
    cfg_extra_fee[str(t_cfg_extra_fee_obj.id)+'_get_js_price'] = t_cfg_extra_fee_obj.get_js_price
    cfg_extra_fee[str(t_cfg_extra_fee_obj.id)+'_get_qg_price'] = t_cfg_extra_fee_obj.get_qg_price
    cfg_extra_fee[str(t_cfg_extra_fee_obj.id)+'_sb_discount'] = t_cfg_extra_fee_obj.sb_discount
    cfg_extra_fee[str(t_cfg_extra_fee_obj.id)+'_bcd_rate'] = t_cfg_extra_fee_obj.bcd_rate
    cfg_extra_fee[str(t_cfg_extra_fee_obj.id)+'_yj_rate'] = t_cfg_extra_fee_obj.yj_rate
    cfg_extra_fee[str(t_cfg_extra_fee_obj.id)+'_xss_rate'] = t_cfg_extra_fee_obj.xss_rate
    cfg_extra_fee[str(t_cfg_extra_fee_obj.id)+'_CURRENCYCODE'] = t_cfg_extra_fee_obj.CURRENCYCODE

from skuapp.table.t_cfg_standard_large_small import t_cfg_standard_large_small
cfg_standard_large_small = {}
t_cfg_standard_large_small_objs = t_cfg_standard_large_small.objects.all()
for t_cfg_standard_large_small_obj in t_cfg_standard_large_small_objs:
    cfg_standard_large_small[str(t_cfg_standard_large_small_obj.standard_id)+str(t_cfg_standard_large_small_obj.standard_large_code)+str(t_cfg_standard_large_small_obj.standard_small_code)+'_CURRENCYCODE'] = t_cfg_standard_large_small_obj.CURRENCYCODE
    cfg_standard_large_small[str(t_cfg_standard_large_small_obj.standard_id)+str(t_cfg_standard_large_small_obj.standard_large_code)+str(t_cfg_standard_large_small_obj.standard_small_code)+'_getprice'] = t_cfg_standard_large_small_obj.getprice
    cfg_standard_large_small[str(t_cfg_standard_large_small_obj.standard_id)+str(t_cfg_standard_large_small_obj.standard_large_code)+str(t_cfg_standard_large_small_obj.standard_small_code)+'_getprice_desc'] = t_cfg_standard_large_small_obj.getprice_desc


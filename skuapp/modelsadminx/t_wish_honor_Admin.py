# -*- coding: utf-8 -*-
from .t_product_Admin import *
from skuapp.table.t_store_configuration_file import *
class t_wish_honor_Admin(object):

    list_display  =('id','ShopNameOfficial','seller','ShopHonor','ImitationRate','EffectiveTrackingRate','DelayedDeliveryRate',
                    'DayAverageScore','RefundRateWithin63To93','updateTime',)
    list_filter   =('id','ShopNameOfficial','seller','ShopHonor','ImitationRate','EffectiveTrackingRate','DelayedDeliveryRate',
                    'DayAverageScore','RefundRateWithin63To93','updateTime',)
    search_fields =('id','ShopNameOfficial','seller','ShopHonor','ImitationRate','EffectiveTrackingRate','DelayedDeliveryRate',
                    'DayAverageScore','RefundRateWithin63To93',)
 
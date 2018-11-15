#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from aliexpress_app.views import aliexpress_price_parity
from aliexpress_app.views import get_aliexpress_competitor_product_info
from aliexpress_app.views import aliexpress_realprice_update
from aliexpress_app.views import aliexpress_competitor_update

urlpatterns = [
    url(r'^get_aliexpress_competitor_product_info/', get_aliexpress_competitor_product_info, name='get_aliexpress_competitor_product_info'),
    url(r'^aliexpress_price_parity/', aliexpress_price_parity, name='aliexpress_price_parity'),
    url(r'^aliexpress_realprice_update/', aliexpress_realprice_update, name='aliexpress_realprice_update'),
    url(r'^aliexpress_competitor_update/', aliexpress_competitor_update, name='aliexpress_competitor_update'),
]

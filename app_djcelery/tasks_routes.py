# coding=utf-8

"""
在这里填写实时任务、定时任务队列路由
real_time：实时任务
timing：定时任务
填写格式如下：
    实时任务格式：'app_djcelery.tasks.timing_multitasking': {'queue': 'real_time', 'routing_key': 'real_time'},
    定时任务格式：'app_djcelery.tasks.only_add': {'queue': 'real_time', 'routing_key': 'real_time'},
"""

# 非批量任务、短时间任务
REAL_TIME_TASKS = {
    'app_djcelery.tasks.timing_multitasking': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.only_add': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.download_trackInfo_pdf': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.download_price_pdf': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.joom_export_excel': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.joom_info_from_wish': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.ebay_open': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.wish_product_infomation': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.import_excel_file': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.generate_delivery_invoices': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.product_registration_form_excel_task': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.get_shopsku_sku_excel': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.get_shopsku_sku_forthwith_excel': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.wish_product_off_shelf_task': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.syn_Logistics_number': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.get_trackno_amazon_india': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.CexportRefundCSVTask': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.ebay_distribution': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.syn_py_info_cg': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.order_out_of_stock_task': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.amazon_product_refresh': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.order_out_of_stock_statistics_task': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.stitch_goods_info': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.update_joom_goods_category_task': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.amazon_reverse_collection': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.wish_advertisement_statistics_task': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.Joom_Recover_Monitor_Task': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.Joom_Get_All_Shop_Products': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.t_report_sales_daily_task': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.wish_change_shipping_to_country': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.will_change_shipping': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.joom_price_parity_by_mq': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.syndata_by_joom_api_shopname': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.syndata_by_joom_api': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.joom_update_products_sevenordernum': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.upload_kc_data_task': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.aliexpress_submitter_link_count': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.aliexpress_import_products_task': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.mymall_import_products_task': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.batch_change_mymall_data_by_task': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.wish_listing_refund_statistics_task': {'queue': 'real_time', 'routing_key': 'real_time'},
    'app_djcelery.tasks.process_rating': {'queue': 'real_time', 'routing_key': 'real_time'},
}


# 批量任务、长时间任务
TIMING_TASKS = {
    'app_djcelery.tasks.hello': {'queue': 'timing', 'routing_key': 'timing'},
    'app_djcelery.tasks.print_hello': {'queue': 'timing', 'routing_key': 'timing'},
    'app_djcelery.tasks.syn_py_info_b': {'queue': 'timing', 'routing_key': 'timing'},
    'app_djcelery.tasks.syn_py_info_cg': {'queue': 'timing', 'routing_key': 'timing'},
    'app_djcelery.tasks.syn_py_info_p': {'queue': 'timing', 'routing_key': 'timing'},
    'app_djcelery.tasks.syn_py_info_kc': {'queue': 'timing', 'routing_key': 'timing'},
    'brick.wish.Haiying_Data.get_data_from_haiying_task.get_data_from_haiying_task': {'queue': 'timing', 'routing_key': 'timing'},
    'brick.wish.Haiying_Data.get_data_from_haiying_task.get_data_from_haiying_viewdata': {'queue': 'timing', 'routing_key': 'timing'},
    'app_djcelery.tasks.wish_distribution_statistics_task': {'queue': 'timing', 'routing_key': 'timing'},
    'app_djcelery.tasks.wish_order_syn_task': {'queue': 'timing', 'routing_key': 'timing'},
    'app_djcelery.tasks.Amazon_india_auto_feed_trackNo': {'queue': 'timing', 'routing_key': 'timing'},
    'app_djcelery.tasks.wish_generate_image_task': {'queue': 'timing', 'routing_key': 'timing'},
    'app_djcelery.tasks.update_wishpbdata_task': {'queue': 'timing', 'routing_key': 'timing'},
    'app_djcelery.tasks.update_ebayapp_price': {'queue': 'timing', 'routing_key': 'timing'},
    'app_djcelery.tasks.update_profitrate_ebay_task': {'queue': 'timing', 'routing_key': 'timing'},
    'app_djcelery.tasks.py_Syn_walmart_main_task': {'queue': 'timing', 'routing_key': 'timing'},
}

# 实时更新采购员数据任务
KC_CURRENTSTOCK_TASKS = {
    'app_djcelery.tasks.exec_purchaser': {'queue': 'kc_purchaser', 'routing_key': 'kc_purchaser'},
    'app_djcelery.tasks.create_report_supplier_t': {'queue': 'kc_purchaser', 'routing_key': 'kc_purchaser'},
}

# WISH商品下架任务
OFF_SHELF_TASKS = {
    'app_djcelery.tasks.wish_product_off_shelf': {'queue': 'off_shelf', 'routing_key': 'off_shelf'},
}


# WISH商品上架任务
ON_SHELF_TASKS = {
    'app_djcelery.tasks.wish_product_on_shelf': {'queue': 'on_shelf', 'routing_key': 'on_shelf'},
}

# wish店铺任务
WISH_SHOPINFO_TASKS = {
    'app_djcelery.tasks.show_wish_honor': {'queue': 'wish_shopinfo', 'routing_key': 'wish_shopinfo'},
    'app_djcelery.tasks.show_wish_pb': {'queue': 'wish_shopinfo', 'routing_key': 'wish_shopinfo'},
    'app_djcelery.tasks.show_wish_screenshot': {'queue': 'wish_shopinfo', 'routing_key': 'wish_shopinfo'},
}

# wish店铺管理
WISH_SHOP_MANAGE = {
    'app_djcelery.tasks.syndata_by_wish_api': {'queue': 'wish_shop_manage', 'routing_key': 'wish_shop_manage'},
    'app_djcelery.tasks.update_goods_information_by_wish_api': {'queue': 'wish_shop_manage', 'routing_key': 'wish_shop_manage'},
    'app_djcelery.tasks.wish_to_publish': {'queue': 'wish_shop_manage', 'routing_key': 'wish_shop_manage'},
}

WISH_REFRESH = {
    'brick.wish.ShopOnlineInfo.F_EXE_SHOP_ONLINE_INFO': {'queue': 'wish_refresh', 'routing_key': 'wish_refresh'},
    'app_djcelery.tasks.syndata_by_wish_api_shopname': {'queue': 'wish_refresh', 'routing_key': 'wish_refresh'},
}

# Joom店铺管理
# JOOM_SHOP_MANAGE = {
#     'app_djcelery.tasks.syndata_by_joom_api_shopname': {'queue': 'joom_shop_manage', 'routing_key': 'joom_shop_manage'},
#     'app_djcelery.tasks.syndata_by_joom_api': {'queue': 'joom_shop_manage', 'routing_key': 'joom_shop_manage'},
# }

# WISH商品下架紧急任务
OFF_SHELF_URGENT_TASKS = {
    'app_djcelery.tasks.product_and_bottom_shelf_func': {'queue': 'off_shelf_urgent', 'routing_key': 'off_shelf_urgent'},
    'app_djcelery.tasks.wish_product_off_shelf_urgent': {'queue': 'off_shelf_urgent', 'routing_key': 'off_shelf_urgent'},
}

# 批量同步商品状态、库存入redis
BATCH_GOODS_STATE_TASKS = {
    'app_djcelery.tasks.Batch_LoadAndImportData_task': {'queue': 'goodsbatchstate_redis', 'routing_key': 'goodsbatchstate_redis'},
}

# 爬虫WEB商品信息
WEB_CRAWLER_TASKS = {
    'app_djcelery.tasks.joom_competitor_update_by_webdriver': {'queue': 'web_crawler', 'routing_key': 'web_crawler'},
    'app_djcelery.tasks.joom_get_our_ratingvalue_by_webdriver': {'queue': 'web_crawler', 'routing_key': 'web_crawler'},
    'app_djcelery.tasks.get_aliexpress_competitor_product_by_request_task': {'queue': 'web_crawler', 'routing_key': 'web_crawler'},
    'app_djcelery.tasks.get_aliexpress_product_ratingvalue_by_request_task': {'queue': 'web_crawler', 'routing_key': 'web_crawler'},
}

#AliExpress店铺管理
ALI_SHOP_MANAGE = {
    'app_djcelery.tasks.refresh_online_info_by_ali_api': {'queue': 'ali_shop_manage', 'routing_key': 'ali_shop_manage'},
    'app_djcelery.tasks.enable_products_by_ali_api': {'queue': 'ali_shop_manage', 'routing_key': 'ali_shop_manage'},
    'app_djcelery.tasks.disable_products_by_ali_api': {'queue': 'ali_shop_manage', 'routing_key': 'ali_shop_manage'},
    'app_djcelery.tasks.syn_products_by_ali_api': {'queue': 'ali_shop_manage', 'routing_key': 'ali_shop_manage'},
    'app_djcelery.tasks.edit_productSKU_stock_by_ali_api': {'queue': 'ali_shop_manage', 'routing_key': 'ali_shop_manage'},
    'app_djcelery.tasks.edit_productSKU_price_by_ali_api': {'queue': 'ali_shop_manage', 'routing_key': 'ali_shop_manage'},
    'app_djcelery.tasks.edit_product_by_ali_api': {'queue': 'ali_shop_manage', 'routing_key': 'ali_shop_manage'},
    'app_djcelery.tasks.upload_product_by_ali_api': {'queue': 'ali_shop_manage', 'routing_key': 'ali_shop_manage'},
}

# Amazon 刊登
AMAZON_UPLOAD = {
    'app_djcelery.tasks.stitch_goods_info': {'queue': 'amazon_upload', 'routing_key': 'amazon_upload'},
}

# 修改普源队列
PY_MODIFY_TASKS = {
    'app_djcelery.tasks.online_syn_to_puyuan_task': {'queue': 'py_modify', 'routing_key': 'py_modify'},
    'app_djcelery.tasks.online_modify_puyuan_task': {'queue': 'py_modify', 'routing_key': 'py_modify'},
    'app_djcelery.tasks.online_sku_binding_puyuan_task': {'queue': 'py_modify', 'routing_key': 'py_modify'},
    'app_djcelery.tasks.online_tort_syn_to_puyuan_task': {'queue': 'py_modify', 'routing_key': 'py_modify'},
    'app_djcelery.tasks.online_modify_py_purchaser_task': {'queue': 'py_modify', 'routing_key': 'py_modify'},
    'app_djcelery.tasks.online_modify_py_possessman2_task': {'queue': 'py_modify', 'routing_key': 'py_modify'},
}

# 业销售业绩获取 gen_execl_saler_profit_data
SALER_PROFIT_TASK = {
    'app_djcelery.tasks.get_saler_profit_data': {'queue': 'get_saler_profit_data', 'routing_key': 'get_saler_profit_data'},
    'app_djcelery.tasks.gen_execl_saler_profit_data': {'queue': 'gen_execl_saler_profit_data', 'routing_key': 'gen_execl_saler_profit_data'},
    'app_djcelery.tasks.py_getgongzi_report': {'queue': 'py_getgongzi_report', 'routing_key': 'py_getgongzi_report'},
}

#lazada店铺管理
LZD_SHOP_MANAGE = {
    'app_djcelery.tasks.get_lazada_product': {'queue': 'get_lazada_product', 'routing_key': 'get_lazada_product'},
}

# Shopee店铺管理
SHP_SHOP_MANAGE = {
    'app_djcelery.tasks.syn_shopee_data': {'queue': 'shp_shop_manage', 'routing_key': 'shp_shop_manage'}
}

TASKS_LIST = [
    REAL_TIME_TASKS,
    TIMING_TASKS,
    OFF_SHELF_TASKS,
    WISH_SHOPINFO_TASKS,
    WISH_SHOP_MANAGE,
    ON_SHELF_TASKS,
    OFF_SHELF_URGENT_TASKS,
    # ATCH_GOODS_STATE_TASKS,
    KC_CURRENTSTOCK_TASKS,
    WEB_CRAWLER_TASKS,
    WISH_REFRESH,
    ALI_SHOP_MANAGE,
    AMAZON_UPLOAD,
    SALER_PROFIT_TASK,
    PY_MODIFY_TASKS,
    LZD_SHOP_MANAGE,
    SHP_SHOP_MANAGE,
]

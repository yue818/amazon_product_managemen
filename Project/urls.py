#!/usr/bin/python
# -*- coding: utf-8 -*-
"""hq_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
#from django.contrib import admin

from django.views.static import serve
from skuapp.views import *
from gather_app.views import *
from storeapp.views import *
from pyapp.views import *
from reportapp.views import *
from wishpubapp.views import *
from sqlapp.views import *
from pyapp.views import shopSKU,show_moreInfo,show_Remark,show_transportGoods,syn_b_goods
import xadmin
xadmin.autodiscover()
#admin.autodiscover()
#handler403 = permission_denied
handler404 = page_not_found
handler500 = page_error1
handler502 = page_error2
handler504 = page_error3
from app_djcelery.views import *
from aliapp.views import *
# from django.contrib import admin
xadmin.autodiscover()
from chart_app.views import *
import joom_app.urls
import aliexpress_app.urls
from picapp.views import *
import mymall_app.urls
import ebayapp.urls
import lzd_app.urls
import shopee_app.urls
# import factory_app.urls
from callbackapp.views import *

urlpatterns = [
    url(r'^$',homepage),
    url(r'^admin/upload/(?P<dir_name>[^/]+)$', upload_image, name='upload_image'),
    # url(r'^$', IndexView.as_view(), name='home'),
    url(r'^t_online_info_wish/order1day/', order1day),
    url(r'^t_online_info_ebay/ebay_order1day/', ebay_order1day),
    url(r'^t_online_info_ebay/ebay_SKU/', ebay_SKU),
    url(r'^t_tort_aliexpress/aliexpress_info/', aliexpress_info),
    url(r'^t_config_apiurl_asin/show_rank/', show_rank),
    url(r'^t_product_mainsku_sku/show_price_sj/', wish_calculate),
    url(r'^t_online_info_wish/SKU/', SKU),
    url(r'^show_1688pic/', show_1688pic),
    url(r'^aliexpress_cc/', aliexpress_cc),
    url(r'^aliexpress_exe/', aliexpress_exe),
    url(r'^batch_suanjia',batch_suanjia),
    url(r'^get_tags/',get_tags),
    url(r'^t_online_info_wish_store/ShopSKU/',ShopSKU_edit,name='ShopSKU_edit'),
    url(r'^t_task_details/details/', t_task_details),
    url(r'^task/sub/', task_sub),
    url(r'^t_task_trunk/trunk/', t_task_trunk),
    url(r'^task/trunk', task_trunk),
    url(r'^t_task_trunk/trunk_form/', trunk_form),
    url(r'^t_task_trunk/bhtc/', trunk_bhtc),
    url(r'^t_task_trunk/wtqx/', trunk_wtqx),
    url(r'^t_task_trunk/rwtj/', t_task_trunk_rwtj),
    url(r'^t_product_up_down/delay/', t_product_up_down_delay),
    url(r'^delay/day', delay_day),
    url(r'^aliexpress_refund_info/',aliexpress_refund_info),
    url(r'^storage/',storage),
    url(r'^addseats/',addseats),
    url(r'^joom_refund/',joom_refund),
    url(r'^price_list/',price_list),
    url(r'^price_list2/',price_list2),
    url(r'^price_list3/',price_list3),
    url(r'^price_list4/',price_list4),
    url(r'^price_list_tab/',price_list_tab),
    url(r'^price_list_file/',price_list_file),
    url(r'^price_list_rz/',price_list_rz),
    url(r'^suanjia1/',suanjia1),
    url(r'^suanjia2/',suanjia2),
    url(r'^suanjia_test/',suanjia_test),
    url(r'^category_info/',category_info),
    url(r'^category_info_add/',category_info_add),
    url(r'^Project/admin/skuapp/t_task_trunk/t_task_son/', t_task_son),
    url(r'^t_online_info_wish/PB/', PB),
    url(r'^t_product_mainsku_all/SKUB/', SKUB),
    url(r'^t_stockorderm_track/t_stockorderm_sku/',t_stockorderm_sku),
    url(r'^t_product_b_goods_shopSKU/shopSKU',shopSKU),
    url(r'^t_product_b_goods_show_transportGoods/show_transportGoods',show_transportGoods),
    url(r'^t_product_b_goods_show_Remark/show_Remark',show_Remark),
    url(r'^t_product_b_goods_show_moreInfo/show_moreInfo',show_moreInfo),
    # url(r'^t_product_b_goods_pic/pic',show_pic),
    # url(r'^t_product_modify_review/skulist_xg/',skulist_xg),
    # url(r'^t_product_modify_entry/skulist_mentry_xg/',skulist_mentry_xg),
    url(r'^Project/admin/', include(xadmin.site.urls), name='xadmin'),
    #url(r'^admin/', admin.site.urls, name='hq name'),
    url(r'^xadmin/', include(xadmin.site.urls), name='xadmin'),
    url(r'^addsurvey/$',addsurvey,name ='addsurvey'),
    url(r'^aaa/$',aaa,name ='aaa'),
    url(r'^adddeveloping/$',adddeveloping,name ='adddeveloping'),
    url(r'^addlog/$',addlog,name ='addlog'),
    #url(r'^import_joom/$',import_joom,name ='import_joom'),
    url(r'^saveform/$',saveform,name ='saveform'),
    url(r'^save_up_down/$',save_up_down,name ='save_up_down'),
    url(r'^t_online_info_logisticPlugin/$',t_online_info_logisticPlugin,name ='t_online_info_logisticPlugin'),
    url(r'^prompt_develop/$', prompt_develop, name='prompt_develop'),
    url(r'^t_product_up_downPlugin/$',t_product_up_downPlugin,name ='t_product_up_downPlugin'),
    url(r'^black_list_Plugin/$',black_list_Plugin,name ='black_list_Plugin'),
    url(r'^kc_currentstock_sku_log/saleseveryday/', saleseveryday),
    url(r'^create_cg_stockorderm_refund/$',create_cg_stockorderm_refund,name ='create_cg_stockorderm_refund'),
    url(r'^cg_stockorderm_show_Goods/show_cg_Goods',show_cg_Goods),
    url(r'^cg_stockorderm_show_refund/show_cg_refund',show_cg_refund),
    url(r'^add_cg_abnormal_display/add_cg_abnormal',add_cg_abnormal),
    url(r'^search_cg_sku/$',search_cg_sku,name ='search_cg_sku'),
    url(r'^insert_cg_abnormal/$',insert_cg_abnormal,name ='insert_cg_abnormal'),
    url(r'^handele_abnorma_status/$',handele_abnorma_status,name ='handele_abnorma_status'),
    url(r'^create_report_supplier/$',create_report_supplier,name ='create_report_supplier'),
    url(r'^update_cg_status/$',update_cg_status,name ='update_cg_status'),
    url(r'^shift_to_ignore/$',shift_to_ignore,name ='shift_to_ignore'),
    url(r'^get_cg_data/$',get_cg_data,name ='get_cg_data'),
    url(r'^shift_to_gift/$',shift_to_gift,name ='shift_to_gift'),
    url(r'^get_cg_bufa/$',get_cg_bufa,name ='get_cg_bufa'),
    url(r'^wirte_to_cg_note/$',wirte_to_cg_note,name ='wirte_to_cg_note'),
    url(r'^create_cg_data/$',create_cg_data,name ='create_cg_data'),
    url(r'^get_cg_remark/$',get_cg_remark,name ='get_cg_remark'),
    url(r'^shift_to_archive/$',shift_to_archive,name ='shift_to_archive'),
    url(r'^shift_to_cg/$',shift_to_cg,name ='shift_to_cg'),
    url(r'^search_SupplierName/$',search_SupplierName,name ='search_SupplierName'),
    url(r'^kc_currentstock_Plugin/$',kc_currentstock_Plugin,name ='kc_currentstock_Plugin'),
    #url(r'^check_box_list/$',check_box_list,name ='check_box_list'),
    url(r'^search_Purchaser/$', search_Purchaser,name='search_Purchaser'),
    url(r'^jump_kc_Status/$', jump_kc_Status,name='jump_kc_Status'),
    url(r'^update_purchaserData/$', update_purchaserData,name='update_purchaserData'),
    url(r'^addmainsku_sku/$',addmainsku_sku,name ='addmainsku_sku'),
    url(r'^button_Plugin/$',button_Plugin,name ='button_Plugin'),
    url(r'^search_sku_Plugin/$',search_sku_Plugin,name ='search_sku_Plugin'),
    url(r'^applymainsku/$',applymainsku),
    url(r'^media/(?P<path>.*)/$', serve, {"document_root": '/data/djangostack-1.9.7/apps/django/django_projects/Project/media/'}),
    url(r'^static/(?P<path>.*)/$', serve, {"document_root": '/data/djangostack-1.9.7/apps/django/django_projects/Project/static/'}),
    #url(r'^$', admin.site.urls),
    url(r'^$', include(xadmin.site.urls), name='xadmin'),

    #app gather_app
    url(r'^addgathermain/$',addgathermain,name ='addgathermain'),

    #url(r'^synchronize_t_product_B_Goods/$',synchronize_t_product_B_Goods,name ='synchronize_t_product_B_Goods'),#
    url(r'^mstsc/$',mstsc,name ='mstsc'),
    url(r'^mstsc2',mstsc2),
    url(r'^mstsc3',mstsc3),
    url(r'^mstsc4',mstsc4),
    url(r'^mstscReboot',mstscReboot),
    url(r'^t_product_modify_review/modify_review_Z_KC/',Z_KC),
    url(r'^button_save/$',button_save,name ='button_save'),
    url(r'^search_sku_save/$',search_sku_save,name ='search_sku_save'),
    url(r'^paypal_save/$',paypalSave,name ='paypalSave'),
    url(r'^t_product_depart_get/Secondary_research/$',add_Secondary_research,name ='add_Secondary_research'),
    url(r'^t_config_apiurl_asin_xprx/Remarks/$',add_Remarks,name ='add_Remarks'),
    url(r'^t_product_depart_get/Secondary_research_result/$',add_Secondary_research_result,name ='add_Secondary_research_result'),
    url(r'^t_config_apiurl_asin_xprx/Remarks_result/$',add_Remarks_result,name ='add_Remarks_result'),
    url(r'^wish_change/',wish_change,name='wish_change'),
    url(r'^wish_save/',wish_save,name='wish_save'),
    url(r'^to_wish_store_distribution/',to_wish_store,name='to_wish_store'),
    url(r'^t_goods_shelves/search_Plugin/',shelves_search,name='shelves_search'),
    url(r'^t_distribution_product_to_store/upload_Implementation_plan/',upload_Implementation_plan,name='upload_Implementation_plan'),
    url(r'apply_track/',applyTrack,name ='applyTrack'),
    url(r'feed_track/',feedTrack,name ='feedTrack'),
    url(r'feed_track_comfir/',feedTrackComfir,name ='feedTrackComfir'),
    url(r'apply_track_comfir/',applyTrackComfir,name ='applyTrackComfir'),
    url(r'trackInfo/',trackInfo,name ='trackInfo'),
    url(r'feed_amazon/',feedAmazon,name ='feedAmazon'),
    url(r'^create_wish_collection_box/',create_wish_collection_box,name='create_wish_collection_box'),
    url(r'^show_wish_variant/',show_wish_variant,name='show_wish_variant'),
    url(r'^save_wish_variant/',save_wish_variant,name='save_wish_variant'),
    url(r'^show_wish_schedule/',show_wish_schedule,name='show_wish_schedule'),
    url(r'^save_wish_schedule/',save_wish_schedule,name='save_wish_schedule'),
    url(r'^show_wish_result/',show_wish_result,name='show_wish_result'),
    url(r'^t_product_image_modify/all_image/',all_image_modify,name='all_image_modify'),
    url(r'^t_product_image_modify/all_image_del/',all_image_modify_del,name='all_image_modify_del'),
    url(r'^show_aliexpress_warning/',show_aliexpress_warning,name='show_aliexpress_warning'),
    url(r'^save_aliexpress_warning/',save_aliexpress_warning,name='save_aliexpress_warning'),
    url(r'^save_aliexpress_image/',save_aliexpress_image,name='save_aliexpress_image'),
    url(r'^show_aliexpress_image/',show_aliexpress_image,name='show_aliexpress_image'),
    url(r'^make_shopname/',make_shopname,name='make_shopname'),
    url(r'^importfile_stocking_demand/',importfile_stocking_demand,name='importfile_stocking_demand'),
    url(r'^importfile_Invoice_BoxPaste/',importfile_Invoice_BoxPaste,name='importfile_Invoice_BoxPaste'),
    url(r'^celery_only_add/',celery_only_add,name='celery_only_add'),
    url(r'^celery_results/',celery_results,name='celery_results'),
    url(r'^show_ebay_variation/',show_ebay_variation,name='show_ebay_variation'),
    url(r'^save_ebay_variation/',save_ebay_variation,name='save_ebay_variation'),
    url(r'^save_ebay_image/', save_ebay_image, name='save_ebay_image'),
    url(r'^show_ebay_image/', show_ebay_image, name='show_ebay_image'),
    url(r'^modify_ebay_schedule/',modify_ebay_schedule,name='modify_ebay_schedule'),
    url(r'^t_templet_ebay_upload_result/',ebay_result_SKU,name='ebay_result_SKU'),
    url(r'^index/',index,name='index'),
    url(r'^celery_mix_opration/',celery_mix_opration,name='celery_mix_opration'),
    url(r'^cexport_refund_to_oss_Plugin/$', cexport_refund_to_oss_Plugin, name='cexport_refund_to_oss_Plugin'),
    url(r'^t_config_store_ebay_regetpes_oauth/', t_config_store_ebay_regetpes_oauth,name='t_config_store_ebay_regetpes_oauth'),
    url(r'^t_config_store_ebay_regetpes_torken/', t_config_store_ebay_regetpes_torken, name='t_config_store_ebay_regetpes_torken'),
    url(r'^t_config_store_ebay_regetpes_plugin/', t_config_store_ebay_regetpes_plugin,name='t_config_store_ebay_regetpes_plugin'),
    url(r'^', include(ebayapp.urls, namespace='ebayapp')),
    url(r'^t_config_wishapi_product_analyse_info_start/', t_config_wishapi_product_analyse_info_start, name='t_config_wishapi_product_analyse_info_start'),
    url(r'^importfile_paypal_tort/',importfile_paypal_tort,name='importfile_paypal_tort'),
    url(r'^importfile_aliexpress_refund/',importfile_aliexpress_refund,name='importfile_aliexpress_refund'),
    url(r'^update_status_by_sku_wish_api/',update_status_by_sku,name='update_status_by_sku'),

    url(r'^syndata_by_wish_api/',syndata,name='syndata'),
    url(r'^syndata_by_wish_api_shopname/',syndata_shopname,name='syndata_shopname'),

    # Joom URL
    url(r'^', include(joom_app.urls, namespace='joom_app')),
    url(r'^lzd_app/', include(lzd_app.urls, namespace='lzd_app')),

    url(r'^up_dis_by_wish_api_shopsku/',dis_enable_by_shopsku,name='dis_enable_by_shopsku'),
    url(r'^edit_update_by_wish_api_listid/',wish_edit_update,name='wish_edit_update'),

    url(r'^change_image/',change_image,name='change_image'),
    url(r'^refresh_sku_info/',refresh_sku_info,name='refresh_sku_info'),
    # url(r'^Project/admin/skuapp/update_order_count/', update_order_count, name='update_order_count'),
    url(r'^refund_chart/',refund_chart,name='refund_chart'),
    url(r'^change_colcol/',change_col,name='change_col'),
    url(r'^syn_b_goods/',syn_b_goods, name='syn_b_goods'),
    url(r'^TestAjax/',TestAjax, name='TestAjax'),

    url(r'^t_online_info_amazon_listing_syn_shopname/', t_online_info_amazon_listing_syn_shopname, name='t_online_info_amazon_listing_syn_shopname'),
    url(r'^t_online_info_amazon_listing_complete_shopname/', t_online_info_amazon_listing_complete_shopname, name='t_online_info_amazon_listing_complete_shopname'),
    url(r'^syndata_by_amazon_api/', syndata_by_amazon_api,name='syndata_by_amazon_api'),
    url(r'^add_amazon_images/',add_amazon_images,name='add_amazon_images'),
    url(r'^save_amazon_images/',save_amazon_images,name='save_amazon_images'),
    url(r'select_amazon_menu/',select_amazon_menu,name='select_amazon_menu'),
    url(r'^show_amazon_schedule/',show_amazon_schedule,name='show_amazon_schedule'),
    url(r'^save_amazon_schedule/',save_amazon_schedule,name='save_amazon_schedule'),
    #/t_templet_amazon_wait_upload/variation/
    url(r'variation/',edit_amazon_variation,name='edit_amazon_variation'),
    url(r'^out_of_stock_chart/',out_of_stock_chart,name='out_of_stock_chart'),

    url(r'^show_feedback_step/',show_feedback_step,name='show_feedback_step'),
    url(r'^show_feedback_picture/',show_feedback_picture,name='show_feedback_picture'),
    url(r'^chioce_large_small/',chioce_large_small,name='chioce_large_small'), # 用于 建资料 页面 选择大小类的函数调用
    url(r'^select_smallcate_by_large/',select_smallcate_by_large,name='select_smallcate_by_large'), # 用于 根据所选择大类 查询小类

    url(r'^chioce_three_cate_of_clothing/',chioce_three_cate_of_clothing,name='chioce_three_cate_of_clothing'), # 用于 开发页面 显示 选择服装三级分类的函数调用
    url(r'^select_next_cate/',select_next_cate,name='select_next_cate'), # 用于 根据所选上级分类 查询下级分类
    url(r'^t_online_info_wish/w_remark/',w_remark,name='w_remark'), # 用于 Wish店铺管理


    url(r'refresh_product_amzon/',refresh_product_amzon,name='refresh_product_amzon'),
    url(r'load_amazon_products/',load_amazon_products,name='load_amazon_products'),
    url(r'^change_joom_picture/',change_joom_picture,name='change_joom_picture'),
    url(r'^importfile_aliexpress_service_divsion_analysis/',aliexpress_service_divsion_analysis,name='aliexpress_service_divsion_analysis'),
    url(r'^task/reverse_collection/', reverse_collection, name='reverse_collection'),
    url(r'^task/get_reverse_info/', get_reverse_info, name='get_reverse_info'),
    url(r'^change_amazon_image/', change_amazon_image, name='change_amazon_image'),
    url(r'^save_amazon_image_change/', save_amazon_image_change, name='save_amazon_image_change'),
    url(r'^show_amazon_pictures/', show_amazon_pictures, name='show_amazon_pictures'),
    url(r'^feedback_zjy_picture/',feedback_zjy_picture,name='feedback_zjy_picture'),
    url(r'^save_feedback_zjy_picture/',save_feedback_zjy_picture,name='save_feedback_zjy_picture'),
    url(r'^product_info_modify_amazon/',product_info_modify_amazon,name='product_info_modify_amazon'),
    url(r'^t_cloth_factor_eidt/update_applyInfo/', update_applyInfo,name='update_applyInfo'),
    url(r'^ali_compare_price/',ali_compare_price,name='ali_compare_price'),
    url(r'^t_product_build_FBA/', t_product_build_FBA,name='t_product_build_FBA'),
    url(r'^t_cloth_factory_dealdata/', t_cloth_factory_dealdata,name='t_cloth_factory_dealdata'),

    url(r'^get_all_productsku_by_mainsku/',get_all_productsku,name='get_all_productsku'), # 用于 主SKU查找子SKU

    url(r'^get_shopsku/',get_shopsku,name='get_shopsku'), # 用于 主SKU查找子SKU

    url(r'^wish_pub_save_image/',wish_pub_save_image,name='wish_pub_save_image'), # 用于 Wish 刊登时保存图片

    url(r'^t_online_info_wish_store_update_title/',wish_store_update_title,name='wish_store_update_title'), # 用于 Wish 批量替换标题

    url(r'^t_online_info_wish_store_change_shipping/',wish_store_change_shipping,name='wish_store_change_shipping'), # 用于 Wish 批量修改运费
    url(r'^t_templet_amazon_upload/',amazon_prodcut_variation,name='amazon_prodcut_variation'),
    url(r'^t_product_depart_get/show_SalesAttr/', edit_show_SalesAttr, name='edit_show_SalesAttr'),# 用于 修改销售所属人
    url(r'^del_feedback_pic/',del_feedback_pic,name='del_feedback_pic'),

    # Aliexpress URL
    url(r'^aliexpress/', include(aliexpress_app.urls, namespace='aliexpress_app')),
    url(r'^wish_store_management/get_refresh_process/', refresh_process, name='refresh_process'),# 用于 wish店铺管理获取刷新进程
    url(r'^wish_store_management/change_wish_express_type/', change_wish_express_type, name='change_wish_express_type'),# 用于 wish店铺管理 修改海外仓类型

    url(r'^app/hh/aliexp-svr/auth-code-get', get_auth_code, name='get_auth_code'),
    url(r'^app/hh/aliexp-svr/auth-token-get', get_auth_token, name='get_auth_token'),
    url(r'^remove_wish_pic_update_flag/',remove_wish_pic_update_flag,name='remove_wish_pic_update_flag'),
    #pulgin url
    url(r'^repeat_sku/',repeat_sku,name='repeat_sku'),
    url(r'^t_config_mstsc_searchplugin/',t_config_searchplugin,name='t_config_mstsc_searchplugin'),
    url(r'^t_tort_info_audit_ipfp/', t_tort_info_audit_ipfp, name='t_tort_info_audit_ipfp'),
    url(r'^t_tort_info_image_info/', t_tort_info_image_info, name='t_tort_info_image_info'),
    url(r'^imageSearch', imageSearch),
    url(r'^sku_countplugin/',sku_countplugin,name='sku_countplugin'),
    url(r'^get_shopname_code/',get_shopname_code,name='get_shopname_code'),
    url(r't_config_mstsc_user_per',t_config_mstsc_user_per,name='t_config_mstsc_user_per'),

    # mymall_app URL
    url(r'^mymallapp/', include(mymall_app.urls, namespace='mymall_app')),

    url(r'^campaign/.*', op_t_wish_pb, name='op_t_wish_pb'),
    url(r'^wishpb_syncshopdata/', op_t_wishpb_sync, name='op_t_wishpb_sync'),
    url(r'^t_work_flow_of_plate_house/update_info/', update_info, name='update_info'),# 更新字段

    url(r'^get_survey_results_info/$', get_survey_results_info, name='get_survey_results_info'),
    url(r'^get-ali1688-page-info/$', get_ali1688_page_info, name='get_ali1688_page_info'),
    url(r'^sales_trend/',sales_trend,name='sales_trend'),
    url(r'^importfile_marketing/',importfile_marketing,name='importfile_marketing'),
    url(r'more_product_informations',more_product_informations,name='more_product_informations'),
    url(r'wish_processed_order/syn/', wish_processed_order_syn),
    url(r'wish_processed_order/show_customer/', wish_processed_order_show_customer),
    url(r'wish_processed_order/ajax/', wish_processed_order_ajax),
    url(r'wish_processed_order/get_syn_status/', wish_processed_order_status),
    url(r'^syn_amazon_cpc_ad/', syn_amazon_cpc_ad,name='syn_amazon_cpc_ad'),
    url(r'^show_inventory_detail/', show_inventory_detail, name='show_inventory_detail'),
    url(r'^show_orders_detail/', show_orders_detail, name='show_orders_detail'),
    url(r'^show_ads_detail/', show_ads_detail, name='show_ads_detail'),
    url(r'wish_notification/syn/', wish_notification_syn),
    url(r'wish_notification/ajax/', wish_notification_ajax),
    url(r'wish_notification/get_syn_status/', wish_notification_status),
    url(r'^listing_refund/',listing_refund,name='listing_refund'),
    url(r'wish_ticket/syn/', wish_ticket_syn),
    url(r'wish_ticket/ajax/', wish_ticket_ajax),
    url(r'wish_ticket/get_syn_status/', wish_ticket_status),
    url(r'^t_product_suringPlugin/', t_product_suringPlugin, name='t_product_suringPlugin'),
    url(r'^show_wish_variant_jp/', show_wish_variant_jp, name='show_wish_variant_jp'),
    url(r'^show_wish_refresh/', show_wish_refresh, name='show_wish_refresh'),
    url(r'^show_edit_jp_info_tile/', show_edit_jp_info_tile, name='show_edit_jp_info_tile'),
    url(r'^show_edit_jp_info_pb/', show_edit_jp_info_pb, name='show_edit_jp_info_pb'),
    url(r'wish_in/syn/', wish_in_syn),
    url(r'wish_in/ajax/', wish_in_ajax),
    url(r'wish_in/get_syn_status/', wish_in_status),
    url(r'^t_cloth_factory_remark/', t_cloth_factory_remark, name='t_cloth_factory_remark'),
    url(r'generate_fba_price_pdf/',generate_fba_price_pdf,name='generate_fba_price_pdf'),
    url(r'^BeyondNum/', BeyondNum, name='BeyondNum'),
    url(r'^listing_rating/',listing_rating,name='listing_rating'),
    url(r'^remove_wish_pic_update_flag/',remove_wish_pic_update_flag,name='remove_wish_pic_update_flag'),
    url(r'refresh_ali_online_info_by_shopname/',refresh_ali_online_info_by_shopname,name='refresh_ali_online_info_by_shopname'),
    url(r'^edit_update_by_ali_api_listid/',edit_update_by_ali_api_listid,name='edit_update_by_ali_api_listid'),
    url(r'^syndata_by_ali_api/',syndata_by_ali_api,name='syndata_by_ali_api'),
    url(r'^syndata_sku_status_by_ali_api/',syndata_sku_status_by_ali_api,name='syndata_sku_status_by_ali_api'),
    url(r'^t_erp_aliexpress_online_info/ShopSKU/',show_ali_child_sku_info,name='show_ali_child_sku_info'),

    # ebay url
    # url(r'^', include(ebayapp.urls, namespace='ebayapp')),

    url(r'^t_supply_chain_production/subsku/',t_supply_chain_production_subsku,name='t_supply_chain_production_subsku'),
    url(r'^t_supply_chain_production_basic/main_pic/',t_supply_chain_production_mainpic,name='t_supply_chain_production_mainpic'),
    url(r'^out_of_stock_schedule_status/',out_of_stock_schedule_status,name='out_of_stock_schedule_status'),
    url(r'generate_mrp_price_india/',generate_mrp_price_india,name='generate_mrp_price_india'),

    url(r't_store_configuration_file/change_status/', update_store_status, name='update_store_status'),  # 店铺配置文件 修改
    url(r't_sku_weight_examine/seach_sku_infor/', seach_sku_infor, name='seach_sku_infor'),  # 克重审核 查询sku信息
    url(r't_online_info_wish_store_upload_image/store_upload_image/', store_upload_image, name='store_upload_image'),  # Wish 店铺管理 用于上传图片
    url(r'^t_templet_wish_publish_draft/change_profitrate/', change_profitrate, name='change_profitrate'),  # Wish 刊登 利润率  价格  计算
    url(r'^t_online_info_wish_store_add_variant/', add_variant, name='add_variant'),  # Wish 店铺管理中增加变体


    url(r'^kc_unsalable_dispose/operation/', kc_unsalable_dispose_operation, name='kc_unsalable_dispose_operation'),
    url(r'^delete_wish_joom_extraimage/',delete_wish_joom_extraimage,name='delete_wish_joom_extraimage'),
    url(r'get_childSKU_by_mainSKU/',get_childSKU_by_mainSKU,name='get_childSKU_by_mainSKU'),
    url(r'check_sku_tortinfo/',check_sku_tortinfo,name='check_sku_tortinfo'),
    url(r'^add_warning_modify/',add_warning_modify,name='add_warning_modify'),
    url(r'^add_information_modify/',add_information_modify,name='add_information_modify'),
    url(r'^show_modify_detail/',show_modify_detail,name='show_modify_detail'),
    url(r'get_template_amazon/',get_template_amazon,name='get_template_amazon'),
    url(r'^add_merge_sku/',add_merge_sku,name='add_merge_sku'),
    url(r'^verify_merge_sku/',verify_merge_sku,name='verify_merge_sku'),
    url(r't_check_report_Plugin/',t_check_report_Plugin,name='t_check_report_Plugin'),
    url(r'deal_checkReportData/',deal_checkReportData,name='deal_checkReportData'),
    url(r'transaction_text_amazon/',transaction_text_amazon,name='transaction_text_amazon'),
    url(r't_stocking_purchase_Plugin/',t_stocking_purchase_Plugin,name='t_stocking_purchase_Plugin'),
    url(r'^save_modify_second/',save_modify_second,name='save_modify_second'),
    url(r'amazon_product_price_modify/', amazon_product_price_modify, name='amazon_product_price_modify'),
    url(r'^t_upload_shopname_chart/',t_upload_shopname_chart,name='t_upload_shopname_chart'),
    url(r'^check_title/',check_title,name='check_title'),   # Wish 刊登校验标题是否侵权
    url(r'^wish_store/edit_shipping_other_country/',edit_shipping,name='edit_shipping'),   # Wish 店铺管理编辑链接的运费
    #url(r'v_product_photo_change/',v_product_photo_change,name='v_product_photo_change'),
    url(r'^aliexpress_online_sku_off/',aliexpress_online_sku_off,name='aliexpress_online_sku_off'),
    url(r'^upload_goods_pic/',upload_goods_pic,name='upload_goods_pic'),

    # shopee_app URL
    url(r'^shopeeapp/', include(shopee_app.urls, namespace='shopee_app')),
    url(r'^modify_purchaser/',modify_purchaser,name='modify_purchaser'),
    url(r'^modify_purchaser_schedule/',modify_purchaser_schedule,name='modify_purchaser_schedule'),
    url(r'^deal_saler_profit/$', deal_saler_profit,name='deal_saler_profit'),
    url(r'^modify_supplier/',modify_supplier,name='modify_supplier'),
    url(r'^wish_activerate/weeklytrend/', get_weeklytrend, name='get_weeklytrend'),
    url(r'change_ad_title/',change_ad_title,name='change_ad_title'),
    url(r'del_ad/',del_ad,name='del_ad'),
    url(r'edit_remark/',edit_remark,name='edit_remark'),
    url(r'show_remark/',show_remark,name='show_remark'),
    url(r'check_amazon_word_tort/',check_amazon_word_tort,name='check_amazon_word_tort'),
    url(r'^fba_deliver_skunum_dealdata/$', fba_deliver_skunum_dealdata,name='fba_deliver_skunum_dealdata'),

    url(r'show_sku_price_detail/', show_sku_price_detail, name='show_sku_price_detail'),
    url(r'show_sku_remove_detail/', show_sku_remove_detail, name='show_sku_remove_detail'),
    url(r'show_sku_pend_detail/', show_sku_pend_detail, name='show_sku_pend_detail'),
    url(r'amazon_product_cost_refresh/', amazon_product_cost_refresh, name='amazon_product_cost_refresh'),
    url(r'show_seller_detail/', show_seller_detail, name='show_seller_detail'),
    url(r'update_duplicate_order/',update_duplicate_order,name='update_duplicate_order'),
    url(r'^store_refund_of_wish/',store_refund_of_wish,name='store_refund_of_wish'),  # Wish店铺退款统计
    url(r'^t_work_flow/.+', t_work_flow_turnto, name='t_work_flow_turnto'),
    # url(r'^factoryapp/', include(factory_app.urls, namespace='factory_app')),
    # 获取速卖通品类
    url(r'skuapp_getcategory',skuapp_getcategory,name='skuapp_getcategory'),
    # 修改速卖通品类
    url(r'skuapp_editcategory',skuapp_editcategory,name='skuapp_editcategory'),
    url(r'show_estimated_detail/', show_estimated_detail, name='show_estimated_detail'),

    url(r'personal_customization_sku/',personal_customization_sku,name='personal_customization_sku'),
    url(r'^get_amazon_comments/', get_amazon_comments, name='get_amazon_comments'),
    url(r'^find_amazon_comments/', find_amazon_comments, name='find_amazon_comments'),
    url(r't_work_flow_of_plate_house_button_click/',t_work_flow_of_plate_house_button_click,name='t_work_flow_of_plate_house_button_click'),
]


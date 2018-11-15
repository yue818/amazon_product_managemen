#-*-coding:utf-8-*-
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from django.utils.safestring import mark_safe
from django.contrib import messages
from skuapp.table.t_templet_config_amazon_published import *
from skuapp.table.t_config_apiurl_amazon import *
from skuapp.table.t_templet_amazon_wait_upload import *
from datetime import datetime
from brick.public.upload_to_oss import *
from Project.settings import BUCKETNAME_ALL_MAINSKU_PIC

"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_templet_amazon_wait_published_Admin.py
 @time: 2017/12/18 12:04
"""
class t_templet_amazon_wait_published_Admin(object):
    variation_item_amazon_flag = True

    def show_image(self, obj):
        rt = u'<img src="%s" style="width: 100px; height: 100px">&nbsp;&nbsp;' % (obj.main_image_url)
        return mark_safe(rt)

    show_image.short_description = u'主图'

    def show_info(self, obj):
        """展示时间、人员信息"""
        st = ''
        if obj.status == '1':
            #     st = u'<font color="#FFCC33">正在处理</font>'
            # elif obj.Status == 'YES':
            st = u'<font color="#FF3333">已采集</font>'
        elif obj.status == '2':
            st = u'<font color="#00BB00">已添加到待刊登</font>'
        rt = u'创建人:%s<br>创建时间:<br>%s<br>更新人:%s<br>更新时间:<br>%s<br>提交状态:%s<br>' \
             % (obj.createUser, obj.createTime, obj.updateUser, obj.updateTime, st)
        return mark_safe(rt)

    show_info.short_description = u'&nbsp;&nbsp;&nbsp;采 集 信 息&nbsp;&nbsp;&nbsp;'

    list_display = ('id', 'show_image', 'item_name', 'show_info')

    list_display_links = ('id')

    actions = ['to_upload_templet']

    # fields = (
    #         'item_name', 'item_sku', 'external_product_id', 'external_product_id_type', 'feed_product_type', 'condition_type',
    #         'quantity', 'department_name', 'brand_name', 'product_description', 'bullet_point1', 'bullet_point2',
    #         'bullet_point3', 'bullet_point4', 'bullet_point5', 'main_image_url', 'swatch_image_url', 'other_image_url1',
    #         'other_image_url2',
    #         'other_image_url3', 'other_image_url4', 'standard_price', 'sale_from_date', 'sale_end_date',
    #         'merchant_shipping_group_name',
    #         'generic_keywords1', 'generic_keywords2', 'generic_keywords3', 'generic_keywords4', 'generic_keywords5',
    #         'manufacturer', 'part_number', 'brand_name', 'warranty_description', 'model', 'model_name',
    #         'update_delete', 'fulfillment_latency', 'display_dimensions_unit_of_measure',
    #         'product_subtype', 'item_package_quantity', 'fulfillment_center_id', 'mfg_minimum',
    #         'mfg_minimum_unit_of_measure',
    #         'unit_count', 'unit_count_type', 'material_type', 'metal_type', 'setting_type', 'ring_size', 'gem_type',
    #         'fit_type',
    #         'department_name1', 'department_name2', 'department_name3', 'department_name4', 'department_name5',
    #         'target_audience_keywords1', 'target_audience_keywords2', 'target_audience_keywords3', 'variation_theme',
    #         )

    fields = ('item_name', 'external_product_id', 'external_product_id_type', 'condition_type',
              'quantity', 'product_description', 'bullet_point1', 'bullet_point2', 'main_image_url', 'other_image_url1',
              'other_image_url2', 'other_image_url3', 'other_image_url4', 'other_image_url5',
              'other_image_url6', 'other_image_url7', 'other_image_url8',
              'bullet_point3', 'bullet_point4', 'bullet_point5', 'standard_price', 'sale_price', 'sale_from_date',
              'sale_end_date', 'merchant_shipping_group_name',
              'generic_keywords1', 'generic_keywords2', 'generic_keywords3', 'generic_keywords4', 'generic_keywords5',
              'manufacturer', 'brand_name', 'warranty_description',
              'update_delete', 'fulfillment_latency', 'display_dimensions_unit_of_measure', 'mfg_minimum',
              'mfg_minimum_unit_of_measure', 'recommended_browse_nodes', 'productSKU', 'item_type',
              )

    form_layout = (
        Fieldset(u'产品主要信息',
                 Row('item_name', 'external_product_id', 'productSKU'),
                 Row('external_product_id_type', 'condition_type'),  # 'feed_product_type',
                 Row('quantity', 'item_type', 'recommended_browse_nodes'),  # 'department_name'
                 css_class='unsort '
                 ),
        Fieldset(u'商品描述',
                 Row('bullet_point1', 'bullet_point2', ),
                 Row('bullet_point3', 'bullet_point4', ),
                 Row('bullet_point5', ),
                 Row('product_description', ),
                 css_class='unsort '
                 ),
        Fieldset(u'图片',
                 Row('main_image_url', ),
                 Row('other_image_url1', 'other_image_url2', 'other_image_url3', 'other_image_url4'),
                 Row('other_image_url5', 'other_image_url6', 'other_image_url7', 'other_image_url8'),
                 css_class='unsort '
                 ),
        Fieldset(u'产品价格/促销',
                 Row('standard_price', 'sale_price'),
                 Row('sale_from_date', ),
                 Row('sale_end_date', ),
                 css_class='unsort '
                 ),
        Fieldset(u'运输模板',
                 Row('merchant_shipping_group_name', ),
                 css_class='unsort '
                 ),
        Fieldset(u'关键词',
                 Row('generic_keywords1', 'generic_keywords2', ),
                 Row('generic_keywords3', 'generic_keywords4', ),
                 Row('generic_keywords5', ),
                 css_class='unsort '
                 ),
        Fieldset(u'厂家信息',
                 Row('manufacturer', 'brand_name'),
                 Row('warranty_description', ),
                 # Row('warranty_description', 'model', 'model_name'),
                 css_class='unsort '
                 ),
        Fieldset(u'操作类型',
                 Row('update_delete', 'fulfillment_latency', 'display_dimensions_unit_of_measure'),
                 css_class='unsort '
                 ),
        Fieldset(u'其它信息',
                 # Row('product_subtype', 'item_package_quantity', 'fulfillment_center_id'),
                 Row('mfg_minimum', 'mfg_minimum_unit_of_measure', ),
                 # Row('unit_count', 'unit_count_type', ),
                 # Row('material_type', 'metal_type', 'setting_type'),
                 # Row('ring_size', 'gem_type', 'fit_type'),
                 css_class='unsort '
                 ),
        # Fieldset(u'适用性别/目标人群',
        #          Row('department_name1', 'department_name2', ),
        #          Row('department_name3', 'department_name4', ),
        #          Row('department_name5', ),
        #          Row('target_audience_keywords1', 'target_audience_keywords2', ),
        #          Row('target_audience_keywords3',),
        #              css_class='unsort '
        #          ),
        # Fieldset(u'变体信息',
        #          Row('variation_theme',),
        #          css_class='unsort '
        #          ),
    )

    def deal_image(self, params):
        upload_to_oss_obj = upload_to_oss(BUCKETNAME_ALL_MAINSKU_PIC)
        result = upload_to_oss_obj.upload_image_to_oss(params=params)
        image_urls = {'image_url': '', 'errorInfo': ''}
        if result['errorcode'] == 0:
            image_urls['image_url'] = result['result']
        else:
            image_urls['errorInfo'] = result['errortext']
        return image_urls

    def save_models(self):
        obj = self.new_obj
        request = self.request
        imageFileFirstName = obj.productSKU + '/Amazon/' + obj.productSKU
        imageFileEndName = '.jpg'
        main_image_url_name = imageFileFirstName + imageFileEndName
        image_urls = self.deal_image({'image_url_path': main_image_url_name, 'imageByte': obj.main_image_url})
        obj.main_image_url = image_urls['image_url']
        if obj.main_image_url == '':
            messages.error(request,
                           'upload image(main_image_url) to oss failed, the reason is "%s"' % image_urls['errorInfo'])
        if obj.other_image_url1:
            main_image_url_name = imageFileFirstName + '_1' + imageFileEndName
            image_urls = self.deal_image({'image_url_path': main_image_url_name, 'imageByte': obj.other_image_url1})
            obj.other_image_url1 = image_urls['image_url']
            if obj.other_image_url1 == '':
                messages.error(request, 'upload image(other_image_url1) to oss failed, the reason is "%s"' % image_urls[
                    'errorInfo'])
        if obj.other_image_url2:
            main_image_url_name = imageFileFirstName + '_2' + imageFileEndName
            image_urls = self.deal_image({'image_url_path': main_image_url_name, 'imageByte': obj.other_image_url2})
            obj.other_image_url2 = image_urls['image_url']
            if obj.other_image_url2 == '':
                messages.error(request, 'upload image(other_image_url2) to oss failed, the reason is "%s"' % image_urls[
                    'errorInfo'])
        if obj.other_image_url3:
            main_image_url_name = imageFileFirstName + '_3' + imageFileEndName
            image_urls = self.deal_image({'image_url_path': main_image_url_name, 'imageByte': obj.other_image_url3})
            obj.other_image_url3 = image_urls['image_url']
            if obj.other_image_url3 == '':
                messages.error(request, 'upload image(other_image_url3) to oss failed, the reason is "%s"' % image_urls[
                    'errorInfo'])
        if obj.other_image_url4:
            main_image_url_name = imageFileFirstName + '_4' + imageFileEndName
            image_urls = self.deal_image({'image_url_path': main_image_url_name, 'imageByte': obj.other_image_url4})
            obj.other_image_url4 = image_urls['image_url']
            if obj.other_image_url4 == '':
                messages.error(request, 'upload image(other_image_url4) to oss failed, the reason is "%s"' % image_urls[
                    'errorInfo'])
        obj.recommended_browse_nodes_id = \
        t_config_apiurl_amazon.objects.filter(category=obj.recommended_browse_nodes, site='EN')[0].id
        obj.createUser = request.user.username
        obj.createTime = datetime.now()
        obj.status = '1'
        obj.save()
# -*-coding:utf-8-*-
from skuapp.table.t_templet_amazon_upload_fail import *
from skuapp.table.t_templet_amazon_recycle_bin import *
from brick.table.t_product_upc_id_amazon import *
from django.db import connection
from django.http import HttpResponseRedirect
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from django.utils.safestring import mark_safe
from django.contrib import messages
from skuapp.table.t_templet_amazon_published_variation import *
from skuapp.table.t_templet_amazon_wait_upload import *
from datetime import datetime
from brick.classredis.classmainsku import *
from brick.classredis.classsku import *
from django.db import connection
from skuapp.views import validation_amazon_product_data, validation_UPC
import time

"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_templet_amazon_collection_box_Admin.py
 @time: 2017/12/15 19:31
"""


class t_templet_amazon_collection_box_Admin(object):
    # plateform_distribution_navigation = True
    site_left_menu_flag = True
    reverse_amazon_collection = True
    variation_item_amazon_flag = True

    def show_image(self, obj):
        if obj.main_image_url:
            # rt = u'<img src="%s" style="width: 100px; height: 100px">&nbsp;&nbsp;' % (obj.main_image_url)
            # rt = '<a href="/change_amazon_image/?id=%s" target="_blank"><img src="%s" style="width: 100px; height: 100px"></a>' % (obj.id, obj.main_image_url)
            rt = '<img id="image_click_%s" src="%s" style="width: 100px; height: 100px">' % (obj.id, obj.main_image_url)
        else:
            main_image_url = ''
            main_image_urls = t_templet_amazon_published_variation.objects.filter(prodcut_variation_id=obj.prodcut_variation_id).values_list('main_image_url')
            if main_image_urls:
                main_image_url = main_image_urls[0][0]
            # rt = u'<img src="%s" style="width: 100px; height: 100px">&nbsp;&nbsp;' % (main_image_url)
            rt = '<img id="image_click_%s" src="%s" style="width: 100px; height: 100px">' % (obj.id, main_image_url)
        rt_script = '''
                <script>
                     $("#image_click_%s").on("click", function(){
                      layer.open({
                       type: 2,
                       skin: "layui-layer-lan",
                       title: "图片编辑",
                       fix: false,
                       shadeClose: true,
                       maxmin: true,
                       area: ["1500px", "500px"],
                       content: "/show_amazon_pictures/?prodcut_variation_id=%s",
                       btn: ["关闭页面"],
                       end : function () {
                            location.reload();
                        },

                       });
                   })
               </script>
               ''' % (obj.id, obj.prodcut_variation_id)
        rt = rt + rt_script
        return mark_safe(rt)

    show_image.short_description = u'主图'

    def show_info(self, obj):
        """展示时间、人员信息"""
        rt = u'创建人:%s<br>创建时间:<br>%s<br>更新人:%s<br>更新时间:<br>%s<br>提交状态:' \
             % (obj.createUser, obj.createTime, obj.updateUser, obj.updateTime)
        state = obj.can_upload
        if state == '-1':
            rt = '%s<br><br><p style="color: #FF3333">%s</p>' % (rt, u'数据待完善')
        elif state == '0':
            rt = '%s<br><br><p style="color: #66FF66">%s</p>' % (rt, u'可转至待发布')
        else:
            rt = '%s<br><br><p style="color: #00BB00">%s</p>' % (rt, u'已提交至待发布')
        return mark_safe(rt)

    show_info.short_description = u'&nbsp;&nbsp;&nbsp;采 集 信 息&nbsp;&nbsp;&nbsp;'

    def show_schedule(self, obj):
        """展示刊登店铺"""
        if obj.ShopSets == '' or obj.ShopSets is None:
            shops = ''
        else:
            shopList = obj.ShopSets.split(',')
            num = len(shopList)
            shops = ''
            for i in range(num):
                if (i + 1) % 10 == 0:
                    shops = shops + shopList[i] + '<br>'
                else:
                    shops = shops + shopList[i] + ','

        rt = '目标店铺：%s<br>' % (shops)

        return mark_safe(rt)

    show_schedule.short_description = u'&nbsp;&nbsp;刊登计划&nbsp;&nbsp;'

    def edit_data(self, obj):
        id = obj.id
        aa = self.request
        bb = str(aa).split('/')
        status = bb[len(bb) - 1].replace("'>", '')
        shopname = obj.ShopSets
        condition = ''
        siteSearch = ''
        if shopname and shopname[0:3] != '---':
            site = shopname.split('-')[-1].split('/')[0]
            ShopName = shopname.split('-')[0] + '-' + shopname.split('-')[1]
            siteSearch = 'ShopName=' + ShopName + '&searchSite=' + site
        if shopname and shopname[0:3] == '---':
            site = shopname.split('-')[-1].split('/')[0]
            siteSearch = 'searchSite=' + site
        if status:
            condition += status
            if shopname:
                condition += '&' + siteSearch
        else:
            condition += '?' + siteSearch
        rt = '<a href="/Project/admin/skuapp/t_templet_amazon_collection_box/%s/update/%s">%s</a>' % (id, condition, u'编辑')
        return mark_safe(rt)

    edit_data.short_description = u'&nbsp;&nbsp;操作&nbsp;&nbsp;'

    def show_variation_info(self, obj):
        """有变体展示变体信息，没有变体展示单体"""
        t_templet_amazon_published_variation_objs = t_templet_amazon_published_variation.objects.filter(
            prodcut_variation_id=obj.prodcut_variation_id)
        if t_templet_amazon_published_variation_objs:
            rt = '<table class="table table-condensed"><tr><td>类型</td><td>变体名</td><td>店铺SKU</td><td>包装数</td></tr>'
            for t_templet_amazon_published_variation_obj in t_templet_amazon_published_variation_objs[0:4]:
                variation_value = ''
                if t_templet_amazon_published_variation_obj.variation_theme == 'Color':
                    variation_value = t_templet_amazon_published_variation_obj.color_name
                if t_templet_amazon_published_variation_obj.variation_theme == 'Size':
                    variation_value = t_templet_amazon_published_variation_obj.size_name
                if t_templet_amazon_published_variation_obj.variation_theme == 'Size-Color':
                    variation_value = t_templet_amazon_published_variation_obj.size_name + '--' + \
                                      t_templet_amazon_published_variation_obj.color_name
                if t_templet_amazon_published_variation_obj.variation_theme == 'MetalType':
                    variation_value = t_templet_amazon_published_variation_obj.MetalType
                if t_templet_amazon_published_variation_obj.variation_theme == 'MetalType-Size':
                    variation_value = t_templet_amazon_published_variation_obj.MetalType + '--' + \
                                      t_templet_amazon_published_variation_obj.size_name
                rt += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (t_templet_amazon_published_variation_obj.variation_theme,
                                                                                 variation_value, t_templet_amazon_published_variation_obj.child_sku,
                                                                                 t_templet_amazon_published_variation_obj.item_quantity,)
            if obj.productSKU:
                rt += '<tr><td><a id="link_id_%s">%s</a></td></tr>' % (obj.id, u'编辑变体')
                rt += "</table><script>$('#link_id_%s').on('click',function(){" \
                      "layer.open({type:2,skin:'layui-layer-lan',title:'编辑变体',fix:false,shadeClose: true," \
                      "maxmin:true,area:['1500px','500px'],content:'/t_templet_amazon_collection_box/variation/?prodcut_variation_id=%s&productSKU=%s'," \
                      "btn: ['关闭页面'],end:function (){location.reload();}});});" \
                      "</script>" % (obj.id, obj.prodcut_variation_id, obj.productSKU)
            else:
                rt += '<tr><td>%s</td></tr></table>' % (u'请先完善商品SKU')
        else:
            if obj.productSKU:
                rt = "<a id='link_id_%s'>%s</a><script>$('#link_id_%s').on('click',function(){" \
                     "layer.open({type:2,skin:'layui-layer-lan',title:'添加变体',fix:false,shadeClose: true," \
                     "maxmin:true,area:['1500px','500px'],content:'/t_templet_amazon_collection_box/variation/?prodcut_variation_id=%s&productSKU=%s'," \
                     "btn: ['关闭页面'],end:function (){location.reload();}});});" \
                     "</script>" % (obj.id, u'添加变体', obj.id, obj.prodcut_variation_id, obj.productSKU)
            else:
                rt = u"请先完善商品SKU"
        return mark_safe(rt)

    show_variation_info.short_description = mark_safe(u'<p style="color:#428BCA" align="center">单体/变体</p>')

    def show_result(self, obj):
        rt = u'未刊登产品'
        t_templet_amazon_upload_fail_objs = t_templet_amazon_upload_fail.objects.filter(prodcut_variation_id=obj.prodcut_variation_id).order_by('-id')
        error_info = {'The SKU data provided is different from': u'UPC重复',
                      'Message/Product/DescriptionData/MerchantShippingGroupName': u'店铺运输方式名错误',
                      'Missing Attributes ': u'缺少字段', 'Can not get images for product_sku:': u'获取图片失败',
                      'You are not authorized to list products in this category': u'无权限刊登此类商品',
                      'ItemPackageQuantity': u'商品数量不能为空',
                      'RecommendedBrowseNode': u'类目树选择错误', 'MinimumManufacturerAgeRecommended': u'最小使用年龄不能为空',
                      'The content of elements must consist of well-formed character data or markup': u'商品种类不能为空',
                      'We could not access the media at URL http://': u'商品刊登成功，但图片缺失，缺失图片的店铺SKU：'}
        if t_templet_amazon_upload_fail_objs:
            t_templet_amazon_upload_fail_obj = t_templet_amazon_upload_fail_objs[0]
            # rt = t_templet_amazon_upload_fail_obj.resultInfo
            if t_templet_amazon_upload_fail_obj.errorMessages:
                errorMessages_temp = u'未知错误'
                for error_message in error_info:
                    if error_message in t_templet_amazon_upload_fail_obj.errorMessages:
                        errorMessages_temp = error_info[error_message]
                if errorMessages_temp == u'缺少字段':
                    need_param_list = t_templet_amazon_upload_fail_obj.errorMessages.split('Missing Attributes ')
                    need_params = ''
                    for i in range(1, len(need_param_list)):
                        need_params += '<br/>' + need_param_list[i].split('. SKU')[0]
                    errorMessages_temp += need_params
                if errorMessages_temp == u'商品刊登成功，但图片缺失，缺失图片的店铺SKU：':
                    need_params = ''
                    if '{"SKU": {"value": "' in obj.errorMessages:
                        need_params_temps = obj.errorMessages.split('{"SKU": {"value": "')
                        for i in range(1, len(need_params_temps)):
                            if '"},' in need_params_temps[i]:
                                need_params += '<br/>' + need_params_temps[i].split('"},')[0]
                    errorMessages_temp += need_params
                rt = '<div style="width: 100%; height: auto; word-wrap:break-word; word-break:break-all; overflow: hidden;  ">' + errorMessages_temp + '</div>'
        return mark_safe(rt)

    show_result.short_description = u'&nbsp;&nbsp;刊登结果&nbsp;&nbsp;'

    list_display = ('show_image', 'productSKU', 'item_name', 'show_variation_info', 'show_schedule', 'show_info', 'show_result', 'edit_data')

    list_display_links = ('id')

    list_editable = ('external_product_id',)

    actions = ['to_upload_templet', 'to_recycle']

    fields = ('item_name', 'external_product_id_type', 'condition_type', 'toy_color', 'jewerly_color', 'material_type',
              'quantity', 'product_description', 'bullet_point1', 'bullet_point2', 'metal_type', 'item_shape',
              'homes_size',
              'bullet_point3', 'bullet_point4', 'bullet_point5', 'standard_price', 'sale_price', 'sale_from_date',
              'sale_end_date', 'fulfillment_latency',
              'homes_color',
              'generic_keywords1', 'generic_keywords2', 'generic_keywords3', 'generic_keywords4', 'generic_keywords5',
              'product_subtype', 'unit_count', 'unit_count_type', 'mfg_minimum', 'clothing_size', 'clothing_color',
              'mfg_minimum_unit_of_measure', 'productSKU', 'item_package_quantity', 'item_type', 'warranty_description',
              'department_name1', 'department_name2', 'department_name3', 'department_name4', 'department_name5',
              'target_audience_keywords1', 'target_audience_keywords2', 'target_audience_keywords3', 'number_of_pieces'
              )

    form_layout = (
        Fieldset(u'产品主要信息',
                 Row('item_name', 'productSKU', 'external_product_id_type', ),
                 Row('quantity', 'item_package_quantity', 'condition_type', ),  # 'feed_product_type',
                 Row('item_type', 'product_subtype'),
                 css_class='unsort '
                 ),
        Fieldset(u'商品描述',
                 Row('bullet_point1', 'bullet_point2', ),
                 Row('bullet_point3', 'bullet_point4', ),
                 # Row('bullet_point5', 'bullet_point6', ),
                 Row('bullet_point5', ),
                 Row('product_description', ),
                 css_class='unsort '
                 ),
        # Fieldset(u'图片',
        #          Row('main_image_url', ),
        #          Row('other_image_url1', 'other_image_url2', 'other_image_url3', 'other_image_url4'),
        #          Row('other_image_url5', 'other_image_url6', 'other_image_url7', 'other_image_url8'),
        #          css_class='unsort '
        #          ),
        Fieldset(u'产品价格/促销',
                 Row('standard_price', 'sale_price'),
                 Row('sale_from_date', 'sale_end_date', ),
                 css_class='unsort '
                 ),
        Fieldset(u'关键词',
                 Row('generic_keywords1', 'generic_keywords2', ),
                 Row('generic_keywords3', 'generic_keywords4', ),
                 Row('generic_keywords5', ),
                 css_class='unsort '
                 ),
        # Fieldset(u'厂家信息/操作类型',
        #          Row('manufacturer', 'brand_name', 'update_delete', ),
        # Row('fulfillment_latency', 'display_dimensions_unit_of_measure'),
        # Row('warranty_description', ),
        # Row('warranty_description', 'model', 'model_name'),
        # css_class='unsort '
        # ),
        Fieldset(u'其它信息',
                 # Row('product_subtype', 'item_package_quantity', 'fulfillment_center_id'),
                 Row('mfg_minimum', 'mfg_minimum_unit_of_measure', 'item_shape'),
                 Row('unit_count', 'unit_count_type', 'metal_type', 'jewerly_color', 'material_type', ),
                 Row('clothing_size', 'clothing_color', 'fulfillment_latency', ),
                 Row('toy_color', 'homes_color', 'homes_size', 'number_of_pieces'),
                 Row('warranty_description', ),
                 # Row('material_type', 'metal_type', 'setting_type'),
                 # Row('ring_size', 'gem_type', 'fit_type'),
                 css_class='unsort '
                 ),
        Fieldset(u'适用性别/目标人群',
                 Row('target_audience_keywords1', 'target_audience_keywords2', 'target_audience_keywords3', ),
                 Row('department_name1', 'department_name2', ),
                 Row('department_name3', 'department_name4', ),
                 Row('department_name5', ),
                 css_class='unsort '
                 ),
    )

    def getTortInfo(self, productSku):
        classsku_obj = classsku(connection)
        mainSKU = classsku_obj.get_bemainsku_by_sku(productSku)
        classmainsku_obj = classmainsku(connection)
        tortInfo = classmainsku_obj.get_tort_by_mainsku(mainSKU)
        return tortInfo

    def save_product_variation(self, request, obj, prodcut_variation_id):
        variation_theme = request.POST.get('variation_theme', '')
        size_names = request.POST.getlist('size_name', '')
        color_names = request.POST.getlist('color_name', '')
        MetalTypes = request.POST.getlist('MetalType', '')
        prices = request.POST.getlist('variation_price', '')
        productSKUs = request.POST.getlist('product_SKU', '')
        item_quantitys = request.POST.getlist('item_quantity', '')
        MetalType = []
        size_name = []
        color_name = []
        productSKU = []
        item_quantity = []
        insert_result = 0
        for sn in size_names:
            if sn:
                size_name.append(sn)
        for cn in color_names:
            if cn:
                color_name.append(cn)
        for pSKU in productSKUs:
            if pSKU:
                productSKU.append(pSKU)
        for mt in MetalTypes:
            if mt:
                MetalType.append(mt)
        for iq in item_quantitys:
            if iq:
                item_quantity.append(iq)
        main_images = request.POST.getlist('variation_images', '')
        all_image_list = {'other_image_url1': '', 'other_image_url2': '',
                          'other_image_url3': '', 'other_image_url4': '',
                          'other_image_url5': '', 'other_image_url6': '',
                          'other_image_url7': '', 'other_image_url8': '', 'main_image_url': ''}
        if variation_theme:
            variationCount = len(size_name)
            if color_name:
                variationCount = len(color_name)
            for i in range(0, variationCount):
                if productSKU:
                    tortInfo = self.getTortInfo(productSKU[i])
                    # messages.error(request, 'tortInfo: %s'%tortInfo)
                    if tortInfo:
                        for tortinfo in tortInfo:
                            if 'Amazon' in tortinfo:
                                insert_result = -1
                                return insert_result
                else:
                    sizeName = ''
                    colorName = ''
                    metalType = ''
                    itemQuantity = ''
                    if main_images[i]:
                        all_image_list = eval(main_images[i])
                    if size_name:
                        sizeName = size_name[i]
                    if item_quantity:
                        itemQuantity = item_quantity[i]
                    if color_name:
                        colorName = color_name[i]
                    if MetalType:
                        metalType = MetalType[i]
                    t_templet_amazon_published_variation_obj = t_templet_amazon_published_variation()
                    t_templet_amazon_published_variation_obj.relationship_type = 'variation'
                    t_templet_amazon_published_variation_obj.item_quantity = itemQuantity
                    t_templet_amazon_published_variation_obj.variation_theme = variation_theme
                    t_templet_amazon_published_variation_obj.parent_child = 'child'
                    t_templet_amazon_published_variation_obj.parent_item_sku = obj.productSKU
                    t_templet_amazon_published_variation_obj.productSKU = productSKU[i]
                    t_templet_amazon_published_variation_obj.color_name = colorName
                    t_templet_amazon_published_variation_obj.size_name = sizeName
                    t_templet_amazon_published_variation_obj.color_map = colorName
                    t_templet_amazon_published_variation_obj.MetalType = metalType
                    t_templet_amazon_published_variation_obj.size_map = sizeName
                    t_templet_amazon_published_variation_obj.other_image_url1 = all_image_list['other_image_url1']
                    t_templet_amazon_published_variation_obj.other_image_url2 = all_image_list['other_image_url2']
                    t_templet_amazon_published_variation_obj.other_image_url3 = all_image_list['other_image_url3']
                    t_templet_amazon_published_variation_obj.other_image_url4 = all_image_list['other_image_url4']
                    t_templet_amazon_published_variation_obj.other_image_url5 = all_image_list['other_image_url5']
                    t_templet_amazon_published_variation_obj.other_image_url6 = all_image_list['other_image_url6']
                    t_templet_amazon_published_variation_obj.other_image_url7 = all_image_list['other_image_url7']
                    t_templet_amazon_published_variation_obj.other_image_url8 = all_image_list['other_image_url8']
                    t_templet_amazon_published_variation_obj.main_image_url = all_image_list['main_image_url']
                    t_templet_amazon_published_variation_obj.price = prices[i]
                    t_templet_amazon_published_variation_obj.prodcut_variation_id = prodcut_variation_id
                    t_templet_amazon_published_variation_obj.save()
        return insert_result

    def save_models(self):
        import urllib, time
        obj = self.new_obj
        request = self.request
        post = request.POST
        searchSite = request.GET.get('searchSite', '')
        ShopSets = post.get('ShopSets', '').encode("utf-8")
        if ShopSets == '0' or ShopSets == 0:
            ShopSets = '---' + searchSite + '/PJ'
        upload_product_type = post.get('upload_product_type', '')
        if upload_product_type == '0' or upload_product_type == 0:
            upload_product_type = ''
        if searchSite is None or searchSite.strip() == '':
            searchSite = ('%s' % ShopSets).split('-')[-1].split('/')[0]
        ShopName = request.GET.get('ShopName', '')
        t_config_shop_alias_objs = t_config_shop_alias.objects.filter(ShopName=ShopSets)
        shopAlias = ''
        if len(t_config_shop_alias_objs) > 0:
            shopAlias = t_config_shop_alias_objs[0].ShopAlias
        obj.ShopSets = ShopSets
        obj.brand_name = shopAlias
        obj.manufacturer = shopAlias
        update_sites = {'US': 'Update', 'DE': 'Aktualisierung', 'FR': 'Actualisation', 'UK': 'Update', 'AU': 'Update', 'IN': 'Update'}
        shipping_group_sites = {'US': 'Migrated Template', 'DE': 'Standardvorlage Amazon', 'FR': 'Modèle par défaut Amazon', 'UK': 'Migrated Template',
                                'AU': 'Migrated Template', 'IN': 'Migrated Template'}
        feed_product_type = request.POST.get('feed_product_type', '')
        if feed_product_type == '0' or feed_product_type == 0:
            feed_product_type = ''
        recommended_browse_nodes = urllib.unquote(request.GET.get('recommended_browse_nodes', '')).replace('RBNAND', '&')
        RootID = request.GET.get('RootID', '')
        prodcut_variation_id = int(time.time() * 1000)
        all_image_list = {'other_image_url1': '', 'other_image_url2': '',
                          'other_image_url3': '', 'other_image_url4': '',
                          'other_image_url5': '', 'other_image_url6': '',
                          'other_image_url7': '', 'other_image_url8': '', 'main_image_url': ''}
        main_images = request.POST.get('main_images', '')
        productSKUlist = [obj.productSKU, ]
        newProductSKUlist = []
        if 'and' in obj.productSKU:
            productSKUlist = obj.productSKU.split('and')
        for productSKU in productSKUlist:
            productSKUtemp = productSKU
            if '*' in productSKU:
                productSKUtemp = productSKU.split('*')[0]
            newProductSKUlist.append(productSKUtemp)
        isTort = 0
        for newProductSKU in newProductSKUlist:
            tortInfo = self.getTortInfo(newProductSKU)
            # messages.error(request, 'tortInfo: %s' % tortInfo)
            if tortInfo:
                for tortinfo in tortInfo:
                    if 'Amazon' in tortinfo:
                        isTort = 1
        if isTort == 0:
            if obj is None or obj.id is None or obj.id <= 0:
                if main_images:
                    all_image_list = eval(main_images)
                obj.other_image_url1 = all_image_list['other_image_url1']
                obj.other_image_url2 = all_image_list['other_image_url2']
                obj.other_image_url3 = all_image_list['other_image_url3']
                obj.other_image_url4 = all_image_list['other_image_url4']
                obj.other_image_url5 = all_image_list['other_image_url5']
                obj.other_image_url6 = all_image_list['other_image_url6']
                obj.other_image_url7 = all_image_list['other_image_url7']
                obj.other_image_url8 = all_image_list['other_image_url8']
                obj.main_image_url = all_image_list['main_image_url']
                obj.recommended_browse_nodes = recommended_browse_nodes
                obj.prodcut_variation_id = prodcut_variation_id
                insert_result = self.save_product_variation(request, obj, prodcut_variation_id)
                if insert_result == 0:
                    # Migrated Template
                    obj.merchant_shipping_group_name = shipping_group_sites[searchSite]
                    obj.update_delete = update_sites[searchSite]
                    obj.item_name = obj.manufacturer + ' ' + obj.item_name
                    obj.upload_product_type = upload_product_type
                    obj.feed_product_type = feed_product_type
                    obj.recommended_browse_nodes_id = RootID
                    obj.createUser = request.user.username
                    obj.part_number = obj.productSKU
                    obj.createTime = datetime.now()
                    obj.status = '1'
                    obj.can_upload = '-1'
                    if validation_amazon_product_data(obj) == 1:
                        obj.can_upload = '0'
                    obj.save()
                    if searchSite:
                        post['_addanother_ywp'] = '/Project/admin/skuapp/t_templet_amazon_collection_box/add/?searchSite=' + searchSite
                else:
                    messages.error(request, '该商品存在侵权记录！！！')
            else:
                old_obj = self.model.objects.get(pk=obj.pk)
                if main_images:
                    all_image_list = eval(main_images)
                    old_obj.other_image_url1 = all_image_list['other_image_url1']
                    old_obj.other_image_url2 = all_image_list['other_image_url2']
                    old_obj.other_image_url3 = all_image_list['other_image_url3']
                    old_obj.other_image_url4 = all_image_list['other_image_url4']
                    old_obj.other_image_url5 = all_image_list['other_image_url5']
                    old_obj.other_image_url6 = all_image_list['other_image_url6']
                    old_obj.other_image_url7 = all_image_list['other_image_url7']
                    old_obj.other_image_url8 = all_image_list['other_image_url8']
                    old_obj.main_image_url = all_image_list['main_image_url']
                else:
                    old_obj.other_image_url1 = obj.other_image_url1
                    old_obj.other_image_url2 = obj.other_image_url2
                    old_obj.other_image_url3 = obj.other_image_url3
                    old_obj.other_image_url4 = obj.other_image_url4
                    old_obj.other_image_url5 = obj.other_image_url5
                    old_obj.other_image_url6 = obj.other_image_url6
                    old_obj.other_image_url7 = obj.other_image_url7
                    old_obj.other_image_url8 = obj.other_image_url8
                    old_obj.main_image_url = obj.main_image_url
                if recommended_browse_nodes:
                    old_obj.recommended_browse_nodes = recommended_browse_nodes
                    old_obj.recommended_browse_nodes_id = RootID
                old_obj.external_product_id = obj.external_product_id
                old_obj.external_product_id_type = obj.external_product_id_type
                old_obj.clothing_color = obj.clothing_color
                old_obj.clothing_size = obj.clothing_size
                old_obj.jewerly_color = obj.jewerly_color
                old_obj.homes_color = obj.homes_color
                old_obj.homes_size = obj.homes_size
                old_obj.item_shape = obj.item_shape
                if obj.item_name.startswith(obj.manufacturer):
                    old_obj.item_name = obj.item_name
                else:
                    old_obj.item_name = obj.manufacturer + ' ' + obj.item_name
                old_obj.toy_color = obj.toy_color
                old_obj.item_type = obj.item_type
                old_obj.manufacturer = obj.manufacturer
                old_obj.upload_product_type = upload_product_type
                old_obj.feed_product_type = feed_product_type
                old_obj.product_subtype = obj.product_subtype
                old_obj.product_description = obj.product_description
                old_obj.brand_name = obj.brand_name
                old_obj.update_delete = update_sites[searchSite]
                old_obj.item_package_quantity = obj.item_package_quantity
                old_obj.standard_price = obj.standard_price
                old_obj.sale_price = obj.sale_price
                old_obj.sale_from_date = obj.sale_from_date
                old_obj.sale_end_date = obj.sale_end_date
                old_obj.condition_type = obj.condition_type
                old_obj.quantity = obj.quantity
                old_obj.merchant_shipping_group_name = shipping_group_sites[searchSite]
                old_obj.bullet_point1 = obj.bullet_point1
                old_obj.bullet_point2 = obj.bullet_point2
                old_obj.bullet_point3 = obj.bullet_point3
                old_obj.bullet_point4 = obj.bullet_point4
                old_obj.bullet_point5 = obj.bullet_point5
                old_obj.generic_keywords = obj.generic_keywords
                old_obj.fulfillment_center_id = obj.fulfillment_center_id
                old_obj.model_name = obj.model_name
                old_obj.warranty_description = obj.warranty_description
                old_obj.variation_theme = obj.variation_theme
                old_obj.model = obj.model
                old_obj.mfg_minimum = obj.mfg_minimum
                old_obj.mfg_minimum_unit_of_measure = obj.mfg_minimum_unit_of_measure
                old_obj.swatch_image_url = obj.swatch_image_url
                old_obj.department_name = obj.department_name
                old_obj.fit_type = obj.fit_type
                old_obj.unit_count = obj.unit_count
                old_obj.unit_count_type = obj.unit_count_type
                old_obj.fulfillment_latency = obj.fulfillment_latency
                old_obj.display_dimensions_unit_of_measure = obj.display_dimensions_unit_of_measure
                old_obj.generic_keywords1 = obj.generic_keywords1
                old_obj.generic_keywords2 = obj.generic_keywords2
                old_obj.generic_keywords3 = obj.generic_keywords3
                old_obj.generic_keywords4 = obj.generic_keywords4
                old_obj.generic_keywords5 = obj.generic_keywords5
                old_obj.department_name1 = obj.department_name1
                old_obj.department_name2 = obj.department_name2
                old_obj.department_name3 = obj.department_name3
                old_obj.department_name4 = obj.department_name4
                old_obj.department_name5 = obj.department_name5
                old_obj.material_type = obj.material_type
                old_obj.metal_type = obj.metal_type
                old_obj.setting_type = obj.setting_type
                old_obj.ring_size = obj.ring_size
                old_obj.gem_type = obj.gem_type
                old_obj.target_audience_keywords1 = obj.target_audience_keywords1
                old_obj.target_audience_keywords2 = obj.target_audience_keywords2
                old_obj.target_audience_keywords3 = obj.target_audience_keywords3
                old_obj.productSKU = obj.productSKU
                old_obj.updateUser = request.user.username
                old_obj.updateTime = datetime.now()
                old_obj.ShopSets = ShopSets
                old_obj.can_upload = '-1'
                if validation_amazon_product_data(obj) == 1:
                    old_obj.can_upload = '0'
                old_obj.number_of_pieces = obj.number_of_pieces
                old_obj.save()
            if ShopName:
                post['_addanother_ywp'] = '/Project/admin/skuapp/t_templet_amazon_collection_box/add/?' \
                                          'ShopName=' + ShopName + '&searchSite=' + searchSite
        else:
            messages.error(request, '该商品存在Amazon侵权记录！！！')

    def to_upload_templet(self, request, queryset):
        time = datetime.now()
        user = request.user.username
        for obj in queryset:
            if obj.status == '2':
                messages.error(request, u'ID是%s已经提交为公共模板，请勿重复提交！' % obj.id)
                continue
            elif obj.can_upload == '-1':
                messages.error(request, u'ID是%s数据未完善，请完善数据后再执行该操作！' % obj.id)
                continue
            else:
                upc_count = 1
                var_cnt = 0
                t_templet_amazon_published_variation_objs = t_templet_amazon_published_variation.objects.filter(prodcut_variation_id=obj.prodcut_variation_id)
                if t_templet_amazon_published_variation_objs.exists():
                    upc_count = len(t_templet_amazon_published_variation_objs)
                    var_cnt = len(t_templet_amazon_published_variation_objs)
                t_product_upc_id_amazon_obj = t_product_upc_id_amazon(connection)
                upc_id_list = []
                for i in range(0, upc_count):
                    upc_id = t_product_upc_id_amazon_obj.update_product_id({'id_type': obj.external_product_id_type})
                    if upc_id is None or upc_id == 0:
                        messages.error(request, u'UPC不够，请联系相关管理员')
                        return
                    upc = t_product_upc_id_amazon_obj.get_newest_product_id({'id': upc_id})
                    upc = upc['external_product_id']
                    if validation_UPC(upc) == 1:
                        i = i - 1
                    upc_id_list.append(upc)
                t_templet_amazon_wait_upload_obj = t_templet_amazon_wait_upload()
                t_templet_amazon_wait_upload_obj.__dict__ = obj.__dict__
                t_templet_amazon_wait_upload_obj.createTime = time
                t_templet_amazon_wait_upload_obj.createUser = user
                t_templet_amazon_wait_upload_obj.updateTime = time
                t_templet_amazon_wait_upload_obj.updateStaff = user
                t_templet_amazon_wait_upload_obj.status = 'NO'
                t_templet_amazon_wait_upload_obj.can_upload = '1'
                if upc_count == 1 and var_cnt == 0:
                    t_templet_amazon_wait_upload_obj.external_product_id = upc_id_list[0]
                else:
                    for i in range(0, upc_count):
                        t_templet_amazon_published_variation_objs[i].external_product_id = upc_id_list[i]
                        t_templet_amazon_published_variation_objs[i].save()
                t_templet_amazon_wait_upload_obj.save()
                obj.status = '2'
                # obj.Flag = 0
                obj.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/').replace('t_templet_amazon_collection_box/',
                                                                                  't_templet_amazon_wait_upload/?_p_status=NO'))

    to_upload_templet.short_description = u'转到待刊登'

    def to_recycle(self, request, queryset):
        time = datetime.now()
        user = request.user.username
        for obj in queryset:
            t_templet_amazon_recycle_bin_obj = t_templet_amazon_recycle_bin()
            t_templet_amazon_recycle_bin_obj.__dict__ = obj.__dict__
            t_templet_amazon_recycle_bin_obj.createTime = time
            t_templet_amazon_recycle_bin_obj.createUser = user
            t_templet_amazon_recycle_bin_obj.updateTime = time
            t_templet_amazon_recycle_bin_obj.updateStaff = user
            t_templet_amazon_recycle_bin_obj.resultInfo = ''
            t_templet_amazon_recycle_bin_obj.errorMessages = ''
            t_templet_amazon_recycle_bin_obj.mqResponseInfo = ''
            t_templet_amazon_recycle_bin_obj.status = '1'
            t_templet_amazon_recycle_bin_obj.save()
            obj.status = '3'
            # obj.Flag = 0
            obj.save()

    to_recycle.short_description = u'扔到回收站'

    def get_list_queryset(self, ):
        """显示可显示的，自己本人的"""
        request = self.request
        qs = super(t_templet_amazon_collection_box_Admin, self).get_list_queryset()
        if request.user.is_superuser:
            qs = qs.filter(status='1')
        else:
            qs = qs.filter(createUser=request.user.username, status='1')
        return qs
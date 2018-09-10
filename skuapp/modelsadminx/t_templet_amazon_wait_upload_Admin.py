#-*-coding:utf-8-*-
from skuapp.table.t_templet_amazon_collection_box import *
from skuapp.table.t_config_shop_alias import *
from brick.table.t_product_upc_id_amazon import *
from skuapp.views import validation_amazon_product_data,validation_UPC
from skuapp.table.t_templet_amazon_upload_result import *
from app_djcelery.tasks import stitch_goods_info
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.db import connection
from brick.table.t_config_online_amazon import *
from skuapp.table.t_templet_amazon_upload_result import *
from skuapp.table.t_templet_amazon_published_variation import *
from brick.public.generate_shop_code import *
from skuapp.table.t_config_mq_info import t_config_mq_info
from datetime import datetime
from brick.classredis.classsku import classsku
from brick.classredis.classmainsku import classmainsku
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from brick.public.combination_sku import G_ZHSKU
from brick.public.shopsku_apply import shopsku_apply

"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_templet_amazon_wait_upload_Admin.py
 @time: 2017/12/16 9:53
"""

class t_templet_amazon_wait_upload_Admin(object):
    # plateform_distribution_navigation = True
    # site_left_menu_flag = True
    amazon_site_left_menu_tree_flag = True
    variation_item_amazon_flag = True
    def show_image(self, obj):
        project_url = self.request.get_full_path()
        if obj.main_image_url:
            rt = '<img id="image_click_%s" src="%s" style="width: 100px; height: 100px">' % (obj.id, obj.main_image_url)
        else:
            main_image_url = ''
            main_image_urls = t_templet_amazon_published_variation.objects.filter(
                prodcut_variation_id=obj.prodcut_variation_id).values_list('main_image_url')
            if main_image_urls:
                main_image_url = main_image_urls[0][0]
            rt = '<img id="image_click_%s" src="%s" style="width: 100px; height: 100px">' % (obj.id, main_image_url)
        if '_p_status=FAILED' in project_url:
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
                    
                    });
                })
            </script>
            ''' % (obj.id, obj.prodcut_variation_id)
            rt = rt + rt_script
        return mark_safe(rt)

    show_image.short_description = u'主图'

    def show_product_sku(self, obj):
        count = 0
        sku_show = ''
        if obj.productSKU:
            for i in obj.productSKU:
                count += 1
                sku_show += i
                if count % 10 == 0:
                    sku_show += '<br>'
        return mark_safe(sku_show)
    show_product_sku.short_description = '商品SKU'

    def show_info(self, obj):
        """展示时间、人员信息"""
        st = ''
        if obj.status == 'NO':
            #     st = u'<font color="#FFCC33">正在处理</font>'
            # elif obj.Status == 'YES':
            st = u'<font color="#FF3333">未刊登</font>'
        elif obj.status == 'FAILED':
            st = u'<font color="#FF3333">刊登失败</font>'
            if obj.can_upload == '-1':
                st += u'<br/><font color="#FF3333">数据待修改</font>'
            if obj.can_upload == '0':
                st += u'<br/><font color="#FF3333">可重新发布</font>'
        else:
            st = u'<font color="#00BB00">提交至刊登</font>'
        rt = u'创建人:%s<br>创建时间:<br>%s<br>更新人:%s<br>更新时间:<br>%s<br>提交状态:%s<br>' \
             % (obj.createUser, obj.createTime, obj.updateUser, obj.updateTime, st)
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
        state = obj.status
        if state == 'NO':
            rt = '%s<br><br><p style="color: #FF3333">%s</p>' % (rt, u'未刊登')
        elif state == 'FAILED':
            rt = '%s<br><br><p style="color: #FF3333">%s</p>' % (rt, u'刊登失败')
            if obj.can_upload == '-1':
                rt += u'<br/><font color="#FF3333">数据待修改</font>'
            if obj.can_upload == '0':
                rt += u'<br/><font color="#FF3333">可重新发布</font>'
        elif state == 'OPEN':
            rt = '%s<br><br><p style="color: #00BB00">%s</p>' % (rt, u'已提交至刊登')

        return mark_safe(rt)
    show_schedule.short_description = u'&nbsp;&nbsp;刊登计划&nbsp;&nbsp;'

    def show_result(self, obj):
        rt = u'未刊登产品'
        t_templet_amazon_upload_result_objs = t_templet_amazon_upload_result.objects.filter(prodcut_variation_id=obj.prodcut_variation_id)
        error_info = {'The SKU data provided is different from': u'UPC重复', 'Message/Product/DescriptionData/MerchantShippingGroupName': u'店铺运输方式名错误',
                      'Missing Attributes ': u'缺少字段', 'Can not get images for product_sku:': u'获取图片失败',
                      'You are not authorized to list products in this category': u'无权限刊登此类商品', 'ItemPackageQuantity': u'商品数量不能为空',
                      'RecommendedBrowseNode': u'类目树选择错误', 'MinimumManufacturerAgeRecommended': u'最小使用年龄不能为空',
                      'The content of elements must consist of well-formed character data or markup': u'商品种类不能为空'}
        if t_templet_amazon_upload_result_objs:
            t_templet_amazon_upload_result_obj = t_templet_amazon_upload_result_objs[0]
            rt = t_templet_amazon_upload_result_obj.resultInfo
            if t_templet_amazon_upload_result_obj.errorMessages:
                errorMessages_temp = ''
                for error_message in error_info:
                    if error_message in t_templet_amazon_upload_result_obj.errorMessages:
                        errorMessages_temp = error_info[error_message]
                if errorMessages_temp == u'缺少字段':
                    need_param_list = t_templet_amazon_upload_result_obj.errorMessages.split('Missing Attributes ')
                    need_params = ''
                    for i in range(1, len(need_param_list)):
                        need_params += '<br/>' + need_param_list[i].split('. SKU')[0]
                    errorMessages_temp += need_params
                if errorMessages_temp == '':
                    temps = t_templet_amazon_upload_result_obj.errorMessages.split('"')
                    for i in range(0,len(temps)):
                        if (i+1)%2 == 0:
                            errorMessages_temp += temps[i] + '<br/>'
                rt += ', Reason: <div style="width: 100%; height: auto; word-wrap:break-word; word-break:break-all; overflow: hidden;  ">'+errorMessages_temp+'</div>'
        return mark_safe(rt)
    show_result.short_description = u'&nbsp;&nbsp;刊登结果&nbsp;&nbsp;'

    def edit_data(self,obj):
        project_url = self.request.get_full_path()
        rt = u'不可编辑'
        if '_p_status=FAILED' in project_url:
            id = obj.id
            aa = self.request
            bb = str(aa).split('/')
            status = bb[len(bb) - 1].replace("'>",'')
            shopname = obj.ShopSets
            condition = ''
            siteSearch = ''
            if shopname:
                site = shopname.split('-')[-1].split('/')[0]
                ShopName = shopname.split('-')[0] + '-' + shopname.split('-')[1]
                siteSearch = 'ShopName=' + ShopName + '&searchSite=' + site
            if status:
                condition += status
                if shopname:
                    condition += '&' + siteSearch
            else:
                condition += '?' + siteSearch
            rt = '<a href="/Project/admin/skuapp/t_templet_amazon_wait_upload/%s/update/%s">%s</a>'%(id,condition,u'编辑')
        return mark_safe(rt)
    edit_data.short_description = u'&nbsp;&nbsp;操作&nbsp;&nbsp;'

    def show_variation_info(self,obj):
        project_url = self.request.get_full_path()
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
                rt += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%(t_templet_amazon_published_variation_obj.variation_theme,
                       variation_value,t_templet_amazon_published_variation_obj.child_sku,
                        t_templet_amazon_published_variation_obj.item_quantity,)
            if '_p_status=FAILED' in project_url:
                rt += '<tr><td><a id="link_id_%s">%s</a></td></tr>'%(obj.id,u'编辑变体')
                rt += "</table><script>$('#link_id_%s').on('click',function(){" \
                      "layer.open({type:2,skin:'layui-layer-lan',title:'编辑变体',fix:false,shadeClose: true," \
                      "maxmin:true,area:['1500px','500px'],content:'/t_templet_amazon_wait_upload/variation/?prodcut_variation_id=%s&productSKU=%s'," \
                      "btn: ['关闭页面'],end:function (){location.reload();}});});" \
                      "</script>"%(obj.id,obj.prodcut_variation_id,obj.productSKU)
            elif len(t_templet_amazon_published_variation_objs) > 4:
                rt += '<tr><td><a id="more_id_%s">更多</a></td></tr></table>' % obj.id
                rt = u"%s<script>$('#more_id_%s').on('click',function()" \
                     u"{layer.open({type:2,skin:'layui-layer-lan',title:'全部变体信息'," \
                     u"fix:false,shadeClose: true,maxmin:true,area:['800px','400px'],btn: ['关闭页面']," \
                     u"content:'/t_templet_amazon_upload/?pvi=%s',});" \
                     u"});</script>" % (rt, obj.id, obj.prodcut_variation_id)
            else:
                rt += '</table>'
            # rt += "</table>"
        else:
            if '_p_status=FAILED' in project_url:
                rt = "<a id='link_id_%s'>%s</a><script>$('#link_id_%s').on('click',function(){" \
                      "layer.open({type:2,skin:'layui-layer-lan',title:'添加变体',fix:false,shadeClose: true," \
                      "maxmin:true,area:['1500px','500px'],content:'/t_templet_amazon_wait_upload/variation/?prodcut_variation_id=%s&productSKU=%s'," \
                      "btn: ['关闭页面'],end:function (){location.reload();}});});" \
                      "</script>"%(obj.id,u'添加变体',obj.id,obj.prodcut_variation_id,obj.productSKU)
            else:
                rt = u'单体'
        return mark_safe(rt)

    show_variation_info.short_description =  mark_safe(u'<p style="color:#428BCA" align="center">单体/变体</p>')

    list_display = ('show_image', 'show_product_sku', 'item_name', 'show_variation_info', 'show_schedule', 'show_info', 'edit_data')

    list_display_links = ('id')

    list_editable = ('external_product_id',)

    actions = ['amazon_distribution', 'to_recycle']

    fields = ('item_name', 'external_product_id_type', 'condition_type', 'toy_color', 'jewerly_color', 'material_type',
              'quantity', 'product_description', 'bullet_point1', 'bullet_point2', 'metal_type', 'item_shape', 'homes_size',
              'bullet_point3', 'bullet_point4', 'bullet_point5', 'standard_price', 'sale_price', 'sale_from_date',
              'sale_end_date', 'fulfillment_latency', 'manufacturer', 'brand_name', 'homes_color',
              'generic_keywords1', 'generic_keywords2', 'generic_keywords3', 'generic_keywords4', 'generic_keywords5',
              'product_subtype', 'unit_count', 'unit_count_type', 'mfg_minimum','clothing_size', 'clothing_color',
              'mfg_minimum_unit_of_measure', 'productSKU', 'item_package_quantity', 'item_type', 'warranty_description',
              'department_name1', 'department_name2', 'department_name3', 'department_name4', 'department_name5',
              'target_audience_keywords1', 'target_audience_keywords2', 'target_audience_keywords3',
              )

    form_layout = (
        Fieldset(u'产品主要信息',
                 Row('item_name', 'productSKU', 'external_product_id_type', ),
                 Row('quantity', 'item_package_quantity', 'condition_type', ),  # 'feed_product_type',
                 Row('item_type', 'product_subtype'),  # 'department_name'
                 Row('manufacturer', 'brand_name',),
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
                 Row('mfg_minimum', 'mfg_minimum_unit_of_measure', 'item_shape' ),
                 Row('unit_count', 'unit_count_type', 'metal_type', 'jewerly_color', 'material_type',),
                 Row('clothing_size', 'clothing_color', 'fulfillment_latency', ),
                 Row('toy_color', 'homes_color', 'homes_size'),
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

    # def conn_shopSKU(self, productSKU, skuResult, count):
    #     all_pro_SKU_list = productSKU.split('and')
    #     pro_SKU_dict = {}
    #     if len(all_pro_SKU_list) == 1:
    #         new_pro_SKU_list = productSKU.split('*')
    #         if len(new_pro_SKU_list) == 1:
    #             pro_SKU_dict[productSKU] = '1'
    #         else:
    #             pro_SKU_dict[new_pro_SKU_list[0]] = new_pro_SKU_list[1]
    #     else:
    #         for each_pro_SKU in all_pro_SKU_list:
    #             each_pro_SKU_list = each_pro_SKU.split('*')
    #             if len(each_pro_SKU_list) == 1:
    #                 pro_SKU_dict[each_pro_SKU] = '1'
    #             else:
    #                 pro_SKU_dict[each_pro_SKU_list[0]] = each_pro_SKU_list[1]
    #     item_sku = ''
    #     item_sku_list = []
    #     for key,value in pro_SKU_dict.items():
    #         item_sku_dict = {}
    #         if value == '1':
    #             item_sku += skuResult['result'][0] + str(skuResult['result'][1] - count) + '+'
    #         else:
    #             item_sku += skuResult['result'][0] + str(skuResult['result'][1] - count) + '*' + str(value) + '+'
    #         item_sku_dict[key] = skuResult['result'][0] + str(skuResult['result'][1] - count)
    #         item_sku_list.append(item_sku_dict)
    #         count = count + 1
    #     return item_sku[:-1],count,item_sku_list

    def conn_shop_sku(self, request, product_sku, sku_result, count):
        item_sku = ''
        if product_sku.find('and') == -1:  # 非组合sku
            # sku个数情况，单个省略*1，多个根据实际情况加 *cnt
            product_sku_and_count_list = product_sku.split('*')
            if len(product_sku_and_count_list) == 1:
                product_sku_local = product_sku
                item_sku += sku_result['result'][0] + str(sku_result['result'][1] - count)
            else:
                product_sku_local = product_sku_and_count_list[0]
                item_sku += sku_result['result'][0] + str(sku_result['result'][1] - count) + '*' + product_sku_and_count_list[1]
        else:  # 组合sku
            # sku_sort = '+'.join(sorted(set([sku for sku in product_sku.split('and') if sku.strip()])))
            sku_sort = product_sku.replace('and', '+')
            zh_sku_dict = G_ZHSKU(sku_sort, connection, request.user.first_name, request.user.username, datetime.now())
            if zh_sku_dict['code'] == 1:
                messages.error(request, u'组合SKU申请错误，请稍后再试')
                return
            product_sku_local = zh_sku_dict['ZHSKU']
            item_sku = sku_result['result'][0] + str(sku_result['result'][1] - count)
        # 返回商品sku（合集商品用组合sku）与店铺sku对应关系，用于sku绑定
        item_sku_list = list()
        item_sku_dict = dict()
        item_sku_dict[product_sku_local] = item_sku.split('*')[0]  # 绑定时只绑定sku，不包含个数信息（如local_sku*10 <-> shop_sku*10 绑定时为 local_sku <-> shop_sku)
        item_sku_list.append(item_sku_dict)
        count += 1
        return item_sku, count, item_sku_list

    def conn_shop_sku_new(self, request, ShopSets,  product_sku, sku_type):
        shop_sku = ''
        error_info = ''
        product_sku_local = ''
        if product_sku.find('and') == -1:  # 非组合sku
            # sku个数情况，单个省略*1，多个根据实际情况加 *cnt
            product_sku_and_count_list = product_sku.split('*')
            if len(product_sku_and_count_list) == 1:
                product_sku_local = product_sku
                # 如果直接填写了组合SKU，则改变组合类型
                if product_sku_local.startswith('ZH') and len(product_sku_local) == 6:
                    sku_type = 'GROUPSKUAPPLY'
                shop_sku_dict = shopsku_apply(product_sku_local, ShopSets, sku_type, request.user.first_name)
                # messages.success(request, 'shop_sku_dict1 is: %s' % str(shop_sku_dict))
                if shop_sku_dict['error_info']:
                    error_info = shop_sku_dict['error_info']
                else:
                    for k, val in shop_sku_dict['defeat_sku'].items():
                        if k == product_sku_local:
                            error_info = val

                if shop_sku_dict['result'] == 'SUCCESS':
                    for k, val in shop_sku_dict['success_sku'].items():
                        if val == product_sku_local:
                            shop_sku = k
            else:
                product_sku_local = product_sku_and_count_list[0]
                # 如果直接填写了组合SKU，则改变组合类型
                if product_sku_local.startswith('ZH') and len(product_sku_local) == 6:
                    sku_type = 'GROUPSKUAPPLY'
                shop_sku_dict = shopsku_apply(product_sku_local, ShopSets, sku_type, request.user.first_name)
                # messages.success(request, 'shop_sku_dict2 is: %s' % str(shop_sku_dict))
                if shop_sku_dict['error_info']:
                    error_info = shop_sku_dict['error_info']
                else:
                    for k, val in shop_sku_dict['defeat_sku'].items():
                        if k == product_sku_local:
                            error_info = val

                if shop_sku_dict['result'] == 'SUCCESS':
                    for k, val in shop_sku_dict['success_sku'].items():
                        if val == product_sku_local:
                            shop_sku = k + '*' + product_sku_and_count_list[1]
        else:  # 组合sku
            # sku_sort = '+'.join(sorted(set([sku for sku in product_sku.split('and') if sku.strip()])))
            sku_sort = product_sku.replace('and', '+')
            zh_sku_dict = G_ZHSKU(sku_sort, connection, request.user.first_name, request.user.username, datetime.now())
            if zh_sku_dict['code'] == 1:
                messages.error(request, u'组合SKU申请错误，请稍后再试')
                return
            product_sku_local = zh_sku_dict['ZHSKU']

            zh_sku_dict = shopsku_apply(product_sku_local, ShopSets, 'GROUPSKUAPPLY', request.user.first_name)

            if zh_sku_dict['error_info']:
                error_info = zh_sku_dict['error_info']
            else:
                for k, val in zh_sku_dict['defeat_sku'].items():
                    if k == product_sku_local:
                        error_info = val

            # messages.success(request, 'zh_sku_dict3 is: %s' % str(zh_sku_dict))
            # messages.success(request, 'zh_sku_dict3  product_sku_local is: %s' % product_sku_local)
            if zh_sku_dict['result'] == 'SUCCESS':
                for k, val in zh_sku_dict['success_sku'].items():
                    if val == product_sku_local:
                        shop_sku = k

        # 返回商品sku（合集商品用组合sku）与店铺sku对应关系，用于sku绑定
        item_sku_list = list()
        item_sku_dict = dict()
        if shop_sku:
            item_sku_dict[product_sku_local] = shop_sku.split('*')[0]  # 绑定时只绑定sku，不包含个数信息（如local_sku*10 <-> shop_sku*10 绑定时为 local_sku <-> shop_sku)
            item_sku_list.append(item_sku_dict)
        # messages.success(request, 'shop_sku is: %s' % shop_sku)
        # messages.success(request, 'item_sku_list is: %s' % str(item_sku_list))
        return shop_sku,item_sku_list, error_info, product_sku_local


    def amazon_distribution(self, request, queryset):
        project_url = self.request.get_full_path()
        """去刊登"""
        for obj in queryset:
            shops = obj.ShopSets
            if (obj.status == 'YES') or (obj.status == 'OPEN'):
                messages.error(request, u'刊登ID：%s已刊登或正在刊登' % obj.id)
                continue
            elif shops == None:
                messages.error(request, u'请确认刊登店铺不为空再刊登！')
                continue
            elif obj.can_upload == '-1':
                messages.error(request, u'ID是%s数据未完善，请完善数据后再执行该操作！' % obj.id)
                continue
            elif obj.can_upload == '2':
                messages.error(request, u'产品：%s 已执行过刊登，请耐心等待不要重复执行刊登操作' % obj.productSKU)
                continue
            else:
                #刊登失败的重新刊登时重新分配UPC
                if '_p_status=FAILED' in project_url:
                    upc_count = 1
                    t_templet_amazon_published_variation_objs = t_templet_amazon_published_variation.objects.filter(
                        prodcut_variation_id=obj.prodcut_variation_id)
                    if t_templet_amazon_published_variation_objs.exists():
                        upc_count = len(t_templet_amazon_published_variation_objs)
                    t_product_upc_id_amazon_obj = t_product_upc_id_amazon(connection)
                    upc_id_list = []
                    for i in range(0, upc_count):
                        upc_id = t_product_upc_id_amazon_obj.update_product_id({'id_type': obj.external_product_id_type})
                        if upc_id is None or upc_id==0:
                            messages.error(request,u'UPC不够，请联系相关管理员')
                            return
                        upc = t_product_upc_id_amazon_obj.get_newest_product_id({'id': upc_id})
                        upc = upc['external_product_id']
                        if validation_UPC(upc) == 1:
                            i = i - 1
                        upc_id_list.append(upc)
                    if upc_count == 1:
                        obj.external_product_id = upc_id_list[0]
                        obj.save()
                    else:
                        for i in range(0,upc_count):
                            t_templet_amazon_published_variation_objs[i].external_product_id = upc_id_list[i]
                            t_templet_amazon_published_variation_objs[i].save()
                #查询待刊登店铺的授权信息
                t_config_online_amazon_obj = t_config_online_amazon(connection)
                auth_info = t_config_online_amazon_obj.getauthByShopName(obj.ShopSets)
                if auth_info:
                    t_config_mq_info_objs = t_config_mq_info.objects.filter(Name='Amazon-RabbitMQ-Server',PlatformName='Amazon')
                    if t_config_mq_info_objs:
                        MQ_dict = {}
                        MQ_dict['IP'] = t_config_mq_info_objs[0].IP
                        for t_config_mq_info_obj in t_config_mq_info_objs:
                            MQ_dict[t_config_mq_info_obj.K] = t_config_mq_info_obj.V
                        t_templet_amazon_published_variation_objs = t_templet_amazon_published_variation.objects.filter(
                            parent_item_sku=obj.productSKU,prodcut_variation_id=obj.prodcut_variation_id)
                        paramsMQ = {'obj_id': obj.id, 'auth_info': auth_info, 'user': request.user.first_name,
                                    'MQ_dict': MQ_dict}

                        # # 生成店铺SKU
                        # # 需生成的店铺sku个数：1个主sku + 变体sku个数
                        # sku_count = 1 + len(t_templet_amazon_published_variation_objs)
                        # sku_result = generate_code_func(connection, obj.ShopSets, sku_count)
                        # if sku_result['Code'] == 0:
                        #     link_sku_list = []
                        #     # 主体情况
                        #     item_sku, count, item_sku_list = self.conn_shop_sku(request, obj.productSKU, sku_result, 0)
                        #     link_sku_list.extend(item_sku_list)
                        #     obj.item_sku = item_sku
                        #     obj.part_number = item_sku
                        #     obj.save()
                        #     # 变体情况
                        #     if t_templet_amazon_published_variation_objs:
                        #         paramsMQ['variation'] = 1
                        #         for variation_obj in t_templet_amazon_published_variation_objs:
                        #             item_sku, count, item_sku_list = self.conn_shop_sku(request, variation_obj.productSKU, sku_result, count)
                        #             link_sku_list.extend(item_sku_list)
                        #             variation_obj.parent_sku = obj.item_sku
                        #             variation_obj.child_sku = item_sku
                        #             variation_obj.save()
                        #     else:
                        #         paramsMQ['variation'] = 0

                        # 生成店铺SKU
                        link_sku_list = list()
                        sku_count = 1 + len(t_templet_amazon_published_variation_objs)
                        if t_templet_amazon_published_variation_objs: # 有变体
                            paramsMQ['variation'] = 1
                            # 主体sku在b_goods表里无记录，直接用主体sku申请店铺sku会报错，用第一个变体的sku代替主sku申请店铺sku
                            # 注：申请店铺sku接口对相同输入会给出不同的输出，即同店铺同商品sku多次申请店铺sku会返回多个不同店铺sku
                            variation_one = t_templet_amazon_published_variation_objs[0]
                            item_sku_main, item_sku_list, error_info,product_sku_local = self.conn_shop_sku_new(request, obj.ShopSets, variation_one.productSKU, 'SONSKUAPPLY')
                            # 申请完后，绑定时绑定主体sku，即把 variation_one - shop_sku 替换为 main_sku - shop_sku
                            # 可能是组合sku，从函数直接返回 product_sku_local
                            if item_sku_main:
                                # messages.success(request, 'item_sku_list before is: %s' % str(item_sku_list))
                                item_sku_list[0][obj.productSKU] = item_sku_list[0].pop(product_sku_local)
                                # messages.success(request, 'item_sku_list after is: %s' % str(item_sku_list))
                                link_sku_list.extend(item_sku_list)
                                obj.item_sku = item_sku_main
                                obj.part_number = item_sku_main
                                obj.save()
                            else:
                                messages.error(request, '申请主体SKU失败: %s' % error_info )
                                return

                            for variation_obj in t_templet_amazon_published_variation_objs:
                                item_sku, item_sku_list, error_info,product_sku_local = self.conn_shop_sku_new(request, obj.ShopSets, variation_obj.productSKU, 'SONSKUAPPLY',)
                                if item_sku:
                                    link_sku_list.extend(item_sku_list)
                                    variation_obj.parent_sku = obj.item_sku
                                    variation_obj.child_sku = item_sku
                                    variation_obj.save()
                                else:
                                    messages.error(request, '申请变体SKU失败: %s' % error_info)
                                    return
                        else:
                            paramsMQ['variation'] = 0
                            item_sku_main, item_sku_list, error_info,product_sku_local = self.conn_shop_sku_new(request, obj.ShopSets, obj.productSKU, 'SONSKUAPPLY')
                            if item_sku_main:
                                link_sku_list.extend(item_sku_list)
                                obj.item_sku = item_sku_main
                                obj.part_number = item_sku_main
                                obj.save()
                            else:
                                messages.error(request, '申请SKU失败: %s' % error_info)
                                return
                        # messages.success(request, 'link_sku_list  is: %s' % str(link_sku_list))
                        paramsMQ['link_sku_list'] = link_sku_list
                        # paramsMQ['skuCount'] = skuCount
                        paramsMQ['skuCount'] = sku_count
                        t_templet_amazon_upload_result_obj = t_templet_amazon_upload_result()
                        t_templet_amazon_upload_result_obj.__dict__ = obj.__dict__
                        t_templet_amazon_upload_result_obj.resultInfo = ''
                        t_templet_amazon_upload_result_obj.mqResponseInfo = ''
                        t_templet_amazon_upload_result_obj.errorMessages = ''
                        t_templet_amazon_upload_result_obj.save()
                        paramsMQ['templet_amazon_upload_result_id'] = t_templet_amazon_upload_result_obj.id
                        paramsMQ['shops'] = shops
                        obj.can_upload = '2'
                        obj.save()
                        stitch_goods_info.delay(paramsMQ)

                    else:
                        messages.error(request, '刊登店铺：%s该店铺未布置终端！！'% shops)
                else:
                    messages.error(request, '刊登店铺：%s该店铺无授权信息/该店铺不存在！！'% shops)
        return HttpResponseRedirect(
            request.META.get('HTTP_REFERER', '/').replace('t_templet_amazon_wait_upload/?_p_status=NO',
                                't_templet_amazon_upload_result/?_p_status=UPLOAD').replace('t_templet_amazon_wait_upload/?_p_status=FAILED',
                                't_templet_amazon_upload_result/?_p_status=UPLOAD'))


    amazon_distribution.short_description = u'执行刊登'

    def to_recycle(self, request, queryset):
        time = datetime.now()
        user = request.user.username
        for obj in queryset:
            t_templet_amazon_collection_box.objects.filter(prodcut_variation_id=obj.prodcut_variation_id,
                                                           productSKU=obj.productSKU, createUser=obj.createUser) \
                .update(status='1', updateUser=user, updateTime=time,can_upload='0')
            obj.status = '0'
            obj.save()
    to_recycle.short_description = u'还原到草稿箱'

    def getTortInfo(self, productSku):
        classsku_obj = classsku(connection)
        mainSKU = classsku_obj.get_bemainsku_by_sku(productSku)
        classmainsku_obj = classmainsku(connection)
        tortInfo = classmainsku_obj.get_tort_by_mainsku(mainSKU)
        return tortInfo

    def rediect_url(self, new_url):
        if new_url:
            new_urls = new_url.split('/')
            test_url = ''
            for i in range(0, len(new_urls)):
                if i == (len(new_urls) - 2) or i == (len(new_urls) - 3):
                    pass
                else:
                    n_url = new_urls[i]
                    status_lists = ['_p_status=NO', '_p_status=FAILED']
                    for status_list in status_lists:
                        if status_list in n_url:
                            n_urls = n_url.split('&')
                            for nn_url in n_urls:
                                if status_list in nn_url:
                                    if status_list == nn_url:
                                        n_url = '?' + nn_url
                                    else:
                                        n_url = nn_url
                    test_url += n_url + '/'
            new_url = test_url[:-1]
        else:
            new_url = '/Project/admin/skuapp/t_templet_amazon_wait_upload/'
        return new_url

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
        # product_relationship_type_list = ['Clothing, Shoes & Jewelry','Tools & Home Improvement','Sports & Outdoors','Pet Supplies',
        #                                   'Patio, Lawn & Garden','Office Products','Home & Kitchen','Health & Household','Beauty & Personal Care',
        #                                   'Baby','Automotive']
        if variation_theme:
            variationCount = len(size_name)
            if color_name:
                variationCount = len(color_name)
            for i in range(0, variationCount):
                tortInfo = self.getTortInfo(productSKU[i])
                if tortInfo == 'AMZ':
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
        import urllib,time
        obj = self.new_obj
        request = self.request
        post = request.POST
        searchSite = request.GET.get('searchSite','')
        ShopName = request.GET.get('ShopName', '')
        ShopSets = post.get('ShopSets', '').encode("utf-8")
        upload_product_type = post.get('upload_product_type', '')
        shopAlias = t_config_shop_alias.objects.filter(ShopName=ShopSets)[0].ShopAlias
        obj.ShopSets = ShopSets
        obj.brand_name = shopAlias
        obj.manufacturer = shopAlias
        update_sites = {'US': 'Update', 'DE': 'Aktualisierung', 'FR': 'Actualisation', 'UK': 'Update', 'AU': 'Update', 'IN': 'Update'}
        shipping_group_sites = {'US': 'Migrated Template', 'DE': 'Standardvorlage Amazon', 'FR': 'Modèle par défaut Amazon', 'UK': 'Migrated Template',
                                'AU': 'Migrated Template', 'IN': 'Migrated Template'}
        feed_product_type = request.POST.get('feed_product_type', '')
        recommended_browse_nodes = urllib.unquote(request.GET.get('recommended_browse_nodes','')).replace('RBNAND', '&')
        RootID = request.GET.get('RootID', '')
        prodcut_variation_id = int(time.time() * 1000)
        all_image_list = {'other_image_url1': '', 'other_image_url2': '',
                                'other_image_url3': '', 'other_image_url4': '',
                                'other_image_url5': '', 'other_image_url6': '',
                                'other_image_url7': '', 'other_image_url8': '', 'main_image_url': ''}
        main_images = request.POST.get('main_images', '')
        productSKUlist = [obj.productSKU,]
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
            if tortInfo == 'AMZ':
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
                insert_result = self.save_product_variation(request,obj, prodcut_variation_id)
                if insert_result == 0:
                    #Migrated Template
                    obj.merchant_shipping_group_name = shipping_group_sites[searchSite]
                    obj.update_delete = update_sites[searchSite]
                    obj.item_name = obj.manufacturer + ' ' + obj.item_name
                    obj.upload_product_type = upload_product_type
                    obj.feed_product_type = feed_product_type
                    obj.recommended_browse_nodes_id = RootID
                    obj.createUser = request.user.username
                    obj.part_number = obj.productSKU
                    obj.createTime = datetime.now()
                    obj.status = 'NO'
                    obj.save()
                else:
                    messages.error(request, '该商品存在侵权记录！！！')
                post['_redirect'] = "/Project/admin/skuapp/t_templet_amazon_wait_upload/?_p_status=NO"
            else:
                new_url = self.rediect_url(request.POST.get('sourceURLs', ''))
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
                old_obj.item_name = obj.item_name
                old_obj.toy_color = obj.toy_color
                old_obj.item_type = obj.item_type
                old_obj.manufacturer = obj.manufacturer
                old_obj.upload_product_type = upload_product_type
                old_obj.feed_product_type = feed_product_type
                old_obj.product_subtype = obj.product_subtype
                old_obj.product_description = obj.product_description
                old_obj.brand_name = obj.brand_name
                old_obj.update_delete = obj.update_delete
                old_obj.item_package_quantity = obj.item_package_quantity
                old_obj.standard_price = obj.standard_price
                old_obj.sale_price = obj.sale_price
                old_obj.sale_from_date = obj.sale_from_date
                old_obj.sale_end_date = obj.sale_end_date
                old_obj.condition_type = obj.condition_type
                old_obj.quantity = obj.quantity
                old_obj.merchant_shipping_group_name = obj.merchant_shipping_group_name
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
                old_obj.ShopSets = ShopSets
                old_obj.updateUser = request.user.username
                old_obj.updateTime = datetime.now()
                if validation_amazon_product_data(obj) == 1:
                    old_obj.can_upload = '0'
                else:
                    old_obj.can_upload = '-1'
                old_obj.save()
                post['_redirect'] = new_url
            post['_addanother_ywp'] = '/Project/admin/skuapp/t_templet_amazon_wait_upload/add/?' \
                                      'ShopName=' + ShopName + '&searchSite=' + searchSite
        else:
            messages.error(request, '该商品存在Amazon侵权记录！！！')

    def get_list_queryset(self,):
        """显示可显示的，自己本人的"""
        request = self.request
        qs = super(t_templet_amazon_wait_upload_Admin, self).get_list_queryset()
        if request.user.is_superuser:
            qs = qs.exclude(status='OPEN')
        else:
            qs = qs.filter(createUser = request.user.username)
        return qs
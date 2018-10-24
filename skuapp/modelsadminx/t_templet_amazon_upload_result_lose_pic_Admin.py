#-*-coding:utf-8-*-


"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_templet_amazon_upload_result_lose_pic_Admin.py
 @time: 2018/4/12 13:59
"""   
from django.utils.safestring import mark_safe
from skuapp.table.t_templet_amazon_published_variation import *
from skuapp.table.t_templet_amazon_upload_result import *
from skuapp.table.t_templet_amazon_collection_box import *
from skuapp.table.t_templet_amazon_wait_upload import t_templet_amazon_wait_upload
from skuapp.table.t_templet_amazon_upload_result_lose_pic import t_templet_amazon_upload_result_lose_pic
from brick.table.t_config_online_amazon import t_config_online_amazon as config_online
from django.db import connection
from django.contrib import messages
from brick.amazon.upload_product.message_to_rabbitmq import MessageToRabbitMq
import json
import datetime


class t_templet_amazon_upload_result_lose_pic_Admin(object):
    # site_left_menu_flag = True
    amazon_site_left_menu_tree_flag = True

    def show_image(self, obj):
        if obj.main_image_url:
            rt = u'<img src="%s" style="width: 100px; height: 100px">&nbsp;&nbsp;' % (obj.main_image_url)
        else:
            main_image_url = ''
            main_image_urls = t_templet_amazon_published_variation.objects.filter(prodcut_variation_id=obj.prodcut_variation_id).values_list('main_image_url')
            if main_image_urls:
                main_image_url = main_image_urls[0][0]
            rt = u'<img src="%s" style="width: 100px; height: 100px">&nbsp;&nbsp;' % (main_image_url)
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
        st = u'<font color="#FF3333">刊登成功，但图片缺失</font>'
        rt = u'创建人:%s<br>创建时间:<br>%s<br>更新人:%s<br>更新时间:<br>%s<br>刊登状态:%s<br>' \
             % (obj.createUser, obj.createTime, obj.updateUser, obj.updateTime, st)
        return mark_safe(rt)
    show_info.short_description = u'&nbsp;&nbsp;&nbsp;采 集 信 息&nbsp;&nbsp;&nbsp;'

    def show_schedule(self, obj):
        """展示刊登店铺"""
        if obj.ShopSets == '' or obj.ShopSets is None:
            shops = ''
            num = 0
        else:
            shopList = obj.ShopSets.split(',')
            num = len(shopList)
            shops = ''
            for i in range(num):
                if (i + 1) % 10 == 0:
                    shops = shops + shopList[i] + '<br>'
                else:
                    shops = shops + shopList[i] + ','
        rt = '目标店铺：%s<br>' % ( shops)
        return mark_safe(rt)
    show_schedule.short_description = u'&nbsp;&nbsp;刊登计划&nbsp;&nbsp;'

    def show_result(self, obj):
        rt = ''
        error_info = {'The SKU data provided is different from': u'UPC重复', 'Message/Product/DescriptionData/MerchantShippingGroupName': u'店铺运输方式名错误',
                      'Missing Attributes ': u'缺少字段', 'Can not get images for product_sku:': u'获取图片失败',
                      'You are not authorized to list products in this category': u'无权限刊登此类商品', 'ItemPackageQuantity': u'商品数量不能为空',
                      'RecommendedBrowseNode': u'类目树选择错误', 'MinimumManufacturerAgeRecommended': u'最小使用年龄不能为空',
                      'The content of elements must consist of well-formed character data or markup': u'商品种类不能为空',
                      'We could not access the media at URL http://': u'商品刊登成功，但图片缺失，缺失图片的店铺SKU：'}
        # rt = obj.resultInfo
        if obj.errorMessages:
            errorMessages_temp = u'未知错误'
            for error_message in error_info:
                if error_message in obj.errorMessages:
                    errorMessages_temp = error_info[error_message]
            if errorMessages_temp == u'缺少字段':
                need_param_list = obj.errorMessages.split('Missing Attributes ')
                need_params = ''
                for i in range(1, len(need_param_list)):
                    need_params += '<br/>' + need_param_list[i].split('. SKU')[0]
                errorMessages_temp += need_params
            if errorMessages_temp == u'商品刊登成功，但图片缺失，缺失图片的店铺SKU：':
                need_params = ''
                if '{"SKU": {"value": "' in obj.errorMessages:
                    need_params_temps = obj.errorMessages.split('{"SKU": {"value": "')
                    for i in range(1,len(need_params_temps)):
                        if '"},' in need_params_temps[i]:
                            need_params += '<br/>' + need_params_temps[i].split('"},')[0]
                errorMessages_temp += need_params
            rt += '<div style="width: 100%; height: auto; word-wrap:break-word; word-break:break-all; overflow: hidden;  ">'+errorMessages_temp+'</div>'
        return mark_safe(rt)
    show_result.short_description = u'&nbsp;&nbsp;刊登结果&nbsp;&nbsp;'

    def show_variation_info(self,obj):
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
            if len(t_templet_amazon_published_variation_objs) > 4:
                rt += '<tr><td><a id="more_id_%s">更多</a></td></tr></table>' % obj.id
                rt = u"%s<script>$('#more_id_%s').on('click',function()" \
                     u"{layer.open({type:2,skin:'layui-layer-lan',title:'全部变体信息'," \
                     u"fix:false,shadeClose: true,maxmin:true,area:['800px','400px'],btn: ['关闭页面']," \
                     u"content:'/t_templet_amazon_upload/?pvi=%s',});" \
                     u"});</script>" % (rt, obj.id, obj.prodcut_variation_id)
            else:
                rt += '</table>'
        else:
            rt = u"单体"
        return mark_safe(rt)

    show_variation_info.short_description =  mark_safe(u'<p style="color:#428BCA" align="center">单体/变体</p>')

    def show_operate_info(self, obj):
        rt = ''
        if obj.is_display == 2:
            rt =u'正在补传图片'
        elif obj.is_display == 3:
            rt = u'补传时获取图片失败'
        elif obj.is_display == 4:
            rt = u'补传图片后台处理失败'
        return mark_safe(rt)
    show_operate_info.short_description = u'处理状态'


    list_display = ('show_image', 'item_sku',  'show_product_sku', 'item_name', 'show_variation_info', 'show_schedule', 'show_info', 'show_result', 'show_operate_info')

    list_display_links = ('id')

    actions = ['reupload_image', 'to_success']

    def reupload_image(self, request, queryset):
        for obj in queryset:
            if obj.is_display == 2:
                messages.error(request, u'店铺sku：%s 已在补传图片，请不要重复提交' % obj.item_sku)
                continue

            t_templet_amazon_upload_result_lose_pic.objects.filter(id=obj.id).update(is_display='2')
            t_config_online_amazon_obj = config_online(connection)
            auth_info = t_config_online_amazon_obj.getauthByShopName(obj.ShopSets)
            wait_upload_obj = t_templet_amazon_wait_upload.objects.filter(ShopSets=obj.ShopSets, item_sku=obj.item_sku)
            amazon_upload_result_id = None
            if len(wait_upload_obj) != 0:
                amazon_upload_result_id = wait_upload_obj[0].id
            else:
                messages.error(request, u'未找到刊登信息，店铺：%s，店铺sku：%s')
                continue
            auth_info['amazon_upload_id'] = amazon_upload_result_id
            auth_info['lose_pic_id'] = obj.id
            auth_info['operate_type'] = 'reupload_image'
            auth_info['user_name'] = request.user.username

            sku_lose_pic_list = list()
            if '{"SKU": {"value": "' in obj.errorMessages:
                need_params_temps = obj.errorMessages.split('{"SKU": {"value": "')
                for i in range(1, len(need_params_temps)):
                    if '"},' in need_params_temps[i]:
                        sku_lose_pic_list.append(need_params_temps[i].split('"},')[0])
            auth_info['sku_lose_pic_list'] = sku_lose_pic_list
            message_to_rabbit_obj = MessageToRabbitMq(auth_info, connection)
            auth_info = json.dumps(auth_info)
            message_to_rabbit_obj.put_message(auth_info)
    reupload_image.short_description = u'图片补传'

    def to_success(self,request, queryset):
        for obj in queryset:
            t_templet_amazon_upload_result.objects.filter(item_sku=obj.item_sku, ShopSets=obj.ShopSets).update(status='SUCCESS', updateUser=request.user.username, updateTime=datetime.datetime.now())
            t_templet_amazon_upload_result_lose_pic.objects.filter(id=obj.id).update(is_display='0', updateUser=request.user.username, updateTime=datetime.datetime.now())
    to_success.short_description = u'转到发布成功'

    def get_list_queryset(self,):
        """显示可显示的，自己本人的"""
        request = self.request
        qs = super(t_templet_amazon_upload_result_lose_pic_Admin, self).get_list_queryset()
        if request.user.is_superuser:
            qs = qs.exclude(is_display='0')
        else:
            qs = qs.filter(createUser=request.user.username).exclude(is_display='0')
        return qs
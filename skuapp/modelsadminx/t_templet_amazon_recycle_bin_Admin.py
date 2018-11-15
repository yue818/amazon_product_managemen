# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_templet_amazon_recycle_bin_Admin.py
 @time: 2018-04-11 14:01
"""  
#-*-coding:utf-8-*-
from django.utils.safestring import mark_safe
from skuapp.table.t_templet_amazon_published_variation import *
from skuapp.table.t_templet_amazon_collection_box import *


class t_templet_amazon_recycle_bin_Admin(object):

    # site_left_menu_flag = True
    amazon_site_left_menu_tree_flag = True

    def show_image(self, obj):
        if obj.main_image_url:
            rt = u'<img src="%s" style="width: 100px; height: 100px">&nbsp;&nbsp;' % (obj.main_image_url)
        else:
            main_image_url = ''
            main_image_urls = t_templet_amazon_published_variation.objects.filter(
                prodcut_variation_id=obj.prodcut_variation_id).values_list('main_image_url')
            if main_image_urls:
                main_image_url = main_image_urls[0][0]
            rt = u'<img src="%s" style="width: 100px; height: 100px">&nbsp;&nbsp;' % (main_image_url)
        return mark_safe(rt)

    show_image.short_description = u'主图'

    def show_info(self, obj):
        """展示时间、人员信息"""
        # st = ''
        # if obj.status == 'SUCCESS':
        #     #     st = u'<font color="#FFCC33">正在处理</font>'
        #     # elif obj.Status == 'YES':
        #     st = u'<font color="#00BB00">刊登成功</font>'
        # elif obj.status == 'FAILED':
        #     st = u'<font color="#66FF66">刊登失敗</font>'
        # else:
        #     st = u'<font color="#FFCC33">正在刊登中</font>'
        rt = u'创建人:%s<br>创建时间:<br>%s<br>更新人:%s<br>更新时间:<br>%s<br>' \
             % (obj.createUser, obj.createTime, obj.updateUser, obj.updateTime)
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

        rt = '目标店铺：%s<br>' % (shops)

        return mark_safe(rt)
    show_schedule.short_description = u'&nbsp;&nbsp;刊登计划&nbsp;&nbsp;'

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


    list_display = ('show_image', 'item_sku', 'item_name', 'show_variation_info', 'show_schedule', 'show_info',)

    list_display_links = ('id')

    actions = ['to_recycle',]

    def to_recycle(self, request, queryset):
        from datetime import datetime
        time = datetime.now()
        user = request.user.username
        for obj in queryset:
            t_templet_amazon_collection_box.objects.filter(prodcut_variation_id=obj.prodcut_variation_id,productSKU=obj.productSKU,createUser=obj.createUser)\
                .update(status='1',updateUser=user,updateTime=time)
            obj.status='0'
            obj.save()

    to_recycle.short_description = u'还原到草稿箱'

    def get_list_queryset(self,):
        """显示可显示的，自己本人的"""
        request = self.request
        qs = super(t_templet_amazon_recycle_bin_Admin, self).get_list_queryset()
        if request.user.is_superuser:
            qs = qs.filter(status='1')
        else:
            qs = qs.filter(createUser = request.user.username,status='1')
        return qs
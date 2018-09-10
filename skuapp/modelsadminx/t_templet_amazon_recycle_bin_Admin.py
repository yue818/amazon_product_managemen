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
        st = ''
        if obj.status == 'SUCCESS':
            #     st = u'<font color="#FFCC33">正在处理</font>'
            # elif obj.Status == 'YES':
            st = u'<font color="#00BB00">刊登成功</font>'
        elif obj.status == 'FAILED':
            st = u'<font color="#66FF66">刊登失敗</font>'
        else:
            st = u'<font color="#FFCC33">正在刊登中</font>'
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

        rt = '<span style="color: #0000FF;font-weight: 600">%d个</span>' % num
        rt = '(%s)目标店铺：%s<br>' % (rt, shops)

        state = obj.status
        if state == 'SUCCESS':
            rt = '%s<br><br><p style="color: #00BB00">%s</p>' % (rt, u'刊登成功')
        elif state == 'FAILED':
            rt = '%s<br><br><p style="color: #66FF66">%s</p>' % (rt, u'刊登失败')
        else:
            rt = '%s<br><br><p style="color: #FFCC33">%s</p>' % (rt, u'正在刊登中')

        return mark_safe(rt)
    show_schedule.short_description = u'&nbsp;&nbsp;刊登计划&nbsp;&nbsp;'

    def show_result(self, obj):
        rt = obj.resultInfo
        if obj.errorMessages:
            rt += ', Reason: '+obj.errorMessages[0:20]
        return mark_safe(rt)
    show_result.short_description = u'&nbsp;&nbsp;刊登结果&nbsp;&nbsp;'


    list_display = ('show_image', 'item_sku', 'item_name', 'show_schedule', 'show_info', 'show_result')

    list_display_links = ('id')
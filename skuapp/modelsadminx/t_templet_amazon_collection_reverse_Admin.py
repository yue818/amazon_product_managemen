# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_templet_amazon_collection_reverse_Admin.py
 @time: 2018-03-08 13:03
"""

from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from skuapp.table.t_templet_amazon_collection_reverse import *
from app_djcelery.tasks import amazon_reverse_collection
from django.utils.safestring import mark_safe
import datetime
from django.contrib import messages
from skuapp.table.t_templet_amazon_wait_upload import *
from django.http import HttpResponseRedirect

class t_templet_amazon_collection_reverse_Admin(object):

    def show_collect_state(self, obj):
        if obj.collect_state == '0':
            rt = '采集中'
        elif obj.collect_state == '1':
            rt = '采集成功'
        elif obj.collect_state == '-1':
            rt = '采集失败'
        else:
            rt = ''
        return mark_safe(rt)
    show_collect_state.short_description = u'采集状态'

    def show_collect_result(self, obj):
        if obj.collect_state == '0':
            rt = ''
        elif obj.collect_state == '1':
            rt = 'success'
        elif obj.collect_state == '-1':
            rt = obj.collect_result
        else:
            rt = ''
        return mark_safe(rt)
    show_collect_result.short_description = u'采集结果'

    def show_image_url(self,obj) :
        url = u'%s' % obj.main_image_url
        rt = '<img src="%s"  width="100" height="100"  alt = "%s"  title="%s"  />' % (url, url, url)
        return mark_safe(rt)
    show_image_url.short_description = u'图片'

    def save_models(self):
        obj = self.new_obj
        request = self.request
        if obj is None or obj.id is None or obj.id <= 0:
            obj.createUser = request.user.username
            obj.createTime = datetime.datetime.now()
            #obj.collect_state = '0'
        obj.save()
        # print 'tiaoshi1----------------------------------------------------------'
        # param = []
        # this_record = []
        # this_record.append(obj.id)
        # this_record.append(obj.dataFromUrl)
        # #this_record.append(request.POST.get('main_image_url'))
        # param.append(this_record)
        # print 'tiaoshi2----------------------------------------------------------'
        # print param
        # print 'tiaoshi3----------------------------------------------------------'
        # obj.collect_state = '0'
        # amazon_reverse_collection(param)
        # print 'tiaoshi4----------------------------------------------------------'
        # obj.save()


    list_display = ('id','dataFromUrl','createUser','createTime', 'item_name','product_description','show_image_url','bullet_point1','bullet_point2','bullet_point3','bullet_point4','bullet_point5','show_collect_state','show_collect_result')
    list_filter = ('id','dataFromUrl','createUser','createTime','item_name','product_description')
    search_fields = ('id','createUser','createTime','dataFromUrl','item_name','product_description','main_image_url', 'bullet_point1','bullet_point2','bullet_point3','bullet_point4','bullet_point5')
    #fields = ('id','dataFromUrl','item_name','product_description','main_image_url','bullet_point1','bullet_point2','bullet_point3','bullet_point4','bullet_point5')
    fields = ('id','dataFromUrl')

    # form_layout = (
    #     Fieldset(u'产品主要信息',
    #              Row('dataFromUrl', 'item_name', 'main_image_url'),
    #              css_class='unsort '
    #              ),
    #     Fieldset(u'商品描述',
    #              Row('bullet_point1', 'bullet_point2', ),
    #              Row('bullet_point3', 'bullet_point4', ),
    #              Row('bullet_point5', ),
    #              Row('product_description', ),
    #              css_class='unsort '
    #              ),
    # )

    actions = ['get_product_info_by_url', 'to_upload_templet']

    def get_product_info_by_url(self, request, queryset):
        print request.user.username
        reverse_info = []
        for record in queryset.all():
            each_info =[]
            collection_reverse_obj = t_templet_amazon_collection_reverse.objects.filter(id=record.id)
            data_id = record.id
            data_url = record.dataFromUrl
            each_info.append(data_id)
            each_info.append(data_url)
            collection_reverse_obj.update(collect_state='0')
            reverse_info.append(each_info)
        amazon_reverse_collection.delay(reverse_info)
    get_product_info_by_url.short_description = u'反向采集'

    def to_upload_templet(self, request, queryset):
        time = datetime.datetime.now()
        user = request.user.username
        for obj in queryset:
            if obj.status == 'YES':
                messages.error(request, u'ID是%s已经提交为公共模板，请勿重复提交！' % obj.id)
            else:
                t_templet_amazon_wait_upload_obj = t_templet_amazon_wait_upload()
                t_templet_amazon_wait_upload_obj.__dict__ = obj.__dict__
                t_templet_amazon_wait_upload_obj.createTime = time
                t_templet_amazon_wait_upload_obj.createUser = user
                t_templet_amazon_wait_upload_obj.updateTime = time
                t_templet_amazon_wait_upload_obj.updateStaff = user
                t_templet_amazon_wait_upload_obj.status = 'NO'
                t_templet_amazon_wait_upload_obj.ShopSets = ''
                t_templet_amazon_wait_upload_obj.save()
                obj.status = '2'
                # obj.Flag = 0
                obj.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/').replace('t_templet_amazon_collection_reverse/',
                                                                                  't_templet_amazon_wait_upload/?_p_status=NO'))
    to_upload_templet.short_description = u'转到刊登'





    def get_list_queryset(self):
            request = self.request
            qs = super(t_templet_amazon_collection_reverse_Admin, self).get_list_queryset()
            qs = qs.exclude(dataFromUrl=None)
            if not request.user.is_superuser:
                qs = qs.filter(createUser=request.user.username)
            return qs
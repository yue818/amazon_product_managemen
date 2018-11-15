# coding=utf-8

from urllib import urlencode
from django.utils.safestring import mark_safe
from datetime import datetime
from django.contrib import messages
from skuapp.table.t_templet_public_joom import t_templet_public_joom
from skuapp.table.t_templet_joom_collection_box import t_templet_joom_collection_box



class t_templet_joom_collection_box_Admin(object):
    search_box_flag = True
    plateform_distribution_navigation = True

    def show_picture(self,obj) :
        """展示主图"""
        from brick.wish.wish_distribution.admin_function import show_picture
        rt = show_picture(obj=obj, plateform='joom')
        return mark_safe(rt)
    show_picture.short_description = u'<span style="color: #428bca">图片</span>'


    def show_variants(self, obj):
        """展示修改变体信息"""
        from brick.wish.wish_distribution.admin_function import show_variants
        rt = show_variants(obj=obj, plateform='joom', page='box')
        return mark_safe(rt)
    show_variants.short_description = mark_safe('<p align="center">变体信息</p>')


    def show_state(self, obj):
        state = obj.Status
        rt = '<br><br><br><font color="#FF3333">未提交</font>'
        if state == 1:
            rt = '<br><br><br><font color="#00BB00">已提交</font>'
        return mark_safe(rt)
    show_state.short_description = u'公共模板<br>提交状态'

    list_display = ('id', 'MainSKU', 'show_picture', 'Title', 'CoreWords', 'Tags', 'show_variants', 'show_state')
    list_editable = ('Title', 'Description', 'Tags', 'CoreWords')
    actions = ['to_public_templet']


    def to_public_templet(self, request, queryset):
        time = datetime.now()
        user = request.user.first_name
        for obj in queryset:
            if obj.Status == 1:
                messages.info(request, u'ID是%s已经提交为公共模板，请勿重复提交！' % obj.id)
            else:
                t_templet_public_joom.objects.create(MainSKU=obj.MainSKU, Title=obj.Title, Description=obj.Description,
                                                     Tags=obj.Tags, MainImage=obj.MainImage, ExtraImages=obj.ExtraImages,
                                                     Variants=obj.Variants, CreateTime=time, CreateStaff=user,
                                                     UpdateTime=time, UpdateStaff=user, SrcProductID=obj.SrcProductID,
                                                     CoreTags=obj.CoreTags, CoreWords=obj.CoreWords,
                                                     B_cost_weight=obj.B_cost_weight, Source=obj.Source, Cate=obj.Cate)
                t_templet_joom_collection_box.objects.filter(id=obj.id).update(Status=1)
    to_public_templet.short_description = u'转为公共模板'


    def get_list_queryset(self):
        qs = super(t_templet_joom_collection_box_Admin, self).get_list_queryset()
        qs = qs.filter(Status=0)
        cate = self.request.GET.get('Cate', '')
        sku = self.request.GET.get('sku', '')
        if cate:
            qs = qs.filter(Cate=cate)
        if sku:
            qs = qs.filter(MainSKU__startswith=sku.upper())
        return qs
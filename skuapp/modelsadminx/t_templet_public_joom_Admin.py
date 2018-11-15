# coding=utf-8


from django.utils.safestring import mark_safe
from skuapp.table.t_templet_joom_wait_upload import *
from datetime import datetime
from django.contrib import messages


class t_templet_public_joom_Admin(object):
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
        rt = show_variants(obj=obj, plateform='joom', page='public')
        return mark_safe(rt)
    show_variants.short_description = mark_safe('<p align="center">变体信息</p>')


    list_display = ('id', 'MainSKU', 'show_picture', 'Title', 'CoreWords', 'Tags', 'show_variants')
    actions = ['to_distridution']


    def to_distridution(self, request, queryset):
        shopname = request.GET.get('shopname', '')
        time = datetime.now()
        user = request.user.first_name
        if shopname == '':
            messages.error(request, '请 先 选 择 去 铺 货 的 店 铺！！！')
        else:
            for obj in queryset:
                t_templet_joom_wait_upload.objects.create(
                            MainSKU=obj.MainSKU, Title=obj.Title,Description=obj.Description, Tags=obj.Tags,
                            MainImage=obj.MainImage, ExtraImages=obj.ExtraImages, Variants=obj.Variants,
                            CreateStaff=user, UpdateTime=time, UpdateStaff=user, Status='NO', CreateTime=time,
                            SrcProductID=obj.SrcProductID, CoreTags=obj.CoreTags, CoreWords=obj.CoreWords,
                            B_cost_weight=obj.B_cost_weight, Source=obj.Source, Used_shopname=shopname, Cate=obj.Cate)

                if obj.Used_shopname == '' or obj.Used_shopname is None:
                    obj.Used_shopname = shopname
                else:
                    obj.Used_shopname += ',%s' % shopname
                obj.save()
    to_distridution.short_description = u'转到待铺货'


    def get_list_queryset(self, ):
        request = self.request
        qs = super(t_templet_public_joom_Admin, self).get_list_queryset()

        shopname = request.GET.get('shopname', '')
        cate = request.GET.get('Cate', '')
        sku = request.GET.get('sku', '')

        if shopname:
            qs = qs.exclude(Used_shopname__contains=shopname)
        if cate:
            qs = qs.filter(Cate=cate)
        if sku:
            qs = qs.filter(MainSKU__startswith=sku.upper())
        return qs

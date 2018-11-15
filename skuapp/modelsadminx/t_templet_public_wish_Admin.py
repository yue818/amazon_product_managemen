# coding=utf-8

from django.utils.safestring import mark_safe
from skuapp.table.t_templet_wish_wait_upload import *
from random import randint
import datetime
from brick.wish.wish_distribution.admin_function import show_picture, show_variants, show_tortInfo, show_id


class t_templet_public_wish_Admin(object):
    search_box_flag = True
    select_checkbox_flag = True
    plateform_distribution_navigation = True

    def show_picture(self, obj):
        """展示主图"""
        rt = show_picture(obj=obj)
        return mark_safe(rt)
    show_picture.short_description = u'<span style="color: #428bca">图片</span>'

    def show_id(self, obj):
        rt = show_id(obj=obj)
        return mark_safe(rt)
    show_id.short_description = u'<span style="color: #428bca">商品来源</span>'

    def show_variants(self, obj):
        """展示修改变体信息"""
        rt = show_variants(obj=obj, plateform='wish', page='public')
        return mark_safe(rt)
    show_variants.short_description = u'<span style="color: #428bca">变体信息</span>'

    def show_info(self, obj):
        """展示时间、人员信息"""
        rt = u'创建人: %s<br>创建时间: %s<br>更新人: %s<br>更新时间: %s' \
             % (obj.CreateStaff, obj.CreateTime, obj.UpdateStaff, obj.UpdateTime)
        return mark_safe(rt)
    show_info.short_description = u'<span style="color: #428bca">------------创建信息------------</span>'

    def show_tortInfo(self, obj):
        rt = show_tortInfo(obj=obj)
        return mark_safe(rt)
    show_tortInfo.short_description = u'<span style="color: #428bca">侵权状态</span>'

    list_display = (
        'id', 'MainSKU', 'show_tortInfo', 'show_picture', 'show_id', 'Title', 'Tags', 'show_variants',
        'UsedNum', 'show_info', 'Remarks'
    )
    list_editable = ('Title', 'Description', 'Tags', 'CoreWords', 'CoreTags')
    list_display_links = ('',)
    list_per_page = 20
    actions = ['to_distridution']

    def to_distridution(self, request, queryset):
        time = datetime.datetime.now()
        format_time = datetime.datetime.strptime(str(time).split('.')[0], '%Y-%m-%d %H:%M:%S')
        user = request.user.first_name
        for obj in queryset:
            plan = {'interval': ''}
            Inval = randint(1, 500)
            plan['start'] = (format_time + datetime.timedelta(minutes=Inval)).strftime("%Y-%m-%d %H:%M:%S")
            t_templet_wish_wait_upload.objects.create(
                MainSKU=obj.MainSKU, Title=obj.Title, Description=obj.Description, Tags=obj.Tags,
                MainImage=obj.MainImage, ExtraImages=obj.ExtraImages, Variants=obj.Variants, TimePlan=plan,
                CreateStaff=user, UpdateTime=time, UpdateStaff=user, Status='NO', CreateTime=time,
                SrcProductID=obj.SrcProductID, PlateForm=obj.PlateForm
            )
            obj.UsedNum += 1
            obj.save()
    to_distridution.short_description = u'转到定时铺货'

    def get_list_queryset(self, ):
        request = self.request
        qs = super(t_templet_public_wish_Admin, self).get_list_queryset()

        main_sku = request.GET.get('main_sku', '')
        productid = request.GET.get('productid', '')
        createname = request.GET.get('createname', '')
        updatename = request.GET.get('updatename', '')
        used_num_start = request.GET.get('num_start', '')
        used_num_end = request.GET.get('num_end', '')
        createtimeStart = request.GET.get('createtimeStart', '')
        createtimeTimeEnd = request.GET.get('createtimeTimeEnd', '')
        refreshTimeStart = request.GET.get('refreshTimeStart', '')
        refreshTimeEnd = request.GET.get('refreshTimeEnd', '')
        if main_sku:
            main_sku = main_sku.split(',')

        searchList = {
            'MainSKU__in': main_sku,  'SrcProductID__exact': productid, 'CreateStaff__exact': createname,
            'UpdateStaff__exact': updatename, 'CreateTime__gte': createtimeStart, 'CreateTime__lt': createtimeTimeEnd,
            'UpdateTime__gte': refreshTimeStart, 'UpdateTime__lt': refreshTimeEnd,
            'UsedNum__gte': used_num_start, 'UsedNum__lt': used_num_end,
        }
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    if k == 'ShopName__exact':
                        if v.find('Wish-') == -1:
                            v = 'Wish-' + v.zfill(4)
                    sl[k] = v
        if sl:
            qs = qs.filter(**sl)

        return qs

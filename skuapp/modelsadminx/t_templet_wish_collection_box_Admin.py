# coding=utf-8

from django.utils.safestring import mark_safe
from django.contrib import messages
from datetime import datetime
from skuapp.table.t_templet_public_wish_review import t_templet_public_wish_review as wish_review
from brick.wish.wish_distribution.admin_function import show_picture, show_variants, show_tortInfo, show_id


class t_templet_wish_collection_box_Admin(object):
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
        rt = show_variants(obj=obj, plateform='wish', page='box')
        return mark_safe(rt)
    show_variants.short_description = u'<span style="color: #428bca">变体信息</span>'

    def show_info(self, obj):
        """展示时间、人员信息"""
        rt = u'创建人: %s<br>创建时间: %s<br>更新人: %s<br>更新时间: %s' \
             % (obj.CreateStaff, obj.CreateTime, obj.UpdateStaff, obj.UpdateTime)
        return mark_safe(rt)
    show_info.short_description = u'<span style="color: #428bca">------------采集信息------------</span>'

    def show_state(self, obj):
        state = obj.Status
        rt = u'<div class="box" style="width:80px;height:30px;background-color:#FF3333;text-align:center;' \
             u'line-height:30px;border-radius:4px">未提交</div>'
        if state == 1:
            rt = u'<div class="box" style="width:80px;height:30px;background-color:#66FF66;text-align:center;' \
                 u'line-height:30px;border-radius:4px">已提交</div>'
        return mark_safe(rt)
    show_state.short_description = u'<span style="color: #428bca">模板审核<br>提交状态</span>'

    def show_tortInfo(self, obj):
        rt = show_tortInfo(obj=obj)
        return mark_safe(rt)
    show_tortInfo.short_description = u'<span style="color: #428bca">侵权状态</span>'

    list_display = (
        'id', 'MainSKU', 'show_tortInfo', 'show_picture', 'show_id', 'Title', 'Tags', 'show_variants',
        'show_state', 'show_info'
    )
    list_editable = ('Title', 'Description', 'Tags', 'CoreWords', 'CoreTags')
    list_display_links = ('',)
    list_per_page = 20
    actions = ['to_public_templet_review']

    def to_public_templet_review(self, request, queryset):
        time = datetime.now()
        user = request.user.first_name

        for obj in queryset:
            if obj.Status == 1:
                messages.info(request, u'ID是%s已经提交公共模板审核，请勿重复提交！' % obj.id)
            else:
                wish_review.objects.create(MainSKU=obj.MainSKU, Title=obj.Title, Description=obj.Description,
                                           Tags=obj.Tags, MainImage=obj.MainImage, ExtraImages=obj.ExtraImages,
                                           Variants=obj.Variants, CreateTime=time, CreateStaff=user,
                                           UpdateTime=time, UpdateStaff=user, SrcProductID=obj.SrcProductID,
                                           ReviewState=0, SkuState=obj.SkuState, PlateForm=obj.PlateForm
                                           )
                obj.Status = 1
                obj.save()
    to_public_templet_review.short_description = u'转到公共模板审核'

    def get_list_queryset(self, ):
        request = self.request
        qs = super(t_templet_wish_collection_box_Admin, self).get_list_queryset()

        if request.user.is_superuser or request.user.username == 'jinyuling':
            qs = qs
        else:
            qs = qs.filter(CreateStaff=request.user.first_name, Status=0)

        main_sku = request.GET.get('main_sku', '')
        productid = request.GET.get('productid', '')
        createname = request.GET.get('createname', '')
        updatename = request.GET.get('updatename', '')
        sstatus = request.GET.get('sstatus', '')
        createtimeStart = request.GET.get('createtimeStart', '')
        createtimeTimeEnd = request.GET.get('createtimeTimeEnd', '')
        refreshTimeStart = request.GET.get('refreshTimeStart', '')
        refreshTimeEnd = request.GET.get('refreshTimeEnd', '')
        if main_sku:
            main_sku = main_sku.split(',')

        searchList = {
            'MainSKU__in': main_sku,  'SrcProductID__exact': productid,  'CreateStaff__exact': createname,
            'UpdateStaff__exact': updatename, 'Status__exact': sstatus, 'CreateTime__gte': createtimeStart,
            'CreateTime__lt': createtimeTimeEnd, 'UpdateTime__gte': refreshTimeStart, 'UpdateTime__lt': refreshTimeEnd,
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

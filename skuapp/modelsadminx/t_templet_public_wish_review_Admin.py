# coding=utf-8

from skuapp.table.t_templet_public_wish import *
from django.utils.safestring import mark_safe
from django.contrib import messages
from brick.wish.wish_distribution.admin_function import show_picture, show_variants, show_tortInfo, show_id


class t_templet_public_wish_review_Admin(object):
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
        rt = show_variants(obj=obj, plateform='wish', page='public_review')
        return mark_safe(rt)
    show_variants.short_description = u'<span style="color: #428bca">变体信息</span>'

    def show_info(self, obj):
        """展示时间、人员信息"""
        rt = u'创建人: %s<br>创建时间: %s<br>更新人: %s<br>更新时间: %s<br>审核人: %s<br>审核时间: %s' \
             % (obj.CreateStaff, obj.CreateTime, obj.UpdateStaff, obj.UpdateTime, obj.ReviewStaff, obj.ReviewTime)
        return mark_safe(rt)
    show_info.short_description = u'<span style="color: #428bca">------创建/更新/审核信息------</span>'

    def show_tortInfo(self, obj):
        rt = show_tortInfo(obj=obj)
        return mark_safe(rt)
    show_tortInfo.short_description = u'<span style="color: #428bca">侵权状态</span>'

    def show_review_state(self, obj):
        if obj.ReviewState == 1:
            rr = u'<div class="box" style="width: 80px;height: 30px;background-color: #66FF66;text-align: center;line-height: 30px;border-radius: 4px">通过</div>'
        elif obj.ReviewState == 2:
            rr = u'<div class="box" style="width: 80px;height: 30px;background-color: #FF3333;text-align: center;line-height: 30px;border-radius: 4px">不通过</div>'
        else:
            rr = u'<div class="box" style="width: 80px;height: 30px;background-color: #FFCC33;text-align: center;line-height: 30px;border-radius: 4px">未审核</div>'
        return mark_safe(rr)
    show_review_state.short_description = u'<span style="color: #428bca">审核状态</span>'

    list_display = (
        'id', 'MainSKU', 'show_tortInfo', 'show_picture', 'show_id', 'Title', 'Tags', 'show_variants',
        'show_review_state', 'show_info', 'Remarks'
    )
    list_editable = ('Title', 'Description', 'Tags', 'Remarks')
    list_display_links = ('',)
    list_per_page = 20
    actions = ['to_public_templet', 'to_reject']

    def to_public_templet(self, request, queryset):
        if request.user.username == 'jinyuling':
            from datetime import datetime
            time = datetime.now()
            user = request.user.first_name
            joom_id = []
            for obj in queryset:
                if obj.ReviewState == 1:
                    messages.info(request, u'ID是%s已经提交为公共模板，请勿重复提交！' % obj.id)
                elif obj.ReviewState == 2:
                    messages.info(request, u'ID是%s已经审核不通过，请勿重复提交！' % obj.id)
                else:
                    joom_id.append(int(obj.id))
                    t_templet_public_wish.objects.create(
                        MainSKU=obj.MainSKU, Title=obj.Title, Description=obj.Description, Tags=obj.Tags,
                        MainImage=obj.MainImage, ExtraImages=obj.ExtraImages, Variants=obj.Variants,
                        CreateTime=time, CreateStaff=obj.CreateStaff, UpdateTime=time, UpdateStaff=obj.CreateStaff,
                        SrcProductID=obj.SrcProductID, UsedNum=0, UpdatePicFlag=0, PlateForm=obj.PlateForm,
                        Remarks=obj.Remarks
                    )
                    obj.ReviewState = 1
                    obj.ReviewTime = time
                    obj.ReviewStaff = user
                    obj.save()
            # 生成joom采集箱数据
            if len(joom_id) != 0:
                from app_djcelery.tasks import joom_info_from_wish
                joom_info_from_wish(joom_id, user, time)
        else:
            messages.error(request, u'你不具有审核权限!!!')
    to_public_templet.short_description = u'转为公共模板(审核员)'

    def to_reject(self, request, queryset):
        if request.user.username == 'jinyuling':
            for obj in queryset:
                if obj.ReviewState == 1:
                    messages.info(request, u'ID是%s已经提交为公共模板，请勿重复提交！' % obj.id)
                elif obj.ReviewState == 2:
                    messages.info(request, u'ID是%s已经审核不通过，请勿重复提交！' % obj.id)
                else:
                    obj.ReviewState = 2
                    obj.save()
        else:
            messages.error(request, u'你不具有审核权限!!!')
    to_reject.short_description = u'审核不通过(审核员)'

    def get_list_queryset(self, ):
        request = self.request
        qs = super(t_templet_public_wish_review_Admin, self).get_list_queryset()

        qs.filter(ReviewState=0)

        main_sku = request.GET.get('main_sku', '')
        productid = request.GET.get('productid', '')
        createname = request.GET.get('createname', '')
        updatename = request.GET.get('updatename', '')
        reviewStatus = request.GET.get('reviewStatus', '')
        createtimeStart = request.GET.get('createtimeStart', '')
        createtimeTimeEnd = request.GET.get('createtimeTimeEnd', '')
        refreshTimeStart = request.GET.get('refreshTimeStart', '')
        refreshTimeEnd = request.GET.get('refreshTimeEnd', '')
        if main_sku:
            main_sku = main_sku.split(',')

        searchList = {
            'MainSKU__in': main_sku,  'SrcProductID__exact': productid, 'CreateStaff__exact': createname,
            'UpdateStaff__exact': updatename, 'ReviewState__exact': reviewStatus, 'CreateTime__gte': createtimeStart,
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

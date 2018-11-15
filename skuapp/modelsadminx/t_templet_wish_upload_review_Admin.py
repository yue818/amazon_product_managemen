# coding=utf-8

from django.utils.safestring import mark_safe
from django.contrib import messages
from datetime import datetime
from brick.wish.wish_distribution.admin_function import show_picture, show_variants, show_tortInfo


class t_templet_wish_upload_review_Admin(object):
    search_box_flag = True
    select_checkbox_flag = True
    plateform_distribution_navigation = True


    def show_picture(self,obj) :
        """展示主图"""
        rt = show_picture(obj=obj)
        return mark_safe(rt)
    show_picture.short_description = u'<span style="color: #428bca">图片</span>'


    def show_tortInfo(self, obj):
        rt = show_tortInfo(obj=obj)
        return mark_safe(rt)
    show_tortInfo.short_description = u'<span style="color: #428bca">侵权状态</span>'


    def show_variants(self, obj):
        """展示修改变体信息"""
        rt = show_variants(obj=obj, plateform='wish', page='upload_review')
        return mark_safe(rt)
    show_variants.short_description = u'<span style="color: #428bca">变体信息</span>'


    def show_create(self, obj):
        status_dict = {'UNSUBMITTED': u'未发布', 'SUBMITTED': u'已发布'}
        staff = obj.CreateStaff
        create_time = obj.CreateTime
        status = obj.PostStatus
        post_time = obj.PostTime
        rt = u'创建人: %s<br>创建时间: %s<br>发布状态: %s' % (staff, create_time, status_dict[status])
        if post_time:
            rt = u'%s<br>发布时间: %s' % (rt, post_time)
        return mark_safe(rt)
    show_create.short_description = u'<span style="color: #428bca">------------创建信息------------</span>'


    def show_review(self, obj):
        status_dict = {'UNREVIEW': u'未审核', 'PASS': u'审核通过', 'FAILE': u'审核不通过'}
        staff = obj.ReviewStaff
        time = obj.ReviewTime
        status = obj.ReviewStatus
        if staff:
            rt = u'审核人: %s<br>审核时间: %s<br>审核状态: %s' % (staff, time, status_dict[status])
        else:
            rt = u'审核状态: %s' % status_dict[status]
        return mark_safe(rt)
    show_review.short_description = u'<span style="color: #428bca">------------审核信息------------</span>'


    def show_distribution(self, obj):
        shop_name = obj.ShopName
        parent_sku = obj.ParentSKU
        schedule = obj.Schedule
        rt = u'铺货店铺: %s<br>ParentSKU: %s<br>预计铺货时间:<br>%s' % (shop_name, parent_sku, schedule)
        return mark_safe(rt)
    show_distribution.short_description = u'<span style="color: #428bca">------------铺货信息------------</span>'


    list_display = (
        'id', 'MainSKU', 'show_tortInfo', 'show_picture', 'Title', 'Tags',  'show_variants', 'show_distribution',
        'show_create', 'show_review', 'Remarks'
    )
    list_display_links = ('',)
    list_editable = ('Title', 'Description', 'Tags', 'Remarks')
    list_per_page = 20
    actions = ['wish_distribution', 'review_pass', 'review_faile']


    def review_pass(self, request, queryset):
        staff = request.user.first_name
        time = datetime.now()
        queryset.filter(ReviewStatus='UNREVIEW').update(ReviewStatus='PASS', ReviewStaff=staff, ReviewTime=time)
    review_pass.short_description = u'审核通过'


    def review_faile(self, request, queryset):
        staff = request.user.first_name
        time = datetime.now()
        queryset.filter(ReviewStatus='UNREVIEW').update(ReviewStatus='FAILE', ReviewStaff=staff, ReviewTime=time)
    review_faile.short_description = u'审核不通过'


    def wish_distribution(self, request, queryset):
        from brick.wish.wish_distribution.wish_distribution import to_distribution
        distribution_id_list = []
        error_id_list = []
        for obj in queryset:
            if obj.ReviewStatus == 'PASS' and obj.PostStatus == 'UNSUBMITTED':
                distribution_id_list.append(int(obj.id))
            else:
                error_id_list.append(obj.id)
        if distribution_id_list:
            to_distribution(distribution_id_tuple=tuple(distribution_id_list))
            queryset.filter(id__in=distribution_id_list).update(PostStatus='SUBMITTED', PostTime=datetime.now())
            messages.info(request, 'id: %s 正在铺货……' % distribution_id_list)
        if error_id_list:
            messages.info(request, 'id: %s 已提交铺货或未审核或审核不通过，请检查后再提交' % distribution_id_list)
    wish_distribution.short_description = u'提交铺货'


    def get_list_queryset(self,):
        request = self.request
        qs = super(t_templet_wish_upload_review_Admin, self).get_list_queryset()

        PostStatus = request.GET.get('PostStatus', '')
        ReviewStatus = request.GET.get('ReviewStatus', '')
        MainSKU = request.GET.get('MainSKU', )
        ShopName = request.GET.get('ShopName', )
        CreateStaff = request.GET.get('CreateStaff', )
        ReviewStaff = request.GET.get('ReviewStaff', )
        createTimeStart = request.GET.get('CreateTimeStart', '')
        createTimeEnd = request.GET.get('CreateTimeEnd', '')
        ScheduleStart = request.GET.get('ScheduleStart', '')
        ScheduleEnd = request.GET.get('ScheduleEnd', '')
        ReviewTimeStart = request.GET.get('ReviewTimeStart', '')
        ReviewTimeEnd = request.GET.get('ReviewTimeEnd', '')
        PostTimeStart = request.GET.get('PostTimeStart', '')
        PostTimeEnd = request.GET.get('PostTimeEnd', '')
        searchList = {'PostStatus__exact': PostStatus, 'ReviewStatus__exact': ReviewStatus, 'MainSKU__exact': MainSKU,
                      'ShopName__exact': ShopName, 'CreateStaff__exact':CreateStaff, 'ReviewStaff__exact':ReviewStaff,
                      'CreateTime__gte': createTimeStart, 'CreateTime__lte': createTimeEnd,
                      'Schedule__gte': ScheduleStart, 'Schedule__lte': ScheduleEnd,
                      'ReviewTime__gte': ReviewTimeStart, 'ReviewTime__lte': ReviewTimeEnd,
                      'PostTime__gte': PostTimeStart, 'PostTime__lte': PostTimeEnd,
                      }
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    if k == 'ShopName__exact':
                        v = 'Wish-' + v.zfill(4)
                    sl[k] = v
        if sl is not None:
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')
        return qs




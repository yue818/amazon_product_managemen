# coding=utf-8

from django.utils.safestring import mark_safe
from django.contrib import messages
from django.http import HttpResponseRedirect
from brick.wish.wish_distribution.admin_function import show_picture, show_variants, show_tortInfo, show_id
from django.db import connection

def check_title(title):
    sResult = {}
    sResult['resultCode'] = 0
    try:
        cur = connection.cursor()
        tort_words_list = []
        not_gray_words_list = []
        sResult['tort_flag'] = '0'
        sResult['gray_flag'] = '0'
        sResult['tort_words'] = ''
        sResult['gray_words'] = ''

        title = title.lower()
        title_list = list(set([word.strip() for word in title.split(' ') if word.strip() and word.isalpha()]))
        title_str = '"' + '","'.join(title_list) + '"'
        tort_sql = 'select word from t_chart_wish_words_tort ;'
        cur.execute(tort_sql)
        tort_infos = cur.fetchall()
        for tort_info in tort_infos:
            if title.find(' ' + tort_info[0] + ' ') >= 0 or title.endswith(' ' + tort_info[0]) or title.startswith(tort_info[0] + ' '):
                tort_words_list.append(tort_info[0])

        gray_sql = 'select word from hq_enwords WHERE word in ({});'.format(title_str)
        cur.execute(gray_sql)
        not_gray_infos = cur.fetchall()
        for not_gray_info in not_gray_infos:
            not_gray_words_list.append(not_gray_info[0])
        gray_words_list = list(set(title_list) ^ set(not_gray_words_list))

        if tort_words_list:
            sResult['tort_flag'] = '1'
            sResult['tort_words'] = ' | '.join(list(set(tort_words_list)))
        if gray_words_list:
            sResult['gray_flag'] = '1'
            sResult['gray_words'] = ' | '.join(list(set(gray_words_list)))
    except Exception, e:
        sResult['resultCode'] = -1
        sResult['errorText'] = '%s:%s' % (Exception, e)
    cur.close()
    return sResult


class t_templet_wish_wait_upload_Admin(object):
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
        rt = show_variants(obj=obj, plateform='wish', page='wait_upload')
        return mark_safe(rt)
    show_variants.short_description = u'<span style="color: #428bca">变体信息</span>'

    def show_tortInfo(self, obj):
        rt = show_tortInfo(obj=obj)
        return mark_safe(rt)
    show_tortInfo.short_description = u'<span style="color: #428bca">侵权状态</span>'

    def show_info(self, obj):
        """展示时间、人员信息"""
        rt = u'创建人: %s<br>创建时间: %s<br>更新人: %s<br>更新时间: %s<br>提交人: %s<br>提交时间: %s' \
             % (obj.CreateStaff, obj.CreateTime, obj.UpdateStaff, obj.UpdateTime, obj.PostStaff, obj.PostTime)
        return mark_safe(rt)
    show_info.short_description = u'<span style="color: #428bca">--------创建/提交信息--------</span>'

    def show_schedule(self, obj):
        """展示铺货店铺、开始时间、结束时间"""
        if obj.ShopSets == None:
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
        if obj.TimePlan == None:
            start = ''
            interval = ''
        else:
            schedule = eval(obj.TimePlan)
            start = schedule['start']
            interval = schedule['interval']
        rt = '<span style="color: #0000FF;font-weight: 600">%d个</span>' % num
        rt = '(%s)目标店铺：%s<br>开始时间：%s<br>时间间隔：%s' % (rt, shops, start, interval)
        rt = "%s<br><br><a id='write_plan_id_%s'>修改执行计划</a>" \
             "<script>$('#write_plan_id_%s').on('click',function(){layer.open(" \
             "{type:2,skin:'layui-layer-lan',title:'执行计划',fix:false,shadeClose: true,maxmin:true," \
             "area:['600px','800px'],content:'/show_wish_schedule/?myId=%s',btn:['关闭页面']});});</script>" \
             % (rt, obj.id, obj.id, obj.id)
        state = obj.Status
        if state == 'NO':
            rt = '%s<br><br><p style="color: #FF3333">%s</p>' % (rt, u'未铺货')
        elif state == 'YES':
            rt = '%s<br><br><p style="color: #66FF66">%s</p>' % (rt, u'已铺货')
        else:
            rt = '%s<br><br><p style="color: #FFCC33">%s</p>' % (rt, u'在展开')
        return mark_safe(rt)
    show_schedule.short_description = u'<span style="color: #428bca">&nbsp;&nbsp;定时铺货计划&nbsp;&nbsp;</span>'

    list_display = (
        'id', 'MainSKU', 'show_tortInfo', 'show_picture', 'show_id', 'Title', 'Tags', 'show_schedule',
        'show_variants', 'show_info'
    )
    list_display_links = ('',)
    list_per_page = 20
    list_editable = ('Title', 'Description', 'Tags')
    actions = ['change_schedule', 'wish_open']

    def change_schedule(self, request, queryset):
        param = request.get_full_path()
        if len(queryset) == 1:
            idList = queryset[0].id
        else:
            idList = []
            for obj in queryset:
                idList.append(str(obj.id))
        return HttpResponseRedirect('/show_wish_schedule/?myId=%s&param=%s' % (idList, param))
    change_schedule.short_description = u'批量填写计划'

    def wish_open(self, request, queryset):
        """去铺货"""
        from brick.wish.wish_distribution.wish_distribution import wish_open
        from skuapp.table.t_product_image_modify import t_product_image_modify
        from datetime import datetime
        wait_open_id_list = []
        exists_id_list = []
        blank_shop_id_list = []
        non_pic_list = []
        new_pic_list = []
        time = datetime.now()
        user = request.user.first_name
        for obj in queryset:
            tort_words = ''
            check_title_result = check_title(obj.Title)
            if check_title_result['resultCode'] == 0:
                if check_title_result['tort_flag'] == '1':
                    tort_words = u'侵权词: ' + check_title_result['tort_words']
            if tort_words:
                messages.error(request, u'id: %s 链接的标题存在%s' % (obj.id, tort_words))
            else:
                image_modify_objs = t_product_image_modify.objects.filter(MainSKU=obj.MainSKU)
                if image_modify_objs.exists():
                    if image_modify_objs[0].UpdateFlag == 0:
                        if (obj.Status == 'YES') or (obj.Status == 'OPEN'):
                            exists_id_list.append(int(obj.id))
                        elif obj.ShopSets == None or obj.ShopSets.strip() == '':
                            blank_shop_id_list.append(int(obj.id))
                        else:
                            wait_open_id_list.append(int(obj.id))
                    else:
                        new_pic_list.append(int(obj.id))
                else:
                    non_pic_list.append(int(obj.id))

        if wait_open_id_list:
            queryset.filter(id__in=wait_open_id_list).update(Status='OPEN', PostTime=time, PostStaff=user)
            wish_open(wait_open_id_tuple=tuple(wait_open_id_list))
            messages.info(request, 'id: %s 已经展开' % wait_open_id_list)
        if exists_id_list:
            messages.error(request, 'id: %s 已铺货或正在展开铺货' % exists_id_list)
        if blank_shop_id_list:
            messages.error(request, 'id: %s 请确认铺货店铺不为空再铺货！' % blank_shop_id_list)
        if non_pic_list:
            messages.error(request, 'id: %s 无备用主图，请等待主图刷新后再铺货！' % non_pic_list)
        if new_pic_list:
            messages.error(request, 'id: %s 主图库有更新，请核对后再铺货！' % new_pic_list)
    wish_open.short_description = u'展开铺货模板'

    def get_list_queryset(self, ):
        request = self.request
        qs = super(t_templet_wish_wait_upload_Admin, self).get_list_queryset()

        if request.user.is_superuser or request.user.username == 'jinyuling':
            qs = qs
        else:
            qs = qs.filter(CreateStaff=request.user.first_name, Status='NO')

        status = request.GET.get('Status', '')
        main_sku = request.GET.get('mainSKU', '')
        createStaff = request.GET.get('CreateStaff', )
        postTimeStart = request.GET.get('PostTimeStart', '')
        postTimeEnd = request.GET.get('PostTimeEnd', '')
        createTimeStart = request.GET.get('CreateTimeStart', '')
        createTimeEnd = request.GET.get('CreateTimeEnd', '')
        if main_sku:
            main_sku = main_sku.split(',')
        searchList = {
            'Status__exact': status, 'MainSKU__in': main_sku, 'CreateStaff__exact': createStaff,
            'PostTime__gte': postTimeStart, 'PostTime__lte': postTimeEnd, 'CreateTime__gte': createTimeStart,
            'CreateTime__lte': createTimeEnd
        }
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    sl[k] = v
        if sl is not None:
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')
        return qs

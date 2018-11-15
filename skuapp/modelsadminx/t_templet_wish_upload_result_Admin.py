# -*- coding: utf-8 -*-

from skuapp.table.t_templet_wish_upload_result import t_templet_wish_upload_result
from django.utils.safestring import mark_safe
from django.contrib import messages
from skuapp.table.t_api_schedule_ing_wish_upload import t_api_schedule_ing_wish_upload
from skuapp.table.t_tort_aliexpress import t_tort_aliexpress



class t_templet_wish_upload_result_Admin(object):
    search_box_flag = True
    select_checkbox_flag = True
    plateform_distribution_navigation = True

    def show_picture(self, obj):
        """展示主图"""
        url = obj.MainImage.replace('-original', '-medium')
        rt = '<img src="%s"  width="120" height="120"  alt = "%s"  title="%s"  />  ' % (url, url, url)
        return mark_safe(rt)
    show_picture.short_description = u'<span style="color: #428bca">图片</span>'


    def show_detail(self, obj):
        rt = '<table   style="text-align:center;" border="1" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1">' \
             '<tr bgcolor="#C00"><th style="text-align:center">店铺SKU</th>' \
             '<th style="text-align:center">商品SKU</th></tr>'
        myVariants = obj.Variants
        if myVariants is None:
            rt = '<p align="center" style="color: red">铺货出现错误，请核对!!!</p>'
        else:
            tempList1 = []
            tempList2 = []
            Variants = eval(myVariants.replace('n"s', 'n`s').replace('<', '&#60;').replace('>', '&#62;').replace('@', '&#64;'))
            tempList1 = [Variants['first']['product']['sku'], Variants['first']['product']['productSKU']]
            tempList2.append(tempList1)
            for product in Variants['second']['product']:
                tempList1 = [product['sku'], product['productSKU']]
                tempList2.append(tempList1)

            i = 0
            for each in tempList2:
                if i < 5:
                    rt = '%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td></tr> ' % (rt, each[0], each[1])
                    i = i + 1
            if len(tempList2) > 5:
                rt = '%s<tr><td><a id="link_id_%s">查看更多</a></td></tr>' % (rt, obj.id)
            else:
                rt = rt
            rt = "%s</table><script>$('#link_id_%s').on('click',function(){layer.open(" \
                 "{type:2,skin:'layui-layer-lan',title:'查看全部',fix:false,shadeClose: true," \
                 "maxmin:true,area:['500px','500px'],content:'/show_wish_result/?myId=%s',});});</script>" % \
                 (rt, obj.id, obj.id)
        return mark_safe(rt)
    show_detail.short_description = u'<span style="color: #428bca">子SKU</span>'


    def show_state(self, obj):
        rt = ''
        state = obj.Status
        if state == 'EXISTS':
            rt = u'重复铺货'
        elif state == 'ING':
            rt = u'正在铺货'
        elif state == 'REPETITION':
            rt = u'店铺内已有此商品'
        elif state == 'SUCCESS':
            rt = u'铺货成功'
        elif state == 'DEFEAT':
            rt = u'铺货失败'
        elif state == 'CANCEL':
            rt = u'铺货取消'
        return mark_safe(rt)
    show_state.short_description = u'<span style="color: #428bca">铺货状态</span>'


    def show_tort(self, obj):
        try:
            ret = t_tort_aliexpress.objects.filter(MainSKU=obj.MainSKU).values('Site')
        except t_tort_aliexpress.DoesNotExist:
            ret = None
        if not ret:
            rt = u"<span style='color: green; font-weight: bold;'>未侵权</span>"
        else:
            rets = list()
            for i in ret:
                if not i['Site']:
                    if u'未知' not in rets:
                        rets.append(u'未知')
                else:
                    if i['Site'] not in rets:
                        rets.append(i['Site'])
            rt = u"<span style='color: red; font-weight: bold;'>%s  侵权</span>" % (','.join(rets))
        return mark_safe(rt)
    show_tort.short_description = u'<span style="color: #428bca">侵权状态</span>'


    def show_mainsku(self, obj):
        main_sku = obj.MainSKU
        main_sku_str = u''
        if main_sku:
            main_sku_list = main_sku.split(',')
        else:
            main_sku_list = []
        if len(main_sku_list) == 1:
            main_sku_str = main_sku
        elif len(main_sku_list) == 2:
            main_sku_str = ','.join(main_sku_list)
        else:
            for i in range(len(main_sku_list)):
                if (i + 1) % 2 == 0:
                    main_sku_str = u'%s<span>%s<span><br>' % (main_sku_str, main_sku_list[i])
                else:
                    main_sku_str = u'%s<span>%s,<span>' % (main_sku_str, main_sku_list[i])
        return mark_safe(main_sku_str)
    show_mainsku.short_description = u'<span style="color: #428bca">主SKU</span>'


    list_display = ('id', 'PID', 'MainSKU', 'show_picture', 'ShopName', 'ParentSKU', 'show_detail',
                    'Submitter', 'InsertTime', 'Schedule', 'show_state', 'show_tort', 'ErrorMessage')
    list_display_links = ('',)
    actions = ['cancel_schedule']


    def cancel_schedule(self, request, queryset):
        for obj in queryset:
            if obj.Status == 'ING':
                result_obj = t_templet_wish_upload_result.objects.filter(id=obj.id)
                result_obj.update(Status='CANCEL')
                t_api_schedule_ing_wish_upload.objects.filter(WishResultID=obj.id).delete()
            else:
                messages.error(request, '铺货ID：%s铺货出错或已经铺货完成，不能执行取消操作' % obj.id)
    cancel_schedule.short_description = u'取消铺货'


    def get_list_queryset(self,):
        request = self.request
        qs = super(t_templet_wish_upload_result_Admin, self).get_list_queryset()

        if request.user.is_superuser or request.user.username == 'jinyuling':
            qs = qs
        else:
            qs = qs.filter(Submitter=request.user.first_name)

        PID = request.GET.get('PID', '')
        ShopName = request.GET.get('ShopName', '')
        submitter = request.GET.get('Submitter', '')
        subStatus = request.GET.get('SubStatus', '')
        mainSKU = request.GET.get('mainSKU', '')
        insertTimeStart = request.GET.get('InsertTimeStart', '')
        insertTimeEnd = request.GET.get('InsertTimeEnd', '')
        ScheduleStart = request.GET.get('ScheduleStart', '')
        ScheduleEnd = request.GET.get('ScheduleEnd', '')
        tortinfo = request.GET.get('tortInfo', '')
        searchList = {
            'ShopName__exact': ShopName, 'Submitter__exact': submitter, 'Status__exact': subStatus, 'PID_exact': PID,
            'MainSKU__exact': mainSKU, 'InsertTime__gte': insertTimeStart, 'InsertTime__lte': insertTimeEnd,
            'Schedule__gte': ScheduleStart, 'Schedule__lte': ScheduleEnd
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
        if sl is not None:
            try:
                qs = qs.filter(**sl)
            except Exception:
                messages.error(request, u'输入的查询数据有问题！')

        mainid_list = list()
        if tortinfo:
            if tortinfo == 'WY':
                mainid_list = t_tort_aliexpress.objects.filter(Site='Wish').values('MainSKU')
            elif tortinfo == 'Y':
                mainid_list = t_tort_aliexpress.objects.exclude(Site='Wish').values('MainSKU')
            elif tortinfo == 'N':
                mainid_list = t_tort_aliexpress.objects.all().values('MainSKU')
            main_ids = list()
            if mainid_list:
                for i in mainid_list:
                    main_ids.append(i['MainSKU'])
            if main_ids:
                if tortinfo == 'WY' or tortinfo == 'Y':
                    qs = qs.filter(MainSKU__in=main_ids)
                elif tortinfo == 'N':
                    qs = qs.exclude(MainSKU__in=main_ids)

        return qs

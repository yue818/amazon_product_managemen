# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from django.contrib import messages
import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render
import json


class t_config_wishapi_product_analyse_info_Admin(object):
    list_per_page = 50
    search_box_flag = True

    def show_SourcePicPath(self,obj) :
        url =u'%s'%(obj.SourcePicPath)
        rt =  '<img src="%s"  width="150" height="150"  alt = "%s"  title="%s" />  '%(url,url,url)
        return mark_safe(rt)
    show_SourcePicPath.short_description = u'图片'

    def show_Name_Pid(self, obj):
        l = obj.Name.split(' ')
        aa = len(l)
        ll = ''
        rt = ''
        if aa <= 6:
            rt = u'标题:<br> %s<br>产品ID:<br><a href=" https://www.wish.com/c/%s" target="_blank">%s</a>' % (obj.Name, obj.Pid, obj.Pid)
        elif aa > 6:
            newe_Title_list = []
            isSupplierID = ''
            for i in range(0, len(l), 6):
                min_list = ''
                for a in l[i:i + 6]:
                    min_list = u'%s%s ' % (min_list, a)
                newe_Title_list.append(min_list)
            for newe_Title in newe_Title_list:
                ll = u'%s%s<br>' % (ll, newe_Title)
            if obj.SupplierID in ['0']:
                isSupplierID = u'否'
            if obj.SupplierID in ['1']:
                isSupplierID = u'是'
            rt = u'标题:<br>%s产品ID:<a href=" https://www.wish.com/c/%s" target="_blank">%s</a><br>是否有供货商:%s' % (ll, obj.Pid, obj.Pid,isSupplierID)
        return mark_safe(rt)
    show_Name_Pid.short_description = u'标题/产品ID/是否有供货商'

    def show_approved_date_ShelveDay_Op_time(self,obj):
        rt = u'开张时间:<br>%s<br>上架时间:<br>%s<br>采集时间:<br>%s' % (obj.approved_date, obj.ShelveDay, obj.Op_time)
        return mark_safe(rt)
    show_approved_date_ShelveDay_Op_time.short_description = u'开张时间/上架时间/采集时间'

    def show_DealName_DealTime(self, obj):
        rt = u'<span style="color: blue">%s</span> <br><br> <span style="color: blue">%s</span>' % (obj.DealName, obj.DealTime)
        return mark_safe(rt)
    show_DealName_DealTime.short_description = u'处理人/处理时间'

    def show_salesgrowth(self, obj):
        salesgrowth = u'%s' % (obj.salesgrowth)
        return mark_safe(salesgrowth+'%')
    show_salesgrowth.short_description = u'增长率'

    def show_NumBought(self, obj):
        numBought = obj.NumBought
        if numBought:
            numBought = long(obj.NumBought)
        return mark_safe(numBought)
    show_NumBought.short_description = u'总购买人数'

    def show_OrdersLast7Days(self, obj):
        ordersLast7Days = obj.OrdersLast7Days
        if ordersLast7Days:
            ordersLast7Days = long(obj.OrdersLast7Days)
        return mark_safe(ordersLast7Days)
    show_OrdersLast7Days.short_description = u'7天order数'

    def show_OrdersLast7to14Days(self, obj):
        ordersLast7to14Days = obj.OrdersLast7to14Days
        if ordersLast7to14Days:
            ordersLast7to14Days = long(obj.OrdersLast7to14Days)
        return mark_safe(ordersLast7to14Days)
    show_OrdersLast7to14Days.short_description = u'前8-14天order数'

    list_display  = ('id','show_SourcePicPath','show_Name_Pid','Remarks','YNDone','Collar','show_NumBought','show_OrdersLast7Days','show_OrdersLast7to14Days','UnitPrice','show_salesgrowth',
                     'show_approved_date_ShelveDay_Op_time','show_DealName_DealTime')
    list_editable = ('Remarks',)
    readonly_fields = ('Collar','NumBought','OrdersLast7Days','show_salesgrowth',)

    actions = ['to_start', 'to_suspend', 'to_complete', 'to_abandaned','have_done']


    def to_start(self, request, queryset):
        urlkey = 1
        wish_data ={}
        for qs in queryset.all():
            if qs.Collar in ['2', 'suspend'] and (qs.DealName is None or qs.DealName == request.user.username):
                qs.Collar = 'start'  # 开始开发
                qs.DealName = request.user.username
                qs.DealTime = datetime.datetime.now()
                qs.save()

                wish_data[urlkey] = {1:qs.Pid, 2:qs.OrdersLast7Days,3:qs.UnitPrice}
                urlkey += 1
                # messages.success(request, '请去调研页面处理 Pid：%s' % qs.Pid)
            elif qs.Collar not in ['2', 'suspend']:
                messages.error(request, '对不起！非待开发状态的产品，无法领用开发。 Pid：%s' % qs.Pid)
            elif qs.DealName is not None and qs.DealName != request.user.username:
                messages.error(request, '对不起！只有开发领用人员为空或为本人，才能开始开发。 Pid：%s' % qs.Pid)
        if wish_data:
            jsonurl = json.dumps(wish_data)
            return HttpResponseRedirect('/t_config_wishapi_product_analyse_info_start/?jsonurl=%s' % jsonurl)
    to_start.short_description = u'开始开发'

    def to_suspend(self, request, queryset):
        for qs in queryset.all():
            if qs.Collar == 'start' and qs.Remarks is not None and qs.Remarks.strip() != '' and qs.DealName == request.user.username:
                qs.Collar = 'suspend'  # 暂停开发
                qs.DealTime = datetime.datetime.now()
                qs.save()

            elif qs.Collar != 'start':
                messages.error(request, '对不起！只有已经开始开发的产品，才可以暂停开发。 Pid：%s' % qs.Pid)
            elif qs.Remarks is None or qs.Remarks.strip() == '':
                messages.error(request, '对不起！请填写暂停开发的原因。 Pid：%s' % qs.Pid)
            elif qs.DealName != request.user.username:
                messages.error(request, '对不起！只有开发领用人员，才能暂停开发。 Pid：%s' % qs.Pid)
    to_suspend.short_description = u'暂停开发'

    def to_complete(self, request, queryset):
        for qs in queryset.all():
            if qs.Collar == 'start' and qs.Remarks is not None and qs.Remarks.strip() != '' and qs.DealName == request.user.username:
                qs.Collar = 'complete'
                qs.YNDone = 'Y'  #完成时置为已做
                qs.DealTime = datetime.datetime.now()
                qs.save()

            elif qs.Collar != 'start':
                messages.error(request, '对不起！只有已经开始开发的产品，才可以完成开发。 Pid：%s' % qs.Pid)
            elif qs.Remarks is None or qs.Remarks.strip() == '':
                messages.error(request, '对不起！请填写完成开发的落地SKU。 Pid：%s' % qs.Pid)
            elif qs.DealName != request.user.username:
                messages.error(request, '对不起！只有开发领用人员，才能执行完成开发动作。 Pid：%s' % qs.Pid)
    to_complete.short_description = u'完成开发'

    def to_abandaned(self, request, queryset):
        for qs in queryset.all():
            if qs.Remarks is not None and qs.Remarks.strip() != '':
                qs.Collar = 'adandaned'
                qs.DealName = request.user.username
                qs.DealTime = datetime.datetime.now()
                qs.save()
            elif qs.Remarks is None or qs.Remarks.strip() == '':
                messages.error(request, '对不起！请填写弃用的原因。 Pid：%s' % qs.Pid)
    to_abandaned.short_description = u'弃用'

    def have_done(self, request, queryset):
        for qs in queryset.all():
            if qs.YNDone == 'N' and qs.Collar in ['2', 'suspend']:
                qs.Collar = 'adandaned'
                qs.YNDone = 'Y'
                qs.DealName = request.user.username
                qs.DealTime = datetime.datetime.now()
                qs.save()
            elif qs.YNDone == 'N' and qs.Collar not in ['2','suspend']:
                messages.error(request, '对不起！开始/暂停/弃用的产品不要再做"已做过"操作。 Pid：%s' % qs.Pid)
            elif qs.YNDone == 'Y':
                messages.error(request, '对不起！不要重复操作已做过。 Pid：%s' % qs.Pid)
    have_done.short_description = u'已做过'


    def get_list_queryset(self, ):
        request = self.request
        qs = super(t_config_wishapi_product_analyse_info_Admin, self).get_list_queryset()
        Pid = request.GET.get('Pid', '')
        Name = request.GET.get('Name', '')
        YNDone = request.GET.get('YNDone', '')
        NumBoughtStart = request.GET.get('NumBoughtStart', '')
        NumBoughtEnd = request.GET.get('NumBoughtEnd', '')
        UnitPriceStart = request.GET.get('UnitPriceStart', '')
        UnitPriceEnd = request.GET.get('UnitPriceEnd', '')
        OrdersLast7DaysStart = request.GET.get('OrdersLast7DaysStart', '')
        OrdersLast7DaysEnd = request.GET.get('OrdersLast7DaysEnd', '')
        OrdersLast7to14DaysStart = request.GET.get('OrdersLast7to14DaysStart', '')
        OrdersLast7to14DaysEnd = request.GET.get('OrdersLast7to14DaysEnd', '')
        SupplierID = request.GET.get('SupplierID', '')
        DealName = request.GET.get('DealName', '')
        DealTimeStart = request.GET.get('DealTimeStart', '')
        DealTimeEnd = request.GET.get('DealTimeEnd', '')
        Op_timeStart = request.GET.get('Op_timeStart', '')
        Op_timeEnd = request.GET.get('Op_timeEnd', '')
        ShelveDayStart = request.GET.get('ShelveDayStart', '')
        ShelveDayEnd = request.GET.get('ShelveDayEnd', '')
        Collar = request.GET.get('Collar', '')

        searchList = {'Pid__exact': Pid, 'Name__contains': Name,'YNDone__exact': YNDone,
                      'NumBought__gte': NumBoughtStart, 'NumBought__lt': NumBoughtEnd,
                      'UnitPrice__gte': UnitPriceStart, 'UnitPrice__lt': UnitPriceEnd,
                      'OrdersLast7Days__gte': OrdersLast7DaysStart, 'OrdersLast7Days__lt': OrdersLast7DaysEnd,
                      'OrdersLast7to14Days__gte': OrdersLast7to14DaysStart,
                      'OrdersLast7to14Days__lt': OrdersLast7to14DaysEnd,
                      'SupplierID__exact': SupplierID, 'DealName__exact': DealName,
                      'DealTime__gte': DealTimeStart, 'DealTime__lt': DealTimeEnd,
                      'Op_time__gte': Op_timeStart, 'Op_time__lt': Op_timeEnd,
                      'ShelveDay__gte': ShelveDayStart, 'ShelveDay__lt': ShelveDayEnd,
                      'Collar__exact': Collar,
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
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'Please enter the correct content!')
        return qs
# -*- coding: utf-8 -*-
from skuapp.table.not_clothing_salesman_registration import *
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from django.utils.safestring import mark_safe
from django.contrib import messages



class not_clothing_salesman_registration_Admin(object):
    search_box_flag = True
    list_display = (
         'ThisMonth','Category', 'Department', 'GroupLeader', 'Salesperson',
         'FirstDay', 'SecondDay', 'ThirdDay','FourthDay', 'FifthDay', 'SixthDay', 'SeventhDay','show_SumofFirstWeek',
         'EighthDay', 'NinthDay', 'TenthDay','EleventhDay', 'TwelfthDay', 'ThirteenthDay', 'FourteenthDay','show_SumofSecondWeek',
         'FifteenthDay', 'SixteenthDay', 'SeventeenthDay', 'EighteenthDay', 'NineteenthDay', 'TwentiethDay', 'TwentyFirstDay','show_SumofThirdWeek',
         'TwentySecondDay', 'TwentyThirdDay', 'TwentyFourthDay','TwentyFifthDay', 'TwentySixthDay', 'TwentySeventhDay', 'TwentyEighthDay','show_SumofFourthWeek',
         'TwentyNinthDay', 'ThirtiethDay', 'ThirtiethFirstDay', 'show_SumofMonth', 'CompletionDegree', 'UnfinishedCause', )

    list_editable = ('FirstDay', 'SecondDay', 'ThirdDay','FourthDay', 'FifthDay', 'SixthDay', 'SeventhDay',
         'EighthDay', 'NinthDay', 'TenthDay','EleventhDay', 'TwelfthDay', 'ThirteenthDay', 'FourteenthDay',
         'FifteenthDay', 'SixteenthDay', 'SeventeenthDay', 'EighteenthDay', 'NineteenthDay', 'TwentiethDay', 'TwentyFirstDay',
         'TwentySecondDay', 'TwentyThirdDay', 'TwentyFourthDay','TwentyFifthDay', 'TwentySixthDay', 'TwentySeventhDay', 'TwentyEighthDay',
         'TwentyNinthDay', 'ThirtiethDay', 'ThirtiethFirstDay', 'CompletionDegree', 'UnfinishedCause', )

    fields = ('ThisYear', 'ThisMonth', 'Category', 'Department', 'GroupLeader', 'Salesperson',)

    form_layout = (
        Fieldset(u'基本信息',
                 Row('ThisYear', 'ThisMonth', 'Category', ),
                 Row('Department', 'GroupLeader', 'Salesperson', ),
                 css_class='unsort '
                 ),

    )

    def show_SumofFirstWeek(self,obj):
        SumofFirstWeek = 0
        rt = ''
        if obj.FirstDay is not None and str(obj.FirstDay).strip() !='':
            SumofFirstWeek += obj.FirstDay
        if obj.SecondDay is not None and str(obj.SecondDay).strip() !='':
            SumofFirstWeek += obj.SecondDay
        if obj.ThirdDay is not None and str(obj.ThirdDay).strip() !='':
            SumofFirstWeek += obj.ThirdDay
        if obj.FourthDay is not None and str(obj.FourthDay).strip() !='':
            SumofFirstWeek += obj.FourthDay
        if obj.FifthDay is not None and str(obj.FifthDay).strip() !='':
            SumofFirstWeek += obj.FifthDay
        if obj.SixthDay is not None and str(obj.SixthDay).strip() !='':
            SumofFirstWeek += obj.SixthDay
        if obj.SeventhDay is not None and str(obj.SeventhDay).strip() !='':
            SumofFirstWeek += obj.SeventhDay

        obj.SumofFirstWeek = SumofFirstWeek
        obj.save()

        rt = "%s%s" % (rt,obj.SumofFirstWeek)

        return mark_safe(rt)

    show_SumofFirstWeek.short_description = u'第一周<br>小计'

    def show_SumofSecondWeek(self,obj):
        SumofSecondWeek = 0
        rt = ''
        if obj.EighthDay is not None  and str(obj.EighthDay).strip() !='':
            SumofSecondWeek += obj.EighthDay
        if obj.NinthDay is not None and str(obj.NinthDay).strip() !='':
            SumofSecondWeek += obj.NinthDay
        if obj.TenthDay is not None and str(obj.TenthDay).strip() !='':
            SumofSecondWeek += obj.TenthDay
        if obj.EleventhDay is not None and str(obj.EleventhDay).strip() !='':
            SumofSecondWeek += obj.EleventhDay
        if obj.TwelfthDay is not None and str(obj.TwelfthDay).strip() !='':
            SumofSecondWeek += obj.TwelfthDay
        if obj.ThirteenthDay is not None and str(obj.ThirteenthDay).strip() !='':
            SumofSecondWeek += obj.ThirteenthDay
        if obj.FourteenthDay is not None and str(obj.FourteenthDay).strip() !='':
            SumofSecondWeek += obj.FourteenthDay

        obj.SumofSecondWeek = SumofSecondWeek

        rt = "%s%s" % (rt,obj.SumofSecondWeek)
        obj.save()

        return mark_safe(rt)

    show_SumofSecondWeek.short_description = u'第二周<br>小计'

    def show_SumofThirdWeek(self,obj):
        SumofThirdWeek = 0
        rt = ''
        if obj.FifteenthDay is not None and str(obj.FifteenthDay).strip() !='':
            SumofThirdWeek += obj.FifteenthDay
        if obj.SixteenthDay is not None and str(obj.SixteenthDay).strip() !='':
            SumofThirdWeek += obj.SixteenthDay
        if obj.SeventeenthDay is not None and str(obj.SeventeenthDay).strip() !='':
            SumofThirdWeek += obj.SeventeenthDay
        if obj.EighteenthDay is not None and str(obj.EighteenthDay).strip() !='':
            SumofThirdWeek += obj.EighteenthDay
        if obj.NineteenthDay is not None and str(obj.NineteenthDay).strip() !='':
            SumofThirdWeek += obj.NineteenthDay
        if obj.TwentiethDay is not None and str(obj.TwentiethDay).strip() !='':
            SumofThirdWeek += obj.TwentiethDay
        if obj.TwentyFirstDay is not None and str(obj.TwentyFirstDay).strip() !='':
            SumofThirdWeek += obj.TwentyFirstDay

        obj.SumofThirdWeek = SumofThirdWeek
        obj.save()
        rt = "%s%s" % (rt,obj.SumofThirdWeek)

        return mark_safe(rt)

    show_SumofThirdWeek.short_description = u'第三周<br>小计'

    def show_SumofFourthWeek(self,obj):
        SumofFourthWeek = 0
        rt = ''
        if obj.TwentySecondDay is not None and str(obj.TwentySecondDay).strip() !='':
            SumofFourthWeek += obj.TwentySecondDay
        if obj.TwentyThirdDay is not None and str(obj.TwentyThirdDay).strip() !='':
            SumofFourthWeek += obj.TwentyThirdDay
        if obj.TwentyFourthDay is not None and str(obj.TwentyFourthDay).strip() !='':
            SumofFourthWeek += obj.TwentyFourthDay
        if obj.TwentyFifthDay is not None and str(obj.TwentyFifthDay).strip() !='':
            SumofFourthWeek += obj.TwentyFifthDay
        if obj.TwentySixthDay is not None and str(obj.FirstDay).strip() !='':
            SumofFourthWeek += obj.TwentySixthDay
        if obj.TwentySeventhDay is not None and str(obj.TwentySeventhDay).strip() !='':
            SumofFourthWeek += obj.TwentySeventhDay
        if obj.TwentyEighthDay is not None and str(obj.TwentyEighthDay).strip() !='':
            SumofFourthWeek += obj.TwentyEighthDay

        obj.SumofFourthWeek = SumofFourthWeek
        obj.save()

        rt = "%s%s" % (rt,obj.SumofFourthWeek)

        return mark_safe(rt)

    show_SumofFourthWeek.short_description = u'第四周<br>小计'

    def show_SumofMonth(self,obj):
        SumofMonth = 0
        rt = ''
        if obj.TwentyNinthDay is not None and str(obj.TwentyNinthDay).strip() !='':
            SumofMonth += obj.TwentyNinthDay
        if obj.ThirtiethDay is not None and str(obj.ThirtiethDay).strip() !='':
            SumofMonth += obj.ThirtiethDay
        if obj.ThirtiethFirstDay is not None and str(obj.ThirtiethFirstDay).strip() !='':
            SumofMonth += obj.ThirtiethFirstDay

        SumofMonth += obj.SumofFirstWeek + obj.SumofSecondWeek + obj.SumofThirdWeek + obj.SumofFourthWeek
        obj.SumofMonth = SumofMonth

        rt = "%s%s" % (rt,obj.SumofMonth)
        obj.save()

        return mark_safe(rt)

    show_SumofMonth.short_description = u'月总和'
    
    def save_models(self):
        obj = self.new_obj
        try:
            obj.save()
        except:
			messages.error(self.request, '添加失败！这条记录已存在！')



    def get_list_queryset(self):
        request = self.request
        qs = super(not_clothing_salesman_registration_Admin, self).get_list_queryset()

        ThisYear = request.GET.get('ThisYear', '')
        ThisMonth = request.GET.get('ThisMonth', '')
        Category = request.GET.get('Category', '')
        Department = request.GET.get('Department', '')
        GroupLeader = request.GET.get('GroupLeader', '')
        Salesperson = request.GET.get('Salesperson', '')

        SumofMonthStart = request.GET.get('SumofMonthStart', '')
        SumofMonthEnd = request.GET.get('SumofMonthEnd', '')

        searchList = {'ThisYear__exact': ThisYear,
                      'ThisMonth__exact': ThisMonth,
                      'Category__exact': Category,
                      'Department__exact': Department,
                      'GroupLeader__exact': GroupLeader,
                      'Salesperson__exact': Salesperson,

                      'SumofMonth__gte': SumofMonthStart, 'SumofMonth__lt': SumofMonthEnd,
                      }
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    # if k == 'ShopName__exact':
                    #  v = 'Wish-' + v.zfill(4)
                    # messages.error(request, v)
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')

        return qs
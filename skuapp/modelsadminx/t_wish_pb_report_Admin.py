#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_wish_pb_report_Admin.py
 @time: 2018-06-16 15:17
"""

from django.contrib import messages
from django.db.models import Sum
from skuapp.table.t_wish_pb_report import t_wish_pb_report_meta, t_wish_pb_report

class t_wish_pb_report_Admin(object):
    t_wish_pb_left_menu = True
    search_box_flag = True
    wishpb_report = True

    list_display_links = ('id',)
    list_display = ('createuser', 'spend', 'gmv', 'spend_gmv')

    def get_list_queryset(self):
        request = self.request
        qs = super(t_wish_pb_report_Admin, self).get_list_queryset()

        flag = request.user.username

        oo = request.GET.get('o', '')
        createuser = request.GET.get('createuser', '')

        pdate_Start = request.GET.get('pdate_Start', '')
        pdate_End = request.GET.get('pdate_End', '')

        searchList = {
                      'createuser__exact': createuser,

                      'p_date__gte': pdate_Start,
                      'p_date__lt': pdate_End,
                      }

        sl = {}
        for k, v in searchList.items():
            if v is not None and v.strip() != '':
                sl[k] = v

        s2 = {'flag__exact': flag}
        if createuser != '':
            s2['createuser__exact'] = createuser

        try:
            if sl is None:
                qs = t_wish_pb_report_meta.objects.all()
            else:
                qs = t_wish_pb_report_meta.objects.filter(**sl)

            qs = qs.values('createuser').annotate(spend=Sum('spend'), gmv=Sum('gmv'), AS=Sum('spend')/Sum('gmv')).values('createuser', 'spend', 'gmv', 'AS').order_by()

            cuserlist = []
            for obj in qs:
                spend_gmv = None if obj['AS'] is None else round(obj['AS'], 4)*100
                values = {'spend': obj['spend'], 'gmv': obj['gmv'], 'spend_gmv': spend_gmv}
                t_wish_pb_report.objects.update_or_create(defaults=values, createuser=obj['createuser'], flag=flag)
                cuserlist.append(obj['createuser'])

            # 没有更新到的user要置为0
            t_wish_pb_report.objects.filter(flag=flag).exclude(createuser__in=cuserlist).update(spend=0, gmv=0, spend_gmv=0)

            #t_wish_pb_report.save()
            qs = t_wish_pb_report.objects.filter(**s2)
            if oo != '':  # 点了排序
                oo = oo.split('.')
                qs = qs.order_by(*oo)
            else:
                qs = qs.order_by('spend_gmv')

        except Exception, ex:
            messages.error(request, 'err:%s' % repr(ex))

        return qs
# -*- coding: utf-8 -*-
from skuapp.table.d_work_report import *

class d_work_report_Admin(object):
    search_box_flag = True
    list_display = (
        'id', 'ReportMan', 'Department', 'ReportDateDay', 'JobContent', 'MeetProblem', 'Harvest', 'Others',)
    list_editable = ( 'ReportDateDay', 'JobContent', 'MeetProblem', 'Harvest', 'Others',)
    
    def get_list_queryset(self):
        request = self.request
        qs = super(d_work_report_Admin, self).get_list_queryset()


        ReportMan = request.GET.get('ReportMan', '')
        Department = request.GET.get('Department', '')

        ReportDateDayStart = request.GET.get('ReportDateDayStart', '')
        ReportDateDayEnd = request.GET.get('ReportDateDayEnd', '')



        searchList = {'ReportMan__exact': ReportMan,
                      'Department__exact': Department,

                      'ReportDateDay__gte': ReportDateDayStart, 'ReportDateDay__lt': ReportDateDayEnd,
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
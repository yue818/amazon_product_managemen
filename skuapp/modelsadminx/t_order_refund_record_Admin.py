# -*-coding=utf-8-*-
from django.contrib import messages


class t_order_refund_record_Admin(object):

    search_box_flag = True

    list_display = ('id','Submiter', 'SubmitTime','ExStatus', 'StaTime','EndTime', 'URL')
    list_display_links = ('id')
    fields = ('StaTime', 'EndTime')


    def get_list_queryset(self, ):
        request = self.request
        qs = super(t_order_refund_record_Admin, self).get_list_queryset()
        submiter = request.GET.get('Submiter', '')
        exStatus = request.GET.get('ExStatus', '')
        submitTimeStart = request.GET.get('SubmitTimeStart', '')
        submitTimeEnd = request.GET.get('SubmitTimeEnd', '')
        staTimeStart = request.GET.get('StaTimeStart', '')
        staTimeEnd = request.GET.get('StaTimeEnd', '')
        endTimeStart = request.GET.get('EndTimeStart', '')
        endTimeEnd = request.GET.get('EndTimeEnd', '')

        searchList = {'Submiter__exact': submiter, 'ExStatus__exact': exStatus,
                      'SubmitTime__gte': submitTimeStart, 'SubmitTime__lt': submitTimeEnd,
                      'StaTime__gte': staTimeStart, 'StaTime__lt': staTimeEnd,
                      'SubmitTime__gte': submitTimeStart, 'SubmitTime__lt': submitTimeEnd,
                      'EndTime__gte': endTimeStart, 'EndTime__lt': endTimeEnd,
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

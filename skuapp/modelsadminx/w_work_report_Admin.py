# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from Project.settings import *
import datetime
import oss2

class w_work_report_Admin(object):
    search_box_flag = True

    def show_AttachmentUrls(self, obj):
        attachmentUrl1 = "";
        attachmentUrl2 = "";
        attachmentUrl3 = "";
        rt = ''
        if obj.AttachmentUrl1 is not None and str(obj.AttachmentUrl1).strip() !='' :
            # attachmentUrl1 =  u'%s%s.%s/%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'report',obj.id,datetime.datetime.now().strftime('%Y%m%d%H%M%S'),obj.AttachmentUrl1)
            attachmentUrl1 =  u'%s%s.%s/report/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,obj.id,str(obj.AttachmentUrl1)[2:])
            rt="%s附件一:<a href=%s>%s</a>;<br>"%(rt,attachmentUrl1,str(obj.AttachmentUrl1)[2:])
        if obj.AttachmentUrl2 is not None and str(obj.AttachmentUrl2).strip() !='' :
            # attachmentUrl2 =  u'%s%s.%s/%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'report',obj.id,datetime.datetime.now().strftime('%Y%m%d%H%M%S'),obj.AttachmentUrl2)
            attachmentUrl2 =  u'%s%s.%s/report/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,obj.id,str(obj.AttachmentUrl2)[2:])
            rt="%s附件二:<a href=%s>%s</a>;<br>"%(rt,attachmentUrl2,str(obj.AttachmentUrl2)[2:])

        # rt =  "附件一:<a href=%s>%s</a>;<br>附件二:<a href=%s>%s</a><br>附件三:<a href=%s>%s</a><br>附件四:<a href=%s>%s</a><br>附件五:<a href=%s>%s</a><br>附件六:<a href=%s>%s</a>;"%(attachmentUrl1,attachmentUrl1,attachmentUrl2,attachmentUrl2,attachmentUrl3,attachmentUrl3,attachmentUrl4,attachmentUrl4,attachmentUrl5,attachmentUrl5,attachmentUrl6,attachmentUrl6)
        return mark_safe(rt)
    show_AttachmentUrls.short_description = u'附件'

    list_display = (
    'ReportMan', 'Department', 'ReportDate', 'LastWweekPlan', 'ThisWeekPlan', 'NextWeekPlan', 'WorkSummary',
    'UnsolvedProblems', 'SolveMethod', 'SolveTime', 'ReportWeek','show_ReportWeekDayStart','show_ReportWeekDayEnd','show_AttachmentUrls',)
    list_editable = ('SolveTime', 'SolveMethod','ThisWeekPlan','ThisWeekPlan','NextWeekPlan','WorkSummary',)

    form_layout = (
        Fieldset(u'基本信息',
                 Row('ReportWeek', 'ReportMan', 'Department', ),
                 css_class='unsort '
                 ),
        Fieldset(u'最近计划',
                 Row('LastWweekPlan', ),
                 Row('ThisWeekPlan', ),
                 Row('NextWeekPlan', ),
                 css_class='unsort  '
                 ),
        Fieldset(u'总结与反思',
                 Row('WorkSummary', ),
                 Row('UnsolvedProblems', ),
                 Row('AttachmentUrl1', 'AttachmentUrl2'),
                 Row('SolveTime', ),
                 Row('SolveMethod', ),
                 css_class='unsort '
                 )
    )

    def save_models(self):
        obj = self.new_obj
        request = self.request
        obj.save()
        if obj.ReportWeek is not None :
            auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
            bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_TORT)

            if obj.AttachmentUrl1 is not None and str(obj.AttachmentUrl1).strip() !='' :
                # bucket.put_object('report/' + str(obj.id) + '/' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '/' + u'%s'%str(obj.AttachmentUrl1)[2:],obj.AttachmentUrl1)
                bucket.put_object(u'report/%s/%s'%(obj.id,str(obj.AttachmentUrl1)[2:]),obj.AttachmentUrl1)

            if obj.AttachmentUrl2 is not None and str(obj.AttachmentUrl2).strip() !='' :
                bucket.put_object(u'report/%s/%s'%(obj.id,str(obj.AttachmentUrl2)[2:]),obj.AttachmentUrl2)

            obj.save()

    #显示报告周的开始和结束日期（周日至周六）
    def show_ReportWeekDayStart(self,obj):
        ReportDate_Week = int(obj.ReportDate.isocalendar()[1])
        ReportDate_Day = int(obj.ReportDate.isocalendar()[2])
        ReportWeekDayStart = ""
        if ReportDate_Week == int(obj.ReportWeek):
            ReportWeekDayStart = obj.ReportDate - datetime.timedelta(days=ReportDate_Day)
        elif ReportDate_Week == int(obj.ReportWeek)+1:
            ReportWeekDayStart = obj.ReportDate - datetime.timedelta(days=ReportDate_Day) - datetime.timedelta(days=7)
        else :
            ReportWeekDayStart =""

        rt = u'%s'%(ReportWeekDayStart.strftime('%Y年%m月%d日'))
        return mark_safe(rt)
    show_ReportWeekDayStart.short_description=u'报告周<br>开始日期'
    
    def show_ReportWeekDayEnd(self,obj):
        ReportDate_Week = int(obj.ReportDate.isocalendar()[1])
        ReportDate_Day = int(obj.ReportDate.isocalendar()[2])
        ReportWeekDayStart = ""
        if ReportDate_Week == int(obj.ReportWeek):
            ReportWeekDayEnd = obj.ReportDate - datetime.timedelta(days=ReportDate_Day) + datetime.timedelta(days=6)
        elif ReportDate_Week == int(obj.ReportWeek)+1:
            ReportWeekDayEnd = obj.ReportDate - datetime.timedelta(days=ReportDate_Day) - datetime.timedelta(days=1)
        else :
            ReportWeekDayEnd =""

        rt = u'%s'%(ReportWeekDayEnd.strftime('%Y年%m月%d日'))
        return mark_safe(rt)
    show_ReportWeekDayEnd.short_description=u'报告周<br>结束日期'
    
    
    

    def get_list_queryset(self):
        request = self.request
        qs = super(w_work_report_Admin, self).get_list_queryset()

        ReportWeek = request.GET.get('ReportWeek', '')
        ReportMan = request.GET.get('ReportMan', '')
        Department = request.GET.get('Department', '')
        SolveMethod = request.GET.get('SolveMethod', '')

        ReportDateStart = request.GET.get('ReportDateStart', '')
        ReportDateEnd = request.GET.get('ReportDateEnd', '')



        searchList = {'ReportWeek__exact': ReportWeek, 'ReportMan__exact': ReportMan,
                      'Department__exact': Department,'SolveMethod__exact': SolveMethod,

                      'ReportDate__gte': ReportDateStart, 'ReportDate__lt': ReportDateEnd,
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
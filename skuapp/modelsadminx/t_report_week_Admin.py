# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import F ,Q


class t_report_week_Admin(object):

    def getYearWeek(self,strdate):
        xxx = strdate.isocalendar()
        YearWeek = '%s%02d'%(xxx[0],xxx[1])
        return YearWeek

    def update_yearweek(self,step_id,step_time,staff_name):#2017-06-29
        if  step_time is   None :
            return
        yearweek_objs1 = t_report_week.objects.filter(YearWeek=step_time,StepID=step_id)
        yearweek_objs2 = yearweek_objs1.filter(StaffName=staff_name)

        if yearweek_objs2.exists()  :
            yearweek_objs2.update(SelfCount=F('SelfCount')+1)
        if not yearweek_objs2.exists():
            obj           = t_report_week()
            obj.YearWeek  = step_time
            obj.StepID    = step_id
            obj.StaffName = staff_name
            obj.SelfCount = 1
            obj.save()


    list_display=('id','YearWeek','AllCount','SelfCount','Avg','Number','StepID','StaffName','Rank')
    search_fields=('id','YearWeek','AllCount','SelfCount','Avg','Number','StepID','StaffName','Rank')
    list_filter = ('id','YearWeek','AllCount','SelfCount','Avg','Number','StepID','StaffName','Rank')

    data_charts = {
        "总数": {'title': u"总数", "x-field": ("YearWeek"), "y-field": ('AllCount'), "order": ('YearWeek',)},
        "人数": {'title': u"人数", "x-field": ("YearWeek"), "y-field": ('Number'), "order": ('YearWeek',)},
        "排名": {'title': u"排名", "x-field": "YearWeek", "y-field": ("Rank"), "order": ('YearWeek',)},
        "平均数-自己总数": {'title': u"平均数-自己总数", "x-field": "YearWeek", "y-field": ('Avg','SelfCount',), "order": ('YearWeek',)}
    }

    #actions = ['to_Syn','to_rank']
    def to_Syn(self,request,queryset):
        all_objs = t_product_enter_ed.objects.all()

        for all_obj in all_objs:
            if all_obj.DYStaffName is not None and all_obj.DYTime is not None:
                DYTime = self.getYearWeek(all_obj.DYTime)  #201726
                self.update_yearweek('DY',DYTime,all_obj.DYStaffName)

            if all_obj.JZLStaffName is not None and all_obj.JZLTime is not None:
                JZLTime = self.getYearWeek(all_obj.JZLTime)  #201726
                self.update_yearweek('JZL',JZLTime,all_obj.JZLStaffName)

            if all_obj.XJStaffName is not None and all_obj.XJTime is not None:
                XJTime = self.getYearWeek(all_obj.XJTime)  #201726
                self.update_yearweek('XJ',XJTime,all_obj.XJStaffName)

            if all_obj.KFStaffName is not None and all_obj.KFTime is not None:
                KFTime = self.getYearWeek(all_obj.KFTime)  #201726
                self.update_yearweek('KF',KFTime,all_obj.KFStaffName)
    to_Syn.short_description = u'同步到周统计'

    def to_rank(self,request,queryset):
        user_objs = t_report_week.objects.all()
        for user_obj in user_objs:
            #rank_objs1 = t_report_week.objects.filter(SelfCount__gt=user_obj.SelfCount,YearWeek=user_obj.YearWeek,StepID=user_obj.StepID)
            rank_objs2 = t_report_week.objects.filter(YearWeek=user_obj.YearWeek,StepID=user_obj.StepID)
            rank_objs1 = rank_objs2.filter(SelfCount__gt=user_obj.SelfCount)
            if rank_objs1.exists() and rank_objs2.exists():
                user_obj.Rank   =  (rank_objs1.count() +1)*(-1)
                user_obj.save()
            if not rank_objs1.exists() and not rank_objs2.exists():
                pass
            if not rank_objs1.exists() and rank_objs2.exists():
                user_obj.Rank   =  -1
                user_obj.save()
            if rank_objs1.exists() and not  rank_objs2.exists():
                pass
    to_rank.short_description = u'排名统计'
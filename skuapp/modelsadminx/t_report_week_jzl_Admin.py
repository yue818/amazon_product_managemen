# -*- coding: utf-8 -*-
from .t_report_week_Admin import *
class t_report_week_jzl_Admin(t_report_week_Admin):

    def get_list_queryset(self):
        request = self.request
        qs = super(t_report_week_jzl_Admin, self).get_list_queryset().filter(StepID='JZL')
        if request.user.is_superuser:
            return qs
        return qs.filter(StaffName = request.user.first_name)

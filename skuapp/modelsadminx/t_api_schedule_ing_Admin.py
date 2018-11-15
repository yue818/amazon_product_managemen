# -*- coding: utf-8 -*-
class t_api_schedule_ing_Admin(object):
    list_display=('id', 'ShopName','PlatformName','CMDID','ScheduleTime','ActualBeginTime','ActualEndTime','Status','ProcessingStatus','Processed','Successful','WithError','WithWarning','TransactionID','InsertTime','UpdateTime','Timedelta','RetryCount',)
    list_filter = ('ScheduleTime','ActualBeginTime','ActualEndTime','Status','ProcessingStatus','InsertTime','UpdateTime')
    search_fields = ('id', 'ShopName','PlatformName','CMDID','ProcessingStatus','TransactionID','Params')


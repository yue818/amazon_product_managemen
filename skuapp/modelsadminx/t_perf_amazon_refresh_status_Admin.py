# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_perf_amazon_refresh_status_Admin.py
 @time: 2018/9/25 10:11
"""
from django.utils.safestring import mark_safe
import datetime
from django.contrib import messages
from django.db.models import Q


class t_perf_amazon_refresh_status_Admin(object):
    amazon_site_left_menu_tree_flag = True
    search_box_flag = True

    def show_product_status(self, obj):
        now = datetime.datetime.now()
        today_zero = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
        if obj.product_refresh_status != 'Success' and obj.product_refresh_remark != '_DONE_NO_DATA_' or obj.product_refresh_begin_time < today_zero:
            style_html = '<p style="color:red; word-break:break-all;">'
        else:
            style_html = '<p style="color:green">'

        product_status_html = '''
        刷新结果：%s <br>
        开始时间：%s <br>
        结束时间：%s <br>
        备       注：%s       
        ''' % (obj.product_refresh_status, obj.product_refresh_begin_time, obj.product_refresh_end_time, obj.product_refresh_remark)
        product_status_html = style_html + product_status_html + '</p>'
        return mark_safe(product_status_html)
    show_product_status.short_description = mark_safe('<p style="color:#428BCA" align="center">商品列表</p>')

    def show_fba_status(self, obj):
        now = datetime.datetime.now()
        today_zero = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
        if obj.fba_refresh_status != 'Success' and obj.fba_refresh_remark != '_DONE_NO_DATA_' or obj.fba_refresh_begin_time < today_zero:
            style_html = '<p style="color:red; word-break:break-all;">'
        else:
            style_html = '<p style="color:green">'

        fba_status_html = '''
        刷新结果：%s <br>
        开始时间：%s <br>
        结束时间：%s <br>
        备       注：%s        
        ''' % (obj.fba_refresh_status, obj.fba_refresh_begin_time, obj.fba_refresh_end_time, obj.fba_refresh_remark)
        fba_status_html = style_html + fba_status_html + '</p>'
        return mark_safe(fba_status_html)
    show_fba_status.short_description = mark_safe('<p style="color:#428BCA" align="center">FBA库存</p>')

    def show_order_status(self, obj):
        now = datetime.datetime.now()
        today_zero = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
        if obj.order_refresh_status != 'Success' and obj.order_refresh_remark != '_DONE_NO_DATA_' or obj.order_refresh_begin_time < today_zero:
            style_html = '<p style="color:red; word-break:break-all;">'
        else:
            style_html = '<p style="color:green">'

        order_status_html = '''
        刷新结果：%s <br>
        开始时间：%s <br>
        结束时间：%s <br>
        备       注：%s            
        ''' % (obj.order_refresh_status, obj.order_refresh_begin_time, obj.order_refresh_end_time, obj.order_refresh_remark)
        order_status_html = style_html + order_status_html + '</p>'
        return mark_safe(order_status_html)
    show_order_status.short_description = mark_safe('<p style="color:#428BCA" align="center">订单</p>')

    def show_receive_status(self, obj):
        now = datetime.datetime.now()
        today_zero = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
        if obj.receive_refresh_status != 'Success' and obj.receive_refresh_remark != '_DONE_NO_DATA_' or obj.receive_refresh_begin_time < today_zero:
            style_html = '<p style="color:red; word-break:break-all;">'
        else:
            style_html = '<p style="color:green">'

        receive_status_html = '''
        刷新结果：%s <br>
        开始时间：%s <br>
        结束时间：%s <br>
        备       注：%s         
        ''' % (obj.receive_refresh_status, obj.receive_refresh_begin_time, obj.receive_refresh_end_time, obj.receive_refresh_remark)
        receive_status_html = style_html + receive_status_html + '</p>'
        return mark_safe(receive_status_html)
    show_receive_status.short_description = mark_safe('<p style="color:#428BCA" align="center">到货日期</p>')

    def show_fee_status(self, obj):
        now = datetime.datetime.now()
        today_zero = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
        if obj.fee_refresh_status != 'Success' and obj.fee_refresh_remark != '_DONE_NO_DATA_' or obj.fee_refresh_begin_time < today_zero:
            style_html = '<p style="color:red; word-break:break-all;">'
        else:
            style_html = '<p style="color:green">'

        fee_status_html = '''
        刷新结果：%s <br>
        开始时间：%s <br>
        结束时间：%s <br>
         备       注：%s        
        ''' % (obj.fee_refresh_status, obj.fee_refresh_begin_time, obj.fee_refresh_end_time, obj.fee_refresh_remark)
        fee_status_html = style_html + fee_status_html + '</p>'
        return mark_safe(fee_status_html)
    show_fee_status.short_description = mark_safe('<p style="color:#428BCA" align="center">预览费用</p>')

    def show_remove_status(self, obj):
        now = datetime.datetime.now()
        today_zero = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
        if obj.remove_refresh_status != 'Success' and obj.remove_refresh_remark != '_DONE_NO_DATA_' or obj.remove_refresh_begin_time < today_zero:
            style_html = '<p style="color:red; word-break:break-all;">'
        else:
            style_html = '<p style="color:green">'

        remove_status_html = '''
        刷新结果：%s <br>
        开始时间：%s <br>
        结束时间：%s <br>
        备       注：%s         
        ''' % (obj.remove_refresh_status, obj.remove_refresh_begin_time, obj.remove_refresh_end_time, obj.remove_refresh_remark)
        remove_status_html = style_html + remove_status_html + '</p>'
        return mark_safe(remove_status_html)
    show_remove_status.short_description = mark_safe('<p style="color:#428BCA" align="center">移除订单</p>')

    def show_finance_status(self, obj):
        now = datetime.datetime.now()
        today_zero = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
        if obj.finance_refresh_status != 'Success' and obj.finance_refresh_remark != '_DONE_NO_DATA_' or obj.finance_refresh_begin_time < today_zero:
            style_html = '<p style="color:red; word-break:break-all;">'
        else:
            style_html = '<p style="color:green">'

        finance_status_html = '''
        刷新结果：%s <br>
        开始时间：%s <br>
        结束时间：%s <br>
        备       注：%s          
        ''' % (obj.finance_refresh_status, obj.finance_refresh_begin_time, obj.finance_refresh_end_time, obj.finance_refresh_remark)
        finance_status_html = style_html + finance_status_html + '</p>'
        return mark_safe(finance_status_html)
    show_finance_status.short_description = mark_safe('<p style="color:#428BCA" align="center">退款订单</p>')

    def show_actionable_status(self, obj):
        now = datetime.datetime.now()
        today_zero = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
        if obj.actionable_refresh_status != 'Success' and obj.actionable_refresh_remark != '_DONE_NO_DATA_' or obj.actionable_refresh_begin_time < today_zero:
            style_html = '<p style="color:red; word-break:break-all;">'
        else:
            style_html = '<p style="color:green">'

        actionable_status_html = '''
        刷新结果：%s <br>
        开始时间：%s <br>
        结束时间：%s <br>
        备       注：%s          
        ''' % (obj.actionable_refresh_status, obj.actionable_refresh_begin_time, obj.actionable_refresh_end_time, obj.actionable_refresh_remark)
        actionable_status_html = style_html + actionable_status_html + '</p>'
        return mark_safe(actionable_status_html)
    show_actionable_status.short_description = mark_safe('<p style="color:#428BCA" align="center">未发货订单</p>')

    def show_actionable_status(self, obj):
        now = datetime.datetime.now()
        today_zero = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
        if obj.actionable_refresh_status != 'Success' and obj.actionable_refresh_remark != '_DONE_NO_DATA_' or obj.actionable_refresh_begin_time < today_zero:
            style_html = '<p style="color:red; word-break:break-all;">'
        else:
            style_html = '<p style="color:green">'

        actionable_status_html = '''
        刷新结果：%s <br>
        开始时间：%s <br>
        结束时间：%s <br>
        备       注：%s          
        ''' % (obj.actionable_refresh_status, obj.actionable_refresh_begin_time, obj.actionable_refresh_end_time, obj.actionable_refresh_remark)
        actionable_status_html = style_html + actionable_status_html + '</p>'
        return mark_safe(actionable_status_html)
    show_actionable_status.short_description = mark_safe('<p style="color:#428BCA" align="center">未发货订单</p>')

    def show_odr_status(self, obj):
        now = datetime.datetime.now()
        today_zero = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
        if obj.odr_refresh_status != 'Success' and obj.odr_refresh_remark != '_DONE_NO_DATA_' or obj.odr_refresh_begin_time < today_zero:
            style_html = '<p style="color:red; word-break:break-all;">'
        else:
            style_html = '<p style="color:green">'

        odr_status_html = '''
        刷新结果：%s <br>
        开始时间：%s <br>
        结束时间：%s <br>
        备       注：%s          
        ''' % (obj.odr_refresh_status, obj.odr_refresh_begin_time, obj.odr_refresh_end_time, obj.odr_refresh_remark)
        odr_status_html = style_html + odr_status_html + '</p>'
        return mark_safe(odr_status_html)
    show_odr_status.short_description = mark_safe('<p style="color:#428BCA" align="center">缺陷订单</p>')

    list_display = ('id', 'name', 'show_product_status', 'show_fba_status', 'show_order_status', 'show_receive_status',
                    'show_fee_status', 'show_remove_status', 'show_finance_status', 'show_actionable_status',)

    def get_list_queryset(self, ):
        qs = super(t_perf_amazon_refresh_status_Admin, self).get_list_queryset().filter(is_valid__exact=1)

        request = self.request
        name = request.GET.get('name', '')
        refresh_result = request.GET.get('refresh_result', '')

        now = datetime.datetime.now()
        today_zero = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)

        if refresh_result == '-1':
            # qs = qs.exclude(Q(product_refresh_status='Success') & Q(product_refresh_remark='_DONE_NO_DATA_') | Q(product_refresh_begin_time=today_zero))
            qs = qs.filter(Q(~Q(product_refresh_status='Success') & ~Q(product_refresh_remark='_DONE_NO_DATA_') | Q(product_refresh_begin_time__lte=today_zero)) |
                           Q(~Q(fba_refresh_status='Success') & ~Q(fba_refresh_remark='_DONE_NO_DATA_') | Q(fba_refresh_begin_time__lte=today_zero)) |
                           Q(~Q(order_refresh_status='Success') & ~Q(order_refresh_remark='_DONE_NO_DATA_') | Q(order_refresh_begin_time__lte=today_zero)) |
                           Q(~Q(receive_refresh_status='Success') & ~Q(receive_refresh_remark='_DONE_NO_DATA_') | Q(receive_refresh_begin_time__lte=today_zero)) |
                           Q(~Q(fee_refresh_status='Success') & ~Q(fee_refresh_remark='_DONE_NO_DATA_') | Q(fee_refresh_begin_time__lte=today_zero)) |
                           Q(~Q(remove_refresh_status='Success') & ~Q(remove_refresh_remark='_DONE_NO_DATA_') | Q(remove_refresh_begin_time__lte=today_zero)) |
                           Q(~Q(finance_refresh_status='Success') & ~Q(finance_refresh_remark='_DONE_NO_DATA_') | Q(finance_refresh_begin_time__lte=today_zero)) |
                           Q(~Q(actionable_refresh_status='Success') & ~Q(actionable_refresh_remark='_DONE_NO_DATA_') | Q(actionable_refresh_begin_time__lte=today_zero))
                           # |Q(~Q(odr_refresh_status='Success') & ~Q(odr_refresh_remark='_DONE_NO_DATA_') | Q(odr_refresh_begin_time__lte=today_zero))
                           )
        elif refresh_result == '1':
            qs = qs.filter(Q(Q(product_refresh_status='Success') | Q(product_refresh_remark='_DONE_NO_DATA_') & Q(product_refresh_begin_time__gte=today_zero)) &
                           Q(Q(fba_refresh_status='Success') | Q(fba_refresh_remark='_DONE_NO_DATA_') & Q(fba_refresh_begin_time__gte=today_zero)) &
                           Q(Q(order_refresh_status='Success') | Q(order_refresh_remark='_DONE_NO_DATA_') & Q(order_refresh_begin_time__gte=today_zero)) &
                           Q(Q(receive_refresh_status='Success') | Q(receive_refresh_remark='_DONE_NO_DATA_') & Q(receive_refresh_begin_time__gte=today_zero)) &
                           Q(Q(fee_refresh_status='Success') | Q(fee_refresh_remark='_DONE_NO_DATA_') & Q(fee_refresh_begin_time__gte=today_zero)) &
                           Q(Q(remove_refresh_status='Success') | Q(remove_refresh_remark='_DONE_NO_DATA_') & Q(remove_refresh_begin_time__gte=today_zero)) &
                           Q(Q(finance_refresh_status='Success') | Q(finance_refresh_remark='_DONE_NO_DATA_') & Q(finance_refresh_begin_time__gte=today_zero)) &
                           Q(Q(actionable_refresh_status='Success') | Q(actionable_refresh_remark='_DONE_NO_DATA_') & Q(actionable_refresh_begin_time__gte=today_zero))
                           # & Q(Q(odr_refresh_status='Success') | Q(odr_refresh_remark='_DONE_NO_DATA_') & Q(odr_refresh_begin_time__gte=today_zero))
                           )
        else:
            pass

        search_list = {
                      'name__icontains': name,
                      }
        sl = {}
        for k, v in search_list.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and str(v).strip() != '':
                    sl[k] = v
        if sl is not None:
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'Please enter the correct content!')
        return qs

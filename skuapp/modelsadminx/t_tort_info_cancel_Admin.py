#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_tort_info_cancel_Admin.py
 @time: 2018-05-08 17:48
"""

from datetime import datetime
from django.utils.safestring import mark_safe
from Project.settings import *
from django.contrib import messages
from skuapp.table.t_tort_info_cancel import t_tort_info_cancel
from skuapp.public.const import tort
from skuapp.public.MyException import MyException as myerr

class t_tort_info_cancel_Admin(object):
    search_box_flag = True
    t_tort_tree_menu_flag = True

    def show_ProductPicUrl(self, obj):
        url = u'%s%s.%s/%s/%s/%s'%(PREFIX, BUCKETNAME_TORT, ENDPOINT_OUT, 'aliexpress', obj.ID, str(obj.ProductPicUrl))
        alt = u'无法显示:%s,%s' % (obj.Site, obj.MainSKU)
        title = 'Site:%s,MainSKU:%s' % (obj.Site, obj.MainSKU)
        rt = '<img src="%s"  width="150" height="150"  alt = "%s"  title="%s"  />  ' % (url, alt, title)
        return mark_safe(rt)
    show_ProductPicUrl.short_description = mark_safe('<p style="color:#428bca;text-align:center">产品图片</p>')

    def show_Site(self, obj):
        return mark_safe(obj.Site)

    show_Site.short_description = mark_safe('<p style="color:#428bca;">侵权站点</p>')

    list_display = ('ID', 'show_ProductPicUrl', 'show_Site', 'MainSKU', 'Intellectual', 'IntellectualCode', 'Trademark', 'ComplainReason',
                    'IPRange', 'IPForbiddenSite', 'SourceUrl', 'Suggestion', 'CancelReason')

    readonly_fields = ('ID', 'Site', 'MainSKU', 'Intellectual', 'IntellectualCode', 'Trademark', 'ComplainReason',
                    'IPRange', 'IPForbiddenSite', 'SourceUrl', 'Suggestion',)

    fields = ('ID', 'Site', 'MainSKU', 'Intellectual', 'IntellectualCode', 'Trademark', 'ComplainReason',
                    'IPRange', 'IPForbiddenSite', 'SourceUrl', 'Suggestion', 'CancelReason')

    list_editable = ('CancelReason')

    actions = ['to_commit', ]

    def to_commit(self, request, objs):

        cnt = 0
        for obj in objs:
            try:
                if obj.CancelReason is None or len(obj.CancelReason) == 0:
                    raise(myerr('10004', u'流水号为%s.'% obj.ID))  # u'请填写撤销侵权原因,流水号为%s.' % obj.ID

                t_tort_info_cancel_obj = t_tort_info_cancel()
                t_tort_info_cancel_obj.__dict__ = obj.__dict__
                t_tort_info_cancel_obj.CancelStaffID = request.user.first_name
                t_tort_info_cancel_obj.CancelTime = datetime.now()
                t_tort_info_cancel_obj.Step = tort.CANCEL_WAIT_AUDIT
                t_tort_info_cancel_obj.save()
                cnt += 1
            except myerr, e:
                messages.error(request, '{0}{1}'.format(e, e.todo))
                continue

        messages.info(request, u'提交审核%d条记录,成功发送%d条.'%(objs.count(), cnt))

    to_commit.short_description = u'提交审核(撤销侵权)'

    def save_models(self):

        obj = self.new_obj
        request = self.request
        Step = obj.Step
        obj.save()
        if Step in (2, 3, 21):
            Step = '2,3,21'

        post = request.POST
        post['_redirect'] = '/Project/admin/skuapp/t_tort_info_cancel/?Step=%s'%(Step,)

    def get_list_queryset(self):
        request = self.request
        qs = super(t_tort_info_cancel_Admin, self).get_list_queryset()

        Step = request.GET.get('Step', '')
        if Step != '':
            Step = Step.split(',')
        MainSKU = request.GET.get('MainSKU', '')
        Site = request.GET.get('Site', '')
        Intellectual = request.GET.get('Intellectual', '')
        StaffID = request.GET.get('StaffID', '')

        TimeStart = request.GET.get('TimeNameStart', '')
        TimeEnd = request.GET.get('TimeNameEnd', '')

        AuditTimeStart = request.GET.get('AuditTimeStart', '')
        AuditTimeEnd = request.GET.get('AuditTimeEnd', '')

        searchList = {'Step__in': Step,
                      'MainSKU__exact': MainSKU,
                      'Site__exact': Site,
                      'Intellectual__exact': Intellectual,
                      'StaffID__exact': StaffID,
                      'UpdateTime__gte': TimeStart,
                      'UpdateTime__lt': TimeEnd,
                      'DealTime1__gte': AuditTimeStart,
                      'DealTime1__lt': AuditTimeEnd,
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
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有误！')
        return qs
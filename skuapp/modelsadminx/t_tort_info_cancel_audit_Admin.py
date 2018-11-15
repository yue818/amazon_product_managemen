#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_tort_info_cancel_audit_Admin.py
 @time: 2018-05-08 17:49
"""

from datetime import datetime
from django.utils.safestring import mark_safe
from Project.settings import *
from django.contrib import messages
from skuapp.table.t_tort_info_cancel_audit import t_tort_info_cancel_audit
from skuapp.public.const import tort
from skuapp.table.t_online_info_wish import t_online_info_wish
from skuapp.public.MyException import MyException as myerr

class t_tort_info_cancel_audit_Admin(object):
    search_box_flag = True
    t_tort_tree_menu_flag = True

    def show_ProductPicUrl(self, obj):
        url = u'%s%s.%s/%s/%s/%s'%(PREFIX, BUCKETNAME_TORT, ENDPOINT_OUT, 'aliexpress', obj.ID, str(obj.ProductPicUrl))
        alt = u'无法显示:%s,%s' % (obj.Site, obj.MainSKU)
        title = 'Site:%s,MainSKU:%s' % (obj.Site, obj.MainSKU)
        rt = '<img src="%s"  width="150" height="150"  alt = "%s"  title="%s"  />  ' % (url, alt, title)
        return mark_safe(rt)
    show_ProductPicUrl.short_description = mark_safe('<p style="color:#428bca;text-align:center">产品图片</p>')

    def show_AttachmentUrls(self, obj):
        rt = ''
        if obj.AttachmentUrl1 is not None and str(obj.AttachmentUrl1).strip() !='' :
            attachmentUrl1 =  u'%s%s.%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'aliexpress',obj.ID,str(obj.AttachmentUrl1))
            rt="%s<a href=%s>%s</a>;<br>"%(rt,attachmentUrl1, u'附件一')
        if obj.AttachmentUrl2 is not None and str(obj.AttachmentUrl2).strip() !='' :
            attachmentUrl2 =  u'%s%s.%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'aliexpress',obj.ID,str(obj.AttachmentUrl2))
            rt="%s<a href=%s>%s</a>;<br>"%(rt,attachmentUrl2, u'附件二')
        if obj.AttachmentUrl3 is not None and str(obj.AttachmentUrl3).strip() !='' :
            attachmentUrl3 =  u'%s%s.%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'aliexpress',obj.ID,str(obj.AttachmentUrl3))
            rt="%s<a href=%s>%s</a>;<br>"%(rt,attachmentUrl3, u'附件三')
        if obj.AttachmentUrl4 is not None and str(obj.AttachmentUrl4).strip() !='' :
            attachmentUrl4 =  u'%s%s.%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'aliexpress',obj.ID,str(obj.AttachmentUrl4))
            rt="%s<a href=%s>%s</a>;<br>"%(rt,attachmentUrl4, u'附件四')
        if obj.AttachmentUrl5 is not None and str(obj.AttachmentUrl5).strip() !='' :
            attachmentUrl5 =  u'%s%s.%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'aliexpress',obj.ID,str(obj.AttachmentUrl5))
            rt="%s<a href=%s>%s</a>;<br>"%(rt,attachmentUrl5, u'附件五')
        if obj.AttachmentUrl6 is not None and str(obj.AttachmentUrl6).strip() !='' :
            attachmentUrl6 =  u'%s%s.%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'aliexpress',obj.ID,str(obj.AttachmentUrl6))
            rt="%s<a href=%s>%s</a>;<br>"%(rt,attachmentUrl6, u'附件六')

        return mark_safe(rt)
    show_AttachmentUrls.short_description = mark_safe('<p style="color:#428bca;">附件列表</p>')

    def show_Site(self, obj):
        return mark_safe(obj.Site)

    show_Site.short_description = mark_safe('<p style="color:#428bca;">侵权站点</p>')

    list_display = ('ID', 'show_ProductPicUrl', 'show_Site', 'MainSKU', 'show_AttachmentUrls', 'Trademark', 'ComplainReason',
                    'IPRange', 'IPForbiddenSite', 'SourceUrl', 'Suggestion', 'CancelReason')

    readonly_fields = ('ID', 'Site', 'MainSKU', 'Trademark', 'ComplainReason',
                    'IPRange', 'IPForbiddenSite', 'SourceUrl', 'Suggestion', 'CancelReason')


    def to_syn_tort_info(self, mainsku):
        try:
            t_online_info_wish.objects.filter(MainSKU=mainsku).update(TortInfo='N')
            return 1
        except:
            return -1

    actions = ['to_commit', 'to_reject', ]

    def to_commit(self, request, objs):

        cnt = 0
        for obj in objs:
            try:
                res = self.to_syn_tort_info(obj.MainSKU)
                if res < 0:
                    raise (myerr('10006', 'MainSKU:%s'%(obj.MainSKU, )))  # 同步侵权信息有误

                t_tort_info_cancel_audit_obj = t_tort_info_cancel_audit()
                t_tort_info_cancel_audit_obj.__dict__ = obj.__dict__
                t_tort_info_cancel_audit_obj.AttacheID = request.user.first_name
                t_tort_info_cancel_audit_obj.DealTime1 = datetime.now()
                t_tort_info_cancel_audit_obj.Step = tort.CANCEL_WAIT_RECEIVE
                t_tort_info_cancel_audit_obj.OperationState = 'N'
                t_tort_info_cancel_audit_obj.save()
                cnt += 1
            except myerr, e:
                messages.error(request, e+e.todo)
                continue

        messages.info(request, u'审核%d条,成功完成%d条.' % (objs.count(), cnt))

    to_commit.short_description = u'审核完成(撤销侵权)'

    def to_reject(self, request, objs):

        cnt = 0
        for obj in objs:
            t_tort_info_cancel_audit_obj = t_tort_info_cancel_audit()
            t_tort_info_cancel_audit_obj.__dict__ = obj.__dict__
            t_tort_info_cancel_audit_obj.AttacheID = request.user.first_name
            t_tort_info_cancel_audit_obj.DealTime1 = datetime.now()
            t_tort_info_cancel_audit_obj.Step = tort.CANCEL_REJECT
            t_tort_info_cancel_audit_obj.save()
            cnt += 1

        messages.info(request, u'驳回%d条,成功驳回%d条.' % (cnt, cnt))

    to_reject.short_description = u'驳回申请(撤销侵权)'

    def save_models(self):
        obj = self.new_obj
        request = self.request
        obj.save()

        post = request.POST
        post['_redirect'] = '/Project/admin/skuapp/t_tort_info_cancel_audit/?Step=11'

    def get_list_queryset(self):
        request = self.request
        qs = super(t_tort_info_cancel_audit_Admin, self).get_list_queryset()

        Step = request.GET.get('Step', '11')
        if Step != '':
            Step = Step.split(',')
        MainSKU = request.GET.get('MainSKU', '')
        IPForbiddenSite = request.GET.get('IPForbiddenSite', '')
        IPRange = request.GET.get('IPRange', '')
        Intellectual = request.GET.get('Intellectual', '')
        StaffID = request.GET.get('StaffID', '')

        TimeStart = request.GET.get('TimeNameStart', '')
        TimeEnd = request.GET.get('TimeNameEnd', '')

        AuditTimeStart = request.GET.get('AuditTimeStart', '')
        AuditTimeEnd = request.GET.get('AuditTimeEnd', '')

        searchList = {'Step__in': Step,
                      'MainSKU__exact': MainSKU,
                      'IPForbiddenSite__contains': IPForbiddenSite,
                      'Intellectual__exact': Intellectual,
                      'IPRange__exact': IPRange,
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
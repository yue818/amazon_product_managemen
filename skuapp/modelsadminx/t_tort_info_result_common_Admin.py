#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_tort_info_result_no_Admin.py
 @time: 2018-05-07 14:03
"""

from datetime import datetime
from django.utils.safestring import mark_safe
from django.contrib import messages
from Project.settings import *
from skuapp.table.t_tort_info_result_common import t_tort_info_result_common
from skuapp.table.t_sys_department_staff import t_sys_department_staff
from skuapp.table.t_sys_department import t_sys_department
from skuapp.public.const import tort
from skuapp.public.MyException import MyException as myerr

class t_tort_info_result_common_Admin(object):
    search_box_flag = True
    t_tort_tree_menu_flag = True
    
    actions = ['to_reject_audit', ]
    def to_reject_audit(self, request, objs):

        cnt = 0
        for obj in objs:
            t_tort_info_audit_obj = t_tort_info_result_common()
            t_tort_info_audit_obj.__dict__ = obj.__dict__
            t_tort_info_audit_obj.AttacheID = request.user.first_name
            t_tort_info_audit_obj.DealTime1 = datetime.now()
            t_tort_info_audit_obj.Step = tort.WAIT_AUDIT
            t_tort_info_audit_obj.OperationState = 'N'
            t_tort_info_audit_obj.save()
            cnt += 1

        messages.info(request, u'驳回%d条,成功驳回%d条.' % (cnt, cnt))

    to_reject_audit.short_description = u'驳回侵权审核'
    
    def show_ProductPicUrl(self, obj):
        url = u'%s%s.%s/%s/%s/%s' % (PREFIX, BUCKETNAME_TORT, ENDPOINT_OUT, 'aliexpress', obj.ID, str(obj.ProductPicUrl))
        alt = u'无法显示:%s,%s' % (obj.Site, obj.MainSKU)
        title = 'Site:%s,MainSKU:%s' % (obj.Site, obj.MainSKU)
        rt = '<img src="%s"  width="150" height="150"  alt = "%s"  title="%s"  />  ' % (url, alt, title)
        return mark_safe(rt)

    show_ProductPicUrl.short_description = u'<span style="color: #428bca">产品图片</span>'

    def show_ReceiveDetail(self, obj):
        rt = u'<span >%s</span>' % obj.ReceiveDetail
        return mark_safe(rt)

    show_ReceiveDetail.short_description = u'<span style="color: #428bca">领用详细信息</span>'
    
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
    
    def show_detail(self,obj):
        rt = "申请人:<br>%s<br>申请时间:<br>%s<br>采购员:%s<br>业绩归属人2:%s" % (obj.StaffID, obj.UpdateTime,obj.Purchaser, obj.SalerName2)
        
        return mark_safe(rt)
    show_detail.short_description = mark_safe('<span style="width:150px;color:#428bca;">详情</span>')
    
    list_display = ('ID', 'show_ProductPicUrl', 'show_detail', 'Site',
                    'MainSKU', 'ProductTitle', 'Trademark','Intellectual', 'SourceUrl','IPForbiddenSite','IPRange','KeyWord','WordCategory',
                    'ProductID','show_AttachmentUrls', 'Suggestion', 
                    )

    readonly_fields = ('ID',)
    list_display_links = ()
    list_editable = ('WordCategory', 'KeyWord',)
    
    def save_models(self):

        obj = self.new_obj
        request = self.request
        Step = obj.Step
        obj.save()
        if Step in (2, 11):
            Step = '2,11'
        else:
            Step = '3,11'

        post = request.POST
        post['_redirect'] = '/Project/admin/skuapp/t_tort_info_result_common_Admin/?Step=%s'%(Step,)

    def get_list_queryset(self):
        request = self.request
        qs = super(t_tort_info_result_common_Admin, self).get_list_queryset()

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

        EnglishName = request.GET.get('EnglishName', '')
        ProductTitle = request.GET.get('ProductTitle', '')
        KeyWord = request.GET.get('KeyWord', '')
        
        searchList = {'Step__in': Step,
                      'MainSKU__exact': MainSKU,
                      'Site__exact': Site,
                      'EnglishName__icontains': EnglishName,
                      'ProductTitle__icontains': ProductTitle,
                      'Intellectual__exact': Intellectual,
                      'StaffID__exact': StaffID,
                      'UpdateTime__gte': TimeStart,
                      'UpdateTime__lt': TimeEnd,
                      'KeyWord__icontains':KeyWord
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





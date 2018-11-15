# -*-coding:utf-8-*-

from django.utils.safestring import mark_safe
from Project.settings import *
import oss2
from datetime import datetime, timedelta
from django.contrib import messages
from xadmin.layout import Fieldset, Row

class t_copyright_Admin(object):
    registration_recipients_menu = True
    search_box_flag = True
    def show_msg(self,obj):
        rt = ''
        if obj.RecipientsMsg:
            rt = '<table border="1" cellspacing="0" cellpadding="0"><tr><td>领用平台</td><td>领用店铺</td><td>领用人</td><td>领用时间</td><td>领用用途</td></tr>'
            for i in obj.RecipientsMsg.split('^'):
                if i:
                    l = i.split('&')
                    # rt += str(l)
                    rt += "<tr><td>" + l[0] + "</td><td>"+ l[1] + "</td><td>"+ l[2] + "</td><td>"+ l[3] + "</td><td>"+ l[4] + "</td></tr>"
            rt += "</table>"
        return mark_safe(rt)
    show_msg.short_description = mark_safe('<p style="color:#428bca;text-align:left;width:90px">领用信息</p>')

    def show_use(self,obj):
        s = u'/Project/admin/skuapp/t_copyright/%s/update/'%(obj.id)
        rt = """<script type="text/javascript">
                $(document).ready(function(){
                  $("#a%s").click(function(){
                  window.alert('请将领用信息填写完整,否则不录入');
                  });
                });
                </script> 
                <a id=a%s href=%s>%s</a><br>""" % (obj.id, obj.id, s, u'领用')
        return mark_safe(rt)



    show_use.short_description = mark_safe('<p style="color:#428bca;text-align:left;width:90px">版权领用</p>')


    def show_AttachmentUrls1(self,obj) :
        request = self.request
        uname = request.user.username
        rt=''
        if obj.AttachmentUrl1 is not None and str(obj.AttachmentUrl1).strip() !='' :
            attachmentUrl1 =  u'%s%s.%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'copyright',obj.id,str(obj.AttachmentUrl1))
            rt = "%s<a href=%s>%s</a>;<br>" % (rt, attachmentUrl1, u'附件链接')

        return mark_safe(rt)
    show_AttachmentUrls1.short_description = mark_safe('<p style="color:#428bca;text-align:left;width:90px">证书及作品样本</p>')

    def show_AttachmentUrls2(self,obj) :
        request = self.request
        uname = request.user.username
        rt=''
        if obj.AttachmentUrl2 is not None and str(obj.AttachmentUrl2).strip() !='' :
            attachmentUrl2 =  u'%s%s.%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'copyright',obj.id,str(obj.AttachmentUrl2))
            rt = "%s<a href=%s>%s</a>;<br>" % (rt, attachmentUrl2, u'附件链接')

        return mark_safe(rt)
    show_AttachmentUrls2.short_description = mark_safe('<p style="color:#428bca;text-align:left;width:90px">盖章作品样本页</p>')

    def show_warning(self,obj) :
        if obj.Status and obj.CommitDate:
            rt = u'<div style="background:blue;color:white;width:100px;">正在进行中</div>'
            if obj.Status == u'已填报' and (obj.CommitDate + timedelta(days=7)).strftime('%Y-%m-%d') < datetime.now().strftime('%Y-%m-%d'):
                rt = u'<div style="background:yellow;color:black;width:100px;">第一次提醒</div>'
            if obj.Status == u'已填报' and (obj.CommitDate + timedelta(days=30)).strftime('%Y-%m-%d') < datetime.now().strftime('%Y-%m-%d'):
                rt = u'<div style="background:red;color:white;width:100px;">第二次提醒</div>'
            elif obj.Status == u'已受理' and (obj.CommitDate + timedelta(days=30)).strftime('%Y-%m-%d') < datetime.now().strftime('%Y-%m-%d'):
                rt = u'<div style="background:red;color:white;width:100px;">第二次提醒</div>'
            elif obj.Status == u'已登记':
                rt = u'<div style="background:green;color:white;width:100px;">已完成,无提醒</div>'
            elif obj.Status == u'失败':
                rt = u'<div style="background:green;color:white;width:100px;">已完成,无提醒</div>'
            return mark_safe(rt)
        else:
            return mark_safe(u'<div style="background:orange;color:white;width:100px;">缺少参数</div>')
    show_warning.short_description = mark_safe('<p style="color:#428bca;text-align:left;width:90px">超时提醒</p>')

    def save_models(self):
        obj = self.new_obj
        request = self.request
        obj.RecipientsPerson = request.user.username
        obj.RecipientsTime = datetime.now().strftime('%Y-%m-%d')
        if obj.RecipientsPlatform is not None and str(obj.RecipientsPlatform).strip() != '' and obj.RecipientsShop is not None and str(obj.RecipientsShop).strip() != '' and \
        obj.RecipientsPurpose is not None and str(obj.RecipientsPurpose).strip() != '':
            s = str(obj.RecipientsPlatform) + u'&' + str(obj.RecipientsShop) + u'&' + str(obj.RecipientsPerson) + u'&' + \
                str(obj.RecipientsTime) + u'&' + str(obj.RecipientsPurpose) + u'^'
            if obj.RecipientsMsg:
                if s not in obj.RecipientsMsg:
                    obj.RecipientsMsg += s
            else:
                obj.RecipientsMsg = s
        obj.save()
        try:
            auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
            bucket = oss2.Bucket(auth, ENDPOINT, BUCKETNAME_TORT)
            if obj.AttachmentUrl1 is not None and str(obj.AttachmentUrl1).strip() != '':
                bucket.put_object(u'%s/%s/%s' % ('copyright', obj.id, str(obj.AttachmentUrl1)), obj.AttachmentUrl1)

            if obj.AttachmentUrl2 is not None and str(obj.AttachmentUrl2).strip() != '':
                bucket.put_object(u'%s/%s/%s' % ('copyright', obj.id, str(obj.AttachmentUrl2)), obj.AttachmentUrl2)

        except Exception, ex:
            pass

    list_display = ('id', 'SKU', 'WorkTitle', 'WorkClass', 'Status', 'RegistrationNo', 'CertificateType', 'RegistrationDate', 'show_warning','show_AttachmentUrls1', 'show_AttachmentUrls2','show_use','show_msg')
    readonly_fields = ('id',)
    list_display_links = ('id', 'show_use',)
    search_fields = ('id','SKU', 'WorkTitle', 'WorkClass', 'Status', 'RegistrationNo', 'CertificateType', 'RecipientsPlatform',)
    list_filter = ('SKU', 'WorkTitle', 'WorkClass', 'Status', 'RegistrationNo', 'CertificateType', 'RecipientsPlatform',)
    list_editable = ('SKU', 'WorkTitle', 'WorkClass', 'Status', 'RegistrationNo', 'CertificateType', 'RegistrationDate')
    show_detail_fields = ['id']
    fields = ('Source', 'SKU', 'WorkTitle',
              'WorkClass', 'CopyrightArea', 'CopyrightOwner',
              'CompletionDate', 'CommitDate', 'Status',
              'RegistrationNo', 'RegistrationDate', 'CertificateType',
              'RecipientsPlatform', 'RecipientsShop', 'Inputer',
              'RecipientsPurpose',
              'AttachmentUrl1', 'AttachmentUrl2')
    form_layout = (
        Fieldset(u'版权信息',
                 Row('Source', 'SKU', 'WorkTitle'),
                 Row('WorkClass', 'CopyrightArea', 'CopyrightOwner'),
                 Row('CompletionDate', 'CommitDate', 'Status'),
                 Row('RegistrationNo', 'RegistrationDate', 'CertificateType'),
                 Row('Inputer'),
                 Row('AttachmentUrl1', 'AttachmentUrl2'),
                 css_class='unsort '
                 ),
        Fieldset(u'领用信息',
                 Row('RecipientsPlatform', 'RecipientsShop'),
                 Row('RecipientsPurpose'),
                 css_class='unsort '
                 ),
    )


    def get_list_queryset(self):
        request = self.request
        qs = super(t_copyright_Admin, self).get_list_queryset()

        WorkClass = request.GET.get('WorkClass', '')
        CopyrightArea = request.GET.get('CopyrightArea', '')
        Status = request.GET.get('Status', '')
        RecipientsMsg = request.GET.get('RecipientsMsg', '')

        searchList = {'WorkClass__exact': WorkClass,
                      'CopyrightArea__exact': CopyrightArea,
                      'Status__exact': Status,
                      'RecipientsMsg__icontains': RecipientsMsg,
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
                messages.error(request, u'输入的查询数据有问题！')
        return qs

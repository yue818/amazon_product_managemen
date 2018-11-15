# -*-coding:utf-8-*-

from django.utils.safestring import mark_safe
from Project.settings import *
import oss2
from datetime import datetime, timedelta
from django.contrib import messages
from xadmin.layout import Fieldset, Row

class t_patents_Admin(object):
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
        s = u'/Project/admin/skuapp/t_patents/%s/update/'%(obj.id)
        rt = """<script type="text/javascript">
            $(document).ready(function(){
              $("#a%s").click(function(){
              window.alert('请将领用信息填写完整,否则不录入');
              });
            });
            </script> 
            <a id=a%s href=%s>%s</a><br>""" % (obj.id, obj.id, s, u'领用')
        return mark_safe(rt)

    show_use.short_description = mark_safe('<p style="color:#428bca;text-align:left;width:90px">专利领用</p>')


    def show_AttachmentUrls1(self,obj) :
        request = self.request
        uname = request.user.username
        rt=''
        if obj.AttachmentUrl1 is not None and str(obj.AttachmentUrl1).strip() !='' :
            attachmentUrl1 =  u'%s%s.%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'patents',obj.id,str(obj.AttachmentUrl1))
            rt = "%s<a href=%s>%s</a>;<br>" % (rt, attachmentUrl1, u'附件链接')

        return mark_safe(rt)
    show_AttachmentUrls1.short_description = mark_safe('<p style="color:#428bca;text-align:left;width:90px">专利请求书</p>')

    def show_AttachmentUrls2(self,obj) :
        request = self.request
        uname = request.user.username
        rt=''
        if obj.AttachmentUrl2 is not None and str(obj.AttachmentUrl2).strip() !='' :
            attachmentUrl2 =  u'%s%s.%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'patents',obj.id,str(obj.AttachmentUrl2))
            rt = "%s<a href=%s>%s</a>;<br>" % (rt, attachmentUrl2, u'附件链接')

        return mark_safe(rt)
    show_AttachmentUrls2.short_description = mark_safe('<p style="color:#428bca;text-align:left;width:90px">受理通知书</p>')

    def show_AttachmentUrls3(self,obj) :
        request = self.request
        uname = request.user.username
        rt=''
        if obj.AttachmentUrl3 is not None and str(obj.AttachmentUrl3).strip() !='' :
            attachmentUrl3 =  u'%s%s.%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'patents',obj.id,str(obj.AttachmentUrl3))
            rt = "%s<a href=%s>%s</a>;<br>" % (rt, attachmentUrl3, u'附件链接')

        return mark_safe(rt)
    show_AttachmentUrls3.short_description = mark_safe('<p style="color:#428bca;text-align:left;width:90px">授权通知书</p>')

    def show_warning(self,obj) :
        if obj.Status and obj.ApplicationDate:
            rt = u'<div style="background:blue;color:white;width:100px;">正在进行中</div>'
            if obj.Status == u'N/A' and (obj.ApplicationDate + timedelta(days=7)).strftime('%Y-%m-%d') < datetime.now().strftime('%Y-%m-%d'):
                rt = u'<div style="background:yellow;color:black;width:100px;">第一次提醒</div>'
            if obj.Status == u'N/A' and (obj.ApplicationDate + timedelta(days=180)).strftime('%Y-%m-%d') < datetime.now().strftime('%Y-%m-%d'):
                rt = u'<div style="background:red;color:white;width:100px;">第二次提醒</div>'
            elif obj.Status == u'受理' and (obj.ApplicationDate + timedelta(days=180)).strftime('%Y-%m-%d') < datetime.now().strftime('%Y-%m-%d'):
                rt = u'<div style="background:red;color:white;width:100px;">第二次提醒</div>'
            elif obj.Status == u'授权':
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
                bucket.put_object(u'%s/%s/%s' % ('patents', obj.id, str(obj.AttachmentUrl1)), obj.AttachmentUrl1)

            if obj.AttachmentUrl2 is not None and str(obj.AttachmentUrl2).strip() != '':
                bucket.put_object(u'%s/%s/%s' % ('patents', obj.id, str(obj.AttachmentUrl2)), obj.AttachmentUrl2)
            
            if obj.AttachmentUrl3 is not None and str(obj.AttachmentUrl3).strip() != '':
                bucket.put_object(u'%s/%s/%s' % ('patents', obj.id, str(obj.AttachmentUrl3)), obj.AttachmentUrl3)

        except Exception, ex:
            pass

    list_display = ('id', 'SKU', 'PatentTitle', 'PatentClass', 'Status', 'OpenNo', 'PatentType', 'ApplicationDate', 'show_warning', 'show_AttachmentUrls1', 'show_AttachmentUrls2','show_AttachmentUrls3','show_use','show_msg')
    readonly_fields = ('id',)
    list_display_links = ('id', 'show_use',)
    search_fields = ('id', 'SKU', 'PatentTitle', 'PatentClass', 'Status', 'OpenNo', 'PatentType')
    list_filter = ('SKU', 'PatentTitle', 'PatentClass', 'Status', 'OpenNo', 'PatentType')
    list_editable = ('SKU', 'PatentTitle', 'PatentClass', 'Status', 'ApplicationNo', 'OpenNo', 'PatentType', 'ApplicationDate')
    show_detail_fields = ['id']
    fields = ('Source', 'SKU', 'PatentTitle',
              'PatentClass', 'PatentArea', 'PatentOwner',
              'ApplicationDate', 'OpenDate', 'Status',
              'ApplicationNo', 'OpenNo', 'PatentType',
              'RecipientsPlatform', 'RecipientsShop',
              'RecipientsPurpose',
              'AttachmentUrl1', 'AttachmentUrl2', 'AttachmentUrl3')
    form_layout = (
        Fieldset(u'版权信息',
                 Row('Source', 'SKU', 'PatentTitle'),
                 Row('PatentClass', 'PatentArea', 'PatentOwner'),
                 Row('ApplicationDate', 'OpenDate', 'Status'),
                 Row('ApplicationNo', 'OpenNo', 'PatentType'),
                 Row('AttachmentUrl1', 'AttachmentUrl2', 'AttachmentUrl3'),
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
        qs = super(t_patents_Admin, self).get_list_queryset()

        PatentClass = request.GET.get('PatentClass', '')
        PatentArea = request.GET.get('PatentArea', '')
        Status = request.GET.get('Status', '')
        RecipientsMsg = request.GET.get('RecipientsMsg', '')

        searchList = {'PatentClass__exact': PatentClass,
                      'PatentArea__exact': PatentArea,
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












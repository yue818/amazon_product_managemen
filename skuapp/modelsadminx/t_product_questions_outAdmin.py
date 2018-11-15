# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from Project.settings import *
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
import oss2
from skuapp.table.t_product_questions_out import t_product_questions_out
from .t_product_questions_outAdmin import *

class t_product_questions_outAdmin(object):
    search_box_flag = True    
    def show_AttachmentUrls(self,obj) :
        attachmentUrl1="";
        attachmentUrl2="";
        attachmentUrl3="";
        attachmentUrl4="";
        attachmentUrl5="";
        attachmentUrl6="";
        rt=''
        if obj.AttachmentUrl1 is not None and str(obj.AttachmentUrl1).strip() !='' :
            attachmentUrl1 =  u'%s%s.%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'questions',obj.id,str(obj.AttachmentUrl1))
            rt="%s附件一:<a href=%s>%s</a>;<br>"%(rt,attachmentUrl1,attachmentUrl1)
        if obj.AttachmentUrl2 is not None and str(obj.AttachmentUrl2).strip() !='' :
            attachmentUrl2 =  u'%s%s.%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'questions',obj.id,str(obj.AttachmentUrl2))
            rt="%s附件二:<a href=%s>%s</a>;<br>"%(rt,attachmentUrl2,attachmentUrl2)
        if obj.AttachmentUrl3 is not None and str(obj.AttachmentUrl3).strip() !='' :
            attachmentUrl3 =  u'%s%s.%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'questions',obj.id,str(obj.AttachmentUrl3))
            rt="%s附件三:<a href=%s>%s</a>;<br>"%(rt,attachmentUrl3,attachmentUrl3)
        if obj.AttachmentUrl4 is not None and str(obj.AttachmentUrl4).strip() !='' :
            attachmentUrl4 =  u'%s%s.%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'questions',obj.id,str(obj.AttachmentUrl4))
            rt="%s附件四:<a href=%s>%s</a>;<br>"%(rt,attachmentUrl4,attachmentUrl4)
        if obj.AttachmentUrl5 is not None and str(obj.AttachmentUrl5).strip() !='' :
            attachmentUrl5 =  u'%s%s.%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'questions',obj.id,str(obj.AttachmentUrl5))
            rt="%s附件五:<a href=%s>%s</a>;<br>"%(rt,attachmentUrl5,attachmentUrl5)
        if obj.AttachmentUrl6 is not None and str(obj.AttachmentUrl6).strip() !='' :
            attachmentUrl6 =  u'%s%s.%s/%s/%s/%s'%(PREFIX,BUCKETNAME_TORT,ENDPOINT_OUT,'questions',obj.id,str(obj.AttachmentUrl6))
            rt="%s附件六:<a href=%s>%s</a>;"%(rt,attachmentUrl6,attachmentUrl6)

        #rt =  "附件一:<a href=%s>%s</a>;<br>附件二:<a href=%s>%s</a><br>附件三:<a href=%s>%s</a><br>附件四:<a href=%s>%s</a><br>附件五:<a href=%s>%s</a><br>附件六:<a href=%s>%s</a>;"%(attachmentUrl1,attachmentUrl1,attachmentUrl2,attachmentUrl2,attachmentUrl3,attachmentUrl3,attachmentUrl4,attachmentUrl4,attachmentUrl5,attachmentUrl5,attachmentUrl6,attachmentUrl6)
        return mark_safe(rt)
    show_AttachmentUrls.short_description = u'附件'
    
    
    list_display=('id','PTitle','Type','Priority','LevelNumber','SubmitDay','Status','StaffIDSubmit','StaffIDCheck','StaffIDHandle','Remark','StaffID','Description','show_AttachmentUrls','UpdateTime',)
    list_display_links=('id',)
    search_fields=('id','Type','PTitle','Priority','LevelNumber','Status','StaffIDSubmit','StaffIDHandle','StaffID','Description','StaffIDCheck',)
    list_filter = ('PTitle','Type','Priority','LevelNumber','SubmitDay','ExpectedDay','Status','StaffIDSubmit','StaffIDHandle','StaffID','Description','UpdateTime','StaffIDCheck','ExecutedDay')
    readonly_fields = ('id','UpdateTime',)
    list_editable = ('PTitle','Type','Priority','LevelNumber','SubmitDay','ExpectedDay','Status','StaffIDSubmit','StaffIDHandle','Remark','StaffID','Description','StaffIDCheck','ExecutedDay',)

    form_layout = (
        Fieldset(u'基本信息',
                       Row('id','StaffID',),
                       Row('PTitle','Type','Status',),
                       Row('Priority','SubmitDay','ExpectedDay',),
                       Row('StaffIDSubmit','StaffIDCheck'),
                       Row('StaffIDHandle','ExecutedDay',),
                       css_class = 'unsort '
                ),
        Fieldset(u'问题描述',
                       Row( 'AttachmentUrl1','AttachmentUrl2'),
                       Row( 'AttachmentUrl3','AttachmentUrl4'),
                       Row( 'AttachmentUrl5','AttachmentUrl6'),
                       Row( 'Description',),
                       css_class = 'unsort  '
                ),
        Fieldset(u'更新时间',
                       Row('UpdateTime',),
                       css_class = 'unsort '
                )
                  )
    
    def get_list_queryset(self):
        request = self.request
        qs = super(t_product_questions_Adimin, self).get_list_queryset()
        return qs.exclude(Status="已完成")

        logger = logging.getLogger('sourceDns.webdns.views')
    #def save_model(self, request, obj, form, change):
    def save_models(self):
        obj = self.new_obj
        request = self.request
        import datetime
        now = datetime.datetime.now()
        
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_TORT)
        try:

            if obj.AttachmentUrl1 is not None and str(obj.AttachmentUrl1).strip() !='' :
                bucket.put_object(u'%s/%s/%s'%('questions',obj.id,str(obj.AttachmentUrl1)),obj.AttachmentUrl1)

            if obj.AttachmentUrl2 is not None and str(obj.AttachmentUrl2).strip() !='' :
                bucket.put_object(u'%s/%s/%s'%('questions',obj.id,str(obj.AttachmentUrl2)),obj.AttachmentUrl2)

            if obj.AttachmentUrl3 is not None and str(obj.AttachmentUrl3).strip() !='' :
                bucket.put_object(u'%s/%s/%s'%('questions',obj.id,str(obj.AttachmentUrl3)),obj.AttachmentUrl3)

            if obj.AttachmentUrl4 is not None and str(obj.AttachmentUrl4).strip() !='' :
                bucket.put_object(u'%s/%s/%s'%('questions',obj.id,str(obj.AttachmentUrl4)),obj.AttachmentUrl4)

            if obj.AttachmentUrl5 is not None and str(obj.AttachmentUrl5).strip() !='' :
                bucket.put_object(u'%s/%s/%s'%('questions',obj.id,str(obj.AttachmentUrl5)),obj.AttachmentUrl5)

            if obj.AttachmentUrl6 is not None and str(obj.AttachmentUrl6).strip() !='' :
                bucket.put_object(u'%s/%s/%s'%('questions',obj.id,str(obj.AttachmentUrl6)),obj.AttachmentUrl6)
        except:
            pass
         
        obj.StaffID = request.user.username
        obj.save()
        if request.method == 'POST':
            files = request.FILES.getlist('myfiles')
            for f in files :
                path = MEDIA_ROOT + 'questions_pic/' + str(obj.id)
                if not os.path.exists(path):
                    os.mkdir(path)
                destination = open(path + '/' +  f.name,'wb+')
                for chunk in f.chunks():
                  destination.write(chunk)
                destination.close()
        
    def get_list_queryset(self):
        request = self.request
        qs = super(t_product_questions_outAdmin, self).get_list_queryset()
        
        status       = request.GET.get('status','')           #状态
        
        searchList = {  'Status__exact':status, 
                        }
                                
        sl = {}
        for k,v in searchList.items():
            if isinstance(v,list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    #if k == 'ShopName__exact':
                        #v = 'Wish-' + v.zfill(4)
                        # messages.error(request, v)
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception,ex:
                messages.error(request,u'输入的查询数据有问题！')
                                
        return qs.filter(IT_IN_OUT='OUT')


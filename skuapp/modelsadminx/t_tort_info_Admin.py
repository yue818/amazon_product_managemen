#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_tort_info_Admin.py
 @time: 2018-05-05 11:18
"""
from django.utils.safestring import mark_safe
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from Project.settings import *
from pyapp.models import b_goods
from skuapp.table.t_tort_info import t_tort_info
from skuapp.public.const import tort
from skuapp.public.MyException import MyException as myerr
from django.contrib import messages
from datetime import datetime
import oss2
import re
import requests

class t_tort_info_Admin(object):
    search_box_flag = True
    t_tort_tree_menu_flag = True

    pmsku = re.compile('[A-Z]+-?\d*')

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

    # 根据商品SKU得到主SKU
    def getMainSKU(self, sku):
        msku = self.pmsku.search(sku)
        if msku:
            return msku.group()
        else:
            return sku

    def save_models(self):
        try:
            obj = self.new_obj
            request = self.request
            Step = tort.CHECKIN if obj.Step is None else obj.Step
            post = request.POST
            post['_redirect'] = '/Project/admin/skuapp/t_tort_info/?Step=%s' % (Step,)

            obj.StaffID = request.user.username
            if Step == tort.CHECKIN:
                obj.MainSKU = self.getMainSKU(obj.MainSKU)
                path = ''
                b_goods_obj = b_goods.objects.filter(MainSKU__exact=obj.MainSKU).values_list('SalerName2', 'Purchaser','GoodsName','BmpUrl','SKU').order_by('SKU')
                if b_goods_obj.count() > 0:
                    for b_goods_list in b_goods_obj:
                        
                        sku = b_goods_list[4]
                        path = 'http://122.226.216.10:89/ShopElf/images/{}.jpg'.format(sku)                        
                        session = requests.session()
                        resp = session.get(path)
                        if resp.status_code == 404:
                            path = ''
                            continue
                        else:
                            obj.ProductPicUrl = 'media/' + sku + '.jpg'
                            obj.SalerName2 = b_goods_list[0]
                            obj.Purchaser = b_goods_list[1]
                            obj.ProductTitle = b_goods_list[2]
                            break
                    if path == '':
                        messages.error(request, 'id : %s 系统当前无法匹配到此sku %s 的相关信息,请手动重新输入' % (obj.ID,obj.MainSKU))          
                    obj.UpdateTime = datetime.now()
                    obj.OperationState = 'W'
                    obj.Step = tort.CHECKIN
                else:
                    messages.error(request, '输入的sku %s 信息有误,查询不到此sku的相关信息!'%obj.MainSKU)

            obj.save()
        except Exception, ex:
            messages.error(request, 'Error:' + repr(ex))
        try:            
            auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
            bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_TORT)
            
            if obj.ProductPicUrl is not None:                                
                #for  object_info in oss2.ObjectIterator(bucket,prefix='%s/%s/%s'%('aliexpress',obj.ID,obj.ProductPicUrl)):
                    #bucket.delete_object(object_info.key)
                picR = requests.get(path)
                bucket.put_object(u'%s/%s/%s'%('aliexpress',obj.ID,obj.ProductPicUrl),picR)

            if obj.AttachmentUrl1 is not None and str(obj.AttachmentUrl1).strip() != '' :
                bucket.put_object(u'%s/%s/%s'%('aliexpress',obj.ID,str(obj.AttachmentUrl1)),obj.AttachmentUrl1)

            if obj.AttachmentUrl2 is not None and str(obj.AttachmentUrl2).strip() != '' :
                bucket.put_object(u'%s/%s/%s'%('aliexpress',obj.ID,str(obj.AttachmentUrl2)),obj.AttachmentUrl2)

            if obj.AttachmentUrl3 is not None and str(obj.AttachmentUrl3).strip() != '' :
                bucket.put_object(u'%s/%s/%s'%('aliexpress',obj.ID,str(obj.AttachmentUrl3)),obj.AttachmentUrl3)

            if obj.AttachmentUrl4 is not None and str(obj.AttachmentUrl4).strip() != '' :
                bucket.put_object(u'%s/%s/%s'%('aliexpress',obj.ID,str(obj.AttachmentUrl4)),obj.AttachmentUrl4)

            if obj.AttachmentUrl5 is not None and str(obj.AttachmentUrl5).strip() != '' :
                bucket.put_object(u'%s/%s/%s'%('aliexpress',obj.ID,str(obj.AttachmentUrl5)),obj.AttachmentUrl5)

            if obj.AttachmentUrl6 is not None and str(obj.AttachmentUrl6).strip() != '' :
                bucket.put_object(u'%s/%s/%s'%('aliexpress',obj.ID,str(obj.AttachmentUrl6)),obj.AttachmentUrl6)
        except Exception, ex:
            messages.error(request, 'Upload file:' + repr(ex))

    list_display = ('ID', 'show_ProductPicUrl', 'StaffID', 'Site',
                    'MainSKU', 'ProductTitle', 'Intellectual',
                    'SalerName2', 'Purchaser', 'ProductID', 'show_AttachmentUrls'
                    )

    readonly_fields = ('ID', )
    list_display_links = ('ID', )

    list_editable = ('Account', 'AccountStaffID', 'Site', 'MainSKU', 'ProductTitle', 'ScoreDeducting', 'Complainant',
                     'Intellectual', 'IntellectualCode', 'Trademark', 'ComplainReason', 'ListingTitle', 'Remark',
                     'ContactWay', 'ComplainID', 'EnglishName', 'EmailText')

    show_detail_fields = ['ID']
    fields = ('MainSKU', 'ProductID', 'ScoreDeducting', 'Remark', 'EnglishName',
              'Intellectual', 'IntellectualCode', 'ComplainReason', 'Complainant', 'Trademark',
              'ContactWay', 'ComplainID', 'AcceptTime', 'Site', 'EmailText',
              'AttachmentUrl1', 'AttachmentUrl2','AttachmentUrl3','AttachmentUrl4','AttachmentUrl5','AttachmentUrl6','ListingTitle',
              )
    form_layout = (
        Fieldset(u'我方信息',
                 Row('Site', 'MainSKU', 'ProductID'),
                 Row('ListingTitle', 'ScoreDeducting', 'EnglishName'),
                 Row('Remark'),
                 css_class='unsort '
                 ),
        Fieldset(u'对方信息',
                 Row('Intellectual', 'IntellectualCode',),
                 Row('Trademark', 'AcceptTime', ),
                 Row('ComplainID', 'Complainant', ),
                 Row('ComplainReason', ),
                 Row('ContactWay'),
                 Row('AttachmentUrl1','AttachmentUrl2','AttachmentUrl3'),
                 Row('AttachmentUrl4','AttachmentUrl5','AttachmentUrl6'),
                 Row('EmailText', ),
                 css_class='unsort '
                 )
    )

    actions = ['to_commit', 'to_delete', ]
    #动态加载actions
    def get_actions(self, request):
        Step = request.GET.get('Step', '')
        if '10' in Step:
            actions = []
        else:
            actions = ['to_commit', 'to_delete', ]

        return actions

    def to_commit(self, request, objs):

        cnt = 0
        for obj in objs:
            t_tort_info_obj = t_tort_info()
            t_tort_info_obj.__dict__ = obj.__dict__
            t_tort_info_obj.StaffID = request.user.first_name
            t_tort_info_obj.UpdateTime = datetime.now()
            t_tort_info_obj.Step = tort.WAIT_AUDIT
            t_tort_info_obj.save()
            cnt += 1

        messages.info(request, u'提交申请%d条记录,成功发送%d条.'%(cnt, cnt))

    to_commit.short_description = u'提交申请'

    def to_delete(self, request, objs):

        cnt = 0
        for obj in objs:
            try:
                if obj.OperationState == 'Y':
                    raise(myerr('10001', '%s,%s.' % (obj.MainSKU, obj.Site)))

                t_tort_info_obj = t_tort_info()
                t_tort_info_obj.__dict__ = obj.__dict__
                t_tort_info_obj.DealStaffID = request.user.first_name
                t_tort_info_obj.DealTime2 = datetime.now()
                t_tort_info_obj.Step = tort.DELETE
                t_tort_info_obj.save()
                cnt += 1
            except myerr, e:
                messages.error(request, e)  # u'此侵权已审核通过,无法删除'
                continue

        messages.info(request, u'删除记录%d条,成功删除%d条.(可联系管理员至回收站查看)' % (objs.count(), cnt))

    to_delete.short_description = u'扔进回收站'

    def get_list_queryset(self):
        request = self.request
        qs = super(t_tort_info_Admin, self).get_list_queryset()

        Step = request.GET.get('Step', '')
        if Step != '':
            Step = Step.split(',')
        MainSKU = request.GET.get('MainSKU', '')
        Site = request.GET.get('Site', '')
        Intellectual = request.GET.get('Intellectual', '')
        StaffID = request.GET.get('StaffID', '')

        TimeStart = request.GET.get('TimeNameStart', '')
        TimeEnd = request.GET.get('TimeNameEnd', '')
        
        EnglishName = request.GET.get('EnglishName', '')
        ProductTitle = request.GET.get('ProductTitle', '')

        searchList = {'Step__in': Step,
                      'MainSKU__exact': MainSKU,
                      'Site__exact': Site,
                      'EnglishName__icontains': EnglishName,
                      'ProductTitle__icontains': ProductTitle,
                      'Intellectual__exact': Intellectual,
                      'StaffID__exact': StaffID,
                      'UpdateTime__gte': TimeStart,
                      'UpdateTime__lt': TimeEnd,
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


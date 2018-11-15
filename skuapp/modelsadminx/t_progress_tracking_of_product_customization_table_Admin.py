# -*- coding: utf-8 -*-
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from django.utils.safestring import mark_safe
from Project.settings import *
from datetime import datetime
from brick.classredis.classsku import classsku
from django.db import connection
from django.contrib import messages

import oss2

class t_progress_tracking_of_product_customization_table_Admin(object):
    search_box_flag = True
    show_prompt_develop = True
    left_flag = True

    list_per_page = 20
    def del_None(self,col):
        return col if col else ''

    def readonly(self,obj):
        return 'readonly' if obj.RateOfProgress=='2' else ''

    def show_Image(self,obj) :
        rt = '<img src="{}" width="172" height="172"></img>'.format(obj.ImageURL)
        return mark_safe(rt)
    show_Image.short_description = u'图片'

    def show_person_time_info(self, obj):
        rt = u'提交人:%s' % self.del_None(obj.Submiter)
        rt = rt + u' 提交时间:%s' % self.del_None(obj.SubmitTime)
        rt = rt + u'<br>调研员:<input value="%s" style="border:none;background-color:transparent;" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_progress_tracking_of_product_customization_table\')" %s title="%s"/><span id="%s"></span>' % \
              (self.del_None(obj.SurveyPerson), obj.id, 'SurveyPerson', self.readonly(obj),self.del_None(obj.SurveyPerson), str(obj.id) + '_SurveyPerson')
        rt = rt + u'</br>调研时间:<input value="%s" style="border:none;background-color:transparent;" type="datetime-local" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_progress_tracking_of_product_customization_table\')" %s title="%s"/><span id="%s"></span>' % \
             (obj.SurveyTime.strftime('%Y-%m-%dT%H:%M') if obj.SurveyTime else '', obj.id, 'SurveyTime', self.readonly(obj),self.del_None(obj.SurveyTime), str(obj.id) + '_SurveyTime')
        rt = u'%s </br>供应链开发员:<input value="%s" style="border:none;background-color:transparent;" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_progress_tracking_of_product_customization_table\')" %s title="%s"/><span id="%s"></span>' % \
             (rt, self.del_None(obj.SupplyChainDeveloper), obj.id, 'SupplyChainDeveloper', self.readonly(obj),self.del_None(obj.SupplyChainDeveloper), str(obj.id) + '_SupplyChainDeveloper')
        rt = u'%s</br>计划完成时间:<input value="%s" style="border:none;background-color:transparent;" type="datetime-local" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_progress_tracking_of_product_customization_table\')" %s title="%s"/><span id="%s"></span>' % \
             (rt, obj.FinishTime.strftime('%Y-%m-%dT%H:%M') if obj.FinishTime else '',obj.id,'FinishTime', self.readonly(obj),self.del_None(obj.FinishTime),str(obj.id)+'_FinishTime')
        rt = u'%s </br>审核人:<input value="%s" style="border:none;background-color:transparent;" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_progress_tracking_of_product_customization_table\')" %s title="%s"/><span id="%s"></span>' % \
             (rt, self.del_None(obj.CheckPerson), obj.id, 'CheckPerson', self.readonly(obj),self.del_None(obj.CheckPerson), str(obj.id) + '_CheckPerson')
        rt = u'%s</br>审核时间:%s' % (rt, self.del_None(obj.CheckTime),)
        rt = rt + u'</br>完成操作人:%s' % self.del_None(obj.DonePerson)
        rt = rt + u' 完成时间:%s' % self.del_None(obj.DoneTime)
        return mark_safe(rt)
    show_person_time_info.short_description = mark_safe(u'<p align="center"style="color:#428bca;width:340px;">人员/时间信息</p>')

    def show_product_info(self, obj):
        rt = u'产品名称:<input value="%s" style="border:none;background-color:transparent;" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_progress_tracking_of_product_customization_table\')" %s title="%s"/><span id="%s"></span>' % \
             (self.del_None(obj.Name), obj.id, 'Name', self.readonly(obj), self.del_None(obj.Name), str(obj.id) + '_Name')

        skuname = '<span style="color: red;">SKU</span>'
        if obj.SKU and obj.SKU.strip() != 'N/A':
            skuname = 'SKU'

        rt = u'%s </br>%s:<input value="%s" style="border:none;background-color:transparent;" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_progress_tracking_of_product_customization_table\')" %s title="%s"/><span id="%s"></span>' % \
             (rt, skuname, self.del_None(obj.SKU), obj.id, 'SKU', self.readonly(obj), self.del_None(obj.SKU),str(obj.id) + '_SKU')
        rt = u'%s </br>关键字:<input value="%s" style="border:none;background-color:transparent;" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_progress_tracking_of_product_customization_table\')" %s title="%s"/><span id="%s"></span>' % \
             (rt, self.del_None(obj.KeyWords), obj.id, 'KeyWords', self.readonly(obj), self.del_None(obj.KeyWords), str(obj.id) + '_KeyWords')
        rt = u'%s</br>' % rt

        if obj.RateOfProgress in ['0', '1'] and obj.FinishTime and obj.FinishTime.strftime('%Y-%m-%d %H:%M:%S') < datetime.now().strftime('%Y-%m-%d %H:%M:%S'):
            if obj.RateOfProgress == '0':
                rt = rt + u'<div style="background:red;color:white">已超过计划时间,待审核</div>'
            elif obj.RateOfProgress == '1':
                rt = rt + u'<div style="background:red;color:white">已超过计划时间,待完成</div>'
        elif obj.RateOfProgress == '0' and obj.FinishTime and obj.FinishTime.strftime('%Y-%m-%d %H:%M:%S') >= datetime.now().strftime('%Y-%m-%d %H:%M:%S'):
            rt = rt + u'<div style="background:#9E3F3F;color:white">待审核</div>'
        elif obj.RateOfProgress == '1':
            rt = rt + u'<div style="background:green;color:white">已审核，生产中</div>'
        elif obj.RateOfProgress == '2':
            rt = rt + u'<div style="background:green;color:white">已完成</div>'
        elif obj.RateOfProgress == '-1':
            rt = rt + u'<div style="background:dimgrey;color:white">被废弃</div>'

        rt = rt + u'<br>反向链接:<a title="%s" href="%s" target="_blank">%s...</a>' % \
             (obj.ReverseLink, obj.ReverseLink, self.del_None(obj.ReverseLink)[:25])
        rt = u'%s</br>1688链接:<a title="%s" href="%s" target="_blank">%s...</a>' % \
             (rt, obj.SupplierLink, obj.SupplierLink, self.del_None(obj.SupplierLink)[:25])
        rt = u'%s</br>附件下载:<a title="%s" href="%s" target="_blank">%s...</a>' % \
             (rt, obj.Enclosure, obj.Enclosure, str(obj.Enclosure)[:25])

        return mark_safe(rt)
    show_product_info.short_description = mark_safe(u'<p align="center"style="color:#428bca;width:310px;">产品信息</p>')

    def show_SurveyAnalysis(self, obj):
        rt = u'<textarea style="width:100%%;border:none;background-color:transparent;" rows="6" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_progress_tracking_of_product_customization_table\')" %s title="%s"> %s </textarea><br><span id="%s"></span>' % \
             (obj.id,'SurveyAnalysis',self.readonly(obj),self.del_None(obj.SurveyAnalysis),self.del_None(obj.SurveyAnalysis),str(obj.id)+'_SurveyAnalysis')
        return mark_safe(rt)
    show_SurveyAnalysis.short_description = mark_safe(u'<p align="center"style="color:#428bca;width:225px;">调研分析</p>')

    def show_MakeDemand(self, obj):
        rt = u'<textarea style="width:100%%;border:none;background-color:transparent;" rows="6" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_progress_tracking_of_product_customization_table\')" %s title="%s"> %s </textarea><br><span id="%s"></span>' % \
             (obj.id,'MakeDemand',self.readonly(obj),self.del_None(obj.MakeDemand),self.del_None(obj.MakeDemand),str(obj.id)+'_MakeDemand')
        return mark_safe(rt)
    show_MakeDemand.short_description = mark_safe(u'<p align="center"style="color:#428bca;width:225px;">定做要求</p>')

    def show_DevelopRemark(self, obj):
        rt = u'<textarea style="width:100%%;border:none;background-color:transparent;" rows="6" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_progress_tracking_of_product_customization_table\')" %s title="%s"> %s </textarea><br><span id="%s"></span>' % \
             (obj.id,'DevelopRemark',self.readonly(obj),self.del_None(obj.DevelopRemark),self.del_None(obj.DevelopRemark),str(obj.id)+'_DevelopRemark')
        return mark_safe(rt)
    show_DevelopRemark.short_description = mark_safe(u'<p align="center"style="color:#428bca;width:225px;">开发备注</p>')

    def show_CheckRemark(self, obj):
        rt = u'<textarea style="width:100%%;border:none;background-color:transparent;" rows="6" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_progress_tracking_of_product_customization_table\')" %s title="%s"> %s </textarea><br><span id="%s"></span>' % \
             (obj.id,'CheckRemark',self.readonly(obj),self.del_None(obj.CheckRemark),self.del_None(obj.CheckRemark),str(obj.id)+'_CheckRemark')
        return mark_safe(rt)
    show_CheckRemark.short_description = mark_safe(u'<p align="center"style="color:#428bca;width:225px;">审核意见</p>')

    list_display=('id', 'show_Image', 'show_product_info', 'show_SurveyAnalysis', 'show_MakeDemand', 'show_DevelopRemark', 'show_CheckRemark', 'show_person_time_info',)

    fields = ['MainSKU', 'Enclosure']
    form_layout = (
        Fieldset(u'检索信息',
                 Row('MainSKU', 'Enclosure',),
                 css_class='unsort '
                 ),
    )

    actions = ['to_check', 'to_complete', 'to_nullify']
    def to_check(self, request, objs):

        isClothes = request.GET.get('clothes', '0')
        if isClothes == '1':
            messages.warning(request, u'定做服装无须审核....')
            return

        for obj in objs:
            if obj.RateOfProgress == '0' and (obj.CheckPerson == request.user.first_name or not obj.CheckPerson):
                obj.RateOfProgress = '1'
                obj.CheckPerson = request.user.first_name
                obj.CheckTime = datetime.now()
                obj.save()

    to_check.short_description = u'审核'

    def to_complete(self, request, objs):
        objs.filter(RateOfProgress='1', SKU__isnull=False).exclude(SKU='').exclude(SKU='N/A').update(
            RateOfProgress='2',DonePerson=request.user.first_name,DoneTime=datetime.now()
        )

    to_complete.short_description = u'完成'

    def to_nullify(self, request, objs):
        isClothes = request.GET.get('clothes', '0')
        if isClothes == '1':
            messages.warning(request, u'定做服装不能废弃....')
            return

        objs.filter(RateOfProgress__in=['0', '1']).update(
            RateOfProgress='-1',DonePerson=request.user.first_name,DoneTime=datetime.now()
        )

    to_nullify.short_description = u'废弃'



    def save_models(self):
        obj = self.new_obj
        old_obj = None
        if obj is None or obj.id is None or obj.id <=0:
            pass
        else:
            old_obj = self.model.objects.get(pk=obj.pk)

        try:
            clothes = self.request.GET.get('clothes', '0')
            v_progress = clothes
            if clothes == '1':
                self.request.POST['_redirect'] = "/Project/admin/skuapp/t_progress_tracking_of_product_customization_table/?clothes=1"

            bemainsku = classsku(connection).get_bemainsku_by_sku(obj.MainSKU)

            enclosure = obj.Enclosure
            if obj.Enclosure:
                filename = '%s/%s/%s' % (self.request.user.username, datetime.now().strftime('%Y%m%d%H%M%S'),obj.Enclosure)
                auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
                bucket = oss2.Bucket(auth, ENDPOINT, BUCKETNAME_DOWNLOAD)
                presult = bucket.put_object(filename, obj.Enclosure)
                _content = presult.__dict__
                enclosure = PREFIX + BUCKETNAME_DOWNLOAD + '.' + ENDPOINT_OUT + '/' + filename
                if _content['status'] != 200:
                    raise Exception(u'附件上传失败!请稍后重试  code: %s' % _content['status'])

            image_list      = self.request.POST.getlist('product_image',[])
            sku_list        = self.request.POST.getlist('sku',[])
            name_list       = self.request.POST.getlist('name',[])
            keyword_list    = self.request.POST.getlist('keywords',[])
            surveyname_list = self.request.POST.getlist('surveyname',[])
            surveytime_list = self.request.POST.getlist('surveytime',[])
            reverselink_list  = self.request.POST.getlist('reverselink',[])
            supplierlink_list = self.request.POST.getlist('supplierlink',[])
            developer_list    = self.request.POST.getlist('salerName2',[])
            finishtime_list   = self.request.POST.getlist('FinishTime',[])

            insert_into = []
            for i in range(len(sku_list)):
                insert_into.append(self.model(
                    ImageURL=image_list[i],MainSKU=bemainsku,SKU=sku_list[i],Name=name_list[i],
                    KeyWords=keyword_list[i],ReverseLink=reverselink_list[i],SupplierLink=supplierlink_list[i],
                    SurveyPerson=surveyname_list[i],SurveyTime=surveytime_list[i],SupplyChainDeveloper=developer_list[i],
                    FinishTime=finishtime_list[i],SurveyAnalysis='',MakeDemand='',DevelopRemark='',CheckPerson='',
                    CheckTime=None,CheckRemark='',RateOfProgress=v_progress,Enclosure=enclosure,
                    Submiter=self.request.user.first_name,SubmitTime=datetime.now(),FromClothes=clothes
                ))

            self.model.objects.bulk_create(insert_into)

        except Exception, e:
            messages.error(self.request, u'%s:%s' % (Exception, e))

    def get_context(self):

        context = super(t_progress_tracking_of_product_customization_table_Admin, self).get_context()

        clothes = self.request.GET.get('clothes', '0')
        if clothes == '1':
            context['add_url'] = '/Project/admin/skuapp/t_progress_tracking_of_product_customization_table/add/?clothes=1'

        return context


    def get_list_queryset(self):
        request = self.request
        qs = super(t_progress_tracking_of_product_customization_table_Admin, self).get_list_queryset()
        try:
            with_update = self.model.objects.filter(
                RateOfProgress='1', FinishTime__isnull=False, FinishTime__lt=datetime.now(), SKU__isnull=False
            ).exclude(SKU='').exclude(SKU='N/A')
            with_update.update(RateOfProgress='2')

            isClothes = request.GET.get('clothes', '0')
            productsku = request.GET.get('productsku')
            productname = request.GET.get('productname')
            surveyperson = request.GET.get('surveyperson')
            developer = request.GET.get('developer')
            checkperson = request.GET.get('checkperson')
            doneperson = request.GET.get('doneperson')
            surveytimeStart = request.GET.get('surveytimeStart')
            surveytimeEnd = request.GET.get('surveytimeEnd')
            finishtimeStart = request.GET.get('finishtimeStart')
            finishtimeEnd = request.GET.get('finishtimeEnd')
            checktimeStart = request.GET.get('checktimeStart')
            checktimeEnd = request.GET.get('checktimeEnd')
            donetimeStart = request.GET.get('donetimeStart')
            donetimeEnd = request.GET.get('donetimeEnd')

            seachfilter = {
                'SKU__exact': productsku,
                'FromClothes__exact': isClothes,
                'Name__icontains': productname,
                'SurveyPerson__exact': surveyperson,
                'SupplyChainDeveloper__exact': developer,
                'CheckPerson__exact': checkperson,
                'DonePerson__exact': doneperson,
                'SurveyTime__gte': surveytimeStart,
                'SurveyTime__lt': surveytimeEnd,
                'FinishTime__gte': finishtimeStart,
                'FinishTime__lt': finishtimeEnd,
                'CheckTime__gte': checktimeStart,
                'CheckTime__lt': checktimeEnd,
                'DoneTime__gte': donetimeStart,
                'DoneTime__lt': donetimeEnd
            }

            seachexclude = {}

            status = request.GET.get('status')
            if status == 'pending':
                seachfilter['RateOfProgress__exact'] = '0'
                seachfilter['FinishTime__gte'] = datetime.now()
            elif status == 'producing':
                seachfilter['RateOfProgress__exact'] = '1'
                seachexclude['FinishTime__lt'] = datetime.now()
            elif status == 'completed':
                seachfilter['RateOfProgress__exact'] = '2'
            elif status == 'time_out':
                seachexclude['RateOfProgress__in'] = ['2', '-1']
                seachfilter['FinishTime__lt'] = datetime.now()
            elif status == 'nullify':
                seachfilter['RateOfProgress__exact'] = '-1'

            newdict = {}
            for key, value in seachfilter.items():
                if value:
                    newdict[key] = value

            if newdict:
                qs = qs.filter(**newdict).exclude(**seachexclude)

            return qs
        except Exception, e:
            messages.error(request, u'查询条件错误，请联系IT人员！%s' % e)
            return qs










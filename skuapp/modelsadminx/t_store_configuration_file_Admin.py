# -*- coding: utf-8 -*-
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from datetime import datetime
from django.contrib import messages
from django.utils.safestring import mark_safe

class t_store_configuration_file_Admin(object):
    store_config_flag = True

    def show_Status(self, obj):

        option = u"<option value ='' selected>未知</option><option value ='0'>正常</option><option value ='-1'>异常</option>"
        if obj.Status == '0':
            option = u"<option value ='0' selected>正常</option>" \
                     u"<option value ='-1'>异常</option>"
        elif obj.Status == '-1':
            option = u"<option value ='0'>正常</option>" \
                     u"<option value ='-1' selected>异常</option>"

        store_status = u"<select class='text-field admintextinputwidget form-control' " \
                       u"onchange='change_status(this,\"%s\")'>" % obj.id \
                      + option + \
                      u"</select>"

        type_show = u"</br><span id='%s'></span>" % obj.id

        return mark_safe(store_status + type_show)
    show_Status.short_description = mark_safe(u'<p align="center"style="color:#428bca;">店铺状态</p>')

    list_display =('id','Department','ShopName','show_Status','Seller','Published','Operators',)
    search_fields = ('id','ShopName','Seller','Published','Operators','ShopType','Submitter',)
    list_filter =('ShopName','Seller','Operators','Published','ShopType','Submitter','Department','Status')
    list_display_links = ('id')
    list_editable = ('ShopName','Seller','Published','Operators','Department','RealName',)


    fields = ('ShopName',
              'Seller',
              'Published',
              'Operators',
              'ShopType',
              'Submitter',
              'Department'
              )
              
    form_layout = (
        Fieldset(u'店铺配置',
                    Row('Department',),
                    Row('ShopName',),
                    Row('Seller',),
                    Row('Published',),
                    Row('Operators',),
                    Row('ShopType',),
                    Row('Submitter',),
                    css_class = 'unsort'
                ),
                  )
 
    def save_models(self):
        obj = self.new_obj
        request = self.request
        old_obj = None
        if obj is None or obj.id is None or obj.id <= 0:
            saveobj = self.model.objects.create(id=None)
            obj.id = saveobj.id
        else:
            old_obj = self.model.objects.get(pk=obj.pk)

        if old_obj is None :
            shopnameobj = self.model.objects.filter(ShopName=obj.ShopName)
            if shopnameobj.exists():
                messages.error(request,u'抱歉！该店铺名已经存在。')
                return
        else:
            pass

        if obj.ShopName is not None and obj.ShopName.strip() != '':
            code = obj.ShopName.strip().split('-')
            if len(code) >= 2:
                obj.ShopName_temp = code[0] + '-' + code[1]
            else:
                obj.ShopName_temp = obj.ShopName.strip()
        else:
            messages.error(request, u'抱歉！请填写店铺名称后保存')
            return

        obj.save()

    def get_list_queryset(self):
        request = self.request
        qs = super(t_store_configuration_file_Admin, self).get_list_queryset()

        seachfilter = {}

        Pstatus = request.GET.get('status')
        if Pstatus:
            PlatformID = Pstatus.split('_')[0]
            if PlatformID:
                seachfilter['PlatformID'] = PlatformID

            sstatus = Pstatus.split('_')[-1]

            if sstatus == 's':
                seachfilter['Status'] = '0'
            elif sstatus == 'e':
                seachfilter['Status'] = '-1'
            elif sstatus == 'o':
                seachfilter['Status__isnull'] = True

        if seachfilter:
            qs = qs.filter(**seachfilter)

        return qs

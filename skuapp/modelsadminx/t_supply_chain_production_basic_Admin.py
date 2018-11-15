# -*- coding: utf-8 -*-
from django.contrib import messages
from django.http import HttpResponseRedirect
from .t_product_Admin import *
from Project.settings import *
import requests
import oss2
import os
import StringIO
import json
from pyapp.models import b_goods
from django.db import connection
from django.utils.safestring import mark_safe
from skuapp.table.t_product_mainsku_sku import t_product_mainsku_sku

from brick.classredis.classmainsku import classmainsku
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from skuapp.table.t_supply_chain_production_basic_permission import t_supply_chain_production_basic_permission
import datetime
class t_supply_chain_production_basic_Admin(object):
    list_display=['id','py_pic','product_info','product_properties','style_info','other_info','DateTime']
    list_display_links=('',)
    actions=['to_excel']
    t_supply_chain_production_basic_flag=True
    search_box_flag = True
    downloadxls = True




    def del_None(self,col):
        rt = col
        if not col:
            rt = ''
        return rt

    def product_info(self,obj):
        EditFlag=json.loads(obj.EditFlag) if obj.EditFlag else {}
        request = self.request
        _permission = t_supply_chain_production_basic_permission.objects.filter(
            username=request.user.username).values_list('username')
        permission = [x[0] for x in _permission]

        read = 'readonly'
        if request.user.is_superuser or permission or obj.Lock==0 or not EditFlag.get('MainSKU'):
            read=''
        rt = u'<table CELLSPACING="5">'
        rt = u'%s<tr><th>主SKU：</th><td><input value="%s" size="20" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_supply_chain_production_basic\')" %s title="%s"/><span id="%s"></span></td></tr>' % \
             (rt, self.del_None(obj.MainSKU), obj.id, 'MainSKU', read, self.del_None(obj.MainSKU),
              str(obj.id) + '_MainSKU')
        read = 'readonly'
        if request.user.is_superuser or permission or obj.Lock == 0 or not EditFlag.get('Buyer'):
            read = ''
        rt = u'%s<tr><th>采购员：</th><td><input value="%s" size="20" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_supply_chain_production_basic\')" %s title="%s"/><span id="%s"></span></td></tr>' % \
             (rt, self.del_None(obj.Buyer), obj.id, 'Buyer', read, self.del_None(obj.Buyer),
              str(obj.id) + '_Buyer')
        read = 'readonly'
        if request.user.is_superuser or permission or obj.Lock == 0 or not EditFlag.get('CostPrice'):
            read = ''
        rt = u'%s<tr><th>成本单价：</th><td><input value="%s" size="20" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_supply_chain_production_basic\')" %s title="%s"/><span id="%s"></span></td></tr>' % \
             (rt, self.del_None(obj.CostPrice), obj.id, 'CostPrice', read, self.del_None(obj.CostPrice),
              str(obj.id) + '_CostPrice')
        read = 'readonly'
        if request.user.is_superuser or permission or obj.Lock == 0 or not EditFlag.get('ProcessCosts'):
            read = ''
        rt = u'%s<tr><th>加工费：</th><td><input value="%s" size="20" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_supply_chain_production_basic\')" %s title="%s"/><span id="%s"></span></td></tr></table>' % \
             (rt, self.del_None(obj.ProcessCosts), obj.id, 'ProcessCosts', read, self.del_None(obj.ProcessCosts),
              str(obj.id) + '_ProcessCosts')

        return mark_safe(rt)

    product_info.short_description = u'产品信息'






    def style_info(self,obj):
        EditFlag=json.loads(obj.EditFlag) if obj.EditFlag else {}
        request = self.request
        _permission = t_supply_chain_production_basic_permission.objects.filter(
            username=request.user.username).values_list('username')
        permission = [x[0] for x in _permission]

        read = 'readonly'
        rt = '<table CELLSPACING="5">'
        if request.user.is_superuser or permission or obj.Lock==0 or not EditFlag.get('A_fabric'):
            read=''
        rt = u'%s<tr><th>A面料：</th><td><input value="%s" size="20" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_supply_chain_production_basic\')" %s title="%s"/><span id="%s" style="color:white;"></span></td>' % \
             (rt, self.del_None(obj.A_fabric), obj.id, 'A_fabric', read, self.del_None(obj.A_fabric), str(obj.id) + '_A_fabric')

        read = 'readonly'
        if request.user.is_superuser or permission or obj.Lock==0 or not EditFlag.get('A_address'):
            read=''
        rt = u'%s<th>档口地址：</th><td><input value="%s" size="20" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_supply_chain_production_basic\')" %s title="%s"/><span id="%s" style="color:white;"></span></td></tr> ' % \
             (rt, self.del_None(obj.A_address), obj.id, 'A_address', read, self.del_None(obj.A_address),
              str(obj.id) + '_A_address')

        read = 'readonly'
        if request.user.is_superuser or permission or obj.Lock==0 or not EditFlag.get('A_dosage'):
            read=''
        rt = u'%s<tr><th>用量：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_supply_chain_production_basic\')" %s title="%s"/><span id="%s"></span></th> ' % \
             (rt, self.del_None(obj.A_dosage), obj.id, 'A_dosage', read, self.del_None(obj.A_dosage),
              str(obj.id) + '_A_dosage')

        read = 'readonly'
        if request.user.is_superuser or permission or obj.Lock==0 or not EditFlag.get('A_color'):
            read=''
        rt = u'%s<th>色号：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_supply_chain_production_basic\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt, self.del_None(obj.A_color), obj.id, 'A_color', read, self.del_None(obj.A_color),
              str(obj.id) + '_A_color')



        if request.user.is_superuser or permission or obj.Lock==0 or not EditFlag.get('B_fabric'):
            read=''
        rt = u'%s<tr><th>B面料：</th><td><input value="%s" size="20" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_supply_chain_production_basic\')" %s title="%s"/><span id="%s" style="color:white;"></span></td>' % \
             (rt, self.del_None(obj.B_fabric), obj.id, 'B_fabric', read, self.del_None(obj.B_fabric), str(obj.id) + '_B_fabric')

        read = 'readonly'
        if request.user.is_superuser or permission or obj.Lock==0 or not EditFlag.get('B_address'):
            read=''
        rt = u'%s<th>档口地址：</th><td><input value="%s" size="20" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_supply_chain_production_basic\')" %s title="%s"/><span id="%s" style="color:white;"></span></td></tr> ' % \
             (rt, self.del_None(obj.B_address), obj.id, 'B_address', read, self.del_None(obj.B_address),
              str(obj.id) + '_B_address')

        read = 'readonly'
        if request.user.is_superuser or permission or obj.Lock==0 or not EditFlag.get('B_dosage'):
            read=''
        rt = u'%s<tr><th>用量：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_supply_chain_production_basic\')" %s title="%s"/><span id="%s"></span></th> ' % \
             (rt, self.del_None(obj.B_dosage), obj.id, 'B_dosage', read, self.del_None(obj.B_dosage),
              str(obj.id) + '_B_dosage')

        read = 'readonly'
        if request.user.is_superuser or permission or obj.Lock==0 or not EditFlag.get('B_color'):
            read=''
        rt = u'%s<th>色号：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_supply_chain_production_basic\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt, self.del_None(obj.B_color), obj.id, 'B_color', read, self.del_None(obj.B_color),
              str(obj.id) + '_B_color')




        if request.user.is_superuser or permission or obj.Lock==0 or not EditFlag.get('C_fabric'):
            read=''
        rt = u'%s<tr><th>C面料：</th><td><input value="%s" size="20" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_supply_chain_production_basic\')" %s title="%s"/><span id="%s" style="color:white;"></span></td>' % \
             (rt, self.del_None(obj.C_fabric), obj.id, 'C_fabric', read, self.del_None(obj.C_fabric), str(obj.id) + '_C_fabric')

        read = 'readonly'
        if request.user.is_superuser or permission or obj.Lock==0 or not EditFlag.get('C_address'):
            read=''
        rt = u'%s<th>档口地址：</th><td><input value="%s" size="20" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_supply_chain_production_basic\')" %s title="%s"/><span id="%s" style="color:white;"></span></td></tr> ' % \
             (rt, self.del_None(obj.C_address), obj.id, 'C_address', read, self.del_None(obj.C_address),
              str(obj.id) + '_C_address')

        read = 'readonly'
        if request.user.is_superuser or permission or obj.Lock==0 or not EditFlag.get('C_dosage'):
            read=''
        rt = u'%s<tr><th>用量：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_supply_chain_production_basic\')" %s title="%s"/><span id="%s"></span></th> ' % \
             (rt, self.del_None(obj.C_dosage), obj.id, 'C_dosage', read, self.del_None(obj.C_dosage),
              str(obj.id) + '_C_dosage')

        read = 'readonly'
        if request.user.is_superuser or permission or obj.Lock==0 or not EditFlag.get('C_color'):
            read=''
        rt = u'%s<th>色号：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_supply_chain_production_basic\')" %s title="%s"/><span id="%s"></span></th></tr></table> ' % \
             (rt, self.del_None(obj.C_color), obj.id, 'C_color', read, self.del_None(obj.C_color),
              str(obj.id) + '_C_color')

        return mark_safe(rt)

    style_info.short_description = u'款式资料'



    def other_info(self,obj):
        EditFlag = json.loads(obj.EditFlag) if obj.EditFlag else {}
        request=self.request
        _permission=t_supply_chain_production_basic_permission.objects.filter(username=request.user.username).values_list('username')
        permission=[x[0] for x in _permission]

        read = 'readonly'
        if request.user.is_superuser or permission or obj.Lock==0 or not EditFlag.get('Other'):
            read=''

        rt = '<table CELLSPACING="5">'
        rt = u'%s<tr><th>其他：</th><td><input value="%s" size="20" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_supply_chain_production_basic\')" %s title="%s"/><span id="%s"></span></td></th></table>' % \
             (rt, self.del_None(obj.Other), obj.id, 'Other', read, self.del_None(obj.Other),
              str(obj.id) + '_Other')

        return mark_safe(rt)

    other_info.short_description=u'其他'









    fields=('MainSKU','Buyer','ProcessCosts','OffsetPrinting','DigitalPrinting','DigitalCuts','Watermark',
            'Zipper', 'Cap_rope_ball','Button', 'Elastic','Cornseye_SnapButton', 'LeatherCard','Lace', 'Webbing',
            'ZhuanJi', 'LaTiao','ShaoHua', 'TangTu','Other')

    form_layout = (
        Fieldset(u'主SKU',
                 Row('MainSKU',),

                 css_class='unsort '
                 ),
        Fieldset(u'采购员',
                 Row('Buyer', ),
                 css_class='unsort '
                 ),
        Fieldset(u'价格相关',
                 Row('ProcessCosts',),
                 css_class='unsort '
                 ),
        Fieldset(u'产品属性',
                 Row('OffsetPrinting','DigitalPrinting' ),
                 Row('DigitalCuts','Watermark'),
                 Row('Zipper','Cap_rope_ball'),
                 Row('Button', 'Elastic'),
                 Row('Cornseye_SnapButton', 'LeatherCard'),
                 Row('Lace', 'Webbing'),
                 Row('ZhuanJi', 'LaTiao'),
                 Row('ShaoHua', 'TangTu'),
                 css_class='unsort '
                 ),

    )



    def product_properties(self,obj):
        request=self.request
        EditFlag = json.loads(obj.EditFlag) if obj.EditFlag else {}
        _permission=t_supply_chain_production_basic_permission.objects.filter(username=request.user.username).values_list('username')
        permission=[x[0] for x in _permission]

        read = 'readonly'
        # if request.user.is_superuser or permission or obj.Lock==0:
        #     read=''

        rt = '<table CELLSPACING="5">'
        if request.user.is_superuser or permission or obj.Lock==0 or not EditFlag.get('OffsetPrinting'):
            read=''
        rt = u'%s<tr><th>胶印：</th><td><input value="%s" size="20" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_supply_chain_production_basic\')" %s title="%s"/><span id="%s" style="color:white;">隐藏隐藏</span></td>' % \
             (rt, self.del_None(obj.OffsetPrinting), obj.id, 'OffsetPrinting', read, self.del_None(obj.OffsetPrinting), str(obj.id) + '_OffsetPrinting')

        read = 'readonly'
        if request.user.is_superuser or permission or obj.Lock==0 or not EditFlag.get('DigitalPrinting'):
            read=''
        rt = u'%s<th>数码批印：</th><td><input value="%s" size="20" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_supply_chain_production_basic\')" %s title="%s"/><span id="%s" style="color:white;">隐藏隐藏</span></td></tr> ' % \
             (rt, self.del_None(obj.DigitalPrinting), obj.id, 'DigitalPrinting', read, self.del_None(obj.DigitalPrinting),
              str(obj.id) + '_DigitalPrinting')

        read = 'readonly'
        if request.user.is_superuser or permission or obj.Lock==0 or not EditFlag.get('DigitalCuts'):
            read=''
        rt = u'%s<tr><th>数码裁片：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_supply_chain_production_basic\')" %s title="%s"/><span id="%s"></span></th> ' % \
             (rt, self.del_None(obj.DigitalCuts), obj.id, 'DigitalCuts', read, self.del_None(obj.DigitalCuts),
              str(obj.id) + '_DigitalCuts')

        read = 'readonly'
        if request.user.is_superuser or permission or obj.Lock==0 or not EditFlag.get('Watermark'):
            read=''
        rt = u'%s<th>水印：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_supply_chain_production_basic\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt, self.del_None(obj.Watermark), obj.id, 'Watermark', read, self.del_None(obj.Watermark),
              str(obj.id) + '_Watermark')

        read = 'readonly'
        if request.user.is_superuser or permission or obj.Lock==0 or not EditFlag.get('Zipper'):
            read=''
        rt = u'%s<tr><th>拉链：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_supply_chain_production_basic\')" %s title="%s"/><span id="%s"></span></th> ' % \
             (rt, self.del_None(obj.Zipper), obj.id, 'Zipper', read, self.del_None(obj.Zipper),
              str(obj.id) + '_Zipper')

        read = 'readonly'
        if request.user.is_superuser or permission or obj.Lock==0 or not EditFlag.get('Cap_rope_ball'):
            read=''
        rt = u'%s<th>     帽绳/球：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_supply_chain_production_basic\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt, self.del_None(obj.Cap_rope_ball), obj.id, 'Cap_rope_ball', read, self.del_None(obj.Cap_rope_ball),
              str(obj.id) + '_Cap_rope_ball')

        read = 'readonly'
        if request.user.is_superuser or permission or obj.Lock==0 or not EditFlag.get('Button'):
            read=''
        rt = u'%s<tr><th>纽扣：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_supply_chain_production_basic\')" %s title="%s"/><span id="%s"></span></th> ' % \
             (rt, self.del_None(obj.Button), obj.id, 'Button', read, self.del_None(obj.Button),
              str(obj.id) + '_Button')

        read = 'readonly'
        if request.user.is_superuser or permission or obj.Lock==0 or not EditFlag.get('Elastic'):
            read=''
        rt = u'%s<th>     橡筋：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_supply_chain_production_basic\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt, self.del_None(obj.Elastic), obj.id, 'Elastic', read, self.del_None(obj.Elastic),
              str(obj.id) + '_Elastic')

        read = 'readonly'
        if request.user.is_superuser or permission or obj.Lock==0 or not EditFlag.get('Cornseye_SnapButton'):
            read=''
        rt = u'%s<tr><th>鸡眼/四合扣：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_supply_chain_production_basic\')" %s title="%s"/><span id="%s"></span></th> ' % \
             (rt, self.del_None(obj.Cornseye_SnapButton), obj.id, 'Cornseye_SnapButton', read, self.del_None(obj.Cornseye_SnapButton),
              str(obj.id) + '_Cornseye_SnapButton')

        read = 'readonly'
        if request.user.is_superuser or permission or obj.Lock==0 or not EditFlag.get('LeatherCard'):
            read=''
        rt = u'%s<th>     皮牌：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_supply_chain_production_basic\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt, self.del_None(obj.LeatherCard), obj.id, 'LeatherCard', read, self.del_None(obj.LeatherCard),
              str(obj.id) + '_LeatherCard')

        read = 'readonly'
        if request.user.is_superuser or permission or obj.Lock==0 or not EditFlag.get('Lace'):
            read=''
        rt = u'%s<tr><th>花边：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_supply_chain_production_basic\')" %s title="%s"/><span id="%s"></span></th> ' % \
             (rt, self.del_None(obj.Lace), obj.id, 'Lace', read, self.del_None(obj.Lace),
              str(obj.id) + '_Lace')

        read = 'readonly'
        if request.user.is_superuser or permission or obj.Lock==0 or not EditFlag.get('Webbing'):
            read=''
        rt = u'%s<th>     织带：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_supply_chain_production_basic\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt, self.del_None(obj.Webbing), obj.id, 'Webbing', read, self.del_None(obj.Webbing),
              str(obj.id) + '_Webbing')

        read = 'readonly'
        if request.user.is_superuser or permission or obj.Lock==0 or not EditFlag.get('ZhuanJi'):
            read=''
        rt = u'%s<tr><th>专机：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_supply_chain_production_basic\')" %s title="%s"/><span id="%s"></span></th> ' % \
             (rt, self.del_None(obj.ZhuanJi), obj.id, 'ZhuanJi', read, self.del_None(obj.ZhuanJi),
              str(obj.id) + '_ZhuanJi')

        read = 'readonly'
        if request.user.is_superuser or permission or obj.Lock==0 or not EditFlag.get('LaTiao'):
            read=''
        rt = u'%s<th>     拉条：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_supply_chain_production_basic\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt, self.del_None(obj.LaTiao), obj.id, 'LaTiao', read, self.del_None(obj.LaTiao),
              str(obj.id) + '_LaTiao')

        read = 'readonly'
        if request.user.is_superuser or permission or obj.Lock==0 or not EditFlag.get('ShaoHua'):
            read=''
        rt = u'%s<tr><th>烧花：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_supply_chain_production_basic\')" %s title="%s"/><span id="%s"></span></th> ' % \
             (rt, self.del_None(obj.ShaoHua), obj.id, 'ShaoHua', read, self.del_None(obj.ShaoHua),
              str(obj.id) + '_ShaoHua')

        read = 'readonly'
        if request.user.is_superuser or permission or obj.Lock==0 or not EditFlag.get('TangTu'):
            read=''
        rt = u'%s<th>     烫图：</th><th><input value="%s" type="text" onchange="to_change_work(\'%s\',\'%s\',this.value,\'t_supply_chain_production_basic\')" %s title="%s"/><span id="%s"></span></th></tr> ' % \
             (rt, self.del_None(obj.TangTu), obj.id, 'TangTu', read, self.del_None(obj.TangTu),
              str(obj.id) + '_TangTu')


        rt = rt + '</table>'

        return mark_safe(rt)
    product_properties.short_description = u'产品属性'


    def get_list_queryset(self):
        qs = super(t_supply_chain_production_basic_Admin, self).get_list_queryset()
        request = self.request
        _permission=t_supply_chain_production_basic_permission.objects.filter(username=request.user.username).values_list('username')
        permission=[x[0] for x in _permission]
        if permission or request.user.is_superuser:
            pass
        else:
            qs=qs.filter(Buyer=request.user.first_name)
        MainSKU=request.GET.get(u'MainSKU',u'')
        Buyer=request.GET.get(u'Buyer',u'')
        startdate=request.GET.get(u'DateTimeStart',u'')
        enddate=request.GET.get(u'DateTimeEnd',u'')
        searchList={u'MainSKU__contains':MainSKU,u'Buyer__startswith':Buyer,u'DateTime__gte':startdate,u'DateTime__lte':enddate}
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
                # messages.error(request, ex)
                messages.error(request, u'Please enter the correct content!')
        return qs



    def to_excel(self,request,objs):
        from xlwt import *
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s' % (path))
        workbook = Workbook()
        sheet1 = workbook.add_sheet(u'sheet1',)  # 创建sheet
        row0 = [u'主SKU',u'采购员',u'成本单价',u'加工费',u'胶印',u'数码批印',u'数码裁片',u'水印',
                u'拉链',u'帽绳/球',u'纽扣',u'橡筋',u'鸡眼/四合扣',u'皮牌',u'花边',u'织带',
                u'专机',u'拉条',u'烧花',u'烫图',u'A面料',u'A档口地址',u'A用量',u'A色号',u'B面料',u'B档口地址',u'B用量',u'B色号',
                u'C面料',u'C档口地址',u'C用量',u'C色号',u'其他']
        datalist=[]

        for obj in objs:
            datalist.append([obj.MainSKU,obj.Buyer,obj.CostPrice,obj.ProcessCosts,obj.OffsetPrinting,
                             obj.DigitalPrinting,obj.DigitalCuts,obj.Watermark,obj.Zipper,obj.Cap_rope_ball,obj.Button,
                             obj.Elastic,obj.Cornseye_SnapButton,obj.LeatherCard,obj.Lace,obj.Webbing,obj.ZhuanJi,obj.LaTiao,
                             obj.ShaoHua,obj.TangTu,obj.A_fabric,obj.A_address,obj.A_dosage,obj.A_color,obj.B_fabric,
                             obj.B_address,obj.B_dosage,obj.B_color,obj.C_fabric,obj.C_address,obj.C_dosage,obj.C_color,obj.Other])
        for i in range(0, len(row0)):
            sheet1.write(0, i, row0[i])
        for row,rowdata in enumerate(datalist):
            row=row+1
            for j in range(0,len(row0)):
                sheet1.write(row,j,rowdata[j])

        filename = request.user.username + '_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
        workbook.save(path + '/' + filename)
        os.popen(r'chmod 777 %s' % (path + '/' + filename))

        # 上传oss对象
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT, BUCKETNAME_XLS)
        bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
        # 删除现有的
        for object_info in oss2.ObjectIterator(bucket,
                                               prefix='%s/%s_' % (request.user.username, request.user.username)):
            bucket.delete_object(object_info.key)
        bucket.put_object(u'%s/%s' % (request.user.username, filename), open(path + '/' + filename))

        messages.error(request, u'%s%s.%s/%s/%s' % (PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, request.user.username,
                                                    filename) + u':成功导出,可点击Download下载到本地............................。')
    to_excel.short_description=u'导出Excel'




    def save_models(self):
        obj = self.new_obj
        request = self.request
        subskus = classmainsku(connection).get_sku_by_mainsku(obj.MainSKU)
        if subskus:
            for subsku in subskus:
                py_obj=b_goods.objects.filter(SKU=subsku).values('CostPrice').first()
                if py_obj:
                    obj.CostPrice=py_obj.get('CostPrice')
                    break
        obj.Lock = 1
        obj.DateTime=datetime.datetime.now()
        if not obj.Buyer:
            obj.Buyer=request.user.first_name
        obj.save()

    def py_pic(self,obj):
        MainSKU=obj.MainSKU
        info=MainSKU+' (split) '+str(obj.id)
        defaultpic=obj.Main_Pic
        # _subskus=b_goods.objects.filter(MainSKU=MainSKU).values_list('SKU')
        # subskus=[x[0] for x in _subskus]
        # info=''
        # for subsku in subskus:
        #     info=info+str(int(obj.id))+","+'http://122.226.216.10:89/ShopElf/images/{}.jpg'.format(subsku)+","+subsku+'(*&#'
        #
        if not defaultpic and MainSKU:
            # _subskus = t_product_mainsku_sku.objects.filter(MainSKU=MainSKU).values_list('ProductSKU')
            # subskus = [x[0] for x in _subskus]
            subskus =classmainsku(connection).get_sku_by_mainsku(MainSKU)
            if subskus:
                for subsku in subskus:
                    url = 'http://122.226.216.10:89/ShopElf/images/{}.jpg'.format(subsku)
                    try:
                        pic_response=requests.get(url, timeout=0.3)
                        if pic_response.status_code==200:
                            break
                    except Exception:
                        pass
                else:
                    url = 'http://fancyqube-sv.oss-cn-shanghai.aliyuncs.com/8WDXkA6gAa/l5pyikRRWW.jpg'
            else:
                try:
                    url = 'http://122.226.216.10:89/ShopElf/images/{}.jpg'.format(MainSKU)
                    pic_response = requests.get(url, timeout=0.2)
                    if pic_response.status_code != 200:
                        url = 'http://fancyqube-sv.oss-cn-shanghai.aliyuncs.com/8WDXkA6gAa/l5pyikRRWW.jpg'
                except Exception:
                    url = 'http://fancyqube-sv.oss-cn-shanghai.aliyuncs.com/8WDXkA6gAa/l5pyikRRWW.jpg'
            obj.Main_Pic = url
            obj.save()
        elif defaultpic:
            url = defaultpic
        else:
            url = 'http://fancyqube-sv.oss-cn-shanghai.aliyuncs.com/8WDXkA6gAa/l5pyikRRWW.jpg'

        rt = '<table><tr><img src="%s" width="150" height="150" alt = "%s" title="%s">' \
             '</img></tr>'%(url,url,url)

        rt = u'%s<tr><td>' \
             u'<button type="button" class="btn btn-primary btn-xs" id="edit_supply_chain_production_button" ' \
             u'onclick="gen_pic(\'%s\')">更多图片</button></td></tr></table>' % (rt,info)

        return mark_safe(rt)

    py_pic.short_description=u'图片'





# coding:utf8
from __future__ import unicode_literals

from distutils.log import Log

import xadmin
# from nose import loader
from django.utils.safestring import mark_safe
from brick.public.upload_to_oss import upload_to_oss
from xadmin import views
from xadmin.plugins.inline import Inline
from xadmin.views import BaseAdminPlugin
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field, Div, FormActions, Submit, Button, ButtonHolder, InlineRadios, Reset, StrictButton, HTML, Hidden, Alert
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
import datetime

from skuapp.table.goods_quality_check import Newshop_feedback, GoodsResponse_table, BugerResponse_table, WarehouseSpecialist_table, \
    GoodsCheck_table, Result_table
from django.contrib import messages


'''

'''


class Newshop_feedbackAdmin(object):
    """
    平台提交
    """

    actions = ['to_goods_response', 'to_bug_response']


    def to_goods_response(self, request, queryset):
        # to_good_data = GoodsResponse_table.objects.filter(name=request.name)
        return HttpResponseRedirect('/Project/admin/skuapp/goodsresponse_table/')

    to_goods_response.short_description = u'产品专员反馈信息'

    def to_bug_response(self, request, queryset):

            
        return HttpResponseRedirect('/Project/admin/skuapp/bugerresponse_table/%s')%([bug for bug in to_bug_response ]['sku'])
    to_bug_response.short_description = u'采购员反馈信息'




    def name(self,obj):

        return mark_safe('<p>%s</p>'%self.request.user.first_name)
    name.short_description=u'提交人'



    list_display = ['sku','name', 'terrace', 'order_number', 'request_type', 'requset_response','others','put_time','update_time']
                    
    #list_display_links=['picture','picture1','picture2']
    search_fields = ['sku','terrace', 'order_number', 'sku', 'request_type', 'requset_response', 'picture','picture1','picture2',
                      'sku','update_time']
    list_filter = ['sku','terrace', 'order_number', 'sku', 'request_type', 'requset_response', 'picture','picture1','picture2', 'put_time',
                   'update_time']
    list_editable=['others']

    #设置定时刷新
    refresh_times=[False,60]
    



    






class GoodsResponse_tableAdmin(object):
    """
    产品专员反馈信息
    """

    
    
    

    list_display = ['sku','name', 'supplier_name', 'goods_name','remark' ,'time','updata_time']

    search_fields = ['name', 'supplier_name', 'goods_name', 'remark' ,'time','updata_time']
    list_filter = ['name', 'supplier_name', 'goods_name', 'remark' ,'time','updata_time']

    list_readonly = ['name', ]

    refresh_times = [False,60]

    actions=['to_bug_response','GoodsCheck']

    def to_bug_response(self, request, queryset):

        return HttpResponseRedirect('/Project/admin/skuapp/bugerresponse_table/')
    to_bug_response.short_description = u'采购员反馈'

    def GoodsCheck(self, request, queryset):

        return HttpResponseRedirect('/Project/admin/skuapp/goodscheck_table/')

    GoodsCheck.short_description = u'品控组审核'












class BugerResponse_tableAdmin(object):
    """
    采购反馈表
    """
    list_display = ['sku','name', 'supplier_name', 'goods_name', 'goods_category', 'remark' ,'time','update_time']

    search_fields = ['name', 'supplier_name', 'goods_name', 'goods_category', 'remark' ,'time','update_time']
    list_filter = ['name', 'supplier_name', 'goods_name', 'goods_category', 'remark' ,'time','update_time']

    refresh_times = [False,60]

    actions=['GoodsCheck','WarehouseSpecialist']

    def GoodsCheck(self, request, queryset):

        return HttpResponseRedirect('/Project/admin/skuapp/goodscheck_table/')

    GoodsCheck.short_description = u'品控组审核'

    def WarehouseSpecialist(self, request, queryset):

        return HttpResponseRedirect('/Project/admin/skuapp/warehousespecialist_table')

    WarehouseSpecialist.short_description = u'仓库负责人反馈'


    # add_form_template='button.html'
    # change_form_template='button.html'


class WarehouseSpecialist_tableAdmin(object):
    """
    仓库反馈信息
    """
    list_display = ['sku', 'name', 'charge_number','goods_numbers','remark', 'time', 'update_time']

    search_fields = ['name', 'sku','remark','goods_numbers', 'time', 'update_time']
    list_filter = ['name', 'sku','remark', 'goods_numbers','time', 'update_time']
    list_editable=['goods_numbers',]

    actions=['GoodsCheck',]


    def GoodsCheck(self, request, queryset):
        # to_bug_response = GoodsResponse_table.objects.filter(name=request.name)
        return HttpResponseRedirect('/Project/admin/skuapp/goodscheck_table/')

    GoodsCheck.short_description = u'品控组审核'

    def charge_number(self, obj):
        rt = '<table   style="text-align:center;" border="1" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1"><tr bgcolor="#C00"><th style="text-align:center">采购专员</th><th style="text-align:center">供应商</th><th style="text-align:center">产品名称</th><th style="text-align:center">备注</th></tr>'
        GoodsResponse_table_show = GoodsResponse_table.objects.values('name', 'supplier_name', 'goods_name', 'remark').filter(sku=obj.sku)

        i = 0
        for goods in GoodsResponse_table_show:
            if i < 4:
                rt = '%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> ' % (
                rt, goods['name'], goods['supplier_name'],
                goods['goods_name'],goods['remark'])

                i = i + 1
        if len(GoodsResponse_table_show) > 5:
            rt = '%s<tr><td><a id="link_id_%s">查看更多</a></td></tr>' % (rt, obj.name)
        else:
            rt = rt
        rt = "%s</table><script>$('#link_id_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['500px','500px'],content:'/Project/admin/skuapp/bugerresponse_table/?abc=%s',});});</script>" % (
        rt, obj.id, obj.name)
        return mark_safe(rt)

    charge_number.short_description = mark_safe('<p align="center">采购详情</p>')







class GoodsCheck_tableAdmin(object):
    """
    品控审核表
    """
    list_display = ['sku','name', 'goodsresponse', 'goodsResponse_result','bugerresponse','bugerResponse_result','warehousespecialist','warehouseSpecialist_result','time','update_time']

    search_fields = ['name', 'sku', 'goodsResponse_result','bugerResponse_result','warehouseSpecialist_result','time','update_time']
    list_filter = ['name','sku', 'goodsResponse_result','bugerResponse_result','warehouseSpecialist_result','time','update_time']
    list_editable=['goodsResponse_result','bugerResponse_result','warehouseSpecialist_result']

    
    
    
    def bugerresponse(self, obj):
        rt = '<table   style="text-align:center;" border="1" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1"><tr bgcolor="#C00"><th style="text-align:center">sku</th><th style="text-align:center">采购专员</th><th style="text-align:center">供应商</th><th style="text-align:center">产品名称</th><th style="text-align:center">产品分类</th><th style="text-align:center">备注</th></tr>'
        GoodsResponse_table_show = BugerResponse_table.objects.values('sku','name', 'supplier_name', 'goods_name','goods_category','remark').filter(sku=obj.sku)
                                                                      

        i = 0
        for goods in GoodsResponse_table_show:
            if i < 4:
                rt = '%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> ' % (
                    rt, goods['sku'],goods['name'], goods['supplier_name'],goods['goods_category'],
                    goods['goods_name'], goods['remark'])

                i = i + 1
        if len(GoodsResponse_table_show) > 5:
            rt = '%s<tr><td><a id="link_id_%s">查看更多</a></td></tr>' % (rt, obj.sku)
        else:
            rt = rt
        rt = "%s</table><script>$('#link_id_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['500px','500px'],content:/Project/admin/skuapp/bugerresponse_table/?abc=%s',});});</script>" % (rt, obj.id, obj.id)
            
        return mark_safe(rt)

    bugerresponse.short_description = mark_safe('<p align="center">采购详情</p>')












    def goodsresponse(self, obj):
        rt = '<table   style="text-align:center;" border="1" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1"><tr bgcolor="#C00"><th style="text-align:center">sku</th><th style="text-align:center">采购专员</th><th style="text-align:center">供应商</th><th style="text-align:center">产品名称</th><th style="text-align:center">备注</th></tr>'
        GoodsResponse_table_show = GoodsResponse_table.objects.values('sku','name', 'supplier_name', 'goods_name','remark').filter(sku=obj.sku)
                                                                      

        i = 0
        for goods in GoodsResponse_table_show:
            if i < 4:
                rt = '%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> ' % (
                    rt,goods['sku'], goods['name'], goods['supplier_name'],
                    goods['goods_name'], goods['remark'])

                i = i + 1
        if len(GoodsResponse_table_show) > 5:
            rt = '%s<tr><td><a id="link_id_%s">查看更多</a></td></tr>' % (rt, obj.name)
        else:
        
            rt = rt
        rt = "%s</table><script>$('#link_id_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['500px','500px'],content:'/Project/admin/skuapp/bugerresponse_table/?abc=%s',});});</script>" % (rt, obj.id, obj.id)
            
        return mark_safe(rt)

    goodsresponse.short_description = mark_safe('<p align="center">产品专员反馈与结果</p>')











    def warehousespecialist(self, obj):
        rt = '<table   style="text-align:center;" border="1" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1"><tr bgcolor="#C00"><th style="text-align:center">sku</th><th style="text-align:center">仓库负责人</th><th style="text-align:center">采购数量</th><th style="text-align:center">备注</th></tr>'
        GoodsResponse_table_show = WarehouseSpecialist_table.objects.values('sku','name', 'goods_numbers', 'remark').filter(sku=obj.sku)
                                                                      

        i = 0
        for goods in GoodsResponse_table_show:
            if i < 4:
                rt = '%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> ' % (
                    rt, goods['sku'],goods['name'], goods['goods_numbers'],goods['remark'])
                     

                i = i + 1
        if len(GoodsResponse_table_show) > 5:
            rt = '%s<tr><td><a id="link_id_%s">查看更多</a></td></tr>' % (rt, obj.name)
        else:
            rt = rt
        rt = "%s</table><script>$('#link_id_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['500px','500px'],content:'/Project/admin/skuapp/WarehouseSpecialist_table/?abc=%s',});});</script>" % (rt, obj.id, obj.id)
            
        return mark_safe(rt)

    warehousespecialist.short_description = mark_safe('<p align="center">仓库方反馈与结果</p>')






class Result_tableAdmin(object):
    """
    结果反馈信息总表
    """
    list_display = ['sku','terrace','goodsresponse', 'gooods_check_man', 'goodsResponse_result','bugerresponse','buger_check_man','bugerResponse_result','warehousespecialist','warehouse_check_man','warehouseSpecialist_result','time','update_time']
    search_fields = [ 'time','update_time']
    list_filter = [ 'time','update_time']
    refresh_times=[False,60]
    list_editable=['goodsResponse_result','bugerResponse_result','warehouseSpecialist_result',]
    search_box_flag = True









    def bugerresponse(self, obj):
        rt = '<table   style="text-align:center;" border="1" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1"><tr bgcolor="#C00"><th style="text-align:center">sku</th><th style="text-align:center">采购专员</th><th style="text-align:center">供应商</th><th style="text-align:center">产品名称</th><th style="text-align:center">产品分类</th><th style="text-align:center">备注</th></tr>'
        GoodsResponse_table_show = BugerResponse_table.objects.values('sku','name', 'supplier_name', 'goods_name','goods_category','remark').filter(sku=obj.sku)
                                                                      

        i = 0
        for goods in GoodsResponse_table_show:
            if i < 4:
                rt = '%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> ' % (
                    rt, goods['sku'],goods['name'], goods['supplier_name'],goods['goods_category'],
                    goods['goods_name'], goods['remark'])

                i = i + 1
        if len(GoodsResponse_table_show) > 5:
            rt = '%s<tr><td><a id="link_id_%s">查看更多</a></td></tr>' % (rt, obj.sku)
        else:
            rt = rt
        rt = "%s</table><script>$('#link_id_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['500px','500px'],content:/Project/admin/skuapp/bugerresponse_table/?abc=%s',});});</script>" % (rt, obj.id, obj.id)
            
        return mark_safe(rt)

    bugerresponse.short_description = mark_safe('<p align="center">采购详情</p>')












    def goodsresponse(self, obj):
        rt = '<table   style="text-align:center;" border="1" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1"><tr bgcolor="#C00"><th style="text-align:center">sku</th><th style="text-align:center">采购专员</th><th style="text-align:center">供应商</th><th style="text-align:center">产品名称</th><th style="text-align:center">备注</th></tr>'
        GoodsResponse_table_show = GoodsResponse_table.objects.values('sku','name', 'supplier_name', 'goods_name','remark').filter(sku=obj.sku)
                                                                      

        i = 0
        for goods in GoodsResponse_table_show:
            if i < 4:
                rt = '%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> ' % (
                    rt,goods['sku'], goods['name'], goods['supplier_name'],
                    goods['goods_name'], goods['remark'])

                i = i + 1
        if len(GoodsResponse_table_show) > 5:
            rt = '%s<tr><td><a id="link_id_%s">查看更多</a></td></tr>' % (rt, obj.name)
        else:
        
            rt = rt
        rt = "%s</table><script>$('#link_id_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['500px','500px'],content:'/Project/admin/skuapp/bugerresponse_table/?abc=%s',});});</script>" % (rt, obj.id, obj.id)
            
        return mark_safe(rt)

    goodsresponse.short_description = mark_safe('<p align="center">产品专员反馈与结果</p>')











    def warehousespecialist(self, obj):
        rt = '<table   style="text-align:center;" border="1" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1"><tr bgcolor="#C00"><th style="text-align:center">sku</th><th style="text-align:center">仓库负责人</th><th style="text-align:center">采购数量</th><th style="text-align:center">备注</th></tr>'
        GoodsResponse_table_show = WarehouseSpecialist_table.objects.values('sku','name', 'goods_numbers', 'remark').filter(sku=obj.sku)
                                                                      

        i = 0
        for goods in GoodsResponse_table_show:
            if i < 4:
                rt = '%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> ' % (
                    rt, goods['sku'],goods['name'], goods['goods_numbers'],goods['remark'])
                     

                i = i + 1
        if len(GoodsResponse_table_show) > 5:
            rt = '%s<tr><td><a id="link_id_%s">查看更多</a></td></tr>' % (rt, obj.name)
        else:
            rt = rt
        rt = "%s</table><script>$('#link_id_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['500px','500px'],content:'/Project/admin/skuapp/WarehouseSpecialist_table/?abc=%s',});});</script>" % (rt, obj.id, obj.id)
            
        return mark_safe(rt)

    warehousespecialist.short_description = mark_safe('<p align="center">仓库方反馈与结果</p>')










    def terrace(self,obj):

        rt = '<table   style="text-align:center;" border="1" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1"><tr bgcolor="#C00"><th style="text-align:center">sku</th><th style="text-align:center">提交人</th><th style="text-align:center">平台</th><th style="text-align:center">浦沅订单号</th><th style="text-align:center">问题类型</th><th style="text-align:center">具体反馈</th></tr>'
        Newshop_feedback_show = Newshop_feedback.objects.values('sku','put_name', 'terrace', 'order_number','request_type','requset_response').filter(sku=obj.sku)


        i = 0
        for goods in Newshop_feedback_show:
            if i < 4:
                rt = '%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> ' % (
                    rt, goods['sku'],goods['put_name'], goods['terrace'],goods['order_number'], 
                    goods['request_type'], goods['requset_response'])

                i = i + 1
        if len(Newshop_feedback_show) > 5:
            rt = '%s<tr><td><a id="link_id_%s">查看更多</a></td></tr>' %(rt,obj.sku)
        else:
            rt = rt
        rt = "%s</table><script>$('#link_id_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['500px','500px'],content:'/Project/admin/skuapp/newshop_feedback/?abc=%s',});});</script>" % (rt, obj.id, obj.id)
            
        return mark_safe(rt)

    terrace.short_description=mark_safe("<p align='center'>平台反馈信息</p>")


        #url = u'https://contestimg.wish.com/api/webimage/%s-medium.jpg'%str(obj.ProductID)
        #rt =  '<img src="%s"  width="120" height="120"  alt = "%s"  title="%s"  />  '%(url,url,url)
        #return mark_safe(rt)











    def get_list_queryset(self):
        
        request = self.request
        qs = super(Result_tableAdmin, self).get_list_queryset()
        sku = request.GET.get('sku', '')
        gooods_check_man = request.GET.get('gooods_check_man','')
        buger_check_man = request.GET.get('buger_check_man','')
        bugerResponse_result = request.GET.get('bugerResponse_result','')

            
        warehouse_check_man = request.GET.get('warehouse_check_man','')
        warehouseSpecialist_result = request.GET.get('warehouseSpecialist_result','')
        time=request.GET.get('time','')
        update_time=request.GET.get('update_time','')
        
        


        
        searchList = {  
                        'sku__exact': sku,
                        'gooods_check_man__exact': gooods_check_man, 
                        'buger_check_man__exact': buger_check_man,
                        'bugerResponse_result__exact': bugerResponse_result,
                        'warehouse_check_man__exact':warehouse_check_man, 
                        'warehouseSpecialist_result__exact': warehouseSpecialist_result,
                        'time__exact':time,
                        'update_time__exact':update_time,

                      }
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    # if k == 'ShopName__exact':
                    #  v = 'Wish-' + v.zfill(4)
                    # messages.error(request, v)
                    sl[k] = v
        if sl is not None:

            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')

        return qs







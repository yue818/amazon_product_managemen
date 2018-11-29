# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from .models import *
from django.db import transaction,connection
from django import forms
import xadmin
from django.utils.safestring import mark_safe
from Project.settings import *
from django.contrib import messages  
from django.shortcuts import render_to_response,RequestContext  
from django.template import Context  
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db import models
from xadmin.sites import site
from xadmin.views import BaseAdminPlugin, ListAdminView
from pyapp.models import *
from skuapp.table.t_shopsku_information_binding import t_shopsku_information_binding
from datetime import datetime as ddtime
from pyapp.models import b_goodsskulinkshop as py_b_goodsskulinkshop
from pyapp.models import b_goodssku as py_b_goodssku
import csv
from pyapp.plugin.syn_b_goods_plugin import syn_b_goods_plugin
from skuapp.table.t_product_mainsku_sku import *
from pyapp.modelsadminx.t_cloth_factory_dispatch_apply_Admin import t_cloth_factory_dispatch_apply_Admin
from brick.classredis.classshopsku import classshopsku
from skuapp.table.t_online_info import t_online_info
from django_redis import get_redis_connection
redis_coon = get_redis_connection(alias='product')
classshopsku_obj = classshopsku(db_conn=None,redis_conn=redis_coon)
from pyapp.table.t_cloth_factory_dispatch_apply import t_cloth_factory_dispatch_apply
xadmin.site.register(t_cloth_factory_dispatch_apply,t_cloth_factory_dispatch_apply_Admin)
from pyapp.table.kc_currentstock_sku import kc_currentstock_sku
from sqlapp.models import *
from pyapp.table.kc_currentstock_cg_purchaser import kc_currentstock_cg_purchaser
from django.contrib.auth.models import User

class t_stockorderm_refund_Admin(object):
    orderm_tree_menu = True
    search_box_flag = True
    actions = ['batch_to_archive']
    
    def batch_to_archive(self,request,objs):
        import datetime
        import pymssql
        
        try:
            userID = [each.id for each in User.objects.filter(groups__id__in=[19])]
            if request.user.id not in userID:
                messages.info(request, u'Sorry,该用户不具备归档的权限!')
            else:
                result_error = 0
                result_success = 0
                pyuanConn = pymssql.connect(host='122.226.216.10', port=18793, user='sa', password='$%^AcB2@9!@#',database='ShopElf', charset='utf8')
                sqlpycur = pyuanConn.cursor()
                nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                logs = request.user.first_name + ' ' + nowtime + ' 订单归档!'.decode('utf-8')
                for qs in objs:         
                    sqlpy1 = '''update cg_stockorderm set Archive = 1,ArchiveDate='%s' where NID = %s;
                            insert into CG_StockLogs(OrderType,OrderNid,Operator,Logs) values('采购订单',%s,'%s','%s')''' % (nowtime,qs.stockordermID,qs.stockordermID,request.user.first_name,logs)
                    sqlpycur.execute(sqlpy1)
                    #sqlpycur.execute('commit')
                
                    if qs.refundWay in ['计损订单']:
                        t_stockorderm_refund.objects.filter(stockordermID=qs.stockordermID).update(Archive=1,refundStatus='-1',archiveMan=request.user.first_name,archiveTime=nowtime)
                    else:
                        #if qs.transferNumber:#有转账流水号的直接退款成功
                            #t_stockorderm_refund.objects.filter(stockordermID=qs.stockordermID).update(Archive=1,refundStatus=3,archiveMan=request.user.first_name,archiveTime=nowtime)
                        #else:
                        t_stockorderm_refund.objects.filter(stockordermID=qs.stockordermID).update(Archive=1,refundStatus=1,archiveMan=request.user.first_name,archiveTime=nowtime)
                    result_success += 1
                pyuanConn.commit()
                sqlpycur.close()
                pyuanConn.close()
                
                messages.info(request, u'选中%d条,成功归档%d条.' % (objs.count(), result_success))
        except Exception, e:
            messages.error(request,'%s'%repr(e))
            pass
    batch_to_archive.short_description = u'批量归档'  
    
    def show_diff_price(self,obj):
        rt = 0
        try:
            rt =  obj.SystemMoney - obj.refundMoney
        except Exception, e:
            pass
        return mark_safe(rt)
    show_diff_price.short_description = mark_safe('<p style="color:#428bca;">差价</p>')

    def show_handle_archive(self, obj):
        rt = ''
        archive_obj = cg_stockorderm.objects.filter(NID=obj.stockordermID).values()
        if not archive_obj:
            messages.error(self.request,'订单%s普源不存在!'%obj.billNumber)
        else:
            if archive_obj[0]['Archive'] == 0:
                rt = '<input type="checkbox" id="cg_%s" onclick="update_cg_archive_%s()"></input>' % (obj.NID,obj.NID)
            else:
                rt = '<input type="checkbox" id="cg_%s" onclick="update_cg_archive_%s()" checked></input>' % (obj.NID,obj.NID)
            rt = rt + '''<span id="cgt_id_ts_%s" style="color:#F00"></span><script>{function update_cg_archive_%s(){var cgcheck =  document.getElementById("cg_%s");
                if(cgcheck.checked==1){$.ajax({url:"/shift_to_archive/",type:"GET",contentType:"application/x-www-form-urlencoded:charset=UTF-8",datatype:"json",
                data:{"index":1,"id":%s},success:function(data,textStatus,jqXHR){if(data.status==0){document.getElementById("cgt_id_ts_%s").innerHTML="已归档!";}
                else if(data.status==1){document.getElementById("cgt_id_ts_%s").innerHTML="Failed,No Permmison!";document.getElementById('cg_%s').checked='';}
                else{document.getElementById("cgt_id_ts_%s").innerHTML="服务器内部错误!";document.getElementById('cg_%s').checked='';}},error:function(data){alert("failed");}})}
                else{$.ajax({url:"/shift_to_archive/",type:"GET",contentType:"application/x-www-form-urlencoded:charset=UTF-8",datatype:"json",data:{"index":2,"id":%s},
                success:function(data,textStatus,jqXHR){if(data.status==0){document.getElementById("cgt_id_ts_%s").innerHTML="已取消归档!";}
                else if(data.status==1){document.getElementById("cgt_id_ts_%s").innerHTML="Failed,No Permmison!";document.getElementById('cg_%s').checked='';}
                else{document.getElementById("cgt_id_ts_%s").innerHTML="服务器内部错误!";document.getElementById('cg_%s').checked='';}},error:function(){alert("failed");}})}}}
                </script>'''%(obj.NID,obj.NID,obj.NID,obj.stockordermID,obj.NID,obj.NID,obj.NID,obj.NID,obj.NID,obj.stockordermID,obj.NID,obj.NID,obj.NID,obj.NID,obj.NID)
            
        return mark_safe(rt)
    show_handle_archive.short_description = mark_safe('<p style="width:60px;color:#428bca;">归档</p>')
    
    list_display_links = ('NID',)
    list_display = ('billNumber','refundWay','purchaser','alibabaRefundNumber','refundNum','refundMoney','show_diff_price','transferNumber','refundReason','processer','note','refundDate','show_handle_archive')
    list_editable = ('transferNumber','refundNum','refundMoney','refundReason','note',)
    
    def get_list_queryset(self,):
        request = self.request
        qs = super(t_stockorderm_refund_Admin, self).get_list_queryset()

        refundDateStart = request.GET.get('refundDateStart','')
        refundDateEnd = request.GET.get('refundDateEnd','')
        BillNumber = request.GET.get('BillNumber','')
        #BillNumber = [ gs for gs in BillNumber.split(',') if gs ]
        processer = request.GET.get('processer','')
        processer = [ gs for gs in processer.split(',') if gs ]
        Purchaser = request.GET.get('Purchaser','')
        Purchaser = [ gs for gs in Purchaser.split(',') if gs ]
        transferNumber = request.GET.get('transferNumber','')
        #transferNumber = [ gs for gs in transferNumber.split(',') if gs ]
        Notes = request.GET.get('Notes','')
        refundWay = request.GET.get('refundWay','')
        refundWay = [ gs for gs in refundWay.split(',') if gs ]
        alibabaRefundNumber = request.GET.get('alibabaRefundNumber','')
        
        searchList = {'billNumber__icontains':BillNumber,'purchaser__in': Purchaser,
                    'alibabaRefundNumber__icontains':alibabaRefundNumber,
                    'processer__in': processer,'transferNumber__icontains': transferNumber,
                    'refundDate__gte': refundDateStart, 'refundDate__lt': refundDateEnd,
                    'note__icontains':Notes,'refundWay__in':refundWay}
            
        sl = {}
        for k,v in searchList.items():
            if isinstance(v,list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    sl[k] = v
        if not sl:
            if self.request.user.first_name in kc_currentstock_cg_purchaser.objects.filter(permission=0).values_list('Purchaser',flat=True):
                qs = qs.filter(purchaser=self.request.user.first_name)
        try:
            qs = qs.filter(**sl)
        except Exception,ex:
            messages.error(request,u'输入的查询数据有问题！')
    
        return qs.filter(refundStatus=0)
xadmin.site.register(t_stockorderm_refund,t_stockorderm_refund_Admin)

class t_stockorderm_refund_track_Admin(object):#采购退款跟踪
    orderm_tree_menu = True
    search_box_flag = True
    
    def show_handle_refund(self, obj):
        rt = '''<script>function update_cg_archive_%s(){var cgcheck =  document.getElementById("cg_%s");
            if(cgcheck.checked==1){$.ajax({url:"/shift_to_archive/",type:"GET",
            contentType:"application/x-www-form-urlencoded:charset=UTF-8",datatype:"json",data:{"index":3,"id":%s},
            success:function(data,textStatus,jqXHR){if(data.status==0)document.getElementById("cgt_id_ts_%s").innerHTML="已选择!";
            else if(data.status==1){document.getElementById("cgt_id_ts_%s").innerHTML="Failed,No Permmison!";document.getElementById("cg_%s").checked='';}
            else{document.getElementById("cgt_id_ts_%s").innerHTML="服务器内部错误!";document.getElementById("cg_%s").checked='';}
            },error:function(data){alert("failed");}})}
            else{$.ajax({url:"/shift_to_archive/",type:"GET",
            contentType:"application/x-www-form-urlencoded:charset=UTF-8",datatype:"json",data:{"index":4,"id":%s},
            success:function(data,textStatus,jqXHR){if(data.status==0)document.getElementById("cgt_id_ts_%s").innerHTML="已取消!";
            else if(data.status==1){document.getElementById("cgt_id_ts_%s").innerHTML="Failed,No Permmison!";document.getElementById("cg_%s").checked='';}
            else{document.getElementById("cgt_id_ts_%s").innerHTML="服务器内部错误!";document.getElementById("cg_%s").checked=true;}
            },error:function(){alert("failed");}})}}</script>
            <input type="checkbox" id="cg_%s" onclick="update_cg_archive_%s()">
            <span id="cgt_id_ts_%s" style="color:#F00"><span>''' %(obj.NID,obj.NID,obj.stockordermID,obj.NID,obj.NID,obj.NID,obj.NID,obj.NID,obj.stockordermID,obj.NID,obj.NID,obj.NID,obj.NID,obj.NID,obj.NID,obj.NID,obj.NID)
            
        return mark_safe(rt)
    show_handle_refund.short_description = mark_safe('<p style="width:80px;color:#428bca;">退款成功</p>')

    list_display_links = ('NID',)
    list_display = ('billNumber','refundWay','purchaser','alibabaRefundNumber','refundNum','refundMoney','transferNumber','refundReason','processer','note','financeNote','refundDate','show_handle_refund')
    list_editable = ('transferNumber','refundNum','refundMoney','refundReason','note','financeNote')
    
    def get_list_queryset(self,):
        request = self.request
        qs = super(t_stockorderm_refund_track_Admin, self).get_list_queryset()

        refundDateStart = request.GET.get('refundDateStart','')
        refundDateEnd = request.GET.get('refundDateEnd','')
        BillNumber = request.GET.get('BillNumber','')
        #BillNumber = [ gs for gs in BillNumber.split(',') if gs ]
        processer = request.GET.get('processer','')
        processer = [ gs for gs in processer.split(',') if gs ]
        Purchaser = request.GET.get('Purchaser','')
        Purchaser = [ gs for gs in Purchaser.split(',') if gs ]
        
        transferNumber = request.GET.get('transferNumber','')
        #transferNumber = [ gs for gs in transferNumber.split(',') if gs ]
        
        Notes = request.GET.get('Notes','')
        refundWay = request.GET.get('refundWay','')
        refundWay = [ gs for gs in refundWay.split(',') if gs ]
        
        alibabaRefundNumber = request.GET.get('alibabaRefundNumber','')
        
        searchList = {'billNumber__icontains':BillNumber,'purchaser__in': Purchaser,
                    'alibabaRefundNumber__icontains':alibabaRefundNumber,
                    'processer__in': processer,'transferNumber__icontains': transferNumber,
                    'refundDate__gte': refundDateStart, 'refundDate__lt': refundDateEnd,
                    'note__icontains':Notes,'refundWay__in':refundWay}
            
        sl = {}
        for k,v in searchList.items():
            if isinstance(v,list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    sl[k] = v
        if not sl:
            if self.request.user.first_name in kc_currentstock_cg_purchaser.objects.filter(permission=0).values_list('Purchaser',flat=True):
                qs = qs.filter(purchaser=self.request.user.first_name)
        try:
            qs = qs.filter(**sl)
        except Exception,ex:
            messages.error(request,u'输入的查询数据有问题！')
    
        return qs.filter(refundStatus=1,Archive=1)
xadmin.site.register(t_stockorderm_refund_track,t_stockorderm_refund_track_Admin)

class t_stockorderm_refund_success_confirm_Admin(object):#财务确认退款成功
    orderm_tree_menu = True
    search_box_flag = True
    
    def show_handle_refund(self, obj):
        rt = '''<script>function update_cg_archive_%s(){var cgcheck =  document.getElementById("cg_%s");
            if(cgcheck.checked==1){$.ajax({url:"/shift_to_archive/",type:"GET",
            contentType:"application/x-www-form-urlencoded:charset=UTF-8",datatype:"json",data:{"index":5,"id":%s},
            success:function(data,textStatus,jqXHR){if(data.status==0)document.getElementById("cgt_id_ts_%s").innerHTML="已选择!";
            else if(data.status==1){document.getElementById("cgt_id_ts_%s").innerHTML="Failed,No Permmison!";document.getElementById("cg_%s").checked='';}
            else{document.getElementById("cgt_id_ts_%s").innerHTML="服务器内部错误!";document.getElementById("cg_%s").checked='';}
            },error:function(data){alert("failed");}})}
            else{$.ajax({url:"/shift_to_archive/",type:"GET",
            contentType:"application/x-www-form-urlencoded:charset=UTF-8",datatype:"json",data:{"index":6,"id":%s},
            success:function(data,textStatus,jqXHR){if(data.status==0)document.getElementById("cgt_id_ts_%s").innerHTML="已取消!";
            else if(data.status==1){document.getElementById("cgt_id_ts_%s").innerHTML="Failed,No Permmison!";document.getElementById("cg_%s").checked='';}
            else{document.getElementById("cgt_id_ts_%s").innerHTML="服务器内部错误!";document.getElementById("cg_%s").checked=true;}
            },error:function(){alert("failed");}})}}
            function track_cg_archive_%s(){var cgcheck =  document.getElementById("track_%s");
            if(cgcheck.checked==1){$.ajax({url:"/shift_to_archive/",type:"GET",
            contentType:"application/x-www-form-urlencoded:charset=UTF-8",datatype:"json",data:{"index":7,"id":%s},
            success:function(data,textStatus,jqXHR){if(data.status==0)document.getElementById("track_id_ts_%s").innerHTML="已选择!";
            else if(data.status==1){document.getElementById("track_id_ts_%s").innerHTML="Failed,No Permmison!";document.getElementById("track_%s").checked='';}
            else{document.getElementById("track_id_ts_%s").innerHTML="服务器内部错误!";document.getElementById("track_%s").checked='';}
            },error:function(data){alert("failed");}})}
            else{$.ajax({url:"/shift_to_archive/",type:"GET",
            contentType:"application/x-www-form-urlencoded:charset=UTF-8",datatype:"json",data:{"index":8,"id":%s},
            success:function(data,textStatus,jqXHR){if(data.status==0)document.getElementById("track_id_ts_%s").innerHTML="已取消!";
            else if(data.status==1){document.getElementById("track_id_ts_%s").innerHTML="Failed,No Permmison!";document.getElementById("track_%s").checked='';}
            else{document.getElementById("track_id_ts_%s").innerHTML="服务器内部错误!";document.getElementById("track_%s").checked=true;}
            },error:function(){alert("failed");}})}}</script>
            <div><input type="checkbox" id="cg_%s" onclick="update_cg_archive_%s()">退款成功<span id="cgt_id_ts_%s" style="color:#F00"></span></div><br>
            <div><input type="checkbox" id="track_%s" onclick="track_cg_archive_%s()">驳回至订单跟踪<span id="track_id_ts_%s" style="color:#F00"></span></div>''' %(
            obj.stockordermID,obj.stockordermID,obj.stockordermID,obj.stockordermID,obj.stockordermID,obj.stockordermID,obj.stockordermID,obj.stockordermID,obj.stockordermID,
            obj.stockordermID,obj.stockordermID,obj.stockordermID,obj.stockordermID,obj.stockordermID,obj.stockordermID,obj.stockordermID,obj.stockordermID,obj.stockordermID,
            obj.stockordermID,obj.stockordermID,obj.stockordermID,obj.stockordermID,obj.stockordermID,obj.stockordermID,obj.stockordermID,obj.stockordermID,obj.stockordermID,
            obj.stockordermID,obj.stockordermID,obj.stockordermID,obj.stockordermID,obj.stockordermID,obj.stockordermID,obj.stockordermID)
            
        return mark_safe(rt)
    show_handle_refund.short_description = mark_safe('<p style="width:80px;color:#428bca;">财务处理</p>')

    list_display_links = ('NID',)
    list_display = ('billNumber','refundWay','purchaser','alibabaRefundNumber','refundNum','refundMoney','transferNumber','refundReason','processer','note','trackMan','trackTime','show_handle_refund')
    #list_editable = ('transferNumber','refundNum','refundMoney','refundReason','note',)
    
    def get_list_queryset(self,):
        request = self.request
        qs = super(t_stockorderm_refund_success_confirm_Admin, self).get_list_queryset()

        refundDateStart = request.GET.get('refundDateStart','')
        refundDateEnd = request.GET.get('refundDateEnd','')
        BillNumber = request.GET.get('BillNumber','')
        #BillNumber = [ gs for gs in BillNumber.split(',') if gs ]
        processer = request.GET.get('processer','')
        processer = [ gs for gs in processer.split(',') if gs ]
        Purchaser = request.GET.get('Purchaser','')
        Purchaser = [ gs for gs in Purchaser.split(',') if gs ]
        
        transferNumber = request.GET.get('transferNumber','')
        #transferNumber = [ gs for gs in transferNumber.split(',') if gs ]
        
        Notes = request.GET.get('Notes','')
        refundWay = request.GET.get('refundWay','')
        refundWay = [ gs for gs in refundWay.split(',') if gs ]
        
        alibabaRefundNumber = request.GET.get('alibabaRefundNumber','')
        
        searchList = {'billNumber__icontains':BillNumber,'purchaser__in': Purchaser,
                    'alibabaRefundNumber__icontains':alibabaRefundNumber,
                    'processer__in': processer,'transferNumber__icontains': transferNumber,
                    'refundDate__gte': refundDateStart, 'refundDate__lt': refundDateEnd,
                    'note__icontains':Notes,'refundWay__in':refundWay}
            
        sl = {}
        for k,v in searchList.items():
            if isinstance(v,list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    sl[k] = v
        if not sl:
            if self.request.user.first_name in kc_currentstock_cg_purchaser.objects.filter(permission=0).values_list('Purchaser',flat=True):
                qs = qs.filter(purchaser=self.request.user.first_name)
        try:
            qs = qs.filter(**sl)
        except Exception,ex:
            messages.error(request,u'输入的查询数据有问题！')
    
        return qs.filter(refundStatus=2,Archive=1)
xadmin.site.register(t_stockorderm_refund_success_confirm,t_stockorderm_refund_success_confirm_Admin)

class t_stockorderm_refund_success_Admin(object):#退款成功
    orderm_tree_menu = True
    search_box_flag = True
    
    def show_handle_refund(self, obj):
            
        rt = '''<script>function update_cg_archive_%s(){var cgcheck =  document.getElementById("cg_%s");
            if(cgcheck.checked==1){$.ajax({url:"/shift_to_archive/",type:"GET",
            contentType:"application/x-www-form-urlencoded:charset=UTF-8",datatype:"json",data:{"index":3,"id":%s},
            success:function(data,textStatus,jqXHR){if(data.status==0)document.getElementById("cgt_id_ts_%s").innerHTML="退款成功!";
            else if(data.status==1){document.getElementById("cgt_id_ts_%s").innerHTML="Failed,No Permmison!";document.getElementById("cg_%s").checked='';}
            else{document.getElementById("cgt_id_ts_%s").innerHTML="服务器内部错误!";document.getElementById("cg_%s").checked='';}
            },error:function(data){alert("failed");}})}
            else{$.ajax({url:"/shift_to_archive/",type:"GET",
            contentType:"application/x-www-form-urlencoded:charset=UTF-8",datatype:"json",data:{"index":4,"id":%s},
            success:function(data,textStatus,jqXHR){if(data.status==0)document.getElementById("cgt_id_ts_%s").innerHTML="已取消退款成功!";
            else if(data.status==1){document.getElementById("cgt_id_ts_%s").innerHTML="Failed,No Permmison!";document.getElementById("cg_%s").checked='';}
            else{document.getElementById("cgt_id_ts_%s").innerHTML="服务器内部错误!";document.getElementById("cg_%s").checked=true;}
            },error:function(){alert("failed");}})}}</script>
            <input type="checkbox" id="cg_%s" onclick="update_cg_archive_%s()" checked></input>
            <span id="cgt_id_ts_%s" style="color:#F00"><span>''' %(obj.NID,obj.NID,obj.stockordermID,obj.NID,obj.NID,obj.NID,obj.NID,obj.NID,obj.stockordermID,obj.NID,obj.NID,obj.NID,obj.NID,obj.NID,obj.NID,obj.NID,obj.NID)
            
        return mark_safe(rt)
    show_handle_refund.short_description = mark_safe('<p style="width:80px;color:#428bca;">退款成功</p>')

    list_display_links = ('NID',)
    list_display = ('billNumber','refundWay','purchaser','alibabaRefundNumber','refundNum','refundMoney','transferNumber','refundReason','processer','note','financeNote','refundDate','show_handle_refund',)
    list_editable = ('transferNumber','refundNum','refundMoney','refundReason','note','financeNote')
    
    def get_list_queryset(self,):
        request = self.request
        qs = super(t_stockorderm_refund_success_Admin, self).get_list_queryset()

        refundDateStart = request.GET.get('refundDateStart','')
        refundDateEnd = request.GET.get('refundDateEnd','')
        BillNumber = request.GET.get('BillNumber','')
        #BillNumber = [ gs for gs in BillNumber.split(',') if gs ]
        processer = request.GET.get('processer','')
        processer = [ gs for gs in processer.split(',') if gs ]
        Purchaser = request.GET.get('Purchaser','')
        Purchaser = [ gs for gs in Purchaser.split(',') if gs ]
        
        transferNumber = request.GET.get('transferNumber','')
        #transferNumber = [ gs for gs in transferNumber.split(',') if gs ]
        
        Notes = request.GET.get('Notes','')
        refundWay = request.GET.get('refundWay','')
        refundWay = [ gs for gs in refundWay.split(',') if gs ]
        
        alibabaRefundNumber = request.GET.get('alibabaRefundNumber','')
        
        searchList = {'billNumber__icontains':BillNumber,'purchaser__in': Purchaser,
                    'alibabaRefundNumber__icontains':alibabaRefundNumber,
                    'processer__in': processer,'transferNumber__icontains': transferNumber,
                    'refundDate__gte': refundDateStart, 'refundDate__lt': refundDateEnd,
                    'note__icontains':Notes,'refundWay__in':refundWay}
            
        sl = {}
        for k,v in searchList.items():
            if isinstance(v,list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    sl[k] = v
        if not sl:
            if self.request.user.first_name in kc_currentstock_cg_purchaser.objects.filter(permission=0).values_list('Purchaser',flat=True):
                qs = qs.filter(purchaser=self.request.user.first_name)
        try:
            qs = qs.filter(**sl)
        except Exception,ex:
            messages.error(request,u'输入的查询数据有问题！')
    
        return qs.filter(refundStatus=3,Archive=1)
xadmin.site.register(t_stockorderm_refund_success,t_stockorderm_refund_success_Admin)

class b_supplier_money_Admin(object):
    list_display = ('NID')
xadmin.site.register(b_supplier_money,b_supplier_money_Admin)

class t_stockorderd_Admin(object):

    list_display = ('NID','StockOrderNID','GoodsID')
xadmin.site.register(t_stockorderd, t_stockorderd_Admin)

class t_stockorderm_Admin(object):
    show_warning = True
    search_box_flag = True
    
    def show_SKU_list(self,obj) :
        rt='<table   style="text-align:center;" border="1" cellpadding="3" cellspacing="1" bgcolor="#c1c1c1"><tr bgcolor="#C00"><th style="width:80px;text-align:center">商品SKU</th><th style="width:80px;text-align:center">预计可用库存</th><th style="width:80px;text-align:center">已入库数量</th><th style="width:80px;text-align:center">未入库数量</th></tr>'
        GoodsID_objs = t_stockorderd.objects.filter(StockOrderNID=obj.NID)
        try:
            skulist = []
            if GoodsID_objs:
                #messages.error(self.request,'GoodsID_objs = %s'%GoodsID_objs)       
                for GoodsID_obj in GoodsID_objs:
                    skudict = {}
                        
                    sku_objs = kc_currentstock_sku.objects.filter(GoodsID=GoodsID_obj.GoodsID)
                    if sku_objs:
                        skudict['SKU'] = sku_objs[0].SKU
                        skudict['hopeUseNum'] = sku_objs[0].hopeUseNum
                        skudict['InAmount'] = GoodsID_obj.InAmount
                        skudict['NotInAmount'] = GoodsID_obj.Amount - GoodsID_obj.InAmount
                        skulist.append(skudict)
        except Exception,e:
            messages.error(self.request,'---%s'%repr(e))
        #messages.error(self.request,'-----------%s'%skulist)
        if skulist:
            i = 0
            for skuinfo in skulist:
                if i < 5:
                    rt = '%s <tr bgcolor="#FFFFFF"><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> '%(rt,skuinfo['SKU'],skuinfo['hopeUseNum'],skuinfo['InAmount'],skuinfo['NotInAmount'])
                    i = i + 1
            if len(skulist)>5:
                rt = '%s<tr><td><a id="link_id_%s">查看更多</a></td></tr>'%(rt,obj.NID)

        rt = "%s</table><script>$('#link_id_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['500px','500px'],content:'/t_stockorderm_track/t_stockorderm_sku/?track=%s',});});</script>"%(rt,obj.NID,obj.NID)
        return mark_safe(rt)
    show_SKU_list.short_description = mark_safe('<p align="center" style="width:320px;color:#428bca;"> 订单商品</p>')
    
    def show_NotInAmount(self,obj):
        number = round(obj.OrderAmount - obj.InAmount,1)
        return mark_safe(number)
    show_NotInAmount.short_description = mark_safe('<p align="center" style="width:60px;color:#428bca;">未入库数量</p>')
    
    def showStoreName(self,obj):
        rt = ''
        storeName_objs = b_store.objects.filter(NID=obj.StoreID).values()
        if storeName_objs:
            rt = storeName_objs[0]['StoreName']
            
        return mark_safe(rt)
    showStoreName.short_description = mark_safe('<p align="center" style="width:60px;color:#428bca;">采购仓库</p>')
        
    list_display = ('NID','MakeDate','BillNumber','alibabasellername','Recorder','ExpressName','LogisticOrderNo','Note','Memo','showStoreName','OrderAmount','InAmount','show_NotInAmount','SKUCount','show_SKU_list','logisticsStatus','packagestate',)
    #list_editable = ('WarningFlag',)
    #list_filter = ('MakeDate','BillNumber','alibabasellername','Recorder','ExpressName','LogisticOrderNo','Note','Memo','StoreID','ExpressFee','OrderAmount','OrderMoney','InMoney','SKUCount','alibabaorderid','alibabamoney','packagestate','WarningFlag',)
    #search_fields = ('MakeDate','BillNumber','alibabasellername','Recorder','ExpressName','LogisticOrderNo','Note','Memo','StoreID','ExpressFee','OrderAmount','OrderMoney','InMoney','SKUCount','alibabaorderid','alibabamoney','packagestate','WarningFlag',)
    
    def get_list_queryset(self,):
        request = self.request
        qs = super(t_stockorderm_Admin, self).get_list_queryset()

        MakeDateStart = request.GET.get('MakeDateStart','')
        MakeDateEnd = request.GET.get('MakeDateEnd','')
        BillNumber = request.GET.get('BillNumber','')
        alibabasellername = request.GET.get('alibabasellername','')
        Purchaser = request.GET.get('Purchaser','')
        Purchaser = [ gs for gs in Purchaser.split(',') if gs ]
        ExpressName = request.GET.get('ExpressName','')
        
        searchList = {'BillNumber__exact':BillNumber,'Recorder__in': Purchaser,
                    'alibabasellername__exact': alibabasellername,'ExpressName__exact': ExpressName,
                    'MakeDate__gte': MakeDateStart, 'MakeDate__lt': MakeDateEnd}
            
        sl = {}
        for k,v in searchList.items():
            if isinstance(v,list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    #if k == 'ShopName__exact':
                      #  v = 'Wish-' + v.zfill(4)
                        # messages.error(request, v)
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception,ex:
                messages.error(request,u'输入的查询数据有问题！')
    
        return qs    
xadmin.site.register(t_stockorderm, t_stockorderm_Admin)

class b_goodsskulinkshop_Admin(object):
    search_box_flag = True
    list_display=('NID','SKU','ShopSKU','Memo','PersonCode')
    search_fields=('NID','SKU','ShopSKU','Memo','PersonCode')
    
    fields = ('Filename',)

    form_layout = (
        Fieldset(u'请导入解绑文件-格式为"CSV"',
                    Row('Filename'),
                    css_class = 'unsort '
                ),
                  )
    
    actions = ['to_delete',]
    
    def to_delete(self, request, queryset):
        for querysetid in queryset.all():
            t_shopsku_information_binding_objs            = t_shopsku_information_binding()
            t_shopsku_information_binding_objs.SKU        = querysetid.SKU
            t_shopsku_information_binding_objs.ShopSKU    = querysetid.ShopSKU
            t_shopsku_information_binding_objs.Memo       = querysetid.Memo
            t_shopsku_information_binding_objs.PersonCode = querysetid.PersonCode
            t_shopsku_information_binding_objs.Submitter     = request.user.first_name
            t_shopsku_information_binding_objs.SubmitTime    = ddtime.now()
            t_shopsku_information_binding_objs.BindingStatus = u'Unbind'#解绑
            t_shopsku_information_binding_objs.save()

            if len(querysetid.Memo)>=9:
                shopcode = querysetid.Memo[0:9]
            else:
                shopcode = querysetid.Memo

            t_online_info.objects.filter(ShopSKU=querysetid.ShopSKU,ShopName=shopcode).update(SKU=None,MainSKU=None) # 清除online绑定关系

            classshopsku_obj.delsku(querysetid.ShopSKU) # 删除redis数据
            querysetid.delete()

    to_delete.short_description = u'解绑删除'
    
    
    def save_models(self):
        obj     = self.new_obj
        request = self.request

        logger  = logging.getLogger('sourceDns.webdns.views')

        try :
            if obj.Filename is not None and str(obj.Filename).strip() !='' :
                i = 0
                for row in csv.reader(obj.Filename):#obj.Status本身就是16进制字节流，直接reader
                    if i < 1:
                        i = i + 1
                        continue
                    i = i + 1

                    b_goodsskulinkshop_objs = py_b_goodsskulinkshop.objects.filter(SKU = row[0].decode("GBK"),ShopSKU = row[1].decode("GBK"))
                    
                    if b_goodsskulinkshop_objs.exists() :

                        ShopSKU = row[1].decode("GBK")
                        classshopsku_obj.delsku(ShopSKU) # 删除redis中店铺SKU和商品SKU的对应关系

                        if len(row[2].decode("GBK")) >= 9:
                            shopcode = (row[2].decode("GBK"))[0:9]
                        else:
                            shopcode = row[2].decode("GBK")

                        t_online_info.objects.filter(ShopSKU=ShopSKU, ShopName=shopcode).update(SKU=None,MainSKU=None)

                        b_goodsskulinkshop_objs.delete()

                        t_shopsku_information_binding_objs = t_shopsku_information_binding()
                        t_shopsku_information_binding_objs.SKU                 = row[0].decode("GBK") #
                        t_shopsku_information_binding_objs.ShopSKU             = ShopSKU
                        t_shopsku_information_binding_objs.Memo                = row[2].decode("GBK") #/
                        t_shopsku_information_binding_objs.PersonCode          = row[3].decode("GBK") #
                        t_shopsku_information_binding_objs.Filename            = obj.Filename
                        t_shopsku_information_binding_objs.Submitter           = request.user.first_name
                        t_shopsku_information_binding_objs.SubmitTime          = ddtime.now()
                        t_shopsku_information_binding_objs.BindingStatus       = u'Unbind'#解除绑定
                        
                        t_shopsku_information_binding_objs.save()

        except Exception,ex :
            logger.error('%s============================%s'%(Exception,ex))
            messages.error(request,'%s============================%s'%(Exception,ex))
            
    def get_list_queryset(self,):
        request = self.request
        qs = super(b_goodsskulinkshop_Admin, self).get_list_queryset()

        sku = request.GET.get('sku','')
        sku_list=sku.split(',')
        sku_list2=[]
        for sku_l in  sku_list:
            for s in t_product_mainsku_sku.objects.filter(MainSKU=sku_l).values_list('ProductSKU',flat=True):
                sku_list2.append(s)
        for s in  sku_list:
            sku_list2.append(s)

        shopSKU = request.GET.get('shopSKU','')
        shopSKU_list=shopSKU.split(',')
        shopSKU_list2=[]
        for s in shopSKU_list:
            shopSKU_list2.append(s.decode('utf-8'))

        memo = request.GET.get('memo','')
        personCode = request.GET.get('personCode','')
        if(sku==''and shopSKU!=''):
            searchList = {'ShopSKU__in': shopSKU_list2,
                          'Memo__exact':memo, 'PersonCode__exact': personCode,
                          }
        elif(shopSKU==''and  sku!=''):
            searchList = {'SKU__in': sku_list2,
                          'Memo__exact':memo, 'PersonCode__exact': personCode,
                          }
        elif(sku==''and shopSKU==''):
            searchList = {
                      'Memo__exact':memo, 'PersonCode__exact': personCode,
                      }
        else:
            searchList = {'SKU__in': sku_list2,'ShopSKU__in': shopSKU_list2,
                'Memo__exact':memo, 'PersonCode__exact': personCode,
            }
        sl = {}
        for k,v in searchList.items():
            if isinstance(v,list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    #if k == 'ShopName__exact':
                      #  v = 'Wish-' + v.zfill(4)
                        # messages.error(request, v)
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception,ex:
                messages.error(request,u'输入的查询数据有问题！')
    
        return qs    
    
# xadmin.site.register(b_goodsskulinkshop,b_goodsskulinkshop_Admin)
class t_syn_tables_Admin(object):
    list_display=('id','TableName','AllCount','BeginTime','EndTime')
    search_fields=('id','TableName','AllCount','BeginTime','EndTime')
xadmin.site.register(t_syn_tables,t_syn_tables_Admin)
"""
class b_packinfo_Admin(object):
    list_display=('NID','PackCode','PackName','CostPrice','Used','Remark','Weight','BarCode',)
    search_fields=('NID','PackCode','PackName','CostPrice','Used','Remark','Weight','BarCode',)
xadmin.site.register(xxxb_packinfo,b_packinfo_Admin)
"""
class b_goods_Admin(object):
    py_search_flag = True
    actions = ['get_pic']
    def get_pic(self, request, queryset):
        logger = logging.getLogger('sourceDns.webdns.views')
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_PY)
        for querysetid in queryset.all():
            SKU = querysetid.SKU
            SKU = SKU.replace('OAS-','').replace('FBA-','')
            oss_pic = '%s.jpg'%SKU
            exist = bucket.object_exists(oss_pic)
            if exist:
                messages.error(request,"%s :exist"%(SKU))
                logger.error("%s :exist"%(SKU))
                continue
            picurls = 'http://fancyqube.net:89/ShopElf/images/%s.jpg'%(SKU)
            image_bytes = None
            if  picurls is not None :
                try:
                    req = urllib2.Request(picurls)
                    image_bytes = urllib2.urlopen(req, timeout = 15).read()
                except urllib2.HTTPError, e:
                    messages.error(request,e.reason)
                    logger.error("%s :error"%(SKU))
                    continue
                except urllib2.URLError, e:
                    messages.error(request,e.reason)
                    logger.error("%s :error"%(SKU))
                    continue
                if image_bytes is not None:
                    bucket.put_object(u'%s.jpg'%(SKU),image_bytes)
    get_pic.short_description = u'获取普源图片'
    def show_BmpUrl(self,obj) :
        SKU = obj.SKU
        SKU = SKU.replace('OAS-','').replace('FBA-','')
        picurls = 'http://fancyqube.net:89/ShopElf/images/%s.jpg'%(SKU)
        #BmpUrl = u'%s%s.%s/%s.jpg'%(PREFIX,BUCKETNAME_PY,ENDPOINT_OUT,SKU)
        rt =  '<img src="%s"  width="80" height="80"  alt = "%s"  title="%s"  />  '%(picurls,picurls,picurls)
        return mark_safe(rt)
    show_BmpUrl.short_description = u'普源图'
    list_export =()
    list_per_page=50
    show_detail_fields  =  [ 'NID',]
    list_display= ('NID','show_BmpUrl','GoodsCategoryID','CategoryCode','GoodsCode','GoodsName','GoodsStatus','SKU','Material','Class',
                    'Unit','Quantity','SalePrice','CostPrice','GoodsStatus','SalerName','SalerName2','Purchaser','possessMan2','Notes',)
    list_filter = ('GoodsStatus','GoodsCategoryID',) #'SalerName','SalerName2','Purchaser','possessMan2',)
    readonly_fields = ('NID','GoodsCategoryID','CategoryCode','GoodsCode','GoodsName','ShopTitle','SKU','BarCode','FitCode','MultiStyle','Material','Class','Model',
                    'Unit','Style','Brand','LocationID','Quantity','SalePrice','CostPrice','AliasCnName','AliasEnName','Weight','DeclaredValue','OriginCountry','OriginCountryCode',
                    'ExpressID','Used','BmpFileName','BmpUrl','MaxNum','MinNum','GoodsCount','SupplierID','SupplierName','Notes','SampleFlag','SampleCount','SampleMemo','CreateDate','GroupFlag','SalerName',
                    'SellCount','SellDays','PackFee','PackName','GoodsStatus','DevDate','SalerName2','BatchPrice','MaxSalePrice','RetailPrice','MarketPrice','PackageCount','ChangeStatusTime',
                    'StockDays','StoreID','Purchaser','LinkUrl','LinkUrl2','LinkUrl3','StockMinAmount','MinPrice','HSCODE','ViewUser','InLong','InWide','InHigh','InGrossweight','InNetweight',
                    'OutLong','OutWide','OutHigh','OutGrossweight','OutNetweight','ShopCarryCost','ExchangeRate','WebCost','PackWeight','LogisticsCost','GrossRate','CalSalePrice','CalYunFei',
                    'CalSaleAllPrice','PackMsg','ItemUrl','IsCharged','DelInFile','Season','IsPowder','IsLiquid','possessMan1','possessMan2','LinkUrl4','LinkUrl5','LinkUrl6','isMagnetism',
                    'NoSalesDate',)
    search_fields = ('NID','GoodsCategoryID','CategoryCode','GoodsCode','GoodsName','ShopTitle','SKU','BarCode','FitCode','MultiStyle','Material','Class','Model',
                    'Unit','Style','Brand','LocationID','Quantity','SalePrice','CostPrice','AliasCnName','AliasEnName','Weight','DeclaredValue','OriginCountry','OriginCountryCode',
                    'ExpressID','Used','BmpFileName','BmpUrl','MaxNum','MinNum','GoodsCount','SupplierID','SupplierName','Notes','SampleFlag','SampleCount','SampleMemo','GroupFlag','SalerName',
                    'SellCount','SellDays','PackFee','PackName','GoodsStatus','SalerName2','BatchPrice','MaxSalePrice','RetailPrice','MarketPrice','PackageCount',
                    'StockDays','StoreID','Purchaser','LinkUrl','LinkUrl2','LinkUrl3','StockMinAmount','MinPrice','HSCODE','ViewUser','InLong','InWide','InHigh','InGrossweight','InNetweight',
                    'OutLong','OutWide','OutHigh','OutGrossweight','OutNetweight','ShopCarryCost','ExchangeRate','WebCost','PackWeight','LogisticsCost','GrossRate','CalSalePrice','CalYunFei',
                    'CalSaleAllPrice','PackMsg','ItemUrl','IsCharged','DelInFile','Season','IsPowder','IsLiquid','possessMan1','possessMan2','LinkUrl4','LinkUrl5','LinkUrl6','isMagnetism',
                    )

    def get_list_queryset(self):
        request = self.request
        qs = super(b_goods_Admin, self).get_list_queryset()
        GET = request.GET
        SKU = GET.get('sku','')
        GoodsName = GET.get('name','')
        GoodsStatus = GET.get('state','')
        Cate1 = GET.get('cate1','')
        Cate2 = GET.get('cate2','')

        if Cate1 != '':
            if Cate2 != '':
                qs = qs.filter(CategoryCode=Cate2)
            else:
                qs = qs.filter(CategoryCode=Cate1)

        if SKU != '':
            SKU = SKU.replace(' ','')
            if ',' in SKU:
                skuList = SKU.split(',')
            else:
                skuList = SKU.split('，')
            qs = qs.filter(SKU__in=skuList)

        if GoodsStatus != '':
            qs = qs.filter(GoodsStatus__in=GoodsStatus.split(','))

        if GoodsName != '':
            qs = qs.filter(GoodsName__contains=GoodsName)

        return qs



xadmin.site.register(b_goods, b_goods_Admin)
'''
class t_product_B_SupplierAdmin(admin.ModelAdmin):
    list_display = ('id','NID','SupplierName')
    fields=(('id','NID','SupplierName',),)
    list_display_links = ('id',)
    readonly_fields =('id',)
    
adminx.site.register(t_product_B_Supplier, t_product_B_SupplierAdmin)
'''
from skuapp.plugin.py_searchPlugin import *
from skuapp.plugin.t_stockordermPlugin import *
xadmin.site.register_plugin(py_searchPlugin, ListAdminView)
xadmin.site.register_plugin(t_stockordermPlugin, ListAdminView)

from pyapp.plugin.create_cg_data_Plugin import *
xadmin.site.register_plugin(create_cg_data_Plugin, BaseAdminView)
from pyapp.table.t_product_b_goods import *
from pyapp.modelsadminx.t_product_b_goods_all_productsku_Admin import *
xadmin.site.register(t_product_b_goods, t_product_b_goods_all_productsku_Admin)
xadmin.site.register_plugin(syn_b_goods_plugin,ListAdminView)

from pyapp.modelsadminx.p_trade_lack_detail_Admin import p_trade_lack_detail_Admin
from pyapp.table.p_trade_lack_detail import p_trade_lack_detail

xadmin.site.register(p_trade_lack_detail,p_trade_lack_detail_Admin)



from pyapp.modelsadminx.p_trade_lack_info_Admin import p_trade_lack_info_Admin
from pyapp.table.p_trade_lack_info import p_trade_lack_info
xadmin.site.register(p_trade_lack_info,p_trade_lack_info_Admin)


from pyapp.table.kc_currentstock_sku import *
from pyapp.modelsadminx.kc_currentstock_sku_Admin import *
xadmin.site.register(kc_currentstock_sku, kc_currentstock_sku_Admin)
from pyapp.plugin.kc_downloadcsv_Plugin import *
xadmin.site.register_plugin(kc_downloadcsv_Plugin,ListAdminView)
from pyapp.plugin.search_purchaser_Plugin import *
xadmin.site.register_plugin(search_purchaser_Plugin,ListAdminView)
from pyapp.plugin.site_left_menu_Plugin_kc import *
xadmin.site.register_plugin(site_left_menu_Plugin_kc,BaseAdminView)

from pyapp.table.kc_currentstock_sku_log import *
from pyapp.modelsadminx.kc_currentstock_sku_log_Admin import *
xadmin.site.register(kc_currentstock_sku_log, kc_currentstock_sku_log_Admin)
from pyapp.plugin.purchaser_handle_Plugin import *
xadmin.site.register_plugin(purchaser_handle_Plugin,ListAdminView)
from pyapp.plugin.add_cg_abnormal_display_Plugin import *
xadmin.site.register_plugin(add_cg_abnormal_display_Plugin,BaseAdminView)

from pyapp.table.kc_currentstock_sku_log_check import *
from pyapp.modelsadminx.kc_currentstock_sku_log_check_Admin import *
xadmin.site.register(kc_currentstock_sku_log_check, kc_currentstock_sku_log_check_Admin)
from pyapp.plugin.update_purchaserData_Plugin import *
xadmin.site.register_plugin(update_purchaserData_Plugin,BaseAdminView)
from pyapp.plugin.site_left_menu_Plugin_sh import *
xadmin.site.register_plugin(site_left_menu_Plugin_sh,BaseAdminView)
from pyapp.plugin.check_Remark_Plugin import *
xadmin.site.register_plugin(check_Remark_Plugin,BaseAdminView)
from pyapp.plugin.site_left_menu_abnormal_Plugin import *
xadmin.site.register_plugin(site_left_menu_abnormal_Plugin,BaseAdminView)

from pyapp.plugin.show_dataflag_Plugin import *
xadmin.site.register_plugin(show_dataflag_Plugin,BaseAdminView)

from pyapp.table.kc_currentstock_sku_log_realtime import *
from pyapp.modelsadminx.kc_currentstock_sku_log_realtime_Admin import *
xadmin.site.register(kc_currentstock_sku_log_realtime, kc_currentstock_sku_log_realtime_Admin)

from pyapp.table.kc_currentstock_sku_log_ed import *
from pyapp.modelsadminx.kc_currentstock_sku_log_ed_Admin import *
xadmin.site.register(kc_currentstock_sku_log_ed, kc_currentstock_sku_log_ed_Admin)

from pyapp.table.t_show_keywords import t_show_keywords
from pyapp.modelsadminx.t_show_keywords_Admin import t_show_keywords_Admin
xadmin.site.register(t_show_keywords, t_show_keywords_Admin)

from pyapp.table.kc_currentstock_sku_log_ignore import *
from pyapp.modelsadminx.kc_currentstock_sku_log_ignore_Admin import *
xadmin.site.register(kc_currentstock_sku_log_ignore, kc_currentstock_sku_log_ignore_Admin)

from pyapp.table.kc_currentstock_sku_log_abnormal import *
from pyapp.modelsadminx.kc_currentstock_sku_log_abnormal_Admin import *
xadmin.site.register(kc_currentstock_sku_log_abnormal, kc_currentstock_sku_log_abnormal_Admin)

from pyapp.table.kc_currentstock_sku_log_abnormal_completed import *
from pyapp.modelsadminx.kc_currentstock_sku_log_abnormal_completed_Admin import *
xadmin.site.register(kc_currentstock_sku_log_abnormal_completed, kc_currentstock_sku_log_abnormal_completed_Admin)

from pyapp.table.kc_currentstock_sku_log_abnormal_cannot import *
from pyapp.modelsadminx.kc_currentstock_sku_log_abnormal_cannot_Admin import *
xadmin.site.register(kc_currentstock_sku_log_abnormal_cannot, kc_currentstock_sku_log_abnormal_cannot_Admin)

from pyapp.table.kc_currentstock_sku_log_abnormal_purchaser import *
from pyapp.modelsadminx.kc_currentstock_sku_log_abnormal_purchaser_Admin import *
xadmin.site.register(kc_currentstock_sku_log_abnormal_purchaser, kc_currentstock_sku_log_abnormal_purchaser_Admin)

from pyapp.table.kc_currentstock_sku_log_abnormal_exception import *
from pyapp.modelsadminx.kc_currentstock_sku_log_abnormal_exception_Admin import *
xadmin.site.register(kc_currentstock_sku_log_abnormal_exception, kc_currentstock_sku_log_abnormal_exception_Admin)

from pyapp.table.kc_currentstock_sku_log_abnormal_all import *
from pyapp.modelsadminx.kc_currentstock_sku_log_abnormal_all_Admin import *
xadmin.site.register(kc_currentstock_sku_log_abnormal_all, kc_currentstock_sku_log_abnormal_all_Admin)

from pyapp.table.kc_currentstock_sku_log_check_abnormal import *
from pyapp.modelsadminx.kc_currentstock_sku_log_check_abnormal_Admin import *
xadmin.site.register(kc_currentstock_sku_log_check_abnormal, kc_currentstock_sku_log_check_abnormal_Admin)

from pyapp.table.kc_currentstock_sku_statistics import *
from pyapp.modelsadminx.kc_currentstock_sku_statistics_Admin import *
from pyapp.plugin.kc_currentstock_sku_statistics_plugin import *
xadmin.site.register(kc_currentstock_sku_statistics, kc_currentstock_sku_statistics_Admin)
xadmin.site.register_plugin(kc_currentstock_sku_statistics_plugin, ListAdminView)
from pyapp.table.kc_currentstock_sku_log_history import *
from pyapp.modelsadminx.kc_currentstock_sku_log_history_Admin import *
xadmin.site.register(kc_currentstock_sku_log_history, kc_currentstock_sku_log_history_Admin)

from pyapp.table.kc_currentstock_cg_purchaser import *
from pyapp.modelsadminx.kc_currentstock_cg_purchaser_Admin import *
xadmin.site.register(kc_currentstock_cg_purchaser,kc_currentstock_cg_purchaser_Admin)

from pyapp.table.kc_currentstock_sku_notsuggest import *
from pyapp.modelsadminx.kc_currentstock_sku_notsuggest_Admin import *
xadmin.site.register(kc_currentstock_sku_notsuggest,kc_currentstock_sku_notsuggest_Admin)

from pyapp.modelsadminx.t_show_keywords_library_Admin import t_show_keywords_library_Admin
from pyapp.table.t_show_keywords_library import t_show_keywords_library
xadmin.site.register(t_show_keywords_library,t_show_keywords_library_Admin)

from pyapp.table.kc_currentstock_sku_order30 import *
from pyapp.modelsadminx.kc_currentstock_sku_order30_Admin import *
xadmin.site.register(kc_currentstock_sku_order30,kc_currentstock_sku_order30_Admin)

from pyapp.table.kc_currentstock_sku_log_check_error import *
from pyapp.modelsadminx.kc_currentstock_sku_log_check_error_Admin import *
xadmin.site.register(kc_currentstock_sku_log_check_error,kc_currentstock_sku_log_check_error_Admin)

from pyapp.table.kc_currentstock_sku_log_frequent import *
from pyapp.modelsadminx.kc_currentstock_sku_log_frequent_Admin import *
xadmin.site.register(kc_currentstock_sku_log_frequent,kc_currentstock_sku_log_frequent_Admin)

from pyapp.table.kc_currentstock_sku_sales import *
from pyapp.modelsadminx.kc_currentstock_sku_sales_Admin import *
xadmin.site.register(kc_currentstock_sku_sales,kc_currentstock_sku_sales_Admin)
from pyapp.models import b_goodsskulinkshop
from pyapp.modelsadminx.b_goodsskulinkshop_v2_Admin import b_goodsskulinkshop_v2_Admin
xadmin.site.register(b_goodsskulinkshop,b_goodsskulinkshop_v2_Admin)


from pyapp.models import t_log_sku_shopsku_apply
from pyapp.modelsadminx.t_log_sku_shopsku_apply_Admin import t_log_sku_shopsku_apply_Admin
xadmin.site.register(t_log_sku_shopsku_apply, t_log_sku_shopsku_apply_Admin)


from pyapp.models import t_log_sku_shopsku_change
from pyapp.modelsadminx.t_log_sku_shopsku_change_Admin import t_log_sku_shopsku_change_Admin
xadmin.site.register(t_log_sku_shopsku_change, t_log_sku_shopsku_change_Admin)


from xadmin.views import BaseAdminView
from pyapp.plugin.sku_apply_change_Plugin import sku_apply_change_Plugin
xadmin.site.register_plugin(sku_apply_change_Plugin,BaseAdminView)

from xadmin.views import BaseAdminView
from pyapp.plugin.sku_apply_change_hide_original_button_Plugin import sku_apply_change_hide_original_button_Plugin
xadmin.site.register_plugin(sku_apply_change_hide_original_button_Plugin, BaseAdminView)

from pyapp.plugin.oscode_explain_Plugin import oscode_explain_Plugin
xadmin.site.register_plugin(oscode_explain_Plugin,ListAdminView)

from pyapp.table.t_product_b_goods_supplier_modify import t_product_b_goods_supplier_modify
from pyapp.modelsadminx.t_product_b_goods_supplier_modify_Admin import t_product_b_goods_supplier_modify_Admin
xadmin.site.register(t_product_b_goods_supplier_modify,t_product_b_goods_supplier_modify_Admin)

from pyapp.plugin.modify_b_goods_supplier_Plugin import modify_b_goods_supplier_Plugin
xadmin.site.register_plugin(modify_b_goods_supplier_Plugin,ListAdminView)

from pyapp.table.kc_unsalable_dispose import kc_unsalable_dispose
from pyapp.modelsadminx.kc_unsalable_dispose_Admin import kc_unsalable_dispose_Admin
xadmin.site.register(kc_unsalable_dispose, kc_unsalable_dispose_Admin)

from pyapp.plugin.kc_unsalable_dispose_tree_Plugin import kc_unsalable_dispose_tree_Plugin
xadmin.site.register_plugin(kc_unsalable_dispose_tree_Plugin, ListAdminView)

from pyapp.table.b_supplier_category_link_purchaser import b_supplier_category_link_purchaser
from pyapp.modelsadminx.b_supplier_category_link_purchaser_Admin import b_supplier_category_link_purchaser_Admin
xadmin.site.register(b_supplier_category_link_purchaser, b_supplier_category_link_purchaser_Admin)

from pyapp.plugin.bdx_Plugin import bdx_Plugin
xadmin.site.register_plugin(bdx_Plugin, ListAdminView)

from pyapp.table.t_duplicate_order import t_duplicate_order
from pyapp.modelsadminx.t_duplicate_order_Admin import t_duplicate_order_Admin
xadmin.site.register(t_duplicate_order, t_duplicate_order_Admin)

from pyapp.plugin.duplicate_order_plugin import duplicate_order_plugin
xadmin.site.register_plugin(duplicate_order_plugin, ListAdminView)

from pyapp.modelsadminx.Personal_Customization_SKU_Admin import personal_customization_sku_Admin
from pyapp.table.Personal_Customization_SKU import personal_customization_sku
xadmin.site.register(personal_customization_sku,personal_customization_sku_Admin)

from pyapp.plugin.personal_customization_sku_tree_menu_Plugin import personal_customization_sku_tree_menu_Plugin
xadmin.site.register_plugin(personal_customization_sku_tree_menu_Plugin,ListAdminView)

from pyapp.plugin.PCS_hide_page_action_Plugin import hide_page_action_Plugin
xadmin.site.register_plugin(hide_page_action_Plugin,ListAdminView)

from pyapp.plugin.personal_customization_orderPlugin import personal_customization_sku_orderPlugin
xadmin.site.register_plugin(personal_customization_sku_orderPlugin,ListAdminView)


from pyapp.plugin.b_supplier_category_link_purchaser_Plugin import b_supplier_category_link_purchaser_Plugin
xadmin.site.register_plugin(b_supplier_category_link_purchaser_Plugin, BaseAdminView)


from pyapp.table.t_unsalable_products import t_unsalable_products
from pyapp.modelsadminx.t_unsalable_products_Admin import t_unsalable_products_Admin
xadmin.site.register(t_unsalable_products, t_unsalable_products_Admin)

from pyapp.table.t_unsalable_products_refund import t_unsalable_products_refund
from pyapp.modelsadminx.t_unsalable_products_refund_Admin import t_unsalable_products_refund_Admin
xadmin.site.register(t_unsalable_products_refund, t_unsalable_products_refund_Admin)

from pyapp.table.t_unsalable_products_storehouse import t_unsalable_products_storehouse
from pyapp.modelsadminx.t_unsalable_products_storehouse_Admin import t_unsalable_products_storehouse_Admin
xadmin.site.register(t_unsalable_products_storehouse, t_unsalable_products_storehouse_Admin)

from pyapp.table.t_unsalable_products_sale import t_unsalable_products_sale
from pyapp.modelsadminx.t_unsalable_products_sale_Admin import t_unsalable_products_sale_Admin
xadmin.site.register(t_unsalable_products_sale, t_unsalable_products_sale_Admin)

from pyapp.table.t_unsalable_products_upload import t_unsalable_products_upload
from pyapp.modelsadminx.t_unsalable_products_upload_Admin import t_unsalable_products_upload_Admin
xadmin.site.register(t_unsalable_products_upload, t_unsalable_products_upload_Admin)

from pyapp.table.t_unsalable_products_destroy import t_unsalable_products_destroy
from modelsadminx.t_unsalable_products_destroy_Admin import t_unsalable_products_destroy_Admin
xadmin.site.register(t_unsalable_products_destroy, t_unsalable_products_destroy_Admin)

from plugin.t_unsalable_products_left_site_Plugin import t_unsalable_products_left_site_Plugin
xadmin.site.register_plugin(t_unsalable_products_left_site_Plugin, BaseAdminView)

from pyapp.modelsadminx.kc_inventory_Admin import kc_inventory_Admin
from pyapp.table.kc_inventory import kc_inventory
xadmin.site.register(kc_inventory, kc_inventory_Admin)

from pyapp.plugin.kc_inventory_Plugin import kc_inventory_Plugin
xadmin.site.register_plugin(kc_inventory_Plugin, ListAdminView)
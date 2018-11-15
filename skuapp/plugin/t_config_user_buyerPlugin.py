# -*- coding: utf-8 -*-


import xadmin
import logging
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from django.template import loader
from skuapp.table.B_PackInfo import  *
from skuapp.table.t_store_marketplan_execution_log  import *     
from skuapp.table.t_store_marketplan_execution  import * 
from skuapp.table.t_config_user_buyer import *
from skuapp.table.t_online_info import *   
import datetime
import math
        
class t_config_user_buyerPlugin(BaseAdminPlugin):
    show_user_buyer = False
    object_id = 0   
    # 初始化方法根据 ``say_hello`` 属性值返回
    def init_request(self, *args, **kwargs):
        return bool(self.show_user_buyer)
    def get_media(self, media):
        media.add_js([self.static('xadmin/js/xadmin.plugin.t_config_user_buyer.html.js')])
        return media
    def block_after_fieldsets(self, context, nodes):
        #加载子SKU信息
        t_store_marketplan_execution_log_objs = None
        t_store_marketplan_execution_log_objs_count =0
        if context['original']  is  not None :
            logger = logging.getLogger('sourceDns.webdns.views')
            #logger.error("888888888888888888888888888888====%s"%(context))
            #logger.error("7777777777777777777777777777777====%s"%(context['original']))
            #t_store_marketplan_execution_log_objs = t_store_marketplan_execution_log.objects.all()
        #t_store_marketplan_execution_log_in7day_objs = t_store_marketplan_execution_log.objects.filter(Exetime__gte=(datetime.datetime.now()+datetime.timedelta(days=-7)).strftime('%Y-%m-%d %H:%M:%S')).values_list('BuyerAccount')
            #logger.error("t_store_marketplan_execution_log_in7day_objs====%s"%(t_store_marketplan_execution_log_in7day_objs))
        #.exclude(BuyerAccount__in=t_store_marketplan_execution_log_in7day_objs)
            buyer_objs = t_config_user_buyer.objects.filter(Status='Y',StaffId = self.request.user.username)
            
            t_store_marketplan_execution_log_objs = t_store_marketplan_execution_log.objects.filter(Status='EXEING',StaffId= context['user'] )
            #t_store_marketplan_execution_objs = t_store_marketplan_execution.objects.filter()[0:7]
            t_store_marketplan_execution_log_objs_count = t_store_marketplan_execution_log_objs.count()
            #buyer_objs = t_config_user_buyer.objects.filter(UpdateTime__lte=(datetime.datetime.now()+datetime.timedelta(days=-7)).strftime('%Y-%m-%d %H:%M:%S'))
            Quantity_objs = t_store_marketplan_execution.objects.values_list('Quantity',flat=True)
            t1=0
            for Quantity_obj in Quantity_objs:
                t1+=Quantity_obj
            Demand_objs = t_store_marketplan_execution.objects.values_list('Demand',flat=True)
            t2=0
            for Demand_obj in Demand_objs:
                t2+=Demand_obj
            t3=t2-t1
            procount = 3
            
            t_store_marketplan_execution_objls = t_store_marketplan_execution.objects.filter(CreateTime__lte=(datetime.datetime.now()+(datetime.timedelta(days=-1))).strftime('%Y-%m-%d %H:%M:%S'))
            bb=0
            aa=0
            for t_store_marketplan_execution_obj in t_store_marketplan_execution_objls:
                if t_store_marketplan_execution_obj.Demand > t_store_marketplan_execution_obj.Quantity:
                    if t_store_marketplan_execution_obj.Demand>=10:
                        if t_store_marketplan_execution_obj.Quantity == 0:
                            bb += math.ceil(t_store_marketplan_execution_obj.Demand/5)
                        else:
                            bb += t_store_marketplan_execution_obj.Quantity
                    if t_store_marketplan_execution_obj.Demand>5 and t_store_marketplan_execution_obj.Demand<10:
                        if t_store_marketplan_execution_obj.Quantity == 0:
                            bb += math.ceil(t_store_marketplan_execution_obj.Demand/3)
                        else:
                            bb += (t_store_marketplan_execution_obj.Demand-t_store_marketplan_execution_obj.Quantity)
                    else:
                        if t_store_marketplan_execution_obj.Quantity == 0:
                            bb += math.ceil(t_store_marketplan_execution_obj.Demand/2)
                        else:
                            bb += (t_store_marketplan_execution_obj.Demand-t_store_marketplan_execution_obj.Quantity)                 
            
            aa = t_store_marketplan_execution_log.objects.filter(Pid=t_store_marketplan_execution_obj.id,Exetime=(datetime.datetime.now()).strftime('%Y-%m-%d')).count()
            cc = int(bb-aa)
                  
            nodes.append(loader.render_to_string('t_config_user_buyer.html', {'t_store_marketplan_execution_log_objs': t_store_marketplan_execution_log_objs,'t_store_marketplan_execution_log_objs_count': t_store_marketplan_execution_log_objs_count,'buyer_objs':buyer_objs,'t3':t3,'cc':cc,'procount':procount}))


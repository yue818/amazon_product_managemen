# -*- coding: utf-8 -*-
import xadmin
import logging
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from django.template import loader
from skuapp.table.t_product_develop_ing import *
from django.contrib.auth.models import User
from skuapp.table.t_product_survey_history import *
from django.contrib import messages
from django.template import RequestContext
import json
from django.db import connection

class t_prompt_developPlugin(BaseAdminPlugin):
    show_prompt_develop = False
    
    def init_request(self, *args, **kwargs):     
        return bool(self.show_prompt_develop)
        
    def block_after_fieldsets(self, context, nodes):
        if self.model._meta.model_name in ['t_work_flow_of_plate_house', 't_work_battledore']:   #
            nodes.append(loader.render_to_string('t_work_flow_of_plate_house_read_content.html'))
        elif self.model._meta.model_name in ['t_log_sku_shopsku_apply']:  #
            nodes.append(loader.render_to_string('t_log_sku_shopsku_apply_content.html'))
        elif self.model._meta.model_name in ['t_sku_weight_examine']:   # 克重审核
            nodes.append(loader.render_to_string('sku_weight_examine_content.html'))
        elif self.model._meta.model_name in ['t_progress_tracking_of_product_customization_table']:  # 产品定做落地跟踪表
            clothesflag = self.request.GET.get('clothes', 0)
            nodes.append(loader.render_to_string('progress_tracking_of_product_customization_content.html', {'clothesflag': clothesflag}))
        elif self.model._meta.model_name in ['t_config_product_rapid_develop']:  # 快速刊登配置
            from skuapp.table.t_config_product_rapid_develop import t_config_product_rapid_develop
            id = context.get('object_id')
            if id:
                obj = t_config_product_rapid_develop.objects.get(id=id)
                ValueDict = json.loads(obj.ValueDict)
            else:
                ValueDict = {}
            nodes.append(loader.render_to_string(
                't_config_product_rapid_develop_content.html',
                {'valuedict': ValueDict}
            ))
        elif self.model._meta.model_name in ['t_templet_wish_country_shipping']:  # Wish 刊登国家运费配置页面
            from brick.table.t_country_code_name_table import t_country_code_name_table
            from wishpubapp.table.t_templet_wish_country_shipping import t_templet_wish_country_shipping
            countrys_code = t_country_code_name_table(connection).GetAllCountryCode()
            countrys_code_dict = countrys_code.get('data', {})
            id = context.get('object_id')
            if id:
                obj = t_templet_wish_country_shipping.objects.get(id=id)
                ValueList = json.loads(obj.Description)
            else:
                ValueList = []
            nodes.append(loader.render_to_string(
                't_templet_wish_country_shipping_content.html',
                {'countrys_code_dict': sorted(countrys_code_dict.items(),key=lambda x: x[0]), 'ValueList': ValueList}
            ))
        else:
            nodes.append(loader.render_to_string('t_prompt_develop.html'))
            

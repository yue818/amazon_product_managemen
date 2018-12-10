# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: adminx.py
 @time: 2018/12/10 10:04
"""
import xadmin
from xadmin.views import BaseAdminView

# 店铺发货地址配置
from amazon_app.table.t_amazon_fba_inbound_address_cfg import t_amazon_fba_inbound_address_cfg
from amazon_app.modelsadminx.t_amazon_fba_inbound_address_cfg_Admin import t_amazon_fba_inbound_address_cfg_Admin
# 入库计划
from amazon_app.table.t_amazon_fba_inbound_plan import t_amazon_fba_inbound_plan
from amazon_app.modelsadminx.t_amazon_fba_inbound_plan_Admin import t_amazon_fba_inbound_plan_Admin

# 左侧栏
from amazon_app.plugin.amazon_left_menu_tree_plugin import amazon_left_menu_tree_plugin


xadmin.site.register(t_amazon_fba_inbound_address_cfg, t_amazon_fba_inbound_address_cfg_Admin)
xadmin.site.register(t_amazon_fba_inbound_plan, t_amazon_fba_inbound_plan_Admin)

xadmin.site.register_plugin(amazon_left_menu_tree_plugin, BaseAdminView)

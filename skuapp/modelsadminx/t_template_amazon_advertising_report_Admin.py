#-*-coding:utf-8-*-
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from django.utils.safestring import mark_safe
from django.contrib import messages
import decimal
from skuapp.table.t_template_amazon_advertising_report import t_template_amazon_advertising_report


"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_template_amazon_advertising_report_Admin.py
 @time: 2018/8/16 11:01
"""   
class t_template_amazon_advertising_report_Admin(object):
    site_left_menu_tree_amazon_advertising_flag = True

    list_display = ('advertising_campaign_name', 'advertising_group_name', 'cost', )

    list_display_links = ('id',)

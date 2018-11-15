#-*-coding:utf-8-*-
from django.utils.safestring import mark_safe
from django.contrib import messages
from django_redis import get_redis_connection
from django.db import connection
import logging,json
import xadmin

"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_erp_aliexpress_product_recycle_bin_Admin.py
 @time: 2018/5/31 17:56
"""
class t_erp_aliexpress_product_recycle_bin_Admin(object):
    site_left_menu_tree_flag_ali = True
    list_per_page = 20
    list_display = ('subject', 'owner_member_id', )
    # list_editable = ('Remarks')
    list_display_links = ('',)
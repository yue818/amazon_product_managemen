# -*- coding: utf-8 -*-
from skuapp.table.t_cloth_factory import *
from datetime import datetime

class t_cloth_factory_Admin(object):
    list_per_page = 20
    list_display = ('id', 'name', 'value',)

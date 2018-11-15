# -*- coding: utf-8 -*-

from django.utils.safestring import mark_safe
from skuapp.table.t_distribution_staff_statistics_table import *
from django.db import transaction,connection

class t_distribution_staff_statistics_table_Admin(object):
    list_display=('id','Submitter','SubmitTime','SKU_nub','Shop_nub','Links_nub','Succ_nub','Error_nub',
                    'Already_nub','Manual_nub','SKUdis_nub','Orders_nub')
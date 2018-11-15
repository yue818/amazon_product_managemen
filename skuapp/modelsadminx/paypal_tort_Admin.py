# -*- coding: utf-8 -*-
from skuapp.table.paypal_tort import *
from Project.settings import *
from django.contrib import messages
from Project.settings import *





class paypal_tort_Admin(object):
    importfile_plugin2 = True
    search_box_flag = True

    list_display = ('Brand', 'GraphicTrademark',
                    'Site', 'Category', )
                    
    def get_list_queryset(self):
    
        request = self.request
        qs = super(paypal_tort_Admin, self).get_list_queryset()

        Brand = request.GET.get('Brand', '')
        GraphicTrademark = request.GET.get('GraphicTrademark', '')
        Site = request.GET.get('Site', '')
        Category = request.GET.get('Category', '')



        searchList = {'Brand__contains': Brand, 'GraphicTrademark__exact': GraphicTrademark,
                      'Site__exact': Site,'Category__exact': Category,


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
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')
        

        return qs







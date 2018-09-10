# -*- coding:utf-8 -*-

"""
 @desc:
 @author: 孙健
 @site:
 @software: Sublime
"""

# from urllib import unquote
import json
from django.template import loader
from xadmin.views import BaseAdminPlugin
from mymall_app.table.t_mymall_template_publish import t_mymall_template_publish


class mymall_collection_box_plugin(BaseAdminPlugin):
    mymall_collection_box_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.mymall_collection_box_flag)

    def block_after_fieldsets(self, context, nodes):
        id = None
        models_objs = (u'%s' % context['request']).split('/')
        if models_objs[1] == 'Project' and models_objs[2] == 'admin':
            id = models_objs[5]
        elif models_objs[1] == 'xadmin':
            id = models_objs[4]

        AllDict = {}
        AllDict['Title'] = ''
        AllDict['Description'] = ''
        AllDict['Tags'] = ''

        MainDict = {}
        MainDict['MSRP'] = ''
        MainDict['Price'] = ''
        MainDict['Shipping'] = ''
        MainDict['ShippingTime'] = ''
        MainDict['KC'] = ''

        AllDict['MainInfo'] = MainDict
        AllDict['MainSKU'] = ''
        #
        # VDict = {}
        # VDict['SKU'] = ''
        # VDict['ShopSKU'] = ''
        # VDict['Color'] = ''
        # VDict['Size'] = ''
        # VDict['Msrp'] = ''
        # VDict['Price'] = ''
        # VDict['Kc'] = ''
        # VDict['Shipping'] = ''
        # VDict['Shippingtime'] = ''

        AllDict['Variants'] = []
        AllDict['MainImage'] = ''

        AllDict['EPIC'] = []
        for a in range(20):
            AllDict['EPIC'].append('')

        if id != 'add':
            obj = t_mymall_template_publish.objects.filter(id=id)
            if obj.exists():
                AllDict = {}
                AllDict['Title'] = obj[0].Title
                AllDict['Description'] = obj[0].Description
                AllDict['Tags'] = obj[0].Tags
                AllDict['MainInfo'] = json.loads(obj[0].MainInfo)
                AllDict['Variants'] = json.loads(obj[0].Variants)
                AllDict['MainImage'] = obj[0].MainImage
                AllDict['MainSKU'] = obj[0].MainSKU

                AllDict['EPIC'] = []
                if obj[0].ExtraImages:
                    for epic in obj[0].ExtraImages.split('|'):
                        AllDict['EPIC'].append(epic)
                for i in range(20 - len(AllDict['EPIC']) - len(AllDict['Variants'])):
                    AllDict['EPIC'].append('')

        nodes.append(loader.render_to_string('mymall_collection_box_plugin_template.html', {'AllDict': AllDict}))

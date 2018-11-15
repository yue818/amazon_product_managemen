#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_tort_info_tree_menu_Plugin.py
 @time: 2018-05-08 19:09
"""
from xadmin.views import BaseAdminPlugin
from django.template import loader
from skuapp.table.t_tort_info import t_tort_info
from skuapp.table.t_tort_info_audit import t_tort_info_audit
from skuapp.table.t_tort_info_result import t_tort_info_result
from skuapp.table.t_tort_info_cancel import t_tort_info_cancel
from skuapp.table.t_tort_info_cancel_audit import t_tort_info_cancel_audit
from skuapp.table.t_tort_info_sync import t_tort_info_sync
from skuapp.table.t_tort_info_query import t_tort_info_query
from skuapp.public.const import tort
import json

class t_tort_info_tree_menu_Plugin(BaseAdminPlugin):
    t_tort_tree_menu_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.t_tort_tree_menu_flag)

    def validation_url_selected(self, menu_list, new_sourceurl, show_flag):
        flag = 0
        for menu_obj in menu_list:
            to_url = menu_obj['to_url']
            menu_child_obj = menu_obj['child']
            if len(menu_child_obj) > 0:
                new_menu_list, flag, show_flag = self.validation_url_selected(menu_child_obj, new_sourceurl, show_flag)
                if flag == 1:
                    show_flag = 1
                    menu_obj['selected'] = 'selected'
            else:
                if to_url != new_sourceurl:
                    if '?' not in menu_obj['to_url']:
                        to_url = to_url + '?'
                if to_url in new_sourceurl:
                    menu_obj['selected'] = 'selected'
                    flag = 1
        return menu_list, flag, show_flag

    def block_left_navbar(self, context, nodes):

        draft_count = t_tort_info.objects.filter(Step=tort.CHECKIN).count()#侵权登记
        reject_count = t_tort_info.objects.filter(Step=tort.REJECT).count()#驳回侵权申请
        tort_count = t_tort_info.objects.filter(Step__in=[tort.TORT_LIST,tort.SYNC]).count()#侵权列表
        com_tort_count = t_tort_info.objects.filter(Step__in=[tort.COM_TORT_LIST,tort.SYNC_COM]).count()#一般侵权列表
        no_tort_count = t_tort_info.objects.filter(Step__in=[tort.NO_TORT_LIST]).count()#不侵权列表
        wait_audit_count = t_tort_info_audit.objects.filter(Step=tort.WAIT_AUDIT).count()#待审核               
        delete_count = t_tort_info.objects.filter(Step=tort.DELETE).count()#扔到回收站
        sync_count = t_tort_info_sync.objects.filter(Step__in=[tort.TORT_LIST,tort.COM_TORT_LIST]).count()#同步导出
        all_count = t_tort_info.objects.count()
        #total = draft_count+reject_count+delete_count+reject_cancel_count+wait_audit_count+cancel_wait_audit_count+sync_count+cancel_sync_count

        menu_list = [{
            "name": u"IP侵权审核流程",
            "code": "IPMAIN",
            "icon": "icon-th",
            "selected": "",
            "to_url": "",
            "child": [{
                "name": u"侵权申请",
                "code": "RECORD",
                "icon": "icon-minus-sign",
                "parentCode": "IPMAIN",
                "selected": "",
                "to_url": "",
                "child": [
                    {
                        "name": u"侵权登记(" + str(draft_count) + ")",
                        "icon": "",
                        "code": "DRAFT",
                        "parentCode": "RECORD",
                        "selected": "",
                        "to_url": "/Project/admin/skuapp/t_tort_info/?Step=0",
                        "child": []
                    },                    
                ]
            },
                {
                    "name": u"侵权审核",
                    "code": "AUDIT",
                    "icon": "icon-minus-sign",
                    "parentCode": "IPMAIN",
                    "selected": "",
                    "to_url": "",
                    "child": [
                        {
                            "name": u"侵权审核(" + str(wait_audit_count) + ")",
                            "icon": "",
                            "code": "DOAUDIT",
                            "parentCode": "AUDIT",
                            "selected": "",
                            "to_url": "/Project/admin/skuapp/t_tort_info_audit/?Step=1",
                            "child": []
                        },                       
                    ]
                },
                {
                    "name": u"侵权列表",
                    "code": "RECEIVE",
                    "icon": "icon-minus-sign",
                    "parentCode": "IPMAIN",
                    "selected": "",
                    "to_url": "",
                    "child": [
                        {
                            "name": u"一般侵权(" + str(com_tort_count) + ")",
                            "icon": "",
                            "code": "DORECEIVE",
                            "parentCode": "RECEIVE",
                            "selected": "",
                            "to_url": "/Project/admin/skuapp/t_tort_info_result_common/?Step=3,12",
                            "child": []
                        },
                        {
                            "name": u"严重侵权(" + str(tort_count) + ")",
                            "icon": "",
                            "code": "DORECEIVE",
                            "parentCode": "RECEIVE",
                            "selected": "",
                            "to_url": "/Project/admin/skuapp/t_tort_info_result/?Step=2,11",
                            "child": []
                        },                        
                    ]
                },
                 {
                    "name": u"不侵权列表",
                    "code": "NORECEIVE",
                    "icon": "icon-minus-sign",
                    "parentCode": "IPMAIN",
                    "selected": "",
                    "to_url": "",
                    "child": [
                        {
                            "name": u"不侵权列表(" + str(no_tort_count) + ")",
                            "icon": "",
                            "code": "PNORECEIVE",
                            "parentCode": "NORECEIVE",
                            "selected": "",
                            "to_url": "/Project/admin/skuapp/t_tort_info_result_no/?Step=4",
                            "child": []
                        },                
                    ]
                },
                {
                    "name": u"侵权信息同步",
                    "code": "SYNC",
                    "icon": "icon-minus-sign",
                    "parentCode": "IPMAIN",
                    "selected": "",
                    "to_url": "",
                    "child": [
                        {
                            "name": u"侵权同步导入普源(" + str(sync_count) + ")",
                            "icon": "",
                            "code": "DOSYNC",
                            "parentCode": "SYNC",
                            "selected": "",
                            "to_url": "/Project/admin/skuapp/t_tort_info_sync/?Step=2,3",
                            "child": []
                        },                        
                    ]
                },
                {
                    "name": u"侵权全局查询(" + str(all_count) + ")",
                    "code": "QUERY",
                    "icon": "icon-minus-sign",
                    "parentCode": "IPMAIN",
                    "selected": "",
                    "to_url": "/Project/admin/skuapp/t_tort_info_query/",
                    "child": []
                },
                {
                    "name": u"侵权图片展示",
                    "code": "SHOWIMAGE",
                    "icon": "icon-minus-sign",
                    "parentCode": "IPMAIN",
                    "selected": "",
                    "to_url": "/Project/admin/skuapp/t_tort_info_image/",
                    "child": []
                },
            ]
        }]

        sourceURL = str(context['request']).split("'")[1]
        new_sourceURL = sourceURL
        if '?p=' in sourceURL:
            new_sourceURL = sourceURL.replace('?p=', '?')
            if '&' in new_sourceURL:
                new_sourceURL = new_sourceURL.split('?')[0] + '?' + new_sourceURL.split('?')[1].split('&')[1]
            else:
                new_sourceURL = new_sourceURL.split('?')[0]
        attention_text = ''

        show_flag = 0
        menu_list, flag, show_flag = self.validation_url_selected(menu_list, new_sourceURL, show_flag)
        if show_flag == 1:
            nodes.append(loader.render_to_string('site_left_menu_tree_tort_Plugin.html',
                                                 {'menu_list': json.dumps(menu_list), 'attention_text': attention_text}))
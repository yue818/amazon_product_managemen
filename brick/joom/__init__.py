# -*- coding: utf-8 -*-

import logging
from xadmin.plugins.actions import ActionPlugin
from xadmin.views.list import ListAdminView
from .FILTERCONF import FILTER_BUTTON_CONFIG
from .FILTERCONF import FILTER_FIELD_CONFIG

logger = logging.getLogger('break.joom')


def _reset_get_actions():

    def get_actions(actions, *args, **kw):
        new_actions = actions._get_actions()
        full_path = actions.request.get_full_path()
        ac_request = actions.request
        model_name = actions.model.__name__

        if model_name in FILTER_BUTTON_CONFIG.keys():
            if full_path.find(model_name) != -1:
                model_full_path = FILTER_BUTTON_CONFIG[model_name]['full_path']
                filter_buttons = FILTER_BUTTON_CONFIG[model_name]['filter_button']
                for filter_button in filter_buttons:
                    request_key = filter_button['request_key']
                    request_value = filter_button['request_value']
                    del_buttons = filter_button['del_button']
                    if not request_key:
                        if model_full_path == full_path:
                            for action in new_actions.keys():
                                if action in del_buttons:
                                    del new_actions[action]
                    else:
                        if ac_request.GET.get(request_key) == request_value:
                            for action in new_actions.keys():
                                if action in del_buttons:
                                    del new_actions[action]

        # if full_path.find('priceParity_Status=ALL') != -1:
        #     if 'batch_joom_price_parity' in new_actions:
        #         del new_actions['batch_joom_price_parity']
        #     if 'set_joom_product_price_parity_status_todo' in new_actions:
        #         del new_actions['set_joom_product_price_parity_status_todo']
        # elif full_path.find('priceParity_Status=WAIT') != -1:
        #     if 'set_joom_product_price_parity_status_wait' in new_actions:
        #         del new_actions['set_joom_product_price_parity_status_wait']
        #     if 'batch_joom_price_parity' in new_actions:
        #         del new_actions['batch_joom_price_parity']
        # elif full_path.find('priceParity_Status=NO') != -1:
        #     if 'set_joom_product_price_parity_status_no' in new_actions:
        #         del new_actions['set_joom_product_price_parity_status_no']
        #     if 'batch_joom_price_parity' in new_actions:
        #         del new_actions['batch_joom_price_parity']
        #     if 'set_joom_product_price_parity_status_todo' in new_actions:
        #         del new_actions['set_joom_product_price_parity_status_todo']
        # elif full_path.find('priceParity_Status=TODO') != -1:
        #     if 'set_joom_product_price_parity_status_todo' in new_actions:
        #         del new_actions['set_joom_product_price_parity_status_todo']
        #     if 'set_joom_product_price_parity_status_no' in new_actions:
        #         del new_actions['set_joom_product_price_parity_status_no']
        # elif full_path.find('priceParity_Status=SUCCESS') != -1:
        #     if 'set_joom_product_price_parity_status_no' in new_actions:
        #         del new_actions['set_joom_product_price_parity_status_no']
        #     if 'batch_joom_price_parity' in new_actions:
        #         del new_actions['batch_joom_price_parity']
        #     if 'set_joom_product_price_parity_status_todo' in new_actions:
        #         del new_actions['set_joom_product_price_parity_status_todo']
        # elif full_path.find('priceParity_Status=FAILED') != -1:
        #     if 'set_joom_product_price_parity_status_no' in new_actions:
        #         del new_actions['set_joom_product_price_parity_status_no']
        #     if 'batch_joom_price_parity' in new_actions:
        #         del new_actions['batch_joom_price_parity']
        #     if 'set_joom_product_price_parity_status_todo' in new_actions:
        #         del new_actions['set_joom_product_price_parity_status_todo']
        # elif full_path == '/Project/admin/joom_app/t_joom_price_parity/' or \
        #         full_path == '/Project/admin/aliexpress_app/t_aliexpress_price_parity/':
        #     for i in new_actions.keys():
        #         del new_actions[i]
        # elif full_path.find('t_mymall_template_publish') != -1:
        #     if full_path == '/Project/admin/mymall_app/t_mymall_template_publish/':
        #         if 'to_pub' in new_actions:
        #             del new_actions['to_pub']
        #         if 'set_published_failed_to_success' in new_actions:
        #             del new_actions['set_published_failed_to_success']
        #         if 'set_published_falied_to_todo' in new_actions:
        #             del new_actions['set_published_falied_to_todo']
        #         if 'set_published_success_to_falied' in new_actions:
        #             del new_actions['set_published_success_to_falied']
        #     if full_path.find('PublishResult=TODO') != -1:
        #         if 'set_published_failed_to_success' in new_actions:
        #             del new_actions['set_published_failed_to_success']
        #         if 'set_published_falied_to_todo' in new_actions:
        #             del new_actions['set_published_falied_to_todo']
        #         if 'set_published_success_to_falied' in new_actions:
        #             del new_actions['set_published_success_to_falied']
        #     if full_path.find('PublishResult=DONE') != -1:
        #         if 'to_pub' in new_actions:
        #             del new_actions['to_pub']
        #         if 'set_published_failed_to_success' in new_actions:
        #             del new_actions['set_published_failed_to_success']
        #         if 'set_published_falied_to_todo' in new_actions:
        #             del new_actions['set_published_falied_to_todo']
        #         if 'set_published_success_to_falied' in new_actions:
        #             del new_actions['set_published_success_to_falied']
        #     if full_path.find('PublishResult=SUCCESS') != -1:
        #         if 'to_pub' in new_actions:
        #             del new_actions['to_pub']
        #         if 'set_published_failed_to_success' in new_actions:
        #             del new_actions['set_published_failed_to_success']
        #         if 'set_published_falied_to_todo' in new_actions:
        #             del new_actions['set_published_falied_to_todo']
        #     if full_path.find('PublishResult=FAILED') != -1:
        #         if 'to_pub' in new_actions:
        #             del new_actions['to_pub']
        #         if 'set_published_success_to_falied' in new_actions:
        #             del new_actions['set_published_success_to_falied']
        # elif full_path.find('t_online_info_walmart_publish') != -1:
        #     # if pp.find('status=WAITPUBLISH') == -1 or pp.find('status=ACCESS') == -1 or pp.find('status=FAILED') == -1:
        #     #     if 'batch_upload' in new_actions:
        #     #         del new_actions['batch_upload']
        #     if full_path.find('feedStatus=PROCESSED') != -1:
        #         if 'batch_upload' in new_actions.keys():
        #             del new_actions['batch_upload']
        else:
            pass
        return new_actions

    ActionPlugin._get_actions = ActionPlugin.get_actions
    ActionPlugin.get_actions = get_actions

    def get_list_display(list_display):
        new_list_display = list_display._get_list_display()
        full_path = list_display.request.get_full_path()
        ld_request = list_display.request
        model_name = list_display.model.__name__

        if model_name in FILTER_FIELD_CONFIG.keys():
            if full_path.find(model_name) != -1:
                model_full_path = FILTER_FIELD_CONFIG[model_name]['full_path']
                filter_fields = FILTER_FIELD_CONFIG[model_name]['filter_field']
                for filter_field in filter_fields:
                    request_key = filter_field['request_key']
                    request_value = filter_field['request_value']
                    del_fields = filter_field['del_field']
                    if not request_key:
                        if model_full_path == full_path:
                            for field in del_fields:
                                if field in new_list_display:
                                    new_list_display.remove(field)
                    else:
                        if ld_request.GET.get(request_key) == request_value:
                            for field in del_fields:
                                if field in new_list_display:
                                    new_list_display.remove(field)

        # if list_display.request.get_full_path().find('priceParity_Status=ALL') != -1 \
        #         or list_display.request.get_full_path() == '/Project/admin/joom_app/t_joom_price_parity/':
        #     if 'show_Competitor_image' in new_list_display:
        #         new_list_display.remove('show_Competitor_image')
        #     if 'competitor_ProductID' in new_list_display:
        #         new_list_display.remove('competitor_ProductID')
        #     if 'show_competitor_price_range' in new_list_display:
        #         new_list_display.remove('show_competitor_price_range')
        #     if 'show_competitor_Orders7Days' in new_list_display:
        #         new_list_display.remove('show_competitor_Orders7Days')
        #     if 'priceParity_Remarks' in new_list_display:
        #         new_list_display.remove('priceParity_Remarks')
        #     if 'Options' in new_list_display:
        #         new_list_display.remove('Options')
        # else:
        #     pass

        return new_list_display

    ListAdminView._get_list_display = ListAdminView.get_list_display
    ListAdminView.get_list_display = get_list_display


def monkey_patch(DEBUG=False):
    _reset_get_actions()

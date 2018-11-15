# -*- coding: utf-8 -*-
# 中文

from xadmin.views import BaseAdminPlugin
from django.template import loader



class hide_page_action_Plugin(BaseAdminPlugin):
    hide_page_action= False
    def init_request(self, *args, **kwargs):
        return bool(self.hide_page_action)

    def block_left_navbar(self, context, nodes):
        current_url = self.request.get_full_path()

        page = ''
        if 't_stocking_demand_fba' in current_url and 'Status=giveup' in current_url:
            page = 'giveup'
        if 't_stocking_demand_fba' in current_url and 'Status=notgenpurchase' in current_url:
            page = 'notgenpurchase'
        if 't_stocking_demand_fba_purchase' in current_url and 'Status=notpurchase' in current_url:
            page = 'notpurchase'
        if 't_stocking_demand_fba_purchase' in current_url and 'Status=purchasing' in current_url:
            page = 'purchasing'
        if 't_stocking_demand_fba_purchase' in current_url and 'Status=completepurchase' in current_url:
            page = 'completepurchase'
        if 't_stocking_demand_fba_purchase' in current_url and 'Status=abnormalpurchase' in current_url:
            page = 'abnormalpurchase'
        if 't_stocking_demand_fba_check' in current_url and 'Status=check' in current_url:
            page = 'check'
        if 't_stocking_demand_fba_check' in current_url and 'Status=completecheck' in current_url:
            page = 'completecheck'
        if 't_stocking_demand_fba_check' in current_url and 'Status=abnormalcheck' in current_url:
            page = 'abnormalcheck'
        if 't_stocking_demand_fba_genbatch' in current_url and 'Status=genbatch' in current_url:
            page = 'genbatch'
        if 't_stocking_demand_fba_genbatch' in current_url and 'Status=completegenbatch' in current_url:
            page = 'completegenbatch'
        if 't_stocking_rejecting_fba' in current_url and 'Status=completereject' in current_url:
            page = 'completereject'
        if 't_stocking_demand_fbw' in current_url and 'Status=nodemand' in current_url:
            page = 'fbw_nodemand'
        if 't_stocking_demand_fbw' in current_url and 'Status=deliver' in current_url:
            page = 'fbw_deliver'
        if 't_cloth_factory_dispatch_paiding' in current_url and 'currentState=18' in current_url:
            page = 'cloth_currentState'

        nodes.append(loader.render_to_string('hide_page_action.html', {'page': page}))
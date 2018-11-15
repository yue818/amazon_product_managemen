# -*- coding: utf-8 -*-
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from django.template import loader
from paypal.interface import PayPalInterface
from skuapp.table.t_config_paypal_account import *
from skuapp.table.t_config_user_buyer import *
from skuapp.table.t_api_schedule_ing import *
import operator
import logging
from skuapp.table.t_sys_param import t_sys_param
class t_paypal_payout_logPlugin(BaseAdminPlugin):
    paypal_payout = False

    # 初始化方法根据 ``paypal_payout`` 属性值返回
    def init_request(self, *args, **kwargs):
        return bool(self.paypal_payout)

    def get_media(self, media):
        media.add_js([self.static('xadmin/js/xadmin.plugin.t_paypal_payout_log.html.js')])
        return media

    def getBalance(self,interfaceCheck):
        pp = PayPalInterface(API_USERNAME=interfaceCheck['USER'],
                             API_PASSWORD=interfaceCheck['PWD'],
                             API_SIGNATURE=interfaceCheck['SIGNATURE'],
                             API_ENVIRONMENT='PRODUCTION')
        response = pp._call("GetBalance")
        return response['L_AMT0']

    def block_after_fieldsets(self, context, nodes):
        logger = logging.getLogger('sourceDns.webdns.views')
        sort_user_buyers = []
        balances = []
        user_buyers = []
        try:
            paypal_accounts = t_config_paypal_account.objects.all()
            if len(paypal_accounts)>0:
                for accountList in paypal_accounts:
                    api_username = accountList.Api_UserName
                    api_password = accountList.Api_Password
                    api_signature = accountList.Api_Signature
                    interfaceCheck = {'USER': api_username, 'PWD': api_password, 'SIGNATURE': api_signature}
                    try:
                        balance = self.getBalance(interfaceCheck=interfaceCheck)
                    except:
                        balance = '错误'
                    kv = {'Paypal_Account': accountList.Paypal_Account, 'balance': balance}
                    balances.append(kv)

            api_schedule_ings = t_api_schedule_ing.objects.filter(CMDID='payout')
            buyer_id_list = []
            for api_schedule_ing in api_schedule_ings:
                buyer_id = eval(api_schedule_ing.Params)['Buyer_Id']
                buyer_id_list.append(buyer_id)
            config_user_buyers = t_config_user_buyer.objects.filter(Status='Y',PaypalAccount__isnull=False)
            if len(config_user_buyers)>0:
                for config_user_buyer in config_user_buyers:
                    user_buyer_id = str(config_user_buyer.id)
                    if user_buyer_id not in buyer_id_list:
                        user_buyer = {'BuyerAccount': config_user_buyer.BuyerAccount, 'Balance': config_user_buyer.Balance, 'id':config_user_buyer.id}
                        user_buyers.append(user_buyer)
        except:
            pass

        if len(user_buyers)>0:
            sort_user_buyers = sorted(user_buyers,key=operator.itemgetter('Balance'))
        choicese = t_sys_param.objects.values_list('V').filter(Type=47).order_by('Seq')
        accountChoices = []
        for choi in choicese:
            accountChoices.append(float(choi[0]))
        nodes.append(loader.render_to_string('t_paypal_payout.html',
                                             {'paypal_accounts': balances, 'user_buyers': sort_user_buyers, 'accountChoices': accountChoices}))

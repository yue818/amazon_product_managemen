# coding=utf-8

from xadmin.views import BaseAdminPlugin
from django.template import loader



from brick.table.t_developer_info_ebay import *
from django.db import connection
from brick.ebay.ebay_api import *

class t_config_store_ebay_regetpes_plugin(BaseAdminPlugin):
    ebay_regetpes = False

    def init_request(self, *args, **kwargs):
        return bool(self.ebay_regetpes)

    # def get_media(self, media):
    #     media.add_js([self.static('xadmin/js/xadmin.plugin.cexportoss.js')])
    #     return media


    def block_search_cata_nav(self, context, nodes):
        testparam = self.request.GET.get('testparam', '')
        regType = self.request.GET.get('regType', '')
        sessionid = ''
        runame = ''
        accountID = ''
        id = ''
        appID = ''

        if not testparam:
            testparam = ''
        if testparam:
                appID = self.request.GET.get('appID', '')
                id = self.request.GET.get('id', '')
                accountID = self.request.GET.get('accountID', '')
                t_developer_info_ebay_obj = t_developer_info_ebay(connection)
                if appID:
                    developerdata = t_developer_info_ebay_obj.queryDeveloperEbay(appID)
                    runame = developerdata['datasrcset'][2]
                    appinfo = {
                        'appid': appID,
                        'devid': developerdata['datasrcset'][0],
                        'certid': developerdata['datasrcset'][1],
                        'runame': runame,
                    }
                try:
                    if regType == 'Auth':
                        ebayapi_obj = EBayAPI(appinfo)
                        sessionid = ebayapi_obj.getSessionID()
                    else:
                        pass
                except Exception,ex:
                    test_test = str(repr(ex))
        nodes.append(loader.render_to_string('t_config_store_ebay_regetpes.html', {'runame': runame, 'sessionid':sessionid, 'accountID':accountID, 'id':id,'appID':appID,'testparam':testparam,'regType':regType}))

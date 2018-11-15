# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from django.contrib import messages
from brick.table.t_developer_info_ebay import t_developer_info_ebay
from django.db import connection

class t_config_store_ebay_Admin(object):
    ebay_regetpes = True
    search_box_flag = True
    def operation_shopSkuRule(self,obj):
        rt = u'<input type="button" style="border-radius:10px 10px 10px 10px;background-color:#428BCA;display: inline-block;" value="Auth\'n\'Auth授权" onclick="if(confirm(\'是否重新授权？\')){ window.location.href=\'/t_config_store_ebay_regetpes_plugin/?id=%s&appID=%s&accountID=%s&regType=Auth\'};" /><br>' % (obj.id, obj.appID,obj.accountID)
        rt += u'<input type="button" style="border-radius:10px 10px 10px 10px;background-color:#428BCA;display: inline-block;" value="OAuth授权" onclick="if(confirm(\'是否刷新授权？\')){ window.location.href=\'/t_config_store_ebay_regetpes_plugin/?id=%s&appID=%s&accountID=%s&regType=OAuth\'};" /><br>' % (obj.id, obj.appID,obj.accountID)
        return mark_safe(rt)
    operation_shopSkuRule.short_description = u'操作'

    def show_runIp(self,obj):
        t_developer_info_ebay_obj = t_developer_info_ebay(connection)
        developerdata = t_developer_info_ebay_obj.queryDeveloperEbay(obj.appID)
        if developerdata['errorcode'] == 0:
            runIP = developerdata['datasrcset'][3]
        else:
            runIP = ''
        return mark_safe(runIP)
    show_runIp.short_description = u'IP地址'

    def show_accountPassword(self,obj):
        rt = u'********'
        if self.request.user.is_superuser:
            rt = obj.accountPassword
        return mark_safe(rt)
    show_accountPassword.short_description = u'店铺密码'

    list_display = ('id','storeName','siteID','accountID','show_accountPassword','appID','show_runIp','refresh_time','storeOwner', 'paypalAccountLarge', 'paypalAccountHalf','tokenExpireTime', 'status','operation_shopSkuRule')
    list_editable = ('siteID','storeOwner', 'paypalAccountLarge','paypalAccountHalf')

    def get_list_queryset(self, ):
        request = self.request
        qs = super(t_config_store_ebay_Admin, self).get_list_queryset()
        id = request.GET.get('id', '')
        storeName = request.GET.get('storeName', '')
        storeOwner = request.GET.get('storeOwner', '')
        appid = request.GET.get('appid', '')


        searchList = {'id__exact': id, 'storeName__exact': storeName,
                      'storeOwner__exact': storeOwner, 'appID__contains': appid,
                      }
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')
        return qs










# encoding: utf-8
'''
@author: zhangyu
@contact: 292724306@qq.com
@software: pycharm
@file: wish_ticket_Admin.py
@time: 2018-06-11 14:25
'''
import logging
from django.contrib import messages
from django.utils.safestring import mark_safe

from skuapp.table import t_config_online_amazon

logger = logging.getLogger('sourceDns.webdns.views')


class wish_ticket_Admin(object):
    wish_ticket = True
    wish_site_tree_ti = True
    list_display_links = ("",)
    list_display = ['ticket_id', 'open_date', 'last_update_date', 'subject', 'label', 'state', 'shopName', 'Operators',
                    'updateTime','show_wish_ticket_replay']

    def save_models(self):
        pass

    def show_wish_ticket_replay(self,obj):
        access_token = ''
        config_objs = t_config_online_amazon.objects.filter(Name=obj.shopName, K='access_token') # 根据条件查找店铺是否存在
        if config_objs.exists():
            access_token = config_objs[0].V    # 如果存在得到access_token
        else:
            messages.warning(self.request, '%s without access_token info.' % obj.shopName) # 没有则报错
        # 增加回复标签、点击跳转文本框
        rt = "<div style='margin-left: 35px;'><a id=reply_t%s>回复</a></div>" \
             "<script>$('#reply_t%s').on('click',function()" \
             "{layer.open({type:2,skin:'layui-layer-lan',title:'回复',fix:false,shadeClose: true,maxmin:true,area:['1000px','650px']," \
             "content:'/replay/restore/?id=%s&access_token=%s',});});" \
             "</script>" % ( obj.id, obj.id, obj.ticket_id,access_token)
        return mark_safe(rt)
    show_wish_ticket_replay.short_description = mark_safe('<p style="color:#428bca;text-align:center;width:90px;">操作</p>') # 增加操作行

    def get_list_queryset(self, ):

        # logger = logging.getLogger('sourceDns.webdns.views')
        request = self.request
        Operators = ''
        errorShop = request.GET.get('errorShop', '')
        # 超级用户和金玉玲可以看到所有运营店铺
        if self.request.user.is_superuser or self.request.user.username == 'jinyuling' or self.request.user.username == 'meidandan':
            Operators = ''
        else:
            Operators = self.request.user.first_name
        qs = super(wish_ticket_Admin, self).get_list_queryset()
        shopname = request.GET.get('shopname', '')
        status = request.GET.get('status', '')
        list_errorShop = []
        list_errorShop_tmp = ''
        if errorShop == 'yes' or errorShop == 'no':
            from django_redis import get_redis_connection
            r = get_redis_connection(alias='product')
            errorShopName1 = r.get('{}_errorShopName_ti1'.format(request.user.username))
            errorShopName2 = r.get('{}_errorShopName_ti2'.format(request.user.username))
            errorShopName3 = r.get('{}_errorShopName_ti3'.format(request.user.username))
            errorShopName = "{}{}{}".format(errorShopName1, errorShopName2, errorShopName3)
            list_errorShop_tmp = errorShopName.replace('[', '').replace(']', '').replace('u', '').replace("'",
                                                                                                          "") if errorShopName else ''
            list_errorShop = list_errorShop_tmp.split(',')
            for i in range(len(list_errorShop)):
                list_errorShop[i] = 'Wish-' + list_errorShop[i]
        searchList = {'shopName': shopname, 'Operators': Operators}
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    sl[k] = v
        if sl is not None:
            try:
                if errorShop == 'yes':
                    qs = qs.filter(**sl).filter(shopName__in=list_errorShop)
                elif errorShop == 'no':
                    qs = qs.filter(**sl).exclude(shopName__in=list_errorShop)
                else:
                    qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')
        return qs

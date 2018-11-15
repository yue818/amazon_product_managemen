#!/usr/bin/python
# -*-coding:utf-8-*-

"""
 @desc:
 @author: sunjian
 @site:
 @software: Sublime
 @file: site_left_menu_plugin_joom.py
 @time: 2018-03-07 9:25
"""
from django.template import loader
from django.db.models import Q
from xadmin.views import BaseAdminPlugin
from brick.db.dbconnect import run, execute_db
from aliexpress_app.table.t_aliexpress_online_info import t_aliexpress_online_info
from skuapp.table.t_store_configuration_file import t_store_configuration_file


class site_left_menu_Plugin_price_parity_aliexpress(BaseAdminPlugin):
    site_left_menu_flag_price_parity_aliexpress = False

    def init_request(self, *args, **kwargs):
        return bool(self.site_left_menu_flag_price_parity_aliexpress)

    def get_duplicate_pros_by_sevenordernum(self):
        db_res = run({})
        if db_res['errorcode'] == -1:
            print "result['errortext']: %s" % db_res['errortext']
            return

        # sql = "SELECT id FROM (SELECT id, MainSKU FROM t_aliexpress_online_info AS a WHERE Orders7Days=(SELECT MAX(b.Orders7Days) FROM " \
        #     "t_aliexpress_online_info AS b WHERE b.MainSKU IS NOT NULL AND b.MainSKU<>'' AND a.MainSKU = b.MainSKU AND b.`Status`='True'" \
        #     ")) AS c GROUP BY MainSKU;"
        sql = "SELECT max(a.id) AS id FROM t_aliexpress_online_info a,( SELECT MAX(b.Orders7Days) AS maxorder7days,b.MainSKU " \
            "FROM t_aliexpress_online_info AS b WHERE b.MainSKU IS NOT NULL AND b.MainSKU <> '' AND b.`Status` = 'True' " \
            "GROUP BY b.MainSKU) c WHERE a.MainSKU=c.MainSKU AND a.Orders7Days=c.maxorder7days GROUP BY a.MainSKU"
        duplicate_infos = execute_db(sql, db_res['db_conn'], 'select')
        ids = list()
        for i in duplicate_infos:
            ids.append(i['id'])
        return ids

    def get_menu_count(self):
        if self.request.user.is_superuser or (23, u'组长') in self.request.user.groups.values_list():
            shoplist = []
        else:
            objs = t_store_configuration_file.objects.filter(
                Q(Seller=self.request.user.first_name) | Q(Published=self.request.user.first_name) | Q(
                    Operators=self.request.user.first_name)).values('ShopName')
            if objs.exists():
                shoplist = []
                for obj in objs:
                    shoplist.append(obj['ShopName'])
            else:
                shoplist = 'NO'
        # ids = self.get_duplicate_pros_by_sevenordernum()
        # t_aliexpress_online_info_obj = t_aliexpress_online_info.objects.filter(Status='True')
        t_aliexpress_online_info_obj = t_aliexpress_online_info.objects.filter(Status='1')
        if shoplist == 'NO':
            can_price_partiy = 0
            priceParity_Status_limit_weight = 0
            priceParity_Status_wait = 0
            priceParity_Status_todo = 0
            priceParity_Status_success = 0
            priceParity_Status_no = 0
        elif shoplist:
            # can_price_partiy = t_aliexpress_online_info_obj.filter(id__in=ids, ShopName__in=shoplist).count()
            # priceParity_Status_limit_weight = t_aliexpress_online_info_obj.filter(id__in=ids, ShopName__in=shoplist, Weight__gte=0, Weight__lt=28).count()
            can_price_partiy = t_aliexpress_online_info_obj.filter(CanPriceParity__exact=1, ShopName__in=shoplist).count()
            priceParity_Status_limit_weight = t_aliexpress_online_info_obj.filter(CanPriceParity__exact=1, ShopName__in=shoplist, Weight__gte=0, Weight__lte=28).count()
            priceParity_Status_wait = t_aliexpress_online_info_obj.filter(priceParity_Status='WAIT', ShopName__in=shoplist).count()
            priceParity_Status_todo = t_aliexpress_online_info_obj.filter(priceParity_Status='TODO', ShopName__in=shoplist).count()
            priceParity_Status_success = t_aliexpress_online_info_obj.filter(priceParity_Status='SUCCESS', ShopName__in=shoplist).count()
            priceParity_Status_no = t_aliexpress_online_info_obj.filter(priceParity_Status='NO', ShopName__in=shoplist).count()
        else:
            # can_price_partiy = t_aliexpress_online_info_obj.filter(id__in=ids).count()
            # priceParity_Status_limit_weight = t_aliexpress_online_info_obj.filter(id__in=ids, Weight__gte=0, Weight__lt=28).count()
            can_price_partiy = t_aliexpress_online_info_obj.filter(CanPriceParity__exact=1).count()
            priceParity_Status_limit_weight = t_aliexpress_online_info_obj.filter(CanPriceParity__exact=1, Weight__gte=0, Weight__lte=28).count()
            priceParity_Status_wait = t_aliexpress_online_info_obj.filter(priceParity_Status='WAIT').count()
            priceParity_Status_todo = t_aliexpress_online_info_obj.filter(priceParity_Status='TODO').count()
            priceParity_Status_success = t_aliexpress_online_info_obj.filter(priceParity_Status='SUCCESS').count()
            priceParity_Status_no = t_aliexpress_online_info_obj.filter(priceParity_Status='NO').count()

        menu_count = dict()
        menu_count['can_price_partiy'] = can_price_partiy
        menu_count['priceParity_Status_limit_weight'] = priceParity_Status_limit_weight
        menu_count['priceParity_Status_wait'] = priceParity_Status_wait
        menu_count['priceParity_Status_todo'] = priceParity_Status_todo
        menu_count['priceParity_Status_success'] = priceParity_Status_success
        menu_count['priceParity_Status_no'] = priceParity_Status_no

        return menu_count

    def block_left_navbar(self, context, nodes):

        menu_count = self.get_menu_count()

        sourceURL = str(context['request']).split("'")[1]
        title_list = [{'title': u'平台商品', 'selected': '0'}]
        test_list = [
            {'url': '/Project/admin/aliexpress_app/t_aliexpress_price_parity/?priceParity_Status=ALL', 'value': u'可比价(%s)' % menu_count['can_price_partiy'],
                'title': u'平台商品', 'selected': '0'},
            {'url': '/Project/admin/aliexpress_app/t_aliexpress_price_parity/?priceParity_Status=ALL&WeightStart=0&WeightEnd=28', 'value': u'可比价(0~28g)(%s)' % menu_count['priceParity_Status_limit_weight'],
                'title': u'平台商品', 'selected': '0'},
            {'url': '/Project/admin/aliexpress_app/t_aliexpress_price_parity/?priceParity_Status=WAIT', 'value': u'正在比价(%s)' % menu_count['priceParity_Status_wait'],
                'title': u'平台商品', 'selected': '0'},
            {'url': '/Project/admin/aliexpress_app/t_aliexpress_price_parity/?priceParity_Status=TODO', 'value': u'待比价执行(%s)' % menu_count['priceParity_Status_todo'],
                'title': u'平台商品', 'selected': '0'},
            {'url': '/Project/admin/aliexpress_app/t_aliexpress_price_parity/?priceParity_Status=SUCCESS', 'value': u'执行完成(%s)' % menu_count['priceParity_Status_success'],
                'title': u'平台商品', 'selected': '0'},
            {'url': '/Project/admin/aliexpress_app/t_aliexpress_price_parity/?priceParity_Status=NO', 'value': u'无需比价(%s)' % menu_count['priceParity_Status_no'],
                'title': u'平台商品', 'selected': '0'},
        ]
        title = ''
        for tl in test_list:
            to_url = tl['url']
            search_opt = to_url.split('?')[-1]
            if to_url != sourceURL:
                if '?' not in tl['url']:
                    to_url = to_url + '?'
            if search_opt in sourceURL:
                if search_opt == 'priceParity_Status=ALL&WeightStart=0&WeightEnd=28':
                    test_list[0]['selected'] = '0'
                title = tl['title']
                tl['selected'] = '1'
        if title:
            for titleout in title_list:
                if titleout['title'] == title:
                    titleout['selected'] = '1'

        if '/Project/admin/aliexpress_app/t_aliexpress_price_parity/' in sourceURL and \
                sourceURL != '/Project/admin/aliexpress_app/t_aliexpress_price_parity/?priceParity_Status=ALL&WeightStart=0&WeightEnd=28':
            search_opts = sourceURL.split('?')[-1]
            search_opts_list = search_opts.split('&')
            parent_opts = ''
            if len(search_opts_list) > 1:
                get_sear_opts = list()
                for i in search_opts_list:
                    # if i.find('priceParity_Status') == -1:
                    if i.find('shopname') != -1:
                        get_sear_opts.append(i)
                parent_opts = '&'.join(get_sear_opts)
                for i in test_list:
                    i['url'] = i['url'] + '&' + parent_opts

        nodes.append(loader.render_to_string('site_left_menu_Plugin_aliexpress.html', {'title_list': title_list, 'test_list': test_list, 'sourceURL': sourceURL}))

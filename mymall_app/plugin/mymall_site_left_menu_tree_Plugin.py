# -*-coding:utf-8-*-

import json

from xadmin.views import BaseAdminPlugin
from django.db.models import Q
from django.db import connection
from django.template import loader
from django.template import RequestContext
# from django.contrib import messages
# from django.contrib.auth.models import User

from skuapp.table.t_store_configuration_file import t_store_configuration_file
from mymall_app.table.t_mymall_online_info import t_mymall_online_info
from mymall_app.table.t_mymall_template_publish import t_mymall_template_publish
from mymall_app.table.t_mymall_upload_product_info import t_mymall_upload_product_info
"""
 @desc:
 @author: 孙健
 @site:
 @software: PyCharm
 @file: site_left_menu_Plugin_wish.py
 @time: 2018/2/28 8:53
"""


class mymall_site_left_menu_tree_Plugin(BaseAdminPlugin):
    mymall_site_left_menu_tree_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.mymall_site_left_menu_tree_flag)

    def get_result_count(self, sql):
        row_count = None
        try:
            cursor = connection.cursor()
            cursor.execute(sql)
            count = cursor.fetchone()
            cursor.close()
            if count:
                row_count = count[0]
        except Exception:
            pass
        return row_count

    def block_left_navbar(self, context, nodes):
        shopname = self.request.GET.get('shopname')

        mymall_info_obj = t_mymall_online_info
        mymall_publish_obj = t_mymall_template_publish
        mymall_upload_obj = t_mymall_upload_product_info

        if shopname:
            mymall_info_qs = mymall_info_obj.objects.filter(ShopName=shopname)
            mymall_publish_qs = mymall_publish_obj.objects.filter(ShopName=shopname)
            mymall_upload_qs = mymall_upload_obj.objects.filter(ShopName=shopname)
            vflag = 0
        else:
            mymall_info_qs = mymall_info_obj.objects.none()
            mymall_publish_qs = mymall_publish_obj.objects.none()
            mymall_upload_qs = mymall_upload_obj.objects.none()
            vflag = 1

        if self.request.user.is_superuser:
            if vflag == 1:
                aNUM = self.get_result_count("select * from  tri_db." + self.model._meta.db_table)
                if not aNUM:
                    aNUM = mymall_info_obj.objects.all().count()

                # if params == 'Estatus=Enabled':
                oNUM = mymall_info_obj.objects.all().filter(Status='1').count()  # 在线商品

                # if params == 'Estatus=Disabled':
                offNUM = mymall_info_obj.objects.all().filter(Status='0').count()  # 不在线商品

                nNUM = oNUM + offNUM  # 正常商品

                pub_all_num = mymall_publish_obj.objects.all().count()
                to_pub_num = mymall_publish_obj.objects.filter(PublishResult='2').count()
                pub_success_num = mymall_publish_obj.objects.filter(PublishResult='1').count()
                pub_failed_num = mymall_publish_obj.objects.filter(PublishResult='0').count()
                sum_pubed_num = pub_success_num + pub_failed_num

                upload_num = mymall_upload_obj.objects.all().count()
                up_success_num = mymall_upload_obj.objects.filter(ImportFlag=True).count()
                up_failed_num = mymall_upload_obj.objects.filter(ImportFlag=False).count()

            else:
                aNUM = mymall_info_qs.count()  # 全部商品
                oNUM = mymall_info_qs.filter(Status='1').count()  # 在线商品
                offNUM = mymall_info_qs.filter(Status='0').count()  # 不在线商品
                nNUM = oNUM + offNUM  # 正常商品

                pub_all_num = mymall_publish_qs.count()
                to_pub_num = mymall_publish_qs.filter(PublishResult='2').count()
                pub_success_num = mymall_publish_qs.filter(PublishResult='1').count()
                pub_failed_num = mymall_publish_qs.filter(PublishResult='0').count()
                sum_pubed_num = pub_success_num + pub_failed_num

                upload_num = mymall_upload_qs.all().count()
                up_success_num = mymall_upload_qs.filter(ImportFlag=True).count()
                up_failed_num = mymall_upload_qs.filter(ImportFlag=False).count()
        else:
            shoplist = t_store_configuration_file.objects.filter(
                Q(Seller=self.request.user.first_name) |
                Q(Published=self.request.user.first_name) |
                Q(Operators=self.request.user.first_name)
            ).values_list('ShopName', flat=True)

            if shoplist:
                mymall_info_qs = mymall_info_obj.objects.filter(ShopName__in=shoplist)
                mymall_publish_qs = mymall_publish_obj.objects.filter(ShopName__in=shoplist)
                mymall_upload_qs = mymall_upload_obj.objects.filter(ShopName__in=shoplist)

                aNUM = mymall_info_qs.count()  # 全部商品
                oNUM = mymall_info_qs.filter(Status='1').count()  # 在线商品
                offNUM = mymall_info_qs.filter(Status='0').count()  # 不在线商品
                nNUM = oNUM + offNUM  # 正常商品

                pub_all_num = mymall_publish_qs.count()
                to_pub_num = mymall_publish_qs.filter(PublishResult='2').count()
                pub_success_num = mymall_publish_qs.filter(PublishResult='1').count()
                pub_failed_num = mymall_publish_qs.filter(PublishResult='0').count()
                sum_pubed_num = pub_success_num + pub_failed_num

                upload_num = mymall_upload_qs.all().count()
                up_success_num = mymall_upload_qs.filter(ImportFlag=True).count()
                up_failed_num = mymall_upload_qs.filter(ImportFlag=False).count()

            else:
                aNUM = 0  # 全部商品
                oNUM = 0  # 在线商品
                offNUM = 0  # 不在线商品
                nNUM = 0  # 正常商品

                pub_all_num = 0
                to_pub_num = 0
                pub_success_num = 0
                pub_failed_num = 0
                sum_pubed_num = 0

                upload_num = 0
                up_success_num = 0
                up_failed_num = 0

        nowurl = self.request.get_full_path().replace('Estatus=Enabled', '').replace('Estatus=Disabled', '') \
            .replace('PublishResult=TODO', '').replace('PublishResult=DONE', '') \
            .replace('PublishResult=SUCCESS', '').replace('PublishResult=FAILED', '') \
            .replace('importFlag=True', '').replace('importFlag=False', '') \
            .replace('?&', '?').replace('&&', '&')

        if nowurl[-1:] in ['?', '&']:
            nowurl = nowurl[:-1]
        if nowurl.find('?') == -1:
            nowurl = nowurl + '?'
        else:
            nowurl = nowurl + '&'

        flag = 'info_all'

        if 't_mymall_online_info' in nowurl:
            mymall_info_url = nowurl
            mymall_publish_url = nowurl.replace('t_mymall_online_info', 't_mymall_template_publish')
            mymall_upload_url = nowurl.replace('t_mymall_online_info', 't_mymall_upload_product_info')

            flag1 = self.request.GET.get('Estatus')
            if flag1:
                flag = flag1

        elif 't_mymall_template_publish' in nowurl:
            mymall_info_url = nowurl.replace('t_mymall_template_publish', 't_mymall_online_info')
            mymall_publish_url = nowurl
            mymall_upload_url = nowurl.replace('t_mymall_template_publish', 't_mymall_upload_product_info')

            flag = 'pub_all'
            flag1 = self.request.GET.get('PublishResult')
            if flag1:
                flag = flag1

        elif 't_mymall_upload_product_info' in nowurl:
            mymall_info_url = nowurl.replace('t_mymall_upload_product_info', 't_mymall_online_info')
            mymall_publish_url = nowurl.replace('t_mymall_upload_product_info', 't_mymall_template_publish')
            mymall_upload_url = nowurl

            flag = 'up_all'
            flag1 = self.request.GET.get('importFlag')
            if flag1:
                flag = flag1

        else:
            mymall_info_url = '/Project/admin/mymall_app/t_mymall_online_info/?'
            mymall_publish_url = '/Project/admin/mymall_app/t_mymall_template_publish/?'
            mymall_upload_url = '/Project/admin/mymall_app/t_mymall_upload_product_info/?'

        if self.request.user.has_perm('mymall_app.view_t_mymall_online_info') or \
                self.request.user.has_perm('view_t_mymall_online_info') or \
                self.request.user.is_superuser:
            menu_mymall_online_info = {
                "name": u"全部产品(%s)" % nNUM,
                "code": "11",
                "icon": "icon-minus-sign",
                "parentCode": "01",
                "selected": "",
                "to_url": mymall_info_url[:-1],
                "flag": "",
                "child": [
                    {
                        "name": u"启用(%s)" % oNUM,
                        "icon": "",
                        "code": "111",
                        "parentCode": "11",
                        "selected": "",
                        "to_url": mymall_info_url + 'Estatus=Enabled',
                        "flag": 'Enabled',
                        "child": []
                    },
                    {
                        "name": u"未启用(%s)" % offNUM,
                        "icon": "",
                        "code": "112",
                        "parentCode": "11",
                        "selected": "",
                        "to_url": mymall_info_url + 'Estatus=Disabled',
                        "flag": 'Disabled',
                        "child": []
                    },
                ]
            }
        else:
            menu_mymall_online_info = {}

        if self.request.user.has_perm('mymall_app.view_t_mymall_template_publish') or \
                self.request.user.has_perm('view_t_mymall_template_publish') or \
                self.request.user.is_superuser:
            menu_mymall_publish = {
                "name": u"刊登模板(%s)" % pub_all_num,
                "code": "12",
                "icon": "icon-minus-sign",
                "parentCode": "01",
                "selected": "",
                "to_url": mymall_publish_url[:-1],
                "flag": "pub_all",
                "child": [
                    {
                        "name": u"待刊登(%s)" % to_pub_num,
                        "code": "121",
                        "icon": "",
                        "parentCode": "12",
                        "selected": "",
                        "to_url": mymall_publish_url + 'PublishResult=TODO',
                        "flag": "TODO",
                        "child": []
                    },
                    {
                        "name": u"已刊登(%s)" % sum_pubed_num,
                        "code": "122",
                        "icon": "",
                        "parentCode": "12",
                        "selected": "",
                        "to_url": mymall_publish_url + 'PublishResult=DONE',
                        "flag": "DONE",
                        "child": [
                            {
                                "name": u"成功(%s)" % pub_success_num,
                                "icon": "",
                                "code": "1221",
                                "parentCode": "122",
                                "selected": "",
                                "to_url": mymall_publish_url + 'PublishResult=SUCCESS',
                                "flag": 'SUCCESS',
                                "child": []
                            },
                            {
                                "name": u"失败(%s)" % pub_failed_num,
                                "icon": "",
                                "code": "1222",
                                "parentCode": "122",
                                "selected": "",
                                "to_url": mymall_publish_url + 'PublishResult=FAILED',
                                "flag": 'FAILED',
                                "child": []
                            },
                        ]
                    },
                ]
            }
        else:
            menu_mymall_publish = {}

        if self.request.user.has_perm('mymall_app.view_t_mymall_upload_product_info') or \
                self.request.user.has_perm('view_t_mymall_upload_product_info') or \
                self.request.user.is_superuser:
            menu_mymall_upload = {
                "name": u"商品信息导入(%s)" % upload_num,
                "code": "13",
                "icon": "icon-minus-sign",
                "parentCode": "01",
                "selected": "",
                "to_url": "/Project/admin/mymall_app/t_mymall_upload_product_info/",
                "flag": "up_all",
                "child": [
                    {
                        "name": u"已导入(%s)" % up_success_num,
                        "code": "131",
                        "icon": "",
                        "parentCode": "13",
                        "selected": "",
                        "to_url": mymall_upload_url + 'importFlag=True',
                        "flag": "True",
                        "child": []
                    },
                    {
                        "name": u"未导入(%s)" % up_failed_num,
                        "code": "131",
                        "icon": "",
                        "parentCode": "13",
                        "selected": "",
                        "to_url": mymall_upload_url + 'importFlag=False',
                        "flag": "False",
                        "child": []
                    },
                ]
            }
        else:
            menu_mymall_upload = {}

        menu_list = [
            {
                "name": u"店铺管理",
                "code": "01",
                "icon": "icon-th",
                "selected": "",
                "to_url": "",
                "flag": "info_all",
                "child": [
                    menu_mymall_online_info,
                    menu_mymall_publish,
                    menu_mymall_upload,
                ]
            },
        ]

        show_flag = 0
        for menu_obj in menu_list:
            if menu_obj['flag'] == flag:
                menu_obj['selected'] = 'selected'
                show_flag = 1
            if not menu_obj['child']:
                continue
            for menu_o in menu_obj['child']:
                if not menu_o:
                    continue
                if menu_o['flag'] == flag:
                    menu_o['selected'] = 'selected'
                    show_flag = 1
                if menu_o['child']:
                    for menu_ in menu_o['child']:
                        if not menu_:
                            continue
                        if menu_['flag'] == flag:
                            menu_['selected'] = 'selected'
                            show_flag = 1
                        if menu_['child']:
                            for menu_l in menu_['child']:
                                if not menu_l:
                                    continue
                                if menu_l['flag'] == flag:
                                    menu_l['selected'] = 'selected'
                                    show_flag = 1

        if show_flag == 1:
            # messages.error(self.request, 'count-------%s' % self.request.result_count)
            nodes.append(loader.render_to_string('site_left_menu_tree_Plugin.html', {'menu_list': json.dumps(menu_list)}, context_instance=RequestContext(self.request)))

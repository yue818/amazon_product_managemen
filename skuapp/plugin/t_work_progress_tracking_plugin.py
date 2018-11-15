#-*-coding:utf-8-*-
import json
from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.template import RequestContext

class t_work_progress_tracking_plugin(BaseAdminPlugin):
    progress_tracking_plugin = False

    def init_request(self, *args, **kwargs):
        return bool(self.progress_tracking_plugin)

    def show_select_flag(self, m_list, flag):
        show_flag = 0
        for menu in m_list:
            if menu['flag'] == flag:
                menu['selected'] = 'selected'
                show_flag = 1
            if menu['child']:
                menu['child'], show_flag = self.show_select_flag(menu['child'], flag)

        return m_list,show_flag


    def block_left_navbar(self, context, nodes):
        menu_list = [
            {
                "name": u"进度跟踪",
                "code": "00",
                "icon": "icon-th",
                "selected": "",
                "to_url": "",
                "flag": "home",
                "child": [
                    {
                        "name": u"转供应链",
                        "code": "01",
                        "icon": "icon-minus-sign",
                        "parentCode": "00",
                        "selected": "",
                        "to_url": '/Project/admin/skuapp/t_work_flow_of_plate_house/?proflag=-1&status=1',
                        "flag": "1",
                        "child": []
                    },
                    {
                        "name": u"转供应链(已完成)",
                        "code": "02",
                        "icon": "icon-minus-sign",
                        "parentCode": "00",
                        "selected": "",
                        "to_url": '/Project/admin/skuapp/t_work_flow_of_plate_house/?proflag=7&status=2',
                        "flag": "2",
                        "child": []
                    },
                    {
                        "name": u"只打板",
                        "code": "03",
                        "icon": "icon-minus-sign",
                        "parentCode": "00",
                        "selected": "",
                        "to_url": '/Project/admin/skuapp/t_work_battledore/?proflag=-1&status=3',
                        "flag": "3",
                        "child": []
                    },
                    {
                        "name": u"只打板(已完成)",
                        "code": "04",
                        "icon": "icon-minus-sign",
                        "parentCode": "00",
                        "selected": "",
                        "to_url": '/Project/admin/skuapp/t_work_battledore/?proflag=5&status=4',
                        "flag": "4",
                        "child": []
                    },
                ]
            },
        ]

        flag = self.request.GET.get('status')

        menu_list, show_flag = self.show_select_flag(menu_list, flag)

        nodes.append(loader.render_to_string('site_left_menu_tree_Plugin.html',{'menu_list': json.dumps(menu_list)},context_instance=RequestContext(self.request)))

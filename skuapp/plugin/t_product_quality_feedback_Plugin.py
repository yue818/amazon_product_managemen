# coding=utf-8


from xadmin.views import BaseAdminPlugin
from django.template import loader
import re
from skuapp.table.t_product_quality_feedback_submit import t_product_quality_feedback_submit
from skuapp.table.t_product_quality_feedback_cpzy import t_product_quality_feedback_cpzy
from skuapp.table.t_product_quality_feedback_cgy import t_product_quality_feedback_cgy
from skuapp.table.t_product_quality_feedback_zjy_sh import t_product_quality_feedback_zjy_sh
from skuapp.table.t_product_quality_feedback_zjy import t_product_quality_feedback_zjy
from skuapp.table.t_product_quality_feedback_ck import t_product_quality_feedback_ck
from skuapp.table.t_product_quality_feedback_final_sh import t_product_quality_feedback_final_sh


class t_product_quality_feedback_Plugin(BaseAdminPlugin):
    quality_feedback_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.quality_feedback_flag)

    def get_media(self, media):
        media.add_js([self.static('xadmin/js/xadmin.plugin.button.color.js')])
        return media

    def get_num(self, table, button_list):
        all_num = 0
        for each in button_list[:-1]:
            for k, v in each.items():
                if k != 'num':
                    table_obj = table.objects.filter(State=k)
                    quantity = len(table_obj)
                    each['quantity'] = quantity
                    all_num += quantity
        button_list[-1]['quantity'] = all_num
        return button_list


    def block_search_cata_nav(self, context, nodes):
        url = self.request.get_full_path()
        pattern = re.compile(r't_[a-z_]*')
        now_page = re.search(pattern, url).group()
        cate = self.request.GET.get('cate', '')

        pages = ['t_product_quality_feedback_submit', 't_product_quality_feedback_zjy', 't_product_quality_feedback_cpzy',
                 't_product_quality_feedback_cgy', 't_product_quality_feedback_ck', 't_product_quality_feedback_final_sh']

        if now_page == pages[0]:
            button_list = [{'wtj': u'未提交', 'num': 1}, {'tjdzjy': u'提交到质检员', 'num': 2},
                           {'bbh': u'被驳回', 'num': 3}, {'all': u'全部', 'num': 4}]
            table = t_product_quality_feedback_submit
            button_list = self.get_num(table, button_list)
        elif now_page == pages[1]:
            button_list = [{'wcl': u'未处理', 'num':1}, {'tjdcpzy': u'提交到产品专员', 'num':2},
                           {'tjdcgy': u'提交到采购员', 'num':3}, {'tjdck': u'提交到仓库', 'num':4},
                           {'tjdzzsh': u'提交到最终审核', 'num':5}, {'bh': u'已驳回', 'num':6},
                           {'bbh': u'被驳回', 'num': 7}, {'all': u'全部', 'num':8}]
            table = t_product_quality_feedback_zjy
            button_list = self.get_num(table, button_list)
        elif now_page == pages[2]:
            button_list = [{'wcl': u'未处理', 'num':1}, {'tjdzzsh': u'提交到最终审核', 'num':2},
                           {'bh': u'已驳回', 'num':3}, {'bbh': u'被驳回', 'num': 4}, {'all': u'全部', 'num':5}]
            table = t_product_quality_feedback_cpzy
            button_list = self.get_num(table, button_list)
        elif now_page == pages[3]:
            button_list = [{'wcl': u'未处理', 'num':1}, {'tjdzzsh': u'提交到最终审核', 'num':2},
                           {'bh': u'已驳回', 'num': 3}, {'bbh': u'被驳回', 'num': 4}, {'all': u'全部', 'num':5}]
            table = t_product_quality_feedback_cgy
            button_list = self.get_num(table, button_list)
        elif now_page == pages[4]:
            button_list = [{'wcl': u'未处理', 'num':1}, {'tjdzzsh': u'提交到最终审核', 'num':2},
                           {'bh': u'已驳回', 'num':3}, {'bbh': u'被驳回', 'num': 4}, {'all': u'全部', 'num':5}]
            table = t_product_quality_feedback_ck
            button_list = self.get_num(table, button_list)
        elif now_page == pages[5]:
            button_list = [{'wcl': u'未处理', 'num':1}, {'tjdzzjg': u'提交到最终结果', 'num':2}, {'bh': u'已驳回', 'num':3},
                           {'all': u'全部', 'num':4}]
            table = t_product_quality_feedback_final_sh
            button_list = self.get_num(table, button_list)
        else:
            button_list = {}

        if cate == '':
            flag = 1
        else:
            for each in button_list:
                for k, v in each.items():
                    if cate == k:
                        flag = each['num']
                        break

        nodes.append(loader.render_to_string('product_quality_feedback.html',
                                             {'now_url': url.split('?')[0], 'button_list': button_list, 'flag': flag}))

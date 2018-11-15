#-*-coding:utf-8-*-
"""
 @desc:
 @author: wangzhiyang
 @site:
 @software: PyCharm
 @file: t_cloth_factory_Plugin.py
 @time: 2018/3/26 8:53
"""
from xadmin.views import BaseAdminPlugin
from django.template import loader
from pyapp.table.t_cloth_factory_dispatch_apply import t_cloth_factory_dispatch_apply
from skuapp.table.t_cloth_factory_dispatch_needpurchase import t_cloth_factory_dispatch_needpurchase
from skuapp.table.t_cloth_factory_dispatch_noneedpurchase import t_cloth_factory_dispatch_noneedpurchase
from skuapp.table.t_cloth_factory_dispatch_plan import t_cloth_factory_dispatch_plan
from skuapp.table.t_cloth_factory_dispatch_spemanmodify import t_cloth_factory_dispatch_spemanmodify
from skuapp.table.t_cloth_factory_dispatch_paiding import t_cloth_factory_dispatch_paiding
from skuapp.table.t_cloth_factory_dispatch_no_audit import t_cloth_factory_dispatch_no_audit
from skuapp.table.t_cloth_factory_dispatch_audit import t_cloth_factory_dispatch_audit
from skuapp.table.t_cloth_factory_dispatch_confirm import t_cloth_factory_dispatch_confirm
from skuapp.table.t_cloth_factory_dispatch_overtobuild import t_cloth_factory_dispatch_overtobuild
from skuapp.table.t_cloth_factory_dispatch_close import t_cloth_factory_dispatch_close
from skuapp.table.t_cloth_factory_dispatch_history import t_cloth_factory_dispatch_history
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
"""  
 @desc:  
 @author: wangzhiyang  
 @site: 
 @software: PyCharm
 @file: t_cloth_factory_Plugin.py
 @time: 2018/3/26 8:53
"""   
class t_cloth_factory_Plugin(BaseAdminPlugin):
    t_cloth_factory = False

    def init_request(self, *args, **kwargs):
        return bool(self.t_cloth_factory)

    def block_left_navbar(self, context, nodes):
        '''
        #状态说：
            0：需采购供应链服装列表
            4、6：采购计划、采购计划审核未通过
            8：采购计划审核
            12、14：供应链专员修改及制定派单计划、排单计划审核未通过（供应链专员修改及制定派单计划 去掉 20180704）
            16：排单计划审核（排单审核去掉2018-06-14）
            16、18：服装工厂排单中（服装工厂排单中 增加2018-09-13）
            20、22：校验交付数量和单价（22部分完成）
            24：生产完成可建普源采购单
            28：已建普源采购单
            32：不需要采购供应链服装列表
        '''
        try:
            from datetime import datetime
            createDateStart = (datetime.now()).strftime('%Y-%m-%d 00:00:00')
            createDateEnd = (datetime.now()).strftime('%Y-%m-%d 23:59:59')
            userID = [each.id for each in User.objects.filter(groups__id__in=[48])]
            if self.request.user.is_superuser or self.request.user.id in userID:
                t_cloth_factory_dispatch_apply_count = t_cloth_factory_dispatch_apply.objects.filter(Q(CategoryCode=u'001.时尚女装') | Q(CategoryCode=u'002.时尚男装')| Q(CategoryCode=u'025.内衣')| Q(CategoryCode=u'021.泳装')| Q(CategoryCode=u'024.儿童服装'),Q(SupplierName=u'广州工厂')|Q(SupplierName=u'易臻工厂')|Q(SupplierName=u'马俊杰')).values(
                    'id').count()
                t_cloth_factory_dispatch_needpurchase_count = t_cloth_factory_dispatch_needpurchase.objects.filter(
                    currentState='0',createDate__gte=createDateStart,createDate__lt=createDateEnd,SuggestNum__gt=0).values('id').count()
                t_cloth_factory_dispatch_noneedpurchase_count = t_cloth_factory_dispatch_noneedpurchase.objects.filter(
                    currentState='32',createDate__gte=createDateStart).values('id').count()
                t_cloth_factory_dispatch_plan_count = t_cloth_factory_dispatch_plan.objects.filter(
                    Q(currentState='4')|Q(currentState='6')).values('id').count()
                t_cloth_factory_dispatch_audit_count = t_cloth_factory_dispatch_audit.objects.filter(currentState='8').values('id').count()
                #t_cloth_factory_dispatch_spemanmodify_count = t_cloth_factory_dispatch_spemanmodify.objects.filter(Q(currentState='12') | Q(currentState='14')).values('id').count()
                t_cloth_factory_dispatch_paiding_count_16 = t_cloth_factory_dispatch_paiding.objects.filter(currentState='16').values('id').count()
                t_cloth_factory_dispatch_paiding_count_18 = t_cloth_factory_dispatch_paiding.objects.filter(currentState='18').values('id').count()
                t_cloth_factory_dispatch_confirm_count = t_cloth_factory_dispatch_confirm.objects.filter(
                    Q(currentState='22') | Q(currentState='20')).values( 'id').count()
                t_cloth_factory_dispatch_overtobuild_count = t_cloth_factory_dispatch_overtobuild.objects.filter(
                    currentState='24').values('id').count()
                t_cloth_factory_dispatch_close_count = t_cloth_factory_dispatch_close.objects.filter(currentState='28').values(
                    'id').count()
                t_cloth_factory_dispatch_history_count = t_cloth_factory_dispatch_history.objects.filter(
                    Q(currentState='0') | Q(currentState='32'),createDate__lt=createDateStart).values('id').count()
            else:
                t_cloth_factory_dispatch_apply_count = t_cloth_factory_dispatch_apply.objects.filter(Q(CategoryCode=u'001.时尚女装') | Q(CategoryCode=u'002.时尚男装')| Q(CategoryCode=u'025.内衣')| Q(CategoryCode=u'021.泳装')| Q(CategoryCode=u'024.儿童服装'),
                    Q(SupplierName=u'广州工厂')|Q(SupplierName=u'易臻工厂')|Q(SupplierName=u'马俊杰'),Purchaser=self.request.user.first_name).values(
                    'id').count()
                t_cloth_factory_dispatch_needpurchase_count = t_cloth_factory_dispatch_needpurchase.objects.filter(
                    currentState='0',buyer = self.request.user.first_name,createDate__gte=createDateStart,createDate__lt=createDateEnd,SuggestNum__gt=0).values('id').count()
                t_cloth_factory_dispatch_noneedpurchase_count = t_cloth_factory_dispatch_noneedpurchase.objects.filter(
                    currentState='32', buyer=self.request.user.first_name,createDate__gte=createDateStart).values('id').count()
                t_cloth_factory_dispatch_plan_count = t_cloth_factory_dispatch_plan.objects.filter(
                    Q(currentState='4') | Q(currentState='6'),buyer = self.request.user.first_name).values('id').count()
                t_cloth_factory_dispatch_audit_count = t_cloth_factory_dispatch_audit.objects.filter(
                    currentState='8',buyer = self.request.user.first_name).values('id').count()
                #t_cloth_factory_dispatch_spemanmodify_count = t_cloth_factory_dispatch_spemanmodify.objects.filter(Q(currentState='12') | Q(currentState='14'),buyer = self.request.user.first_name).values('id').count()
                t_cloth_factory_dispatch_paiding_count_16 = t_cloth_factory_dispatch_paiding.objects.filter(currentState='16',buyer = self.request.user.first_name).values('id').count()
                t_cloth_factory_dispatch_paiding_count_18 = t_cloth_factory_dispatch_paiding.objects.filter(currentState='18',buyer = self.request.user.first_name).values('id').count()
                t_cloth_factory_dispatch_confirm_count = t_cloth_factory_dispatch_confirm.objects.filter(
                    Q(currentState='22') | Q(currentState='20'),buyer = self.request.user.first_name).values('id').count()
                t_cloth_factory_dispatch_overtobuild_count = t_cloth_factory_dispatch_overtobuild.objects.filter(
                    currentState='24',buyer = self.request.user.first_name).values('id').count()
                t_cloth_factory_dispatch_close_count = t_cloth_factory_dispatch_close.objects.filter(
                    currentState='28',buyer = self.request.user.first_name).values(
                    'id').count()
                t_cloth_factory_dispatch_history_count = t_cloth_factory_dispatch_history.objects.filter(
                    Q(currentState='0') | Q(currentState='32'),buyer = self.request.user.first_name,createDate__lt=createDateStart).values('id').count()
            sourceURL = str(context['request']).split("'")[1]
            title_list = [{'title': u'供应链服装排单流程', 'selected': '0'}]
            test_list = [{'url': '/Project/admin/pyapp/t_cloth_factory_dispatch_apply/', 'value': u'1-全部供应链服装列表('+str(t_cloth_factory_dispatch_apply_count)+')',
                          'title': u'供应链服装排单流程', 'selected': '0'},
                         {'url': '/Project/admin/skuapp/t_cloth_factory_dispatch_needpurchase/','value': u'2.1-需采购供应链服装列表(' + str(t_cloth_factory_dispatch_needpurchase_count) + ')',
                          'title': u'供应链服装排单流程', 'selected': '0'},
                         {'url': '/Project/admin/skuapp/t_cloth_factory_dispatch_noneedpurchase/','value': u'2.2-不需采购供应链服装列表(' + str(t_cloth_factory_dispatch_noneedpurchase_count) + ')',
                          'title': u'供应链服装排单流程', 'selected': '0'},
                        {'url': '/Project/admin/skuapp/t_cloth_factory_dispatch_plan/', 'value': u'3-采购计划('+str(t_cloth_factory_dispatch_plan_count)+')',
                          'title': u'供应链服装排单流程', 'selected': '0'},
                         {'url': '/Project/admin/skuapp/t_cloth_factory_dispatch_audit/', 'value': u'4-采购计划审核('+str(t_cloth_factory_dispatch_audit_count)+')',
                          'title': u'供应链服装排单流程', 'selected': '0'},
                         {'url': '/Project/admin/skuapp/t_cloth_factory_dispatch_paiding/?currentState=16','value': u'5.1-未转工厂交付系统(' + str(t_cloth_factory_dispatch_paiding_count_16) + ')',
                          'title': u'供应链服装排单流程', 'selected': '0'},
                         {'url': '/Project/admin/skuapp/t_cloth_factory_dispatch_paiding/?currentState=18','value': u'5.2-转工厂交付系统处理中(' + str(t_cloth_factory_dispatch_paiding_count_18) + ')',
                          'title': u'供应链服装排单流程', 'selected': '0'},
                         {'url': '/Project/admin/skuapp/t_cloth_factory_dispatch_confirm/', 'value': u'6-校验交付数量和单价('+str(t_cloth_factory_dispatch_confirm_count)+')',
                          'title': u'供应链服装排单流程', 'selected': '0'},
                         {'url': '/Project/admin/skuapp/t_cloth_factory_dispatch_overtobuild/', 'value': u'7-生产完成可建普源采购单('+str(t_cloth_factory_dispatch_overtobuild_count)+')',
                          'title': u'供应链服装排单流程', 'selected': '0'},
                         {'url': '/Project/admin/skuapp/t_cloth_factory_dispatch_close/', 'value': u'8-已建普源采购单('+str(t_cloth_factory_dispatch_close_count)+')',
                          'title': u'供应链服装排单流程', 'selected': '0'},
                         {'url': '/Project/admin/skuapp/t_cloth_factory_dispatch_history/', 'value': u'9-需采购和不需采购历史数据(' + str(t_cloth_factory_dispatch_history_count) + ')',
                          'title': u'供应链服装排单流程', 'selected': '0'},]
            title = ''
            flag = 0
            for tl in test_list:
                to_url = tl['url']
                if to_url != sourceURL:
                    if '?' not in tl['url']:
                        to_url = to_url + '?'
                if to_url in sourceURL:
                    title = tl['title']
                    tl['selected'] = '1'
                    flag = 1
            if title:
                for titleout in title_list:
                    if titleout['title'] == title:
                        titleout['selected'] = '1'
            if flag == 1:
                nodes.append(loader.render_to_string('t_cloth_factory_left_menu_Plugin.html',
                                                     {'title_list': title_list, 'test_list': test_list, 'sourceURL': sourceURL}))
        except Exception as e:
            messages.info(request,u'error:%s,加载左侧树形菜单栏存在问题，请联系开发人员。'% ( str(e)))
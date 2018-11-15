#-*-coding:utf-8-*-
from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.contrib import messages
from skuapp.table.t_template_amazon_advertising_business_count_report import t_template_amazon_advertising_business_count_report
from skuapp.table.t_template_amazon_advertising_business_report import t_template_amazon_advertising_business_report
from skuapp.table.t_template_amazon_advertising_business_daily_report import t_template_amazon_advertising_business_daily_report
from skuapp.table.t_template_amazon_advertising_business_count_shop_report import t_template_amazon_advertising_business_count_shop_report
from skuapp.table.t_template_amazon_advertising_keywords_report import t_template_amazon_advertising_keywords_report
"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: site_left_menu_tree_amazon_advertising_Plugin.py
 @time: 2018/2/28 8:53
"""   
class site_left_menu_tree_amazon_advertising_Plugin(BaseAdminPlugin):
    site_left_menu_tree_amazon_advertising_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.site_left_menu_tree_amazon_advertising_flag)

    def validation_url_selected(self, menu_list, new_sourceURL, show_flag):
        for menu_obj in menu_list:
            to_url = menu_obj['to_url']
            menu_child_obj = menu_obj['child']
            if len(menu_child_obj) > 0:
                if to_url == new_sourceURL:
                    menu_obj['selected'] = 'selected'
                    show_flag = 1
                    break
                menu_child_obj, show_flag = self.validation_url_selected(menu_child_obj, new_sourceURL, show_flag)
            else:
                if to_url != new_sourceURL:
                    if '?' not in menu_obj['to_url']:
                        to_url = to_url + '?'
                if to_url == new_sourceURL:
                    menu_obj['selected'] = 'selected'
                    show_flag = 1
                    break
        # messages.error(self.request, 'code: %s' % menu_obj['code'])
        return menu_list, show_flag

    def block_left_navbar(self, context, nodes):
        actions_temp = {'Selection_ad': [],
                        'Continuous_ad': [0],
                        'Stoping_ad': [0,1],
                        'All_ad': [0, 1]}
        all_count = t_template_amazon_advertising_business_report.objects.values('id').count()
        daily_count = t_template_amazon_advertising_business_daily_report.objects.values('id').count()
        abc_count = t_template_amazon_advertising_business_count_report.objects.values('id').count()
        shop_count = t_template_amazon_advertising_business_count_shop_report.objects.values('id').count()
        abc_se_count = t_template_amazon_advertising_business_count_report.objects.filter(advertising_status__exact='ENABLED',
                                                           advertising_online_status__exact='Selection_ad').values('id').count()
        abc_co_count = t_template_amazon_advertising_business_count_report.objects.filter(advertising_status__exact='ENABLED',
                                                           advertising_online_status__exact='Continuous_ad').values('id').count()
        abc_st_count = t_template_amazon_advertising_business_count_report.objects.filter(advertising_status__exact='PAUSED',
                                                           advertising_online_status__exact='Stoping_ad').values('id').count()
        keywords_count = t_template_amazon_advertising_keywords_report.objects.values('id').count()

        menu_list = [{
            "name": u"Amazon广告管理",
            "code": "AMAGGGL",
            "icon": "icon-th",
            "selected": "",
            "to_url": "",
            "child": [{
                    "name": u"全部广告(%s)"%all_count,
                    "code": "QBGG",
                    "icon": "icon-minus-sign",
                    "parentCode": "AMAGGGL",
                    "selected": "",
                    "to_url": "/Project/admin/skuapp/t_template_amazon_advertising_business_report/",
                    "child": []
                },{
                    "name": u"店铺广告汇总(%s)"%shop_count,
                    "code": "DPGGHZ",
                    "icon": "icon-minus-sign",
                    "parentCode": "AMAGGGL",
                    "selected": "",
                    "to_url": "/Project/admin/skuapp/t_template_amazon_advertising_business_count_shop_report/",
                    "child": []
                }, {
                    "name": u"店铺广告日统计报表(%s)"%daily_count,
                    "code": "DPGGRTJ",
                    "icon": "icon-minus-sign",
                    "parentCode": "AMAGGGL",
                    "selected": "",
                    "to_url": "/Project/admin/skuapp/t_template_amazon_advertising_business_daily_report/",
                    "child": []
                }, {
                    "name": u"广告汇总(%s)"%abc_count,
                    "code": "GGHZ",
                    "icon": "icon-minus-sign",
                    "parentCode": "AMAGGGL",
                    "selected": "",
                    "to_url": "/Project/admin/skuapp/t_template_amazon_advertising_business_count_report/",
                    "child": [
                        {
                            "name": u"选品广告(%s)"%abc_se_count,
                            "icon": "",
                            "code": "XPGG",
                            "parentCode": "GGHZ",
                            "selected": "",
                            "to_url": "/Project/admin/skuapp/t_template_amazon_advertising_business_count_report/?"
                                      "_p_advertising_status=ENABLED&_p_advertising_online_status=Selection_ad",
                            "child": []
                        },{
                            "name": u"连续广告(%s)"%abc_co_count,
                            "icon": "",
                            "code": "LXGG",
                            "parentCode": "GGHZ",
                            "selected": "",
                            "to_url": "/Project/admin/skuapp/t_template_amazon_advertising_business_count_report/?"
                                      "_p_advertising_status=ENABLED&_p_advertising_online_status=Continuous_ad",
                            "child": []
                        },{
                            "name": u"停止广告(%s)"%abc_st_count,
                            "icon": "",
                            "code": "TZGG",
                            "parentCode": "GGHZ",
                            "selected": "",
                            "to_url": "/Project/admin/skuapp/t_template_amazon_advertising_business_count_report/?"
                                      "_p_advertising_status=PAUSED&_p_advertising_online_status=Stoping_ad",
                            "child": []
                        },]
                },{
                    "name": u"全部广告关键词(%s)"%keywords_count,
                    "code": "QBGGGJC",
                    "icon": "icon-minus-sign",
                    "parentCode": "AMAGGGL",
                    "selected": "",
                    "to_url": "/Project/admin/skuapp/t_template_amazon_advertising_keywords_report/",
                    "child": []
                }, ]
            }]
        url_dict = {"/Project/admin/skuapp/t_template_amazon_advertising_business_report/": [],
                    "/Project/admin/skuapp/t_template_amazon_advertising_business_count_report/": ['_p_advertising_status=ENABLED&_p_advertising_online_status=Selection_ad',
                                                                                                   '_p_advertising_status=PAUSED&_p_advertising_online_status=Stoping_ad',
                                                                                                   '_p_advertising_status=ENABLED&_p_advertising_online_status=Continuous_ad'],
                    "/Project/admin/skuapp/t_template_amazon_advertising_business_daily_report/": [],
                    '/Project/admin/skuapp/t_template_amazon_advertising_business_count_shop_report/': [],
                    "/Project/admin/skuapp/t_template_amazon_advertising_keywords_report/": [],
                    }
        sourceURL = self.request.get_full_path()
        # messages.error(self.request, 'sourceURL: %s' % sourceURL)
        # new_sourceURL = sourceURL
        from_url = sourceURL.split('?')[0]
        new_sourceURL = from_url
        for k, v in url_dict.items():
            if from_url == k:
                for param_value in v:
                    if param_value in sourceURL:
                        new_sourceURL += '?' + param_value

        show_flag = 0
        menu_list, show_flag = self.validation_url_selected(menu_list, new_sourceURL, show_flag)
        # messages.error(self.request, 'show_flag: %s' % show_flag)
        # messages.error(self.request, 'menu_list: %s' % menu_list)
        actions = actions_temp[self.request.GET.get('_p_advertising_online_status', 'All_ad')]


        if show_flag == 1:
            import json
            attention_text = ''
            # 左侧栏文字
            attention_text = u'<span style="height: 50px;width: 240px;font-size: 16px; color:red;">' \
                             u'广告命名规则：店铺主SKU(店铺SKU)/父ASIN(子ASIN)-关键词-A/M/a/m' \
                             u'<br>' \
                             u'<br>' \
                             u'广告阀值：' \
                             u'<br>' \
                             u'1. 点击率小于 0.5%' \
                             u'<br>' \
                             u'2. 点击成本大于0.8' \
                             u'<br>' \
                             u'3. 订单/点击量小于0.1' \
                             u'<br>' \
                             u'4. ACOS 大于40%' \
                             u'<br>' \
                             u'5. AS  大于 15%-----标红' \
                             u'<br>' \
                             u'6. AT 大于 30%' \
                             u'<br>' \
                             u'7.转化率小于10%' \
                             u'<br>' \
                             u'<br>' \
                             u'关键词阀值：' \
                             u'<br>' \
                             u'1. 点击率小于 2%' \
                             u'<br>' \
                             u'2. 转化率小于 10%' \
                             u'<br>' \
                             u'3. 每次点击成本大于 0.7' \
                             u'<br>' \
                             u'4. ACOS 大于35%' \
                             u'<br>' \
                             u'<br>' \
                             u'预算：每天的广告预算（显示数据累加）' \
                             u'<br>' \
                             u'曝光量：广告产品展示的次数' \
                             u'<br>' \
                             u'点击量：通过广告点击产品的次数' \
                             u'<br>' \
                             u'点击率：点击量/曝光量' \
                             u'<br>' \
                             u'花费：点击广告产生的费用' \
                             u'<br>' \
                             u'点击成本：花费/点击量' \
                             u'<br>' \
                             u'订单数：通过广告产生形成的订单' \
                             u'<br>' \
                             u'广告销售额：通过广告产生的销售额' \
                             u'<br>' \
                             u'ACOS=花费/广告销售额' \
                             u'<br>' \
                             u'访问量：访问商品总次数' \
                             u'<br>' \
                             u'订购量：订购商品总数' \
                             u'<br>' \
                             u'业务报告销售额：订购商品总销售额' \
                             u'<br>' \
                             u'转化率=订购量/访问量' \
                             u'<br>' \
                             u'AT=广告订单数/业务报告订购量' \
                             u'<br>' \
                             u'AS=花费/订购商品总销售额' \
                             u'<//span><br//>'
            # # 左侧栏图片
            # attention_text += '<br//><br//><img id="img_left" class="x" src="http:////fancyqube-tort.oss-cn-shanghai.aliyuncs.com/aliexpress/1/IPflowchart.png">'
            nodes.append(loader.render_to_string('site_left_menu_tree_amazon_ad_Plugin.html',
                                                 {'menu_list': json.dumps(menu_list),
                                                  'attention_text': attention_text,
                                                  'new_actions': actions}))
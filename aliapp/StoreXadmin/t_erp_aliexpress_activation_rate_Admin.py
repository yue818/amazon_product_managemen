#-*-coding:utf-8-*-
import datetime
import json
from aliapp.Redis_connect import redis_aliexprss
from aliapp.models import t_erp_aliexpress_online_info
from aliapp.models import t_erp_aliexpress_shop_info
from aliapp.models import t_erp_aliexpress_product_daily
from aliapp.models import t_erp_aliexpress_activation_rate
from aliapp.models import t_erp_aliexpress_activation_rate_overview
from aliapp.models import t_erp_aliexpress_config_category

class t_erp_aliexpress_activation_rate_Admin(object):
    activation_rate_flag=True
    search_box_flag = True
    list_display_links = ('',)
    list_display=['category','submitter','activation_rate','activation_count','product_count','updatetime']



    def main(self,gmt_start,gmt_end):
        query_dict={}
        query_dict['gmt_create__gte']=gmt_start
        query_dict['gmt_create__lt']=gmt_end
        new_gmt_end = (datetime.datetime.strptime(gmt_end.strip(), '%Y-%m-%d') - datetime.timedelta(days=1)).strftime(
            '%Y-%m-%d')
        gmt_time = gmt_start.strip() + '-' + new_gmt_end.strip()
        ra = redis_aliexprss()
        redis_name = 'ali_activation_rate__{}'.format(gmt_time)

        category_dict = {}
        category_objs = t_erp_aliexpress_config_category.objects.values('category_id', 'category_name_zh',
                                                                        'full_path_zh', 'category_level')
        for obj in category_objs:
            if obj['category_level'] in (1, '1', u'1'):
                category_dict[int(obj['category_id'])] = obj['category_name_zh']
            else:
                categoryname = obj['full_path_zh'].split('>>')[0]
                if categoryname == '服装/服饰配件':
                    secondcategory = obj['full_path_zh'].split('>>')[1]
                    if secondcategory.strip().startswith('服饰配饰'):
                        category_dict[int(obj['category_id'])] = '服饰配饰'
                    else:
                        category_dict[int(obj['category_id'])] = '服装'
                else:
                    category_dict[int(obj['category_id'])] = categoryname

            for c in [200003561, 200003565, 200003564, 200003566, 200003568, 200003577, 200003569, 200003567]:
                category_dict[c] = '电子烟'

        category_switch = {"箱包": "箱包鞋类", "运动及娱乐": "运动鞋服包/户外配附", "家具和室内装饰品": "家居&家具", "玩具": "母婴&玩具",
                           "手表": "珠宝饰品及配件", "孕婴童": "母婴&玩具", "鞋子": "箱包鞋类", "电脑和办公": "电脑网络&办公文教",
                           "家用电器": "家用电器", "电话和通讯": "手机配件", "家装（硬装）": "家装&灯具&工具", "安全防护": "安全防护",
                           "工具": "家装&灯具&工具", "办公文教用品": "电脑网络&办公文教", "照明灯饰": "家装&灯具&工具",
                           "家居用品": "家居&家具", "汽车、摩托车": "汽摩配", "安防": "安全防护", }

        # 品类关系替换
        for category_id, v in category_dict.items():
            if str(v) in category_switch:
                category_dict[category_id] = category_switch[str(v)]

        objs = t_erp_aliexpress_online_info.objects.filter(**query_dict)\
            .values_list('owner_member_id', 'product_id', 'submitter','activation_flag','category_id')

        shopcatagory_objs = t_erp_aliexpress_shop_info.objects.values('accountName', 'cata_zh')
        shopcatagory_dict = {}
        for obj in shopcatagory_objs:
            shopcatagory_dict[obj['accountName']] = obj['cata_zh']

        submitter_dict = {}
        product_sales = set()
        for obj in objs:
            submitter = obj[2]
            if not submitter or submitter == u'\x00':
                submitter = u'unknow'
            product_id = obj[1]
            category_id = int(obj[4])
            accountName = obj[0]
            if obj[3] in ('1', 1, u'1'):
                product_sales.add(product_id)
            if not isinstance(submitter_dict.get(submitter), dict):  # 初始化 submitter_dict
                submitter_dict[submitter] = {}

            _category = category_dict.get(category_id, '家居&家具')
            if _category == '其他特殊类':
                _category = '其他特殊类(' + shopcatagory_dict[accountName] + '账号)'
            elif _category == '珠宝饰品及配件':
                if shopcatagory_dict[accountName] == '服装服饰':
                    _category = '珠宝饰品及配件(服装账号)'
            elif _category == '服装':
                if shopcatagory_dict[accountName] == '珠宝饰品及配件':
                    _category = '服装(饰品账号)'

            if not isinstance(submitter_dict[submitter].get(_category), set):
                submitter_dict[submitter][_category] = set()

            submitter_dict[submitter][_category].add(product_id)

        for submitter in submitter_dict:
            tmp = {}
            for category in submitter_dict[submitter]:
                if tmp.get(category, None) is None:
                    tmp[category] = set()
                product_set = submitter_dict[submitter][category]
                tmp[category].update(product_set)
            for category in tmp:
                product_set = tmp[category]
                activation_count = len(product_set & product_sales)
                rate = round(activation_count * 100.0 / len(product_set), 1)
                defaults = {u'activation_rate': rate, u'activation_count': activation_count,
                            u'product_count': len(product_set)}
                t_erp_aliexpress_activation_rate.objects.update_or_create(submitter=submitter, category=category,gmt_time=gmt_time,
                                                                          updatetime=datetime.datetime.now(),defaults=defaults)

        # 向t_erp_aliexpress_activation_rate_overview表写入统计数据
        objs = t_erp_aliexpress_activation_rate.objects.filter(updatetime=datetime.datetime.now(),gmt_time=gmt_time)
        submitter_dict = {}
        category_dict = {}
        datadict = {'Submitter': [], 'Category': [], }
        activation_count_dict={'Submitter':[],'Category':[]}
        product_count_dict={'Submitter':[],'Category':[]}
        for obj in objs:
            if not isinstance(submitter_dict.get(obj.submitter), dict):
                submitter_dict[obj.submitter] = {'product_count': 0, 'activation_count': 0}
            if not isinstance(category_dict.get(obj.category), dict):
                category_dict[obj.category] = {'product_count': 0, 'activation_count': 0}
            submitter_dict[obj.submitter]['product_count'] += obj.product_count
            submitter_dict[obj.submitter]['activation_count'] += obj.activation_count
            category_dict[obj.category]['product_count'] += obj.product_count
            category_dict[obj.category]['activation_count'] += obj.activation_count
        for submitter, submitter_data in submitter_dict.items():
            submitter_rate = round(submitter_data.get('activation_count') * 100.0 / submitter_data.get('product_count'),1)


            datadict['Submitter'].append([submitter, submitter_rate])
            product_count_dict['Submitter'].append([submitter, submitter_data.get('product_count')])
            activation_count_dict['Submitter'].append([submitter, submitter_data.get('activation_count')])


            defaults = {'rate': submitter_rate, 'type': 0,'activation_count':submitter_data.get('activation_count'),
                        'product_count':submitter_data.get('product_count')}
            t_erp_aliexpress_activation_rate_overview.objects.update_or_create(name=submitter,gmt_time=gmt_time,
                                                                               updatetime=datetime.datetime.now(),
                                                                               defaults=defaults)
        for category, category_data in category_dict.items():
            category_rate = round(category_data.get('activation_count') * 100.0 / category_data.get('product_count'), 1)


            datadict['Category'].append([category,category_rate])
            product_count_dict['Category'].append([category, category_data.get('product_count')])
            activation_count_dict['Category'].append([category, category_data.get('activation_count')])


            defaults = {'rate': category_rate, 'type': 1,'activation_count':category_data.get('activation_count'),
                        'product_count':category_data.get('product_count')}
            t_erp_aliexpress_activation_rate_overview.objects.update_or_create(name=category,gmt_time=gmt_time,
                                                                               updatetime=datetime.datetime.now(),
                                                                               defaults=defaults)
        result={}
        result['Submitter_rate']=json.dumps(datadict['Submitter'])
        result['Category_rate']=json.dumps(datadict['Category'])
        result['Submitter_product_count']=json.dumps(product_count_dict['Submitter'])
        result['Category_product_count'] = json.dumps(product_count_dict['Category'])
        result['Submitter_activation_count']=json.dumps(activation_count_dict['Submitter'])
        result['Category_activation_count'] = json.dumps(activation_count_dict['Category'])
        result['tdate']=gmt_time


        ra.set_data(redis_name,result)
        ra.redis_conn.expire(redis_name, 10800)


    def get_list_queryset(self):
        request = self.request
        qs = super(t_erp_aliexpress_activation_rate_Admin, self).get_list_queryset()
        UpdateTime_start = request.GET.get('UpdateTime_start',datetime.datetime.now().strftime('%Y-%m-%d'))
        UpdateTime_end = request.GET.get('UpdateTime_end','')
        gmt_start=request.GET.get('gmt_start','')
        gmt_end=request.GET.get('gmt_end','')
        submitter=request.GET.get('submitter','').split(',')
        category=request.GET.get('category','').split(',')
        searchList = {'updatetime__gte': UpdateTime_start, 'updatetime__lt': UpdateTime_end,}
        if category !=['',]:
            searchList.update({'category__in':category})
        if submitter !=['',]:
            searchList.update({'submitter__in':submitter})

        if gmt_end or gmt_start:
            if not gmt_end:
                gmt_end=datetime.datetime.now().strftime('%Y-%m-%d')
            if not gmt_start:
                gmt_start=(datetime.datetime.now()-datetime.timedelta(days=30)).strftime('%Y-%m-%d')
            new_gmt_end = (
                        datetime.datetime.strptime(gmt_end.strip(), '%Y-%m-%d') - datetime.timedelta(days=1)).strftime(
                '%Y-%m-%d')
            gmt_time = gmt_start.strip() + '-' + new_gmt_end.strip()
            objs_exists=t_erp_aliexpress_activation_rate_overview.objects.filter(gmt_time=gmt_time).exists()
            redis_name = 'ali_activation_rate__{}'.format(gmt_time)
            ra = redis_aliexprss()
            ra_query = ra.hgetall_data(redis_name)
            if not objs_exists or not ra_query:
                self.main(gmt_start,gmt_end)
            searchList.update({'gmt_time__exact':gmt_time})
        else:
            qs=qs.filter(gmt_time__isnull=True,updatetime=datetime.datetime.now())
            if not qs.exists():
                qs=qs.filter(gmt_time__isnull=True)

        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    sl[k] = v
        if sl is not None:
            # try:
            qs = qs.filter(**sl)
        return qs
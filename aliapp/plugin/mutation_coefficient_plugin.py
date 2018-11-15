#-*-coding:utf-8-*-
from xadmin.views import BaseAdminPlugin
from django.template import loader
import datetime
from aliapp.models import v_erp_aliexpress_mutation_coefficient
from aliapp.Redis_connect import redis_aliexprss
import json
class mutation_coefficient_plugin(BaseAdminPlugin):
    mutation_coefficient_flag=False

    def init_request(self, *args, **kwargs):
        return bool(self.mutation_coefficient_flag)

    def get_data(self):
        ra=redis_aliexprss()

        weekday = datetime.datetime.weekday(datetime.datetime.now())
        last_week = datetime.datetime.now().isocalendar()[1] - 1
        redis_name = 'ali_mutation_coefficient_{}'.format(last_week)

        if weekday!=5:
            redis_data = ra.hgetall_data(redis_name)
            if redis_data and redis_data.get('category'):
                return redis_data
        objs=v_erp_aliexpress_mutation_coefficient.objects.filter(week=last_week).values('product_id','wow_sales','wow_rate','cata_zh','shopName','sales','lastweek_sales','submitter')

        top_sales={}
        top_wow_rate={}
        top_wow_sales={}
        shopname_dict={}
        category_dict={}
        submitter_dict={}
        for obj in objs:
            product_id=int(obj['product_id'])
            wow_sales=int(obj['wow_sales'])
            wow_rate=float(obj['wow_rate'])
            shopName=obj['shopName']
            category=obj['cata_zh']
            sales=int(obj['sales'])
            lastweek_sales = int(obj['lastweek_sales'])
            if lastweek_sales>=10:
                top_wow_rate[product_id]=wow_rate
            top_sales[product_id]=sales
            top_wow_sales[product_id]=wow_sales
            submitter=obj['submitter']

            if not isinstance(shopname_dict.get(shopName,None),dict):
                shopname_dict[shopName]={'sales':0,'lastweek_sales':0}
            shopname_dict[shopName]['sales']+=sales
            shopname_dict[shopName]['lastweek_sales'] += lastweek_sales

            if not isinstance(category_dict.get(category,None),dict):
                category_dict[category]={'sales':0,'lastweek_sales':0}
            category_dict[category]['sales']+=sales
            category_dict[category]['lastweek_sales'] += lastweek_sales

            if not isinstance(submitter_dict.get(submitter,None),dict):
                submitter_dict[submitter]={'sales':0,'lastweek_sales':0}
            submitter_dict[submitter]['sales']+=sales
            submitter_dict[submitter]['lastweek_sales'] += lastweek_sales

        for submitter in submitter_dict:
            lastweek_sales=submitter_dict[submitter]['lastweek_sales']
            sales=submitter_dict[submitter]['sales']
            if lastweek_sales>0:
                submitter_dict[submitter]['wow_rate'] = round((sales-lastweek_sales)*100.0/lastweek_sales,1)
            else:
                submitter_dict[submitter]['wow_rate'] = sales* 100.0

        for category in category_dict:
            lastweek_sales=category_dict[category]['lastweek_sales']
            sales=category_dict[category]['sales']
            if lastweek_sales>0:
                category_dict[category]['wow_rate'] = round((sales-lastweek_sales)*100.0/lastweek_sales,1)
            else:
                category_dict[category]['wow_rate'] = sales* 100.0

        top20sales=sorted(top_sales.items(),key=lambda item:item[1],reverse=True)[:20]  #上周销量前二十
        top20wow_sales=sorted(top_wow_sales.items(),key=lambda item:item[1],reverse=True)[:20] #上周环比销量增加前二十
        top20wow_rate=sorted(top_wow_rate.items(),key=lambda item:item[1],reverse=True)[:20]  #上周环比销量增加率前二十
        result={'submitter':json.dumps(submitter_dict),'category':json.dumps(category_dict),
                'shopname':json.dumps(shopname_dict),'topsales':json.dumps(top20sales),
                'topwow_sales':json.dumps(top20wow_sales),'topwow_rate':json.dumps(top20wow_rate),'week':last_week}
        ra.set_data(redis_name, result)
        ra.redis_conn.expire(redis_name, 604800)
        return result

    def block_search_cata_nav(self,context, nodes):
        nodes.append(loader.render_to_string('mutation_coefficient_echarts.html',self.get_data()))

#-*-coding:utf-8-*-
from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.template import RequestContext
from aliapp.models import t_erp_aliexpress_activation_rate
import json
import datetime
from aliapp.Redis_connect import redis_aliexprss
class activation_rate_plugin(BaseAdminPlugin):
    activation_rate_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.activation_rate_flag)


    def Getdata(self):
        request=self.request
        gmt_start=request.GET.get('gmt_start','')
        gmt_end=request.GET.get('gmt_end','')


        ra = redis_aliexprss()
        if not gmt_start and not gmt_end:
            rate_data = ra.hgetall_data('ali_activation_rate__{}'.format(datetime.datetime.now().strftime('%Y-%m-%d')))
        else:
            if not gmt_end:
                gmt_end=datetime.datetime.now().strftime('%Y-%m-%d')
            if not gmt_start:
                gmt_start=(datetime.datetime.now()-datetime.timedelta(days=30)).strftime('%Y-%m-%d')
            new_gmt_end = (
                    datetime.datetime.strptime(gmt_end.strip(), '%Y-%m-%d') - datetime.timedelta(days=1)).strftime(
                '%Y-%m-%d')
            gmt_time = gmt_start.strip() + '-' + new_gmt_end.strip()
            rate_data=ra.hgetall_data('ali_activation_rate__{}'.format(gmt_time))
            tdate=rate_data.get('tdate')
            new_tdate=int(''.join(tdate.split('-')))
            rate_data['tdate']=new_tdate
        return rate_data


    def block_search_cata_nav(self,context, nodes):
        nodes.append(loader.render_to_string('activation_rate_echarts.html',self.Getdata()))


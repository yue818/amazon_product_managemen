#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_report_sales_clothingsystem_chart_Plugin.py
 @time: 2018-04-09 10:29
"""

from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.db import connection
import json
from brick.function.week_and_date import *
from datetime import datetime


class t_report_sales_clothingsystem_chart_Plugin(BaseAdminPlugin):

    sales_clothingsystem_chart = False

    def init_request(self, *args, **kwargs):
        return bool(self.sales_clothingsystem_chart)

    def _get_timename(self, tt, cate):
        format = {'day': '%Y-%m-%d', 'week': '%Y-%W', 'month': '%Y-%m'}
        t1 = tt.split('-')
        tt = datetime(year=int(t1[0]), month=int(t1[1]), day=int(t1[2]))

        return tt.strftime(format[cate])

    def get_para(self, parastr):
        parastr = parastr.replace(' ', '')
        parastr = parastr[parastr.find('?') + 1:]
        parastr = parastr.split('&')
        try:
            para = {y[0]: y[1] for y in map(lambda x: x.split('='), parastr)}
        except Exception, ex:
            para = {}

        if 'cate' not in para:
            para['cate'] = 'day'

        conv = {'day': '1', 'week': '2', 'month': '3'}
        wherestr = ' Where TimeType=%s' % conv[para['cate']]
        for k, v in para.items():
            if k == 'TimeNameStart':
                wherestr += """ and TimeName>='%s'""" % self._get_timename(v, para['cate'])
            elif k == 'TimeNameEnd':
                wherestr += """ and TimeName<='%s'""" % self._get_timename(v, para['cate'])
            elif k == 'ShopName':
                wherestr += "and ShopName like '%s%%'" % v
            elif k in ('PlatformName', 'ProductID', 'MainSKU', 'ShopName', 'SalesVolume'):
                wherestr += """ and %s='%s'""" % (k, v)

        return wherestr

    def block_search_cata_nav(self, context, nodes):
        sourceURL = str(context['request']).split("'")[1]
        wherestr = self.get_para(sourceURL)

        date_data = []
        sales_data = []
        tiflag = [(1, u'每日销售量'), (2, u'每周销售量'), (3, u'每月销售量')]
        tmp = [a.split('=')[1] for a in wherestr.split() if 'TimeType' in a][0]
        flag, title = tiflag[int(tmp)-1]

        cur = connection.cursor()
        sql = '''select TimeName,sum(SalesVolume) as SalesVolume
                             from t_report_sales_clothingsystem
                             %s 
                             group by TimeName order by 1 desc limit 30''' % (wherestr,)

        cur.execute(sql)
        infos = cur.fetchall()
        cur.close()
        for info in infos:
            date_data.append(info[0])
            sales_data.append(int(info[1]))

        date_data.reverse()
        sales_data.reverse()

        context = {
            'flag': flag,
            'title': title,
            'date_data': json.dumps(date_data),
            'sales_data': sales_data
        }

        nodes.append(loader.render_to_string('t_report_sales_clothingsystem_chart.html', context))
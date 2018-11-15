#-*-coding:utf-8-*-

from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.contrib import messages
from django.db import connection
from skuapp.table.t_amazon_pro_comment import t_amazon_pro_comment
import json
import datetime


class t_amazon_comment_analy_Plugin(BaseAdminPlugin):
    comment_report = False

    def init_request(self, *args, **kwargs):
        return bool(self.comment_report)

    def getdata(self, param):
        data = {}

        sql_total = '''SELECT star,count(star)as count from t_amazon_pro_comment where asin='%s' group by star ORDER BY star DESC'''

        sql_color = '''select color, count(if(star=5.0,1,null)) as s5,count(if(star=4.0,1,null)) as s4,count(if(star=3.0,1,null)) as s3,count(if(star=2.0,1,null)) as s2,count(if(star=1.0,1,null)) as s1,
                       count(1) as s from t_amazon_pro_comment where asin='%s' group by color ORDER BY s DESC;'''

        sql_si = "select DISTINCT si from t_amazon_pro_comment where asin='%s'"

        sql_si_color ='''select color, %s, count(1) as s from t_amazon_pro_comment where asin='%s' group by color ORDER BY s DESC;'''

        query_sql_total = (sql_total % param['asin'])
        query_sql_color = (sql_color % param['asin'])
        query_sql_size = (sql_si % param['asin'])

        # messages.info(self.request, u'query_sql:%s.'%query_sql)
        cursor = connection.cursor()
        # 总星统计
        cursor.execute(query_sql_total)
        data1 = cursor.fetchall()
        data['data1'] = list(data1)
        if not data['data1']:
            return data['data1']

        # 颜色星级统计
        cursor.execute(query_sql_color)
        data2 = cursor.fetchall()
        if data2[0][0] != '':
            data['data2'] = list(data2)
        else:
            data['data2'] = []

        # 颜色，尺寸统计
        cursor.execute(query_sql_size)
        size = cursor.fetchall()
        silist = []
        if size[0][0] != '':
            data['data3'] = list(size)
            for info in size:
                silist.append(info[0])
        else:
            data['data3'] = []


        if silist:
            cntlist = ','.join(["count( if (si='%s', 1, null)) as '%s'" % (si, si) for si in silist])
            query_sql_size_color = (sql_si_color % (cntlist, param['asin']))
            cursor.execute(query_sql_size_color)
            data4 = cursor.fetchall()
            data['data4'] = list(data4)
        else:
            data['data4'] = []

        cursor.close()
        return data

    def block_search_cata_nav(self, context, nodes):

        request = self.request
        param = {}
        param['asin'] = request.GET.get('asin', '')
        if param['asin'] != '':
            data = self.getdata(param)

            if data:
                title = u'asin号为%s的评价星级总览' % (param['asin'],)

                context = {
                    'title': title,
                    'total': json.dumps(data['data1']),
                    'color': json.dumps(data['data2']),
                    'size': json.dumps(data['data3']),
                    'size_color': json.dumps(data['data4']),
                }

            else:
                messages.error(request, u'无相关数据, 请检查查询条件.')


            nodes.append(loader.render_to_string('t_amazon_comment_analy.html', context))
        else:
            nodes.append(loader.render_to_string('t_amazon_comment_analy.html',{
                    'total': json.dumps([]),
                    'color': json.dumps([]),
                    'size': json.dumps([]),
                }))



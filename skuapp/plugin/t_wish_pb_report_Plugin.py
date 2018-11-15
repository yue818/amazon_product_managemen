#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_wish_pb_report_Plugin.py
 @time: 2018-06-19 13:18
"""
from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.contrib import messages
from django.db import connection
import json
import datetime


class t_wish_pb_report_Plugin(BaseAdminPlugin):
    wishpb_report = False

    def init_request(self, *args, **kwargs):
        return bool(self.wishpb_report)

    def get_Begday(self, vdate, datatype):

        if datatype == 'week':
            t_date = datetime.datetime.strptime(vdate, '%Y-%m-%d')
            dayOfWeek = t_date.weekday()  # weekday() 返回的是0-6是星期一到星期日 Monday Sunday
            to_day = t_date - datetime.timedelta(days=dayOfWeek)
            to_day = to_day.strftime('%Y-%m-%d')
        elif datatype == 'month':
            to_day = vdate[:8]+'01'
        else:
            to_day = vdate

        return to_day

    def get_Endday(self, vdate, datatype):

        if datatype == 'week':
            t_date = datetime.datetime.strptime(vdate, '%Y-%m-%d')-datetime.timedelta(days=1)
            dayOfWeek = t_date.weekday()
            to_day = t_date + datetime.timedelta(days=6 - dayOfWeek)
            to_day = to_day.strftime('%Y-%m-%d')
        elif datatype == 'month':
            t_date = datetime.datetime.strptime(vdate, '%Y-%m-%d')-datetime.timedelta(days=1)
            if t_date.month == 12:
                to_day = vdate[:8] + '31'
            else:
                to_day = datetime.date(t_date.year, t_date.month + 1, 1) - datetime.timedelta(1)
                to_day = to_day.strftime('%Y-%m-%d')
        else:
            to_day = vdate

        return to_day

    def getdata(self, param):

        sql_day = '''select date_format(p_date,'%%Y-%%m-%%d') as p_date,sum(spend) as spend,sum(gmv) as gmv,
        ifnull(round(sum(spend)/sum(gmv)*100,2),if(sum(spend)=0,0,500)) as aass
        from v_t_wish_pb_report
        %s
        group by p_date
        order by 1 '''

        sql_week = '''select 
        CONCAT_WS('~',date_sub(p_date,INTERVAL weekday(p_date) DAY),date_sub(p_date,INTERVAL weekday(p_date)-6 DAY)) as p_date,
        sum(spend) as spend,sum(gmv) as gmv,ifnull(round(sum(spend)/sum(gmv)*100,2),if(sum(spend)=0,0,500)) as aass
        from v_t_wish_pb_report
        %s
        group by date_format(p_date,'%%Y-%%u')
        order by 1 '''

        sql_month = '''select date_format(p_date,'%%Y-%%m') as p_date,sum(spend) as spend,sum(gmv) as gmv,
        ifnull(round(sum(spend)/sum(gmv)*100,2),if(sum(spend)=0,0,500)) as aass
        from v_t_wish_pb_report
        %s
        group by date_format(p_date,'%%Y-%%m')
        order by 1 '''

        query = ''
        if param['createuser'] != '':
            query = " where createuser = '%s'" % param['createuser']
            if param['pdate_Start'] != '':
                query += " and p_date>='%s'" % param['pdate_Start']
            if param['pdate_End'] != '':
                query += " and p_date<='%s'" % param['pdate_End']
        elif param['pdate_Start'] != '':
            query = " where p_date>='%s'" % param['pdate_Start']
            if param['pdate_End'] != '':
                query += " and p_date<='%s'" % param['pdate_End']
        elif param['pdate_End'] != '':
            query = " where p_date<='%s'" % param['pdate_End']

        if param['datatype'] == 'week':
            query_sql = (sql_week % query)
        elif param['datatype'] == 'month':
            query_sql = (sql_month % query)
        else:
            query_sql = (sql_day % query)

        # messages.info(self.request, u'query_sql:%s.'%query_sql)
        cursor = connection.cursor()
        cursor.execute(query_sql)
        data = cursor.fetchall()
        cursor.close()

        return data

    def block_search_cata_nav(self, context, nodes):

        request = self.request
        param = {}
        param['createuser'] = request.GET.get('createuser', '')
        param['datatype'] = request.GET.get('datatype', '')
        param['pdate_Start'] = request.GET.get('pdate_Start', '')
        param['pdate_End'] = request.GET.get('pdate_End', '')

        if param['pdate_Start'] != '':
            param['pdate_Start'] = self.get_Begday(param['pdate_Start'], param['datatype'])
        if param['pdate_End'] != '':
            param['pdate_End'] = self.get_Endday(param['pdate_End'], param['datatype'])

        data = self.getdata(param)

        datelist = []
        spend = []
        gmv = []
        s_gmv = []
        title = u'活动AS统计报表'
        # p_date,spend,gmv,aass
        if len(data) > 0:
            for info in data:
                datelist.append(info[0])
                spend.append(float(info[1]))
                gmv.append(float(info[2]))
                s_gmv.append(float(info[3]))

            trans = {'month': u'每月', 'week': u'每周', '': u'每日'}
            if param['datatype'] == 'week':
                title = u'%s活动AS统计报表(%s~%s)' % (trans[param['datatype']], min(datelist)[:10], max(datelist)[11:],)
            else:
                title = u'%s活动AS统计报表(%s~%s)' % (trans[param['datatype']], min(datelist), max(datelist),)
        else:
            messages.error(request, u'无相关数据, 请检查查询条件.')

        subtitle = u'广告创建人:%s'%(u'全部' if param['createuser']=='' else param['createuser'])

        context = {
            'title': title,
            'subtitle': subtitle,
            'datelist': json.dumps(datelist),
            's_gmv': s_gmv,
            'spend': spend,
            'gmv': gmv
        }

        nodes.append(loader.render_to_string('t_wish_pb_report.html', context))
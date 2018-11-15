#-*-coding:utf-8-*-


"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: amazon_advertising_report_Plugin.py
 @time: 2018/8/27 19:44
"""   
from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.contrib import messages
from django.db import connection
import json
from skuapp.table.t_template_amazon_advertising_business_report import t_template_amazon_advertising_business_report

class amazon_advertising_report_Plugin(BaseAdminPlugin):
    amazon_advertising_report_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.amazon_advertising_report_flag)

    def getdata(self, param):

        sql_day = '''select date_format(advertising_business_date,'%%Y-%%m-%%d') as p_date,sum(ordered_sales) as ordered_sales,
        sum(ordered_count) as ordered_count,sum(cost) as cost, ifnull(round(sum(cost)/sum(sales_count)*100,2),0.00) as ACoS,
        ifnull(round(sum(cost)/sum(ordered_sales)*100,2),0.00) as AS_amazon,
        ifnull(round(sum(orders_count)/sum(ordered_count)*100,2),0.00) as AT_amazon
        from t_template_amazon_advertising_business_report
        %s
        group by p_date
        order by 1 '''

        sql_week = '''select 
        CONCAT_WS('~',date_sub(advertising_business_date,INTERVAL weekday(advertising_business_date) DAY),date_sub(advertising_business_date,INTERVAL weekday(advertising_business_date)-6 DAY)) as advertising_business_date,
        sum(ordered_sales) as ordered_sales,
        sum(ordered_count) as ordered_count,sum(cost) as cost, ifnull(round(sum(cost)/sum(sales_count)*100,2),0.00) as ACoS,
        ifnull(round(sum(cost)/sum(ordered_sales)*100,2),0.00) as AS_amazon,
        ifnull(round(sum(orders_count)/sum(ordered_count)*100,2),0.00) as AT_amazon
        from t_template_amazon_advertising_business_report
        %s
        group by date_format(advertising_business_date,'%%Y-%%u')
        order by 1 '''

        sql_month = '''select date_format(advertising_business_date,'%%Y-%%m') as advertising_business_date,sum(ordered_sales) as ordered_sales,
        sum(ordered_count) as ordered_count,sum(cost) as cost, ifnull(round(sum(cost)/sum(sales_count)*100,2),0.00) as ACoS,
        ifnull(round(sum(cost)/sum(ordered_sales)*100,2),0.00) as AS_amazon,
        ifnull(round(sum(orders_count)/sum(ordered_count)*100,2),0.00) as AT_amazon
        from t_template_amazon_advertising_business_report
        %s
        group by date_format(advertising_business_date,'%%Y-%%m')
        order by 1 '''

        query = " where ShopSKU = '%s' and shopname = '%s'" % (param['ShopSKU'], param['shopname'])
        # if param['createuser'] != '':
        #     query = " where createuser = '%s'" % param['createuser']
        #     if param['pdate_Start'] != '':
        #         query += " and p_date>='%s'" % param['pdate_Start']
        #     if param['pdate_End'] != '':
        #         query += " and p_date<='%s'" % param['pdate_End']
        if param['pdate_Start'] != '':
            query += " and advertising_business_date>='%s'" % param['pdate_Start']

        if param['pdate_End'] != '':
            query += " and advertising_business_date<='%s'" % param['pdate_End']

        if param['uploadtime_End'] != '':
            query += " and upload_time<='%s'" % param['uploadtime_End']

        if param['datatype'] == 'week':
            query_sql = (sql_week % query)
        elif param['datatype'] == 'month':
            query_sql = (sql_month % query)
        else:
            query_sql = (sql_day % query)

        #messages.info(self.request, u'query_sql:%s.'%query_sql)
        cursor = connection.cursor()
        cursor.execute(query_sql)
        data = cursor.fetchall()
        cursor.close()

        return data

    def block_search_cata_nav(self, context, nodes):
        request = self.request
        param = {}
        is_single = request.GET.get('is_single', '')
        param['datatype'] = request.GET.get('datatype', '')
        param['ShopSKU'] = request.GET.get('_p_ShopSKU', '')
        param['shopname'] = request.GET.get('_p_shopname', '')
        param['pdate_Start'] = request.GET.get('pdate_Start', '')
        param['pdate_End'] = request.GET.get('pdate_End', '')
        param['uploadtime_End'] = request.GET.get('uploadtime_End', '')
        if is_single and is_single == '1':
            # advertising_business_reports = t_template_amazon_advertising_business_report.objects.filter(shopname__exact=shopname,ShopSKU__exact=ShopSKU).order_by('advertising_business_date')
            data = self.getdata(param)
            datelist = []
            ordered_sales = []
            ordered_count = []
            ACoS = []
            AS_amazon = []
            AT_amazon = []
            cost = []
            title = u'活动AS统计报表'
            if len(data) > 0:
                for info in data:
                    datelist.append(info[0])
                    ordered_sales.append(float(info[1]))
                    ordered_count.append(int(info[2]))
                    cost.append(float(info[3]))
                    ACoS.append(float(info[4]))
                    AS_amazon.append(float(info[5]))
                    AT_amazon.append(float(info[6]))

                trans = {'month': u'每月', 'week': u'每周', 'day': u'每日'}
                if param['datatype'] == 'week':
                    title = u'%s活动AS统计报表(%s~%s)' % (trans[param['datatype']], min(datelist)[:10], max(datelist)[11:],)
                else:
                    title = u'%s活动AS统计报表(%s~%s)' % (trans[param['datatype']], min(datelist), max(datelist),)
            else:
                messages.error(request, u'无相关数据, 请检查查询条件.')

            subtitle = u'广告创建人:全部'
            to_url = request.get_full_path().replace("&datatype="+param['datatype'], '')
            context = {
                'title': title,
                'subtitle': subtitle,
                'datelist': json.dumps(datelist),
                'ACoS': ACoS,
                'ordered_sales': ordered_sales,
                'ordered_count': ordered_count,
                'cost': cost,
                'AS_amazon': AS_amazon,
                'AT_amazon': AT_amazon,
                'datatype': param['datatype'],
                'to_url': to_url
            }

            nodes.append(loader.render_to_string('amazon_advertising_report_Plugin.html',
                                                 context))
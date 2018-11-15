# -*- coding: utf-8 -*-
"""
 @desc:
 @author: changyang
 @site:
 @software: PyCharm
 @file: sales_show_byplatformnamePlugin.py
 @time: 2018-04-12 20:08
"""
from __future__ import division
from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.db import connection
import json
from django.contrib import messages
from datetime import datetime
import datetime as datime


class sales_show_byplatformnamePlugin(BaseAdminPlugin):

    sales_show_PlatformName_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.sales_show_PlatformName_flag)

    def get_media(self, media):
        media.add_js([self.static('xadmin/js/xadmin.plugin.button.color.js')])
        return media

    def showplatfrom(self,PlatformName):

        cursor = connection.cursor()
        cursor.execute(
            "select OrderDay,SalesVolume from t_report_sales_daily_byPlatform WHERE PlatformName=%s and OrderDay>=%s ORDER by OrderDay DESC;",
            (PlatformName, self.begdate, ))
        objs = cursor.fetchall()
        cursor.close()

        daylist = []
        saleslist = []
        for obj in objs:
            daylist.append('%s' % obj[0].strftime('%Y%m%d'))
            saleslist.append(int(obj[1]))

        for i, d in enumerate(self.daylista):
            if d not in daylist:
                saleslist.insert(i, 0)
                daylist.insert(i, d)

        sales7ordery = [round(sum(saleslist[i:i + 7]) / len(saleslist[i:i + 7]), 2) for i in range(len(saleslist))]
        percent = round(sum(saleslist)/self.salestotal, 4)*100 if self.salestotal else 0
        title = u'%s平台日销量|%s%%' % (PlatformName, str(percent))

        sales7ordery.reverse()
        daylist.reverse()
        saleslist.reverse()

        return (title, daylist, saleslist, sales7ordery)

    def block_search_cata_nav(self, context, nodes):

        title99 = u'全平台日销量|100%'
        x = datetime.now() + datime.timedelta(days=-90)
        self.begdate = x.strftime('%Y-%m-%d')

        cursor = connection.cursor()
        cursor.execute(
            "select OrderDay,sum(SalesVolume) as SalesVolume from t_report_sales_daily_byPlatform where OrderDay>='%s' group by OrderDay order by OrderDay DESC;"% self.begdate, )
        objs = cursor.fetchall()
        cursor.close()

        self.daylista = []
        daylist99 = []
        saleslist99 = []
        for obj in objs:
            y = '%s' % obj[0].strftime('%Y%m%d')
            daylist99.append(y)
            self.daylista.append(y)
            saleslist99.append(int(obj[1]))

        self.salestotal = sum(saleslist99)
        sales7ordery99 = [round(sum(saleslist99[i:i + 7]) / len(saleslist99[i:i + 7]), 2) for i in range(len(saleslist99))]

        sales7ordery99.reverse()
        daylist99.reverse()
        saleslist99.reverse()

        # 单平台计算
        cursor = connection.cursor()
        cursor.execute(
            "SELECT PlatformName,sum(SalesVolume) AS SalesVolume FROM t_report_sales_daily_byPlatform WHERE PlatformName !='' GROUP BY PlatformName ORDER BY SalesVolume DESC;", )
        obj1s = cursor.fetchall()
        cursor.close()
        
        i = 0
        title = []
        daylist = []
        saleslist = []
        sales7ordery = []
        for i in range(0, len(obj1s)):
            #messages.error(self.request, '%s*****%s'% (i, obj1s[i][0]))
            a, b, c, d = self.showplatfrom(obj1s[i][0])
            title.append(a)
            daylist.append(b)
            saleslist.append(c)
            sales7ordery.append(d)
            #messages.error(self.request, '%s*****%s****%s' % (title[i],daylist[i],saleslist[i]))


        returndata = {'title': title99, 'daylist': json.dumps(daylist99), 'saleslist': json.dumps(saleslist99), 'sales7ordery': json.dumps(sales7ordery99),
                      'title0': title[0], 'daylist0': json.dumps(daylist[0]), 'saleslist0': json.dumps(saleslist[0]), 'sales7ordery0': json.dumps(sales7ordery[0]),
                      'title1': title[1], 'daylist1': json.dumps(daylist[1]), 'saleslist1': json.dumps(saleslist[1]), 'sales7ordery1': json.dumps(sales7ordery[1]),
                      'title2': title[2], 'daylist2': json.dumps(daylist[2]), 'saleslist2': json.dumps(saleslist[2]), 'sales7ordery2': json.dumps(sales7ordery[2]),
                      'title3': title[3], 'daylist3': json.dumps(daylist[3]), 'saleslist3': json.dumps(saleslist[3]), 'sales7ordery3': json.dumps(sales7ordery[3]),
                      'title4': title[4], 'daylist4': json.dumps(daylist[4]), 'saleslist4': json.dumps(saleslist[4]), 'sales7ordery4': json.dumps(sales7ordery[4]),
                      'title5': title[5], 'daylist5': json.dumps(daylist[5]), 'saleslist5': json.dumps(saleslist[5]), 'sales7ordery5': json.dumps(sales7ordery[5]),
                      'title6': title[6], 'daylist6': json.dumps(daylist[6]), 'saleslist6': json.dumps(saleslist[6]), 'sales7ordery6': json.dumps(sales7ordery[6]),
                      'title7': title[7], 'daylist7': json.dumps(daylist[7]), 'saleslist7': json.dumps(saleslist[7]), 'sales7ordery7': json.dumps(sales7ordery[7]),
                      'title8': title[8], 'daylist8': json.dumps(daylist[8]), 'saleslist8': json.dumps(saleslist[8]), 'sales7ordery8': json.dumps(sales7ordery[8]),
                      'title9': title[9], 'daylist9': json.dumps(daylist[9]), 'saleslist9': json.dumps(saleslist[9]), 'sales7ordery9': json.dumps(sales7ordery[9]),
                      'title10': title[10], 'daylist10': json.dumps(daylist[10]), 'saleslist10': json.dumps(saleslist[10]), 'sales7ordery10': json.dumps(sales7ordery[10]),
                      'title11': title[11], 'daylist11': json.dumps(daylist[11]), 'saleslist11': json.dumps(saleslist[11]), 'sales7ordery11': json.dumps(sales7ordery[11]),
                      'title12': title[12], 'daylist12': json.dumps(daylist[12]), 'saleslist12': json.dumps(saleslist[12]), 'sales7ordery12': json.dumps(sales7ordery[12]),
                      'title13': title[13], 'daylist13': json.dumps(daylist[13]), 'saleslist13': json.dumps(saleslist[13]), 'sales7ordery13': json.dumps(sales7ordery[13]),
                      'title14': title[14], 'daylist14': json.dumps(daylist[14]), 'saleslist14': json.dumps(saleslist[14]), 'sales7ordery14': json.dumps(sales7ordery[14]),
                      'title15': title[15], 'daylist15': json.dumps(daylist[15]), 'saleslist15': json.dumps(saleslist[15]), 'sales7ordery15': json.dumps(sales7ordery[15]),
                      'title16': title[16], 'daylist16': json.dumps(daylist[16]), 'saleslist16': json.dumps(saleslist[16]), 'sales7ordery16': json.dumps(sales7ordery[16]),
                      'title17': title[17], 'daylist17': json.dumps(daylist[17]), 'saleslist17': json.dumps(saleslist[17]), 'sales7ordery17': json.dumps(sales7ordery[17]),
                      'title18': title[18], 'daylist18': json.dumps(daylist[18]), 'saleslist18': json.dumps(saleslist[18]), 'sales7ordery18': json.dumps(sales7ordery[18]),
                      'title19': title[19], 'daylist19': json.dumps(daylist[19]), 'saleslist19': json.dumps(saleslist[19]), 'sales7ordery19': json.dumps(sales7ordery[19]),
                      }

        nodes.append(loader.render_to_string('sales_show1.html', returndata))
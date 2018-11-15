#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime

from django_redis import get_redis_connection
from django.core.management.base import BaseCommand

from brick.db.dbconnect import run
from brick.classredis.classsku import classsku
from aliexpress_app.table.t_aliexpress_online_info import t_aliexpress_online_info
from aliexpress_app.table.t_aliexpress_online_info_detail import t_aliexpress_online_info_detail


class Command(BaseCommand):

    def handle(self, *args, **options):
        start_time = datetime.datetime.now()
        db_res = run({})
        if db_res['errorcode'] == -1:
            print "result['errortext']: %s" % db_res['errortext']
            return
        db_conn = db_res['db_conn']
        redis_conn = get_redis_connection(alias='product')

        classsku_obj = classsku(db_cnxn=db_conn, redis_cnxn=redis_conn)
        num = t_aliexpress_online_info.objects.filter(Status='1').count()
        num = int(num / 1000) + 1
        for i in range(num):
            start_num = i * 1000
            i += 1
            end_num = i * 1000
            print '==============handle start num range, start_num: %s, end_num: %s' % (start_num, end_num)
            products_info = t_aliexpress_online_info.objects.filter(Status='1')[start_num:end_num]
            for i in products_info:
                pro_detail = t_aliexpress_online_info_detail.objects.filter(ProductID=i.ProductID)
                # if i.SKU:
                #     pro_detail = i.SKU.split(',')
                # else:
                #     continue
                weight_list = list()
                for j in pro_detail:
                    sku = j.SKU
                    # sku = j
                    weight = classsku_obj.get_weight_by_sku(sku)
                    j.Weight = weight
                    j.save()
                    weight_list.append(weight)
                weight_list.sort()
                min_weight = weight_list[0]
                i.Weight = min_weight
                i.save()
            print '==============handle over num range, start_num: %s, end_num: %s' % (start_num, end_num)
            # if i > 5:
            # break
        end_time = datetime.datetime.now()
        print 'handle time: %s' % (end_time - start_time).total_seconds()

# -*- coding: utf-8 -*-

import re
import datetime
import logging

from django.db.models import Q
from django.db import connection
from brick.table.t_large_small_corresponding_cate import t_large_small_corresponding_cate

from joom_app.table.t_online_info_joom import t_online_info_joom

logger = logging.getLogger('django')


def get_joom_cate(MainSKU):
    t_large_small_corresponding_cate_obj = t_large_small_corresponding_cate(connection)
    # MainSKU,大类，小类  不在更新了
    MainSKULargeCate = None
    MainSKUSmallCate = None

    mlist = []
    if MainSKU:
        mlist = re.findall(r'[0-9]+|[a-z]+|[A-Z|]+|[-]', MainSKU)
    if len(mlist) >= 1:
        MainSKUSmallCate = mlist[0]  # 小类
        lResult = t_large_small_corresponding_cate_obj.getLargeClassBySmallClass(MainSKUSmallCate)
        if lResult['code'] == 1:
            MainSKULargeCate = lResult['largecode']

    return MainSKULargeCate, MainSKUSmallCate


def update_joom_cate():
    # all_num = t_online_info_joom.objects.all().count()
    all_num = t_online_info_joom.objects.filter(Q(MainSKULargeCate__isnull=True) | Q(MainSKUSmallCate__isnull=True)).count()
    logger.debug("[x] All JOOM NUMBERS: %s" % all_num)
    cursor = connection.cursor()
    start_time = datetime.datetime.now()
    logger.debug("[.] Start Time: %s" % start_time)

    for i in range(all_num / 10000 + 1):
        range_start_time = datetime.datetime.now()
        logger.debug("[.] Range Start Time: %s" % range_start_time)
        start_num = i * 10000
        end_num = (i + 1) * 10000
        logger.debug("[.] BEGAIN <==> Start Num: %s, End Num: %s" % (start_num, end_num))
        # joom_infos = t_online_info_joom.objects.all().values('id', 'MainSKU')[start_num:end_num]
        joom_infos = t_online_info_joom.objects.filter(
            Q(MainSKULargeCate__isnull=True) | Q(MainSKUSmallCate__isnull=True)
        ).values('id', 'MainSKU')[start_num:end_num]
        joom_cate_list = list()
        kwargs = dict()
        kwargs['cursor'] = cursor
        kwargs['datas'] = list()
        for info in joom_infos:
            MainSKU = info['MainSKU']
            obj_id = info['id']
            MainSKULargeCate, MainSKUSmallCate = get_joom_cate(MainSKU)
            joom_tuple = (MainSKULargeCate, MainSKUSmallCate, obj_id)
            joom_cate_list.append(joom_tuple)
        kwargs['datas'] = joom_cate_list
        excute_update_joom_cate(**kwargs)
        logger.debug("[.] OVER <==> Start Num: %s, End Num: %s" % (start_num, end_num))
        range_end_time = datetime.datetime.now()
        logger.debug("[.] Range End Time: %s" % range_end_time)
        logger.debug("[.] Range Handle Time: %s" % (range_end_time - range_start_time).total_seconds())

    end_time = datetime.datetime.now()
    logger.debug("[.] End Time: %s" % end_time)
    logger.debug("[.] ALL Handle Time: %s" % (end_time - start_time).total_seconds())

    cursor.close()


def excute_update_joom_cate(**kw):
    cursor = kw['cursor']
    sql = "UPDATE t_online_info_joom SET MainSKULargeCate=%s, MainSKUSmallCate=%s WHERE id=%s"
    cursor.executemany(sql, kw['datas'])
    cursor.execute('commit')

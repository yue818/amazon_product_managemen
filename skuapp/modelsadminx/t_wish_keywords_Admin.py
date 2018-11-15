# -*- coding: utf-8 -*-
from django.contrib import messages
from Project.settings import *
import errno
import datetime
import oss2
import os


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5 (except OSError, exc: for Python <2.5)
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


class t_wish_keywords_Admin(object):
    search_box_flag = True
    wish_key_words = True

    list_display = ('id', 'keyword', 'poArrRate', 'preCompe', 'proBid', 'rank', 'updateTime')

    actions = ['to_excel',]

    def to_excel(self, request, queryset):
        from xlwt import *
        DOWNLOAD_KEY_WORDS = 'wishkeywords'

        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s' % (path))

        w = Workbook()
        sheet = w.add_sheet('t_wish_keywords')

        sheet.write(0, 0, u'关键词')
        sheet.write(0, 1, u'预计可能达到')
        sheet.write(0, 2, u'预估竞争度')

        # 写数据
        row = 0
        for qs in queryset:
            row += 1
            column = 0
            sheet.write(row, column, qs.keyword)
            column += 1
            sheet.write(row, column, qs.poArrRate)
            column += 1
            sheet.write(row, column, qs.preCompe)
        filename = request.user.username + '_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
        w.save(path + '/' + filename)
        os.popen(r'chmod 777 %s' % (path + '/' + filename))

        # 上传oss对象
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT_OUT, BUCKETNAME_XLS)
        bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
        # 删除现有的
        for object_info in oss2.ObjectIterator(bucket,prefix='%s/%s_' % (DOWNLOAD_KEY_WORDS, request.user.username)):
            bucket.delete_object(object_info.key)
        bucket.put_object(u'%s/%s' % (DOWNLOAD_KEY_WORDS, filename), open(path + '/' + filename))

        messages.success(request, u'%s%s.%s/%s/%s' % (PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, DOWNLOAD_KEY_WORDS,filename) + u':成功导出,可点击Download下载到本地............................。')
    to_excel.short_description = u'导出EXCEL'



    def get_list_queryset(self, ):
        request = self.request
        qs = super(t_wish_keywords_Admin, self).get_list_queryset()
        keyword = request.GET.get('keyword', '')
        poArrRate = request.GET.get('poArrRate', '')
        preCompe = request.GET.get('preCompe', '')
        proBid = request.GET.get('proBid', '')
        rank_Str = request.GET.get('rankStart', '')
        rank_End = request.GET.get('rankEnd', '')
        updateTime_Str = request.GET.get('updateTimeStart', '')
        updateTime_End = request.GET.get('updateTimeEnd', '')

        searchList = {'keyword__contains': keyword,'poArrRate__exact': poArrRate,'preCompe__exact': preCompe,
                      'proBid__exact': proBid, 'rank__gte': rank_Str, 'rank__lt': rank_End,
                      'updateTime__gte': updateTime_Str, 'updateTime__lt': updateTime_End,}
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'Please enter the correct content!')
        return qs


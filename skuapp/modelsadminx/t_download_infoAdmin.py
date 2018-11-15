# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from django.db.models  import Q
from Project.settings import *
from django_redis import get_redis_connection
from django.contrib import messages
redis_db = get_redis_connection(alias='product')

class t_download_info_Admin(object):
    def show_url(self,obj):
        rt = ''
        if obj.appname is not None and obj.appname.strip() != '':
            download_address = '%s%s.%s/%s'%(PREFIX,BUCKETNAME_DOWNLOAD,ENDPOINT_OUT,obj.appname)
            rt='<a href="%s">%s</a>'%(download_address,download_address)
        return mark_safe(rt)
    show_url.short_description='下载地址'


    def show_progress_bar(self, obj):
        rt = '1/1'
        key_exists = redis_db.hget(obj.appname, 'total')
        if key_exists is not None:
            total = key_exists
            processed = redis_db.hget(obj.appname, 'processed')
            rt = '%s/%s' % (processed, total)
        if obj.Datasource == 't_use_productsku_apply_for_shopsku' and (obj.appname is None or obj.appname == ''):
            rt = '1/2'
        elif obj.Datasource == 't_use_productsku_apply_for_shopsku' and obj.appname is not None and obj.appname.strip() != '' :
            rt = '2/2'
        return mark_safe(rt)

    show_progress_bar.short_description = u'下载进度'
	
    list_display=('id','appname','abbreviation','show_url', 'show_progress_bar','updatetime')
    search_fields=('appname','abbreviation') 

    def get_list_queryset(self, ):
        request = self.request
        qs = super(t_download_info_Admin, self).get_list_queryset()
        if request.user.is_superuser:
            return qs
        return qs.filter(Q(Belonger=request.user.username)|Q(Belonger__isnull=True))




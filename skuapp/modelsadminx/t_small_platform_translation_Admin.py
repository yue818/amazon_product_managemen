# -*- coding: utf-8 -*-
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
import urllib, urllib2, sys
import logging
from django.contrib import messages
import csv
from .t_product_Admin import *
from django.utils.safestring import mark_safe
from datetime import datetime

class t_small_platform_translation_Admin(object):
    # http://fancyqube-download.oss-cn-shanghai.aliyuncs.com/Translated/20171105131332_29.csv
    def show_download_link(self,obj):
        rt = ''
        if obj.Has_been_translated is not None and obj.Has_been_translated.strip() != '':
            rt = u'<a href = "http://fancyqube-download.oss-cn-shanghai.aliyuncs.com/Translated/%s">%s</a>'%(obj.Has_been_translated,obj.Has_been_translated)
        return mark_safe(rt)
    show_download_link.short_description = u'已翻译'
    
    list_display=('id','Waiting_for_translation','FromLanguage','show_download_link','ToLanguage','Submiter','SubmitTime','StartTime','ExportTime','Process',)
    list_filter=('FromLanguage','ToLanguage','Submiter','SubmitTime','ExportTime','Process',)
    search_fields=('id','Waiting_for_translation','FromLanguage','Has_been_translated','ToLanguage','Submiter','Process',)

    fields =  ('Waiting_for_translation','FromLanguage','ToLanguage',)
    
    form_layout = (
        Fieldset(u'请导入需要翻译的文件(.CSV)',
                Row('FromLanguage','ToLanguage',),
                Row('Waiting_for_translation',),
                css_class = 'unsort '
                ))
                
    def save_models(self):
        obj     = self.new_obj
        request = self.request
        logger  = logging.getLogger('sourceDns.webdns.views')
        
        ACCESS_KEY_ID= 'LTAIH6IHuMj6Fq2h'
        ACCESS_KEY_SECRET = 'N5eWsbw8qBkMfPREkgF2JnTsDASelM'
        ENDPOINT = 'vpc100-oss-cn-shanghai.aliyuncs.com'
        ENDPOINT_OUT = 'oss-cn-shanghai.aliyuncs.com'
        BUCKETNAME_CSV  = 'fancyqube-xls'
        
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_CSV)
        try :
            if obj.Waiting_for_translation is not None and str(obj.Waiting_for_translation).strip() !='' and obj.FromLanguage is not None and obj.FromLanguage.strip() != '' and obj.ToLanguage is not None and obj.ToLanguage.strip() != '':
                bucket.put_object(u'%s/%s'%('translation',str(obj.Waiting_for_translation)),obj.Waiting_for_translation)
                
                obj.Waiting_for_translation = str(obj.Waiting_for_translation)
                obj.Submiter   = request.user.first_name
                obj.SubmitTime = datetime.now()
                obj.Process    = '0'
                obj.save()
                
            else:
                messages.error(request,u'请导入需要翻译的文件，并选择好需要翻译的语言以及需要翻译成的语言！！！')

        except Exception,ex :
            logger.error('%s============================%s'%(Exception,ex))
            messages.error(request,'%s============================%s'%(Exception,ex))
    
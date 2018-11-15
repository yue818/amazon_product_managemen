# -*- coding: utf-8 -*-
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
import urllib, urllib2, sys
from skuapp.table.t_translation import t_translation
from datetime import datetime
import logging
from django.contrib import messages
import csv
from .t_product_Admin import *

class t_translation_Admin(object):
    downloadxls = True
    list_display=('id','Translated','Title','Description','FromLanguage','Submiter','SubmitTime','Title_ed','Description_ed','ToLanguage','ExportTime',)
    list_filter=('Submiter','SubmitTime','FromLanguage','ToLanguage','ExportTime',)
    search_fields=('id','Translated','Title','Description','Submiter','Title_ed','Description_ed',)

    fields =  ('Translated','FromLanguage','ToLanguage',)
    
    form_layout = (
        Fieldset(u'请导入需要翻译的文件(.CSV)',
                Row('Translated','FromLanguage','ToLanguage',),
                css_class = 'unsort '
                ))
                
                
    actions = ['to_translation_excel',]
    
    def to_translation_excel(self,request,queryset):
        from xlwt import *
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        #if not os.path.exists(path):
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s'%(MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s'%(path))

        w = Workbook()
        sheet = w.add_sheet(u'翻译后数据')

        sheet.write(0,0,u'标题')
        sheet.write(0,1,u'描述')

        #写数据
        id_list = []
        row = 0
        for qs in queryset:
            
            row = row + 1
            column = 0
            sheet.write(row,column,qs.Title_ed)

            column = column + 1
            Description = u'<ul><li>' + qs.Description_ed.replace('\n','</li><li>') + '</li></ul>'
            sheet.write(row,column,Description)
            id_list.append(qs.id)
                
        filename = request.user.username + '_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
        w.save(path + '/' +  filename)
        os.popen(r'chmod 777 %s'%(path + '/' +  filename))
        
        #上传oss对象
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT,BUCKETNAME_XLS)
        bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
        
        queryset.filter(id__in=id_list).update( ExportTime= datetime.now())
        
        #删除现有的
        for  object_info in oss2.ObjectIterator(bucket,prefix='%s/%s_'%(request.user.username,request.user.username)):
            bucket.delete_object(object_info.key)
        bucket.put_object(u'%s/%s'%(request.user.username,filename),open(path + '/' +  filename))

        messages.error(request,u'%s%s.%s/%s/%s'%(PREFIX,BUCKETNAME_XLS,ENDPOINT_OUT,request.user.username,filename) + u':成功导出,可点击Download下载到本地............................。' )
    to_translation_excel.short_description = u'导出Excel'
                
                
    
    def to_translate (self,FromLanguage,Translated,ToLanguage):
        host = 'http://jisuzxfy.market.alicloudapi.com'
        path = '/translate/translate'
        method = 'GET'
        appcode = '2cd4ea81891e4118bee6ecfae5d0f2f1'
        querys = 'from=' + FromLanguage + '&' + '%s'%(urllib.urlencode({'text':Translated})) + '&to=' + ToLanguage + '&type=google'
                #'from=    en              &     %s                                                     &to=     es           &type=google'
        bodys = {}
        url = host + path + '?' + querys

        print '---------%s'%url
        request = urllib2.Request(url)
        request.add_header('Authorization', 'APPCODE ' + appcode)
        response = urllib2.urlopen(request)
        # {"status":"0","msg":"ok","result":{"type":"google","from":"en","to":"es","text":"This is the test","result":"Esta es la prueba"}}
        _content = eval(response.read())
        result = ''
        if _content['status'] == '0' and _content['msg'] == 'ok':
            result = _content['result'].get('result','')
        return result
    
    def save_models(self):
        obj     = self.new_obj
        request = self.request
        logger  = logging.getLogger('sourceDns.webdns.views')
        try :
            if obj.Translated is not None and str(obj.Translated).strip() !='' and obj.FromLanguage is not None and obj.FromLanguage.strip() != '' and obj.ToLanguage is not None and obj.ToLanguage.strip() != '':
                i = 0
                INSERT_INTO = []
                for row in csv.reader(obj.Translated):#obj.Status本身就是16进制字节流，直接reader
                    if i < 1:
                        i = i + 1
                        continue
                    i = i + 1
                    if (row[0].decode("GBK")).strip() != '' and (row[1].decode("GBK")).strip() != '':
                        title       = self.to_translate(obj.FromLanguage,row[0].decode("GBK"),obj.ToLanguage)
                        description = self.to_translate(obj.FromLanguage,row[1].decode("GBK"),obj.ToLanguage)
                        logger.error('%s=========%s'%(title,description))
                    
                        INSERT_INTO.append(t_translation(Translated=obj.Translated,Title=row[0].decode("GBK"),Description=row[1].decode("GBK"),
                        Submiter=request.user.first_name,SubmitTime=datetime.now(),Title_ed=title,Description_ed=description,FromLanguage=obj.FromLanguage,ToLanguage=obj.ToLanguage
                        ))
                        logger.error('------====%s'%(INSERT_INTO))
                t_translation.objects.bulk_create(INSERT_INTO)
                                            
            else:
                messages.error(request,u'请导入需要翻译的文件，并选择好需要翻译的语言以及需要翻译成的语言！！！')

        except Exception,ex :
            logger.error('%s============================%s'%(Exception,ex))
            messages.error(request,'%s============================%s'%(Exception,ex))
    
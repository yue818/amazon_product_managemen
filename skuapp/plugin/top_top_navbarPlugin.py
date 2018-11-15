# -*- coding: utf-8 -*-
import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView, ModelFormAdminView, CommAdminView, BaseAdminView
import logging

from django.db import transaction, connection
from django.template import loader
from datetime import datetime, timedelta
from skuapp.table.model_name import *
from skuapp.table.t_help import *
from skuapp.table.t_history import *
# import datetime as datime
import urllib2
import bs4
from bs4 import BeautifulSoup
from django.contrib import messages

from skuapp.table.v_UMG import *
class top_top_navbarPlugin(BaseAdminPlugin):
    top_top_navbar = True
    #objs = None
    help_objs = None
    history=None

    def init_request(self, *args, **kwargs):
        return bool(self.top_top_navbar)
    def block_top_top_navbar(self, context, nodes):
        # logger = logging.getLogger('sourceDns.webdns.views')
        # messages.error(self.request, 'top1-------%s' % datetime.now())
        Dic = {'add':'增加','update':'更新','?status=mycreate&Flow_Status=TC,SH,CL,NYZ,YZ': '我的创建', '?status=mytask&Flow_Status=TC,SH,CL,NYZ,YZ': '我的任务', '?status=myjoin&Flow_Status=TC,SH,CL,NYZ,YZ': '我的参与', '?status=all&Flow_Status=TC,SH,CL,NYZ,YZ': '全部任务', '?status=taskout&Flow_Status=TC,SH,CL,NYZ,YZ': '逾期任务','t_task_trunk':'主线任务'}


        ownobject_name= ('t_product_survey_ing','t_product_develop_ing','t_product_enquiry_ing','t_product_build_ing','t_product_art_ing',
                  't_product_publish_ed','t_product_photograph','t_sys_shopdef','t_product_wait_publish',
                  't_product_art_ed',
                )
        import itertools
        if context['user'].is_superuser:
            all_group2_objs = model_name.objects.values('group2','group2_seq').order_by('group2_seq').distinct()
            all_group1_objs =  model_name.objects.values('group2','group1','group1_seq').order_by('group1_seq').distinct()
            all_model_objs  =  model_name.objects.values('app_label','group1','model','model_name','table_name').order_by('Serial').distinct()
            records_count = 0
            cursor = connection.cursor()
            for all_model_obj in all_model_objs:
                if all_model_obj['table_name'] is not None and all_model_obj['table_name'].strip() != '':
                    try:
                        try:
                            sql = "select * from  tri_db." + all_model_obj['table_name']
                            cursor.execute(sql)
                        except:
                            sql = "select count(*) from  " + all_model_obj['table_name']
                            cursor.execute(sql)

                        count = cursor.fetchone()
                        records_count = count[0]
                        all_model_obj['model_name'] = u'%s(%s)' % (all_model_obj['model_name'], records_count)
                    except:
                        continue
            cursor.close()

        else:
            all_group2_objs =  v_UMG.objects.values('group2','group2_seq').filter(user_id=context['user'].id).order_by('group2_seq').distinct()
            all_group1_objs =  v_UMG.objects.values('group2','group1','group1_seq').filter(user_id=context['user'].id).order_by('group1_seq').distinct()
            all_model_objs  =  v_UMG.objects.values('app_label','group1','model','model_name','table_name').filter(user_id=context['user'].id).order_by('Serial').distinct()
            records_count = 0
            cursor = connection.cursor()
            for all_model_obj in all_model_objs:
                if all_model_obj['table_name'] is not None and all_model_obj['table_name'].strip() != '':
                    try:
                        try:
                            if all_model_obj['model'] in ownobject_name:
                                sql = "select count(*) from  " + all_model_obj['table_name']
                                sql += "  where StaffID = \'%s\' ;" % (context['user'].username,)
                            else:
                                sql = "select * from  tri_db." + all_model_obj['table_name']
                            cursor.execute(sql)
                        except:
                            sql = "select count(*) from  " + all_model_obj['table_name']
                            cursor.execute(sql)

                        count = cursor.fetchone()
                        records_count = count[0]
                        all_model_obj['model_name'] = u'%s(%s)' % (all_model_obj['model_name'], records_count)
                    except:
                        continue

            cursor.close()

        StepID_objs = u'%s'%context['request']
        AAA = StepID_objs.split('/')
        User_url= u'%s'%context['request']
        B=User_url.split("'")[-2]
        URL='http://online.fancyqube.net'+B

        if len(B.split('/')[-1])!=0:
            D=Dic.get(B.split('/')[-1],' ')
        else:
            D=Dic.get(B.split('/')[-2],' ')

        try:
           url_unfall_name=B.split('/')[4]
        except:
              url_unfall_name=B.split('/')[2]

        user_name=context['request'].user.username
        Mode_Name = model_name.objects.filter(model=url_unfall_name)
        if len(Mode_Name)==0:
            Mode_Name=D+url_unfall_name
        else:
            Mode_Name=D+Mode_Name[0].model_name

        try:
            u_url=t_history.objects.filter(username=context['request'].user.username).latest('url_time').url_names
        except:
            u_url=None

        if u_url==Mode_Name: 
             obj_time=t_history.objects.filter(username=context['request'].user.username).latest('url_time')
             obj_time.url_time=datetime.now()
             obj_time.user_urls=URL
             obj_time.save()
        else:
            t_history.objects.create(username=user_name, url_time=datetime.now(),
                                     url_names=Mode_Name, user_urls=URL,)

        help_objs = t_help.objects.values('HelpContent').filter(StepID=AAA[-2])
        historys=t_history.objects.values('username','user_url','url_time','url_names','user_urls').filter(username=context['request'].user.username).order_by('-url_time')

        t_history.objects.filter(url_time__lt=(datetime.now()+timedelta(days=-7))).delete()

        cursor = connection.cursor()
        cursor.execute("select model,url from mm_bookmarks WHERE userid=%s and username=%s;",
                       (self.request.user.id,self.request.user.first_name))
        objs = cursor.fetchall()
        cursor.close()
        objdict = {}
        for obj in objs:
            objdict[obj[0]] = obj[1]

        for all_model_obj in all_model_objs:
            if objdict.has_key(all_model_obj['model'].split('/?')[0]):
                if all_model_obj['model'].find('/?') != -1:
                    all_model_obj['model'] = all_model_obj['model'] + '&' + objdict[all_model_obj['model'].split('/?')[0]].split('?')[-1]
                if all_model_obj['model'].find('/?') == -1:
                    all_model_obj['model'] = all_model_obj['model'] + objdict[all_model_obj['model']]
        count = 0
        nodes.append(loader.render_to_string('top_top_navbar.html', {'all_group2_objs':all_group2_objs,'all_group1_objs':all_group1_objs,
                                                            'all_model_objs':all_model_objs,'help_objs':help_objs,'history':historys,}))



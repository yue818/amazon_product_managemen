#-*-coding:utf-8-*-
from xadmin.views import BaseAdminPlugin
from django.template import loader
from skuapp.table.t_templet_amazon_collection_box import *
from skuapp.table.t_templet_amazon_wait_upload import *
from skuapp.table.t_templet_amazon_upload_result import *
from skuapp.table.t_online_info_amazon_listing import *
from skuapp.table.t_templet_amazon_recycle_bin import *
from skuapp.table.t_templet_amazon_upload_fail import *
from skuapp.table.t_templet_amazon_upload_result_lose_pic import *
"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: site_left_menu_Plugin.py
 @time: 2018/2/28 8:53
"""   
class site_left_menu_Plugin(BaseAdminPlugin):
    site_left_menu_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.site_left_menu_flag)

    def block_left_navbar(self, context, nodes):
        #createUser = self.request.user.username,
        if self.request.user.is_superuser:
            t_templet_amazon_collection_box_count = t_templet_amazon_collection_box.objects.filter(status='1').values(
                'id').count()
            t_templet_amazon_wait_upload_count_no = t_templet_amazon_wait_upload.objects.filter(status='NO').values(
                'id').count()
            t_templet_amazon_upload_result_upload_count = t_templet_amazon_upload_result.objects.filter(
                status='UPLOAD').values('id').count()
            t_templet_amazon_wait_upload_count_failed = t_templet_amazon_upload_fail.objects.filter(is_display='1').values('id').count()
            t_templet_amazon_wait_upload_count_success = t_templet_amazon_upload_result.objects.filter(
                status='SUCCESS').values('id').count()
            t_templet_amazon_recycle_bin_count = t_templet_amazon_recycle_bin.objects.filter(status='1').values('id').count()
            t_templet_amazon_upload_result_lose_pic_count = t_templet_amazon_upload_result_lose_pic.objects.exclude(is_display='0').values('id').count()
        else:
            t_templet_amazon_collection_box_count = t_templet_amazon_collection_box.objects.filter(status='1',createUser = self.request.user.username).values(
                'id').count()
            t_templet_amazon_wait_upload_count_no = t_templet_amazon_wait_upload.objects.filter(status='NO',createUser = self.request.user.username).values(
                'id').count()
            t_templet_amazon_upload_result_upload_count = t_templet_amazon_upload_result.objects.filter(
                status='UPLOAD',createUser = self.request.user.username).values('id').count()
            t_templet_amazon_wait_upload_count_failed = t_templet_amazon_upload_fail.objects.filter(is_display='1',createUser = self.request.user.username).values('id').count()
            t_templet_amazon_wait_upload_count_success = t_templet_amazon_upload_result.objects.filter(
                status='SUCCESS',createUser = self.request.user.username).values('id').count()
            t_templet_amazon_recycle_bin_count = t_templet_amazon_recycle_bin.objects.filter(status='1', createUser = self.request.user.username).values('id').count()
            t_templet_amazon_upload_result_lose_pic_count = t_templet_amazon_upload_result_lose_pic.objects.filter(createUser = self.request.user.username).exclude(is_display='0').values(
                'id').count()



        sourceURL = str(context['request']).split("'")[1]
        title_list = [{'title': u'草稿箱', 'selected': '0'}, {'title': u'待发布产品', 'selected': '0'},{'title': u'回收站', 'selected': '0'}, {'title': u'在线产品', 'selected': '0'}]
        test_list = [{'url': '/Project/admin/skuapp/t_templet_amazon_collection_box/', 'value': u'Amazon草稿箱('+str(t_templet_amazon_collection_box_count)+')',
                      'title': u'草稿箱', 'selected': '0'},
                     {'url': '/Project/admin/skuapp/t_templet_amazon_wait_upload/?_p_status=NO', 'value': u'待发布('+str(t_templet_amazon_wait_upload_count_no)+')',
                      'title': u'待发布产品', 'selected': '0'},
                     {'url': '/Project/admin/skuapp/t_templet_amazon_upload_result/?_p_status=UPLOAD', 'value': u'发布中('+str(t_templet_amazon_upload_result_upload_count)+')',
                      'title': u'待发布产品', 'selected': '0'},
                     {'url': '/Project/admin/skuapp/t_templet_amazon_upload_fail/', 'value': u'发布失败('+str(t_templet_amazon_wait_upload_count_failed)+')',
                      'title': u'待发布产品', 'selected': '0'},
                     {'url': '/Project/admin/skuapp/t_templet_amazon_upload_result/?_p_status=SUCCESS','value': u'发布成功('+str(t_templet_amazon_wait_upload_count_success)+')',
                      'title': u'待发布产品', 'selected': '0'},
                     {'url': '/Project/admin/skuapp/t_templet_amazon_upload_result_lose_pic/',
                      'value': u'发布后图片缺失(' + str(t_templet_amazon_upload_result_lose_pic_count) + ')',
                      'title': u'待发布产品', 'selected': '0'},
                     {'url': '/Project/admin/skuapp/t_templet_amazon_recycle_bin/',
                      'value': u'回收站(' + str(t_templet_amazon_recycle_bin_count) + ')',
                      'title': u'回收站', 'selected': '0'},
                     {'url': '/Project/admin/skuapp/t_online_info_amazon_listing/', 'value': u'所有分类',
                      'title': u'在线产品', 'selected': '0'},]
        title = ''
        flag = 0
        new_sourceURL = sourceURL
        if '?p=' in sourceURL:
            new_sourceURL = sourceURL.replace('?p=', '?')
            if '&' in new_sourceURL:
                new_sourceURL = new_sourceURL.split('?')[0] + '?' + new_sourceURL.split('?')[1].split('&')[1]
            else:
                new_sourceURL = new_sourceURL.split('?')[0]
        for tl in test_list:
            to_url = tl['url']
            if to_url != new_sourceURL:
                if '?' not in tl['url']:
                    to_url = to_url + '?'
            if to_url in new_sourceURL:
                title = tl['title']
                tl['selected'] = '1'
                flag = 1
        if title:
            for titleout in title_list:
                if titleout['title'] == title:
                    titleout['selected'] = '1'
        if flag == 1:
            nodes.append(loader.render_to_string('site_left_menu_Plugin.html',
                                                 {'title_list': title_list, 'test_list': test_list, 'sourceURL': sourceURL}))

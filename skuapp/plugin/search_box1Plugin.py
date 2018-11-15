# -*- coding: utf-8 -*-

from xadmin.views import BaseAdminPlugin
from django.template import loader
from urllib import unquote
#from django.template import RequestContext
from skuapp.table.search_box_plugin import *
from Project.settings import *
from django.contrib import messages
class search_box1Plugin(BaseAdminPlugin):
    search_box1_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.search_box1_flag)

    def getParam(self, searchKey, searchParams,newUrl):
        searchParam = ''
        for each in searchParams:
            paramf = each.split("=")[0]
            if searchKey == paramf:
                uu = each + '&'
                newUrl = newUrl.replace(uu, '')
                searchParam = unquote(each.split('=')[1])
        paramList = {'newUrl': newUrl, 'searchParam': searchParam}
        return  paramList

    def block_search_cata_nav(self, context, nodes):

        request = self.request
        GET = request.GET
        Cate1 = GET.get('cate1', '0')
        Cate2 = GET.get('cate2', '0')
        Cate3 = GET.get('cate3', '0')

        category = {u'1.男款T恤': u'男款T恤', u'2.女款T恤': u'女款T恤', u'3.男款背心': u'男款背心',
                    u'4.女款背心': u'女款背心', u'5.男款长裤': u'男款长裤', u'6.女款长裤': u'女款长裤',
                    u'7.男款短裤': u'男款短裤', u'8.女款短裤': u'女款短裤', u'9.半身裙': u'半身裙',
                    u'10.连衣裙': u'连衣裙', u'11.连体衣': u'连体衣', u'12.泳装': u'泳装'}

        selectDict = {}
        selectDict['cate1'] = Cate1
        selectDict['cate2'] = Cate2
        selectDict['cate3'] = Cate3
        if Cate1 == '0':
            selectDict['text1'] = '全部分类'
        else:
            selectDict['text1'] = category[Cate1]
        if Cate2 == '0':
            selectDict['text2'] = '全部'
        else:
            selectDict['text2'] = ''
        if Cate3 == '0':
            selectDict['text3'] = '全部'
        else:
            selectDict['text3'] = ''




        sourceURL = str(context['request']).split("'")[1]

        # begin 用于控制选择页数后，再按过滤条件查询(查询结果如果小于之前选择业务报错)
        strUrl = sourceURL
        if "?" in sourceURL:
            mainUrl = sourceURL.split("?")[0]
            strUrl = mainUrl + '?'
            conditionsAllParam = sourceURL.split("?")[1]
            conditionsParam = conditionsAllParam.split("&")
            for row in conditionsParam:
                if len(row) >= 2 and row[:2] == 'p=':
                    continue
                strUrl = strUrl + row + '&'
            if strUrl[-1] == "&":
                sourceURL = strUrl[:-1]
        # end

        StepID_objs = u'%s' % context['request']
        AAA = self.model._meta.model_name

        config_path = STATIC_ROOT + 'search_box_plugin_config.txt'
        cfile = open(config_path)
        lines = cfile.readlines()
        inputs1 = []
        inputs_id1 = []
        inputs2 = []
        inputs_id2 = []
        for line in lines:
            if line is None or line.strip() == '':
                continue
            if '{' not in line:
                continue
            search_dict = eval(line)
            if search_dict['model_name'] == AAA:
                if search_dict['inputs'] == '1':
                    if  '{' in search_dict['defult_value1']:
                        search_dict['defult_value1'] = eval(search_dict['defult_value1'])
                    inputs1.append(search_dict)
                    inputs_id1.append(search_dict['id'])
                else:
                    inputs2.append(search_dict)
                    inputs_id2.append(search_dict['id'])

        newUrl = sourceURL
        if "?" in sourceURL:
            newUrl += "&"
            condition = newUrl.split("?")[1]
            conditions = condition.split("&")
            count_params = []
            count_filters = []
            for condition_i in conditions:
                if condition_i is not None and condition_i.strip() != '':
                    count_filters.append(condition_i)
                    count_params.append(condition_i.split("=")[0])

            for input1 in inputs1:
                if input1['urlname1'] in count_params:
                    paramList1 = self.getParam(input1['urlname1'], count_filters, newUrl)
                    newUrl = paramList1['newUrl']
                    input1['value1'] = paramList1['searchParam']
            for input2 in inputs2:
                if input2['urlname1'] in count_params or input2['urlname2'] in count_params:
                    paramList1 = self.getParam(input2['urlname1'], count_filters, newUrl)
                    newUrl = paramList1['newUrl']
                    input2['value1'] = paramList1['searchParam']
                    if input2['urlname2'] is not None and input2['urlname2'].strip() != '':
                        paramList2 = self.getParam(input2['urlname2'], count_filters, newUrl)
                        newUrl = paramList2['newUrl']
                        input2['value2'] = paramList2['searchParam']
                        if input2['isDate']==1:
                            import datetime
                            endTime = paramList2['searchParam']
                            if endTime is not None and endTime.strip() != '':
                                date_time = datetime.datetime.strptime(endTime, '%Y-%m-%d')
                                date_time = date_time + datetime.timedelta(days = -1)
                                input2['value2'] = str(date_time).split(' ')[0]

            if 'cate1' in count_params:
                paramList1 = self.getParam('cate1', count_filters, newUrl)
                newUrl = paramList1['newUrl']
            if 'cate2' in count_params:
                paramList1 = self.getParam('cate2', count_filters, newUrl)
                newUrl = paramList1['newUrl']
            if 'cate3' in count_params:
                paramList1 = self.getParam('cate3', count_filters, newUrl)
                newUrl = paramList1['newUrl']
        else:
            newUrl += "?"

        nodes.append(loader.render_to_string('search_box1_plugin.html',
                                             {'newUrl': newUrl, 'inputs1': inputs1, 'inputs2': inputs2,
                                              'inputs_id1': inputs_id1, 'inputs_id2': inputs_id2,
                                              'category':category,'choice':selectDict}))
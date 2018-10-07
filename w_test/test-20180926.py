# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: test-20180926.py
 @time: 2018/9/26 15:33
"""


def SKUNodeInfo(self, obj):
    try:
        rt = ''
        from skuapp.table.t_cloth_factory_dispatch_needpurchase import t_cloth_factory_dispatch_needpurchase
        t_cloth_factory_dispatch_needpurchase_objs = t_cloth_factory_dispatch_needpurchase.objects.filter(SKU=obj.SKU).filter(
            Q(currentState=8) | Q(currentState=16) | Q(currentState=18) | Q(currentState=20) | Q(currentState=22) | Q(currentState=24)).order_by('-currentState').values_list('productNumbers',
                                                                                                                                                                              'currentState',
                                                                                                                                                                              'genPurchaseDate',
                                                                                                                                                                              'applyDate', 'auditDate',
                                                                                                                                                                              'speModifyDate',
                                                                                                                                                                              'disPatchDate',
                                                                                                                                                                              'confirmDate',
                                                                                                                                                                              'closeDate',
                                                                                                                                                                              'completeNumbers')
        rt = u'<p style="width:200px;">'
        if len(t_cloth_factory_dispatch_needpurchase_objs) == 0:
            rt = rt + u'<strong>其他流程节点无该商品信息</strong><br>'
        else:
            rt = rt + u'<strong>其他流程信息(采购数量;完成数量;时间):</strong><br>'
            rt_4 = 0
            rt_8 = 0
            rt_16 = 0
            rt_20 = 0
            rt_24 = 0
            dt_4 = ''
            dt_8 = ''
            dt_16 = ''
            dt_20 = ''
            dt_24 = ''
            cm_22 = 0
            cm_24 = 0
            for rowObj in t_cloth_factory_dispatch_needpurchase_objs:
                ###'productNumbers','currentState','genPurchaseDate','applyDate','auditDate','speModifyDate','disPatchDate','confirmDate','closeDate','completeNumbers'
                if int(rowObj[1]) == 4 or int(rowObj[1]) == 6:
                    rt_4 += 1
                if int(rowObj[1]) == 8 and rowObj[0] is not None and int(rowObj[0]) != 0:
                    rt_8 += rowObj[0]
                    dt_8 = str(rowObj[3])[:10]
                if (int(rowObj[1]) == 16 or int(rowObj[1]) == 18) and rowObj[0] is not None and int(rowObj[0]) != 0:
                    rt_16 += rowObj[0]
                    dt_16 = str(rowObj[4])[:10] if rowObj[6] is not None else ''
                if (int(rowObj[1]) == 20 or int(rowObj[1]) == 22) and rowObj[0] is not None and int(rowObj[0]) != 0:
                    rt_20 += rowObj[0]
                    dt_20 = str(rowObj[6])[:10] if rowObj[6] is not None else ''
                    if rowObj[9] is not None and rowObj[9] != '':
                        cm_22 += int(rowObj[9])
                if int(rowObj[1]) == 24 and rowObj[0] is not None and int(rowObj[0]) != 0:
                    rt_24 += rowObj[0]
                    dt_24 = str(rowObj[7])[:10] if rowObj[6] is not None else ''
                    if rowObj[9] is not None and rowObj[9] != '':
                        cm_24 += int(rowObj[9])
            if rt_4 > 0:
                rt = rt + u'<strong>流程节点-采购计划:</strong>存在采购计划<br>'
            if rt_8 > 0:
                rt = rt + u'<strong>流程节点-采购计划审核:</strong>%s;%s <br>' % (str(rt_8), dt_8)
            if rt_16 > 0:
                rt = rt + u'<strong>流程节点-服装工厂排单:</strong>%s;%s <br>' % (str(rt_16), dt_16)
            if rt_20 > 0:
                rt = rt + u'<strong>流程节点-检验交付数量和单价:</strong>%s;%s;%s<br>' % (str(rt_20), str(cm_22), dt_20)
            if rt_24 > 0:
                rt = rt + u'<strong>流程节点-生产完成可建普源采购单:</strong>%s;%s;%s<br>' % (str(rt_24), str(cm_24), dt_24)
        rt = rt + u'</p>'
    except Exception as e:
        messages.info(self.request, obj.SKU + str(e))
        rt = ''
    return mark_safe(rt)


SKUNodeInfo.short_description = mark_safe(u'<p style="width:200px;color:#428bca;" align="center">流程节点信息</p>')

# coding=utf-8


from django.utils.safestring import mark_safe
from Project.settings import MEDIA_ROOT, ACCESS_KEY_ID, ACCESS_KEY_SECRET, ENDPOINT, BUCKETNAME_XLS, PREFIX, ENDPOINT_OUT
import oss2, os
from datetime import datetime
from django.contrib import messages
from skuapp.modelsadminx.t_product_Admin import mkdir_p


class t_product_quality_feedback_final_result_Admin(object):
    search_box_flag = True
    downloadxls = True

    def show_img(self, obj):
        rt = u'<img src="%s"  width="120" height="120"><style>img{cursor: pointer; transition: all 0.6s;} ' \
             u'img:hover{transform: scale(4);}</style>' % obj.Picture_1
        if obj.Picture_2 or obj.Picture_3 or obj.Picture_4 or obj.Picture_5:
            rt = u"%s<br><a id=pic_%s>全部图片</a><script>$('#pic_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan'," \
                 u"title:'全部图片',fix:false,shadeClose: true,maxmin:true,area:['800px','600px']," \
                 u"content:'/show_feedback_picture/?id=%s&page=final_result',});});</script>" % (rt, obj.id, obj.id, obj.id)
        return mark_safe(rt)
    show_img.short_description = u'<span style="color: #428bca">提交人图片</span>'

    def show_img_zjy(self, obj):
        rt = u'<img src="%s"  width="120" height="120"><style>img{cursor: pointer; transition: all 0.6s;} ' \
             u'img:hover{transform: scale(4);}</style>' % 1
        if obj.ZJY_Pic:
            pic_list = obj.ZJY_Pic.split('|')
            rt = u'<img src="%s"  width="120" height="120"><style>img{cursor: pointer; transition: all 0.6s;} ' \
                 u'img:hover{transform: scale(4);}</style>' % pic_list[0]
        rt = u"%s<br><a id=img_%s>全部图片</a><script>$('#img_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan'," \
             u"title:'全部图片',fix:false,shadeClose: true,maxmin:true,area:['800px','600px']," \
             u"content:'/feedback_zjy_picture/?id=%s&page=final_result',});});</script>" % (rt, obj.id, obj.id, obj.id)
        return mark_safe(rt)

    show_img_zjy.short_description = u'<span style="color: #428bca">质检员图片</span>'


    def show_submit(self, obj):
        rr = '<span>提交日期：%s</span><br><span>提交人：%s<span>' % (obj.SubmitTime, obj.Submitter)
        return mark_safe(rr)
    show_submit.short_description = u'<span style="color: #428bca">提交信息</span>'

    def show_detail(self, obj):
        detail_list = obj.Detail.split('\n')
        rr = ''
        for detail in detail_list:
            if rr == '':
                rr = '<span >%s</span>' % detail
            else:
                rr = '%s<br><span >%s</span>' % (rr, detail)
        return mark_safe(rr)
    show_detail.short_description = u'<span style="color: #428bca">具体反馈</span>'

    def show_product(self, obj):
        sku = u'<span>SKU：%s<span>' % obj.SKU
        plateform = u'<span>平台：%s<span>' % obj.Plateform
        order_id = u'<span>订单号：%s<span>' % obj.OrderID
        rr = u'%s<br>%s<br>%s' % (sku, plateform, order_id)
        return mark_safe(rr)
    show_product.short_description = u'<span style="color: #428bca">订单信息</span>'


    list_display = ('id', 'show_product', 'show_submit', 'show_img', 'show_img_zjy', 'ProblemType', 'show_detail',
                    'ZJY', 'ZJY_Note', 'CPZY', 'CPZY_Note', 'CGY', 'CGY_Note', 'CKY', 'CK_Note', 'ZJY_Final', 'Final_Note')
    list_display_links = ('',)
    actions = ['to_excel']


    def to_excel(self, request, queryset):
        problem_type = {'fch': u'仓储部-发错货', 'lfh': u'仓储部-漏发货', 'dh': u'仓储部-点货', 'zjwt': u'仓储部-质检问题',
                        'scj': u'仓储部-上错架', 'ccwt': u'产品部-尺寸问题', 'zlwt': u'产品部-质量问题',
                        'ybwt': u'产品部-预包问题', 'qq': u'侵权', 'cpyxj': u'产品已下架', 'qt': u'其它'}

        from xlwt import *
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s' % (path))

        w = Workbook()
        sheet = w.add_sheet('price_check_1')
        sheet.write(0, 0, u'SKU')
        sheet.write(0, 1, u'平台')
        sheet.write(0, 2, u'浦沅订单号')
        sheet.write(0, 3, u'提交人')
        sheet.write(0, 4, u'提交日期')
        sheet.write(0, 5, u'问题类型')
        sheet.write(0, 6, u'具体反馈')
        sheet.write(0, 7, u'产品专员')
        sheet.write(0, 8, u'产品专员备注')
        sheet.write(0, 9, u'采购员')
        sheet.write(0, 10, u'采购员备注')
        sheet.write(0, 11, u'质检员')
        sheet.write(0, 12, u'质检员备注')
        sheet.write(0, 13, u'仓库员')
        sheet.write(0, 14, u'仓库备注')
        sheet.write(0, 15, u'最终审核人')
        sheet.write(0, 16, u'最终备注')
        sheet.write(0, 17, u'图片一')
        sheet.write(0, 18, u'图片一')
        sheet.write(0, 19, u'图片一')
        sheet.write(0, 20, u'图片一')
        sheet.write(0, 21, u'图片一')

        # 写数据
        row = 0

        for qs in queryset:

            row = row + 1
            column = 0
            sheet.write(row, column, qs.SKU)

            column = column + 1
            sheet.write(row, column, qs.Plateform)

            column = column + 1
            sheet.write(row, column, qs.OrderID)

            column = column + 1
            sheet.write(row, column, qs.Submitter)

            column = column + 1
            sheet.write(row, column, str(qs.SubmitTime))

            column = column + 1
            sheet.write(row, column, problem_type[qs.ProblemType])

            column = column + 1
            sheet.write(row, column, qs.Detail)

            column = column + 1
            sheet.write(row, column, qs.CPZY)

            column = column + 1
            sheet.write(row, column, qs.CPZY_Note)

            column = column + 1
            sheet.write(row, column, qs.CGY)

            column = column + 1
            sheet.write(row, column, qs.CGY_Note)

            column = column + 1
            sheet.write(row, column, qs.ZJY)

            column = column + 1
            sheet.write(row, column, qs.ZJY_Note)

            column = column + 1
            sheet.write(row, column, qs.CKY)

            column = column + 1
            sheet.write(row, column, qs.CK_Note)

            column = column + 1
            sheet.write(row, column, qs.ZJY_Final)

            column = column + 1
            sheet.write(row, column, qs.Final_Note)

            column = column + 1
            sheet.write(row, column, str(qs.Picture_1))

            column = column + 1
            sheet.write(row, column, str(qs.Picture_2))

            column = column + 1
            sheet.write(row, column, str(qs.Picture_3))

            column = column + 1
            sheet.write(row, column, str(qs.Picture_4))

            column = column + 1
            sheet.write(row, column, str(qs.Picture_5))

        filename = request.user.username + '_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
        w.save(path + '/' + filename)
        os.popen(r'chmod 777 %s' % (path + '/' + filename))

        # 上传oss对象
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT, BUCKETNAME_XLS)
        bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
        # 删除现有的
        for object_info in oss2.ObjectIterator(bucket,
                                               prefix='%s/%s_' % (request.user.username, request.user.username)):
            bucket.delete_object(object_info.key)
        bucket.put_object(u'%s/%s' % (request.user.username, filename), open(path + '/' + filename))

        messages.error(request, u'%s%s.%s/%s/%s' % (PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, request.user.username,
                                                    filename) + u':成功导出,可点击Download下载到本地............................。')
    to_excel.short_description = u'导出EXCEL'


    def get_list_queryset(self):
        request = self.request
        qs = super(t_product_quality_feedback_final_result_Admin, self).get_list_queryset()

        OrderID = request.GET.get('OrderID', '')
        SKU = request.GET.get('SKU', '')
        Submitter = request.GET.get('Submitter', '')
        CPZY = request.GET.get('CPZY', '')
        CGY = request.GET.get('CGY', '')
        ZJY = request.GET.get('ZJY', '')
        CKY = request.GET.get('CKY', '')
        ZJY_Final = request.GET.get('ZJY_Final', '')
        ProblemType = request.GET.get('ProblemType', '')
        Plateform = request.GET.get('Plateform', '')
        time_start = request.GET.get('time_start', '')
        time_end = request.GET.get('time_end', '')
        clothing = request.GET.get('clothing', '')


        searchList = {'OrderID__exact': OrderID, 'SKU__exact': SKU, 'Submitter__exact': Submitter, 'CPZY__exact': CPZY,
                      'CGY__exact': CGY, 'ZJY__exact': ZJY, 'CKY__exact': CKY, 'ZJY_Final__exact': ZJY_Final,
                      'ProblemType__exact': ProblemType, 'Plateform__exact': Plateform,
                      'SubmitTime__gte': time_start, 'SubmitTime__lt': time_end, 'ClothingFlag': clothing
                    }
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    if k == 'ShopName__exact':
                        if v.find('Wish-') == -1:
                            v = 'Wish-' + v.zfill(4)
                    sl[k] = v
        if sl:
            qs = qs.filter(**sl)

        return qs
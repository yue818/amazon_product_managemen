# coding=utf-8


from aliapp.adminx import *
from skuapp.table.t_store_configuration_file import t_store_configuration_file

class t_erp_aliexpress_online_info_shelf_Admin(t_erp_aliexpress_online_info_Admin):

    actions = ['syn_data_by_ali_api_batch', 'enable_data_by_ali_api_batch', 'disable_data_by_ali_api_batch', ]
    list_per_page = 50

    def syn_data_by_ali_api_batch(self):
        pass
    syn_data_by_ali_api_batch.short_description = ''

    def enable_data_by_ali_api_batch(self):
        pass
    enable_data_by_ali_api_batch.short_description = ''

    def disable_data_by_ali_api_batch(self):
        pass
    disable_data_by_ali_api_batch.short_description = ''


    def show_child_sku(self,obj):
        rt = u'<table class="table table-condensed">' \
             u'<thead><tr><th></th>' \
             u'<th>商品SKU</th><th>商品状态</th>' \
             u'<th>店铺SKU</th><th>库存量</th><th>价格</th><th>折后价</th><th>利润率(%)</th>' \
             u'</tr>' \
             u'</thead><tbody>'
        sku_infos = json.loads(obj.product_skus)
        sku_info_list = sku_infos.get('aeop_ae_product_sku', '')
        infor = []
        shopsku_info_db = {}
        for sku_info in sku_info_list:
            if sku_info:
                shopsku = sku_info.get('sku_code', '')
                shopsku_info_db[shopsku] = {'sku_price': sku_info.get('sku_price', ''), 'ipm_sku_stock': sku_info.get('ipm_sku_stock', ''),
                                            'sku_discount_price': sku_info.get('sku_discount_price', '')}
                eachinfor = {}
                SKU=classshopskuobjs.getSKU(shopsku)
                if SKU is None:
                    eachinfor['SKU'] = None
                else:
                    eachinfor['SKU'] = SKU.split('*')[0]
                eachinfor['SKUKEY'] = ['NotInStore', 'GoodsStatus', 'Number', 'ReservationNum', 'CanSaleDay']
                eachinfor['ShopSKU'] = shopsku
                eachinfor['ShopSKUKEY'] = ['Quantity', 'Price', 'Shipping', 'Status']
                infor.append(eachinfor)
        # 这里调取redis数据
        sInfors = py_SynRedis_tables_obj.BatchReadRedis(infor)
        num = 0

        for a, sinfor in enumerate(sInfors):
            if sinfor['SKUKEY'][1] == '4':
                goodsstatus = u'停售'
            else:
                continue

            shop_sku = sinfor['ShopSKU'].replace('<', '&lt;').replace('>', '&gt;')
            sku_discount_price = shopsku_info_db[shop_sku]['sku_price']
            if shopsku_info_db[shop_sku]['sku_discount_price']:
                sku_discount_price = shopsku_info_db[shop_sku]['sku_discount_price']
            try:
                shopsku_info = shopsku_info_db[shop_sku]
                if shopsku_info['ipm_sku_stock'] <= 0:
                    continue

                sellingPrice = float(sku_discount_price)
                calculate_price_obj = calculate_price(str(sinfor['SKU']))
                profitrate_info = calculate_price_obj.calculate_profitRate(sellingPrice, platformCountryCode='ALIEXPRESS-RUS',
                                                                           DestinationCountryCode='US',category='non_ornament')
                profitrate = profitrate_info['profitRate']
            except:
                profitrate = u'故障'
            profit_id = str(sinfor['SKU']) + str(num)
            num += 1

            style = 'class ="danger"'

            rt = u'%s <tr %s><td><label><input type="checkbox" name="shopskucheck" id="%s_ywp_%s"></label></td>' \
                 u'<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td><a><span id="%s">%s</span></a></td></tr>' % \
                 (rt, style, obj.id, sinfor['ShopSKU'].replace('<', '&lt;').replace('>', '&gt;'),
                  sinfor['SKU'], goodsstatus,sinfor['ShopSKU'].replace('<', '&lt;').replace('>', '&gt;'),
                  shopsku_info['ipm_sku_stock'],
                  shopsku_info_db[shop_sku]['sku_price'], sku_discount_price, profit_id, profitrate,)
            rt = u"%s<script>$('#%s').on('click',function()" \
                 u"{layer.open({type:2,skin:'layui-layer-lan',title:'算价表'," \
                 u"fix:false,shadeClose: true,maxmin:true,area:['1300px','900px']," \
                 u"content:'/price_list/?SKU=%s&sellingPrice=%s&platformCountryCode=%s" \
                 u"&DestinationCountryCode=%s&category=%s',});});</script>" % (
                 rt, profit_id, sinfor['SKU'], sellingPrice, 'ALIEXPRESS-RUS', 'US', 'non_ornament')
        rt += '</tbody></table>'

        return mark_safe(rt)

    show_child_sku.short_description = mark_safe(u'<p align="center"style="color:#428bca;">变体详细信息</p>')


    def get_list_queryset(self,):
        """显示可显示的，自己本人的"""
        from skuapp.table.t_sys_staff_auth import t_sys_staff_auth
        flag = 0
        try:
            flag = t_sys_staff_auth.objects.filter(StaffID=self.request.user.username,urltable="t_erp_aliexpress_online_info").count()
        except:
            pass
        request = self.request
        qs = super(t_erp_aliexpress_online_info_Admin, self).get_list_queryset()

        if request.user.is_superuser:
            qs = qs
        else:
            shop_list = []
            store_conf_objs = t_store_configuration_file.objects.filter(Seller=request.user.first_name).values('ShopName_temp')
            for store_conf_obj in store_conf_objs:
                shop_list.append(store_conf_obj['ShopName_temp'])
            qs = qs.filter(shopName__in=shop_list)


        product_id = request.GET.get('product_id', '')
        shopSKU = request.GET.get('shopSKU', '')
        SKU = request.GET.get('SKU', '')
        MainSKU = request.GET.get('MainSKU', '').split(',')
        Revoked=request.GET.get('revoked','')
        skustock_isempty=request.GET.get('skustock_isempty','')
        skustatus = request.GET.get('skustatus','')  # 商品SKU状态
        tortinfo=request.GET.get('tortinfo','')

        if tortinfo:
            if tortinfo=='-1':
                objs = t_erp_aliexpress_product_sku.objects.filter(Infringing__in=['0','1']).values('product_id').distinct()
                tort_product = [x['product_id'] for x in objs]
                qs=qs.exclude(product_id__in=tort_product)
            else:
                objs = t_erp_aliexpress_product_sku.objects.filter(Infringing=tortinfo).values('product_id').distinct()
                tort_product = [x['product_id'] for x in objs]
                qs = qs.filter(product_id__in=tort_product)
        goodsstatus = []
        if skustatus == '1':
            goodsstatus = [1000, 1100, 1010, 1001, 1110, 1101, 1011, 1111]  # 正常
        if skustatus == '2':
            goodsstatus = [100, 1100, 110, 101, 1110, 1101, 111, 1111]  # 售完下架
        if skustatus == '3':
            goodsstatus = [10, 1010, 110, 11, 1011, 1110, 111, 1111]  # 临时下架
        if skustatus == '4':
            goodsstatus = [1, 1001, 101, 11, 1101, 111, 1011, 1111]  # 停售

        flag=False
        if skustatus and skustock_isempty:
            flag=True
            # oreder = request.GET.get('o','')
            # if oreder:
            #     order_list=oreder.split('.')
            #     allorderstr=''
            #     for orderstr in order_list:
            #         if orderstr.startswith('-'):
            #             allorderstr+=orderstr.lstrip('-')+' DESC,'
            #         else:
            #             if orderstr:
            #                 allorderstr += orderstr + ' ASC,'
            #     allorderstr=allorderstr.rstrip(',')
            # else:
            #     allorderstr='gmt_create DESC'
            #
            # limit='order by {};'.format(allorderstr)
            tmp={'1':'skustatus1_stock__in','2':'skustatus2_stock__in','3':'skustatus3_stock__in','4':'skustatus4_stock__in'}

            if skustock_isempty in ('0',u'0',0):
                qs=qs.filter(**{tmp[skustatus]:[1,10]})
                # objs=t_erp_aliexpress_online_info.objects.raw('SELECT t_info.id as id from t_erp_aliexpress_online_info as t_info  '
                #                                          'LEFT JOIN t_erp_aliexpress_product_sku as t_sku on '
                #                                         't_info.product_id=t_sku.product_id WHERE t_sku.ipm_sku_stock>0 '
                #                                             'and t_sku.GoodsStatus={} and t_sku.removed=0;'.format(skustatus))
            elif skustock_isempty in ('1',u'1',1):
                qs = qs.filter(**{tmp[skustatus]: [0,10]})
                # objs=t_erp_aliexpress_online_info.objects.raw('SELECT t_info.id as id from t_erp_aliexpress_online_info as t_info  '
                #                                          'LEFT JOIN t_erp_aliexpress_product_sku as t_sku on '
                #                                          't_info.product_id=t_sku.product_id WHERE t_sku.ipm_sku_stock=0 '
                #                                             'and t_sku.GoodsStatus={} and t_sku.removed=0;'.format(skustatus))


            #tmp_id=[obj.id for obj in objs]
            #qs=qs.filter(id__in=tmp_id)



        if MainSKU !=['',]:
            mutilSKU=t_erp_aliexpress_product_sku.objects.filter(mutilSKUFlag=1).values('MainSKU')
            for mutilsku in mutilSKU:
                mainsku_list=mutilsku.get('MainSKU','').split("+")
                for mainsku in mainsku_list:
                    if mainsku in MainSKU:
                        MainSKU.append(mutilsku.get('MainSKU'))
            if len(MainSKU) > 300:
                MainSKU = MainSKU[:300]
                messages.error(request, u'MainSKU个数最大为300！')
            t_erp_aliexpress_product_sku_objs = t_erp_aliexpress_product_sku.objects.filter(MainSKU__in=MainSKU).values('product_id').distinct()
            qs = qs.filter(product_id__in=t_erp_aliexpress_product_sku_objs)




        stopsales=request.GET.get('StopSales')
        if stopsales:
            StopSales=stopsales.split('-')[1]
            StopSalesFlag=stopsales.split('-')[0]
        else:
            StopSales=None
            StopSalesFlag=None


        if product_id:
            product_ids = [product_id]
            if ',' in product_id:
                product_ids = product_id.split(',')
            qs = qs.filter(product_id__in=product_ids)

        if shopSKU:
            sku_list = [shopSKU]
            if ',' in shopSKU:
                sku_list = shopSKU.split(',')
            t_erp_aliexpress_product_sku_objs = t_erp_aliexpress_product_sku.objects.filter(ShopSKU__in=sku_list).values(
                'product_id').distinct()
            qs = qs.filter(product_id__in=t_erp_aliexpress_product_sku_objs)
        if SKU:
            sku_list = [SKU]
            if ',' in SKU:
                sku_list = SKU.split(',')
                if len(sku_list) > 300:
                    sku_list=sku_list[:300]
                    messages.error(request, u'SKU个数最大为300！')
            mutilSKU = t_erp_aliexpress_product_sku.objects.filter(mutilSKUFlag=1).values('SKU')
            for mutilsku in mutilSKU:
                skus_list = mutilsku.get('SKU','').split("+")
                for sku in skus_list:
                    if sku in sku_list:
                        sku_list.append(mutilsku.get('SKU'))

            t_erp_aliexpress_product_sku_objs = t_erp_aliexpress_product_sku.objects.filter(SKU__in=sku_list).values('product_id').distinct()
            qs = qs.filter(product_id__in=t_erp_aliexpress_product_sku_objs)

        shopname = request.GET.get('shopname', '')
        accountName = request.GET.get('accountName', '').split(',')
        if shopname == 'all':
            shopname = ''

        Title_blurry = request.GET.get('Title_blurry', '')
        Title_exact = request.GET.get('Title_exact', '')
        Sales7Days_start = request.GET.get('Sales7Days_start', '')
        Sales7Days_end = request.GET.get('Sales7Days_end', '')
        Gmt_create_start = request.GET.get('Gmt_create_start', '')
        Gmt_create_end = request.GET.get('Gmt_create_end', '')
        Gmt_modified_start = request.GET.get('Gmt_modified_start', '')
        Gmt_modified_end = request.GET.get('Gmt_modified_end', '')
        UpdateTime_start = request.GET.get('UpdateTime_start', '')
        UpdateTime_end = request.GET.get('UpdateTime_end', '')
        product_status_type = request.GET.get('product_status_type', '')

        category = request.GET.get('category', '')
        tmpdict={}
        if isinstance(StopSales,(str,unicode)):
            if StopSales.isdigit() and int(StopSales)<100:
                tmpdict={'StopSales__range':[1,99]}
            elif StopSales.isdigit() and int(StopSales)==100:
                tmpdict={'StopSales':StopSales}
            elif StopSales.isdigit() and int(StopSales)>100:
                tmpdict = {'StopSales__range': [1,100]}

        if category == 0 or category == '0':
            category = ''
        searchList = {'subject__iexact': Title_exact, 'subject__icontains': Title_blurry,
                      'Sales7Days__gte': Sales7Days_start, 'Sales7Days__lt': Sales7Days_end,
                      'gmt_create__gte': Gmt_create_start, 'gmt_create__lt': Gmt_create_end,
                      'gmt_modified__gte': Gmt_modified_start, 'gmt_modified__lt': Gmt_modified_end,
                      'updatetime__gte': UpdateTime_start, 'updatetime__lt': UpdateTime_end,
                      'product_status_type__exact': product_status_type, 'category_id__exact': category,
                       'shopName__exact': shopname,
                      }

        if not flag:
            if skustock_isempty:
                searchList.update({'skustock_isempty':skustock_isempty,})
            elif goodsstatus:
                searchList.update({'GoodsFlag__in':goodsstatus})
        if accountName and accountName !=['',]:
            searchList.update({'owner_member_id__in': accountName,})
        if Revoked:
            if Revoked in (1,'1',u'1'):
                qs=qs.filter(Q(revoked=1) | Q(revoked=0,product_status_type='service-delete'))
            else:
                searchList.update({'revoked__exact':Revoked})

        else:
            if product_status_type:
                searchList.update({'revoked__exact': '0'})

        if StopSalesFlag:
            searchList.update({'StopSalesFlag__exact':StopSalesFlag,})
        # 商品状态查询
        if tmpdict:
            searchList.update(tmpdict)
        # else:
        #     qs = qs.exclude(product_status_type='Delete')

        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    sl[k] = v
        if sl is not None:
            # try:
            qs = qs.filter(**sl)
            # except Exception, ex:
            #     messages.error(request, u'输入的查询数据有问题！')
        return qs
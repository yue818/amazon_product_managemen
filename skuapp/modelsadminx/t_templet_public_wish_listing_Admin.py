# coding=utf-8


from skuapp.modelsadminx.t_online_info_wish_Admin import *


class t_templet_public_wish_listing_Admin(t_online_info_wish_Admin):
    search_box_flag = True
    search_flag = False
    plateform_distribution_navigation = True
    listing_sku_query = True
    wish_listing_readonly_f = False
    wish_listing_secondplugin = False


    def show_orders7days(self,obj) :
        rt =  "<a id=show_orderlist_%s>日销量</a><script>$('#show_orderlist_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'查看全部',fix:false,shadeClose: true,maxmin:true,area:['1000px','600px'],content:'/t_online_info_wish/order1day/?aID=%s',});});</script>"%(obj.id,obj.id,obj.ProductID)
        rt += '<br><br><a href="/create_wish_collection_box/?productID=%s&mainsku=%s">采集箱</a>' % (obj.ProductID, obj.MainSKU)
        return mark_safe(rt)
    show_orders7days.short_description = u'<span style="color: #428bca">&nbsp;&nbsp;操&nbsp;作&nbsp;&nbsp;</span>'


    def get_list_queryset(self,):
        request = self.request
        qs = super(t_online_info_wish_Admin, self).get_list_queryset()
        status = request.GET.get('status', '')
        shopname = request.GET.get('shopname','')
        seller = request.GET.get('seller','')
        reviewState = request.GET.get('reviewState','')
        reviewState = reviewState.split(',')
        if '' in reviewState:
            reviewState = ''
        tortinfo = request.GET.get('tortInfo','')
        Estatus = request.GET.get('Estatus','')
        dataSources = request.GET.get('dataSources','')
        productId = request.GET.get('productID','')
        mainSKU = request.GET.get('mainSKU','')
        orders7DaysStart = request.GET.get('orders7DaysStart','')
        orders7DaysEnd = request.GET.get('orders7DaysEnd','')
        refreshTimeStart = request.GET.get('refreshTimeStart','')
        refreshTimeEnd = request.GET.get('refreshTimeEnd', '')
        dateUploadedStart = request.GET.get('dateUploadedStart','')
        dateUploadedEnd = request.GET.get('dateUploadedEnd', '')
        lastUpdatedStart = request.GET.get('lastUpdatedStart', '')
        lastUpdatedEnd = request.GET.get('lastUpdatedEnd', '')
        title = request.GET.get('title','')
        searchList = {'ShopName__exact': shopname, 'Seller__exact': seller, 'ReviewState__in': reviewState,
                      'TortInfo__exact': tortinfo, 'Status__exact':Estatus, 'DataSources__exact': dataSources,
                      'ProductID__exact': productId, 'MainSKU__exact':mainSKU,
                      'Orders7Days__gte': orders7DaysStart, 'Orders7Days__lt': orders7DaysEnd,
                      'RefreshTime__gte': refreshTimeStart, 'RefreshTime__lt': refreshTimeEnd,
                      'DateUploaded__gte':dateUploadedStart,'DateUploaded__lt':dateUploadedEnd,
                      'LastUpdated__gte': lastUpdatedStart, 'LastUpdated__lt': lastUpdatedEnd,
                      'Title__icontains':title
                      }
        sl = {}
        for k,v in searchList.items():
            if isinstance(v,list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    if k == 'ShopName__exact':
                        v = 'Wish-' + v.zfill(4)
                    sl[k] = v
        if sl is not None:
            try:
                qs = qs.filter(**sl)
            except Exception,ex:
                messages.error(request,u'输入的查询数据有问题！')

        # 在线
        if status == 'online':
            qs = qs.filter(ReviewState='approved',Status='Enabled')
        # 不在线
        elif status == 'offline':
            qs = qs.filter(Q(ReviewState='approved',Status='Disabled')|Q(ReviewState='pending'))
        # 拒绝
        elif status == 'reject':
            qs = qs.filter(ReviewState='rejected')
        else:
            qs = qs

        mysku = request.GET.get('mysku', '')
        if mysku == '':
            pass
        else:
            skuList = mysku.split(',')
            qs = qs.filter(MainSKU=skuList[0])
            messages.info(request, '当前查询的MainSKU为: %s' % skuList[0])

        return qs
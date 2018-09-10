# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from skuapp.table.t_order_item_amazon_india import *
from skuapp.table.t_order_track_info_amazon_india import *
from skuapp.table.t_shop_amazon_india import *
from django.contrib import messages
import hashlib
import oss2
from skuapp.public.url_Stitching import *
from app_djcelery.tasks import get_trackno_amazon_india,download_trackInfo_pdf,download_price_pdf 
from skuapp.table.t_order_amazon_india import *
import time,datetime
import os,errno,sys
from Project.settings import *
import decimal

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5 (except OSError, exc: for Python <2.5)
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
class t_order_amazon_india_Admin(object):
    amazon_india_FBA_sku_flag = True
    search_box_flag = True
    downloadxls = True

    def show_track_info(self,obj):
        if obj.FulfillmentChannel == 'MFN':
            rt = ''
            t_order_track_info_amazon_india_objs = t_order_track_info_amazon_india.objects.filter(AmazonOrderId=obj.AmazonOrderId)
            if t_order_track_info_amazon_india_objs:
                for t_order_track_info_amazon_india_obj in t_order_track_info_amazon_india_objs:
                    rt += u"物流单号：<a id=trackNumber_%s style='color:#428bca'>%s</a><script>$('#trackNumber_%s').on('click',function(){layer.open({" \
                         u"type:2,skin:'layui-layer-lan',title:'物流信息详情',fix:false,shadeClose: true,maxmin:true,area:['700px','520px'],content:'/Project/admin/skuapp/t_order_amazon_india/trackInfo/?shopname=%s&order_id=%s'," \
                         u"btn:['关闭页面']});});</script>" %(
                        str(t_order_track_info_amazon_india_obj.id),t_order_track_info_amazon_india_obj.trackNumber,str(t_order_track_info_amazon_india_obj.id),obj.ShopName,str(t_order_track_info_amazon_india_obj.id))
                    if t_order_track_info_amazon_india_obj.track_info is None or t_order_track_info_amazon_india_obj.track_info.strip() == '':
                        rt += u'暂无物流信息'
                    rt += '<br/>'
        else:
            rt = ''
        return mark_safe(rt)
    show_track_info.short_description = u'GATI物流信息'

    def local2utc(self, local_st):
        """本地时间转UTC时间（-8:00）"""
        time_struct = time.mktime(local_st.timetuple())
        utc_st = datetime.datetime.utcfromtimestamp(time_struct)
        return utc_st

    def transactionTrackInfo(self, obj):
        textNewStr = 'Check In Scan'#Check In Scan
        textStr1 = 'Package Dispatched'
        isTracked = {'feed': 0,'trackTwo': 0, 'trackId': 0, 'track_status': '0'}
        t_order_track_info_amazon_india_objs = t_order_track_info_amazon_india.objects.filter(
            AmazonOrderId=obj.AmazonOrderId)
        for t_order_track_info_amazon_india_obj in t_order_track_info_amazon_india_objs:
            track_info = t_order_track_info_amazon_india_obj.track_info
            track_status = t_order_track_info_amazon_india_obj.track_status

            isTracked['trackId'] = t_order_track_info_amazon_india_obj.id
            isTracked['track_status'] = t_order_track_info_amazon_india_obj.track_status
            if track_status == '3':
                isTracked['feed'] = 1
                break
            if track_info:
                deal_track_infos = eval(track_info)
                for deal_track_info in deal_track_infos:
                    if deal_track_info:
                        if textNewStr == deal_track_info['Info']:
                            isTracked['feed'] = 1
                        if textStr1 == deal_track_info['Info']:
                            isTracked['trackTwo'] = 1
                            # break
        return isTracked

    def show_track_status(self,obj):
        rt = ''
        if obj.FulfillmentChannel == 'MFN':
            t_order_track_info_amazon_india_objs = t_order_track_info_amazon_india.objects.filter(
                AmazonOrderId=obj.AmazonOrderId)
            for t_order_track_info_amazon_india_obj in t_order_track_info_amazon_india_objs:
                if t_order_track_info_amazon_india_obj.track_status is not None and t_order_track_info_amazon_india_obj.track_status.strip() != '':
                    rt += t_order_track_info_amazon_india_obj.track_StateDesc + '<br/>'
                else:
                    rt += ''
        else:
            rt = ''
        return mark_safe(rt)
    show_track_status.short_description = u'GATI物流状态'

    def getLeaveTime(self,obj):
        leaveTime = {}
        lsd = obj.LatestShipDate
        lud = obj.PurchaseDate
        date_time = datetime.datetime.strptime(lsd.encode('unicode-escape').decode('string_escape'), '%Y-%m-%dT%H:%M:%SZ')
        utc_tran = self.local2utc(datetime.datetime.now())
        firstTime = (date_time - utc_tran).days

        date_time = datetime.datetime.strptime(lud.encode('unicode-escape').decode('string_escape'), '%Y-%m-%dT%H:%M:%SZ')
        secondTime = (utc_tran - date_time).days
        leaveTime['secondTime'] = secondTime
        leaveTime['firstTime'] = firstTime
        return leaveTime

    def click_button(self,obj):
        order_id = obj.id
        if obj.FulfillmentChannel=='MFN':
            leaveTime = self.getLeaveTime(obj)
            t_order_track_info_amazon_india_objs = t_order_track_info_amazon_india.objects.filter(
                AmazonOrderId=obj.AmazonOrderId)
            if obj.OrderStatus == 'Pending':
                rt = u'订单付款未完成'
            elif obj.OrderStatus == 'Canceled':
                rt = u'订单已取消'
            elif obj.OrderStatus == 'Unshipped':
                if t_order_track_info_amazon_india_objs:
                    rt = u'订单已交物流处理'
                    tlth = len(t_order_track_info_amazon_india_objs)
                    isTracked = self.transactionTrackInfo(obj)
                    if tlth > 0:
                        if obj.is_sure_feed is None or obj.is_sure_feed == '':
                            if isTracked['feed'] == 1:
                                url_Stitching_obj = url_Stitching(self.request)
                                postStr = url_Stitching_obj.reStitching_url([],{},{'shopname': obj.ShopName})
                                rt = u'<button id="application1" type="button" style="background-color:#428bca" onclick=' \
                                     u'"window.location.href=\'/Project/admin/skuapp/t_order_amazon_india/feed_amazon/'+postStr+ '&order_id=' + str(
                                    order_id) + '&trackId=' + str(isTracked['trackId']) + u'\'">确认已发货</button>'
                            if leaveTime['firstTime'] == 0:
                                url_Stitching_obj = url_Stitching(self.request)
                                postStr = url_Stitching_obj.reStitching_url([],{},{'shopname': obj.ShopName})
                                rt = u'<button id="application1" type="button" style="background-color:yellow" onclick=' \
                                     u'"window.location.href=\'/Project/admin/skuapp/t_order_amazon_india/feed_amazon/'+postStr+ '&order_id=' + str(
                                    order_id) + '&trackId=' + str(isTracked['trackId']) + u'\'">确认已发货</button>'
                            if isTracked['trackTwo'] == 0 and leaveTime['secondTime'] > 6:
                                rt += u"<br/><label style='color:red'>七天未查到物流信息</label>"
                            if leaveTime['firstTime'] < 4 and leaveTime['firstTime'] > 0:
                                rt += u"<br/><label style='color:red'>请及时同步至Amazon平台</label>"
                        elif obj.is_sure_feed == '1':
                            rt = u'运单号同步Amazon平台中...'
                        elif obj.is_sure_feed == '2':
                            if isTracked['track_status'] == '3':
                                rt = u'订单已完成'
                            rt += u'<br/>(已同步至Amazon平台)'
                else:
                    rt = u'运单号申请中'
                    if obj.applyTracking is None or obj.applyTracking.strip() == '':
                        rt = u"<a id=application1_%s style='color:#428bca'>申请运单号</a><script>$('#application1_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'申请运单号',fix:false,shadeClose: true,maxmin:true,area:['750px','600px'],content:'/Project/admin/skuapp/t_order_amazon_india/apply_track/?shopname=%s&order_id=%s&trackTime=first',btn:['关闭页面'],end:function(){location.reload();}});});</script>" % (
                        str(order_id), str(order_id), obj.ShopName, str(order_id))
                        if leaveTime['secondTime'] > 4:
                            rt += u"<br/><label style='color:red'>请及时发货</label>"
            elif obj.OrderStatus == 'Shipped':
                rt = u'已发货'
        else:
            rt = u'非国内物流'
            if obj.OrderStatus == 'Pending':
                rt += u'(订单付款未完成)'
            elif obj.OrderStatus == 'Canceled':
                rt += u'(订单已取消)'
            elif obj.OrderStatus == 'Unshipped':
                rt += u'(未发货)'
            elif obj.OrderStatus == 'Shipped':
                rt += u'(已发货)'
        return mark_safe(rt)
    click_button.short_description = u'订单操作'

    def calcsign(self, request_data, appKey):
        keyset = sorted(request_data.keys())
        signdata = ''
        for i in range(0, len(keyset)):
            signdata = signdata + keyset[i] + '=' + str(request_data[keyset[i]])
        signdata += 'Key=' + appKey
        m = hashlib.md5()
        m.update(signdata)
        psw = m.hexdigest()
        signature = psw.upper()
        return signature

    def applyPostTrackInfo(self, obj, t_order_item_amazon_india_objs, request):
        t_order_amazon_india_obje = t_order_amazon_india.objects.filter(id=obj.id)
        t_shop_amazon_india_obj = t_shop_amazon_india.objects.filter(ShopName=obj.ShopName)[0]
        url = 'http://120.78.88.110:9090/service/parser'
        timeStamp = int(time.time() * 1000)
        appKey = '6dd8a3d04db5430c9ab1eebe6373b82d'
        appId = '07AADCF1662M1ZH'
        t_order_amazon_india_obj = t_order_amazon_india_obje[0]
        allDV = 0
        goodsToStr = ''
        pweight = 0
        trasationUSD = decimal.Decimal("%.2f" % float(6.6))
        decimal.getcontext().prec = 2
        tsFlag = '0'
        try:
            for t_order_item_amazon_india_obj in t_order_item_amazon_india_objs:
                aliasCnName = t_order_item_amazon_india_obj.AliasCnName
                aliasEnName = t_order_item_amazon_india_obj.AliasEnName
                cargoClass = 1
                if t_order_item_amazon_india_obj.IsCharged == '1':
                    cargoClass = 3
                if t_order_item_amazon_india_obj.IsPowder == '1':
                    cargoClass = 10
                if t_order_item_amazon_india_obj.IsLiquid == '1':
                    cargoClass = 9
                if t_order_item_amazon_india_obj.isMagnetism == '1':
                    cargoClass = 5
                if t_order_item_amazon_india_obj.IsCharged == '1':
                    tsFlag = '1'
                dv = t_order_item_amazon_india_obj.CostPrice / trasationUSD
                allDV += dv
                goodsCount = 1
                SellerSKUList = [t_order_item_amazon_india_obj.SellerSKU, ]
                if '+' in t_order_item_amazon_india_obj.SellerSKU:
                    SellerSKUList = t_order_item_amazon_india_obj.SellerSKU.split('+')
                for sellerSKU in SellerSKUList:
                    if t_order_item_amazon_india_obj.ShopSKU in sellerSKU:
                        if '*' in sellerSKU:
                            goodsCount = int(sellerSKU.split('*')[1])

                pweight += t_order_item_amazon_india_obj.PackWeight + (t_order_item_amazon_india_obj.Weight * goodsCount)
                goodsToStr += '{"CnName":"' + aliasCnName + '","EnName":"' + aliasEnName + '","Description":"","Unit":' + \
                              '"PCS","Sku":"' + t_order_item_amazon_india_obj.SKU + '","Quantity":' + str(
                    t_order_item_amazon_india_obj.QuantityOrdered) + \
                              ',"DeclaredValue":"' + str(
                    dv) + '","DeclareCurrency":"USD","Origin":"CN","CargoClass":' + str(cargoClass) + ',"HsCode":""},'
            shipAddressLine2 = ''
            if t_order_amazon_india_obj.shipAddressLine2 is not None:
                shipAddressLine2 = t_order_amazon_india_obj.shipAddressLine2

            shipAddressLine1 = t_order_amazon_india_obj.shipAddressLine1
            if '"' in shipAddressLine1:
                shipAddressLine1 = shipAddressLine1.replace('"', '\'')
            if '"' in shipAddressLine2:
                shipAddressLine2 = shipAddressLine2.replace('"', '\'')

            pweight = pweight / 1000
            pweight = decimal.Decimal("%.2f" % pweight)

            CustomerRef = t_order_amazon_india_obj.AmazonOrderId
            if tsFlag == '1':
                track_server = 'INWPX-BAT'
            else:
                track_server = 'INWPX'

            toMD5Data1 = '{"CustomerRef":"' + CustomerRef + '","ServiceCode":"' + track_server + '","ConType":2,"ReturnWay":1,"TradeTerms":"FOB",' \
                                  '"CustomerOrderID":"","CodAmount":"0","DomesticExp":"","ReturnLabelData":0,"TrackNumber":"","DepotCode":"SZX","ImportGateway":"","Notes":"' \
                         '","DeclaredValue":"' + str(allDV) + '","DeclareCurrency":"USD","HsCode":"","InsuranceVal":"0","InsuranceCur":"","LabelType":"URL","ShipFrom":' \
                         '{"Name":"' + t_shop_amazon_india_obj.ShopUserName + '","PostCode":"' + t_shop_amazon_india_obj.PostCode + '","Phone":{"Tel":"' + t_shop_amazon_india_obj.UserPhoneTel + \
                         '"},"Mobile":"' + t_shop_amazon_india_obj.Mobile + '","Email":"' + t_shop_amazon_india_obj.Email + '","CountryCode":"' + t_shop_amazon_india_obj.CountryCode + \
                         '","Company":"' + t_shop_amazon_india_obj.Company + '","Address":"' + t_shop_amazon_india_obj.UserAdress + '","Province":"' + t_shop_amazon_india_obj.Province + \
                         '","City":"' + t_shop_amazon_india_obj.City + '"},"ShipTo":{"Name":"' + t_order_amazon_india_obj.shipName + \
                         '","PostCode":"' + t_order_amazon_india_obj.shipPostalCode + '","Phone":{"Tel":""},"Mobile":"' + t_order_amazon_india_obj.shipPhone + \
                         '","Email":"' + t_order_amazon_india_obj.BuyerEmail + '","CountryCode":"' + t_order_amazon_india_obj.shipCountryCode + '","Company":"' + t_order_amazon_india_obj.shipName + '",' + \
                         '"Address":"' + shipAddressLine1 + ', ' + shipAddressLine2 + '","Province":"' + t_order_amazon_india_obj.shipStateOrRegion + '",' + \
                         '"City":"' + t_order_amazon_india_obj.shipCity + '"},"Goods":[' + goodsToStr[:-1] + '],"Packages":[{"CustomerPkgRef":"","PackingType":"2","Weight":"' + str(pweight) + '","Quantity":"1","Dimension":{"L":"0.000","W":"0.000","H":"0.000","U":"M"}}]}'

            request_data = {"AppId": appId, "TimeStamp": timeStamp, "RequestName": "submitShipment",
                            "Content": toMD5Data1}
            tosignature = {"AppId": appId, "TimeStamp": timeStamp}
            signature = self.calcsign(tosignature, appKey)
            request_data['Sign'] = signature
            request_str = '{"AppId":"' + request_data['AppId'] + '","TimeStamp":"' + str(
                request_data['TimeStamp']) + '","RequestName":"submitShipment","Content":' + request_data['Content'] + \
                          ',"Sign":"' + signature + '"}||' + url

            t_order_amazon_india_obje.update(DeclaredValue=allDV, DeclareCurrency='USD')
        except Exception,ex:
            request_str = '-1'
            t_order_amazon_india_obje.update(applyTracking='', dealTime=datetime.datetime.now(),
                                                    dealUser=request.user.username,
                                                    dealAction='apply track number', dealResult='Failed',
                                                    dealResultInfo=ex)
        return request_str

    def track_time(self, obj):
        leaveTime = self.getLeaveTime(obj)
        leaveDays = leaveTime['firstTime']
        rt = u'最迟发货时间:<br/>' + obj.LatestShipDate
        if obj.FulfillmentChannel=='MFN' and obj.OrderStatus == 'Unshipped':
            if obj.is_sure_feed != '2':
                if leaveDays >= 0:
                    if leaveDays > 3:
                        rt += u'<br/>(剩余 ' + str(leaveDays) + u' 天)'
                    else:
                        rt += u'<br/>(<label style="color:red">剩余 ' + str(leaveDays) + u' 天</label>)'
                else:
                    rt += u'<br/>(<label style="color:red">未确认发货已超过 ' + str(leaveDays).replace('-', '') + u' 天</label>)'
        rt += u'<br/><br/>预计签收时间:<br/>最早：'
        if obj.EarliestDeliveryDate is not None:
            rt += obj.EarliestDeliveryDate + u'<br/>最迟：'
            rt += obj.LatestDeliveryDate
        return mark_safe(rt)
    track_time.short_description = u'Amazon订单物流时间'

    def apply_tracks(self, request, queryset):
        from django.db import connection
        request_params = []
        for querysetid in queryset:
            t_order_track_info_amazon_india_objs = t_order_track_info_amazon_india.objects.filter(AmazonOrderId=querysetid.AmazonOrderId)
            if t_order_track_info_amazon_india_objs:
                continue
            else:
                t_order_item_amazon_india_objs = t_order_item_amazon_india.objects.filter(AmazonOrderId=querysetid.AmazonOrderId)
                t_order_amazon_india_obj = t_order_amazon_india.objects.filter(id=querysetid.id)
                if t_order_item_amazon_india_objs:
                    request_str = self.applyPostTrackInfo(querysetid, t_order_item_amazon_india_objs, request)
                    if request_str != '-1':
                        request_str += '||' + str(querysetid.id)
                        request_params.append(request_str)
                        # t_amazon_schedule_ing_obj = t_amazon_schedule_ing()
                        # t_amazon_schedule_ing_obj.ShopName = querysetid.ShopName
                        # t_amazon_schedule_ing_obj.PlatformName = 'Amazon'
                        # t_amazon_schedule_ing_obj.CMDID = 'apply_track_number'
                        # t_amazon_schedule_ing_obj.ScheduleTime = datetime.datetime.now()
                        # t_amazon_schedule_ing_obj.Status = '0'
                        # t_amazon_schedule_ing_obj.InsertTime = datetime.datetime.now()
                        # t_amazon_schedule_ing_obj.UpdateTime = datetime.datetime.now()
                        # t_amazon_schedule_ing_obj.Timedelta = 90
                        # t_amazon_schedule_ing_obj.RetryCount = 0
                        # t_amazon_schedule_ing_obj.Processed = 0
                        # t_amazon_schedule_ing_obj.Successful = 0
                        # t_amazon_schedule_ing_obj.WithError = 0
                        # t_amazon_schedule_ing_obj.WithWarning = 0
                        # t_amazon_schedule_ing_obj.Params = request_str
                        # t_amazon_schedule_ing_obj.save()
                        #get_trackno_amazon_india.delay(connection, request_str)
                        t_order_amazon_india_obj.update(applyTracking='1', dealTime=datetime.datetime.now(),
                                                        dealUser=request.user.username,
                                                        dealAction='apply track number', applyTrackNoTime=datetime.datetime.now())
                else:
                    t_order_amazon_india_obj.update(applyTracking='', dealTime=datetime.datetime.now(),
                                                    dealUser=request.user.username,
                                                    dealAction='apply track number', dealResult='Failed',
                                                    dealResultInfo='There is not any itemsinfo!')

        result_code = {}
        if request_params:
            result_code = get_trackno_amazon_india.delay(request_params)
        return result_code


    apply_tracks.short_description=u'申请运单号'

    def download_pdf(self,obj):
        rt = ''
        t_order_track_info_amazon_india_objs = t_order_track_info_amazon_india.objects.filter(
            AmazonOrderId=obj.AmazonOrderId)
        if t_order_track_info_amazon_india_objs:
            tlth = len(t_order_track_info_amazon_india_objs)
            if t_order_track_info_amazon_india_objs[tlth-1].LableData is not None and t_order_track_info_amazon_india_objs[tlth-1].LableData.strip() != '':
                #<a href="http://cnilink-bucket-name20171127.oss-cn-shenzhen.aliyuncs.com/ec50ceaea477471aa5a4273b5b92094f" download="111.PDF">111111111</a>
                rt = u'<a href="%s" download="%s.pdf">下载面单</a>  ' % (t_order_track_info_amazon_india_objs[tlth-1].LableData,t_order_track_info_amazon_india_objs[tlth-1].trackNumber)
        return mark_safe(rt)
    download_pdf.short_description = u'GATI物流面单'

    def to_excel(self, request, queryset):
        from xlwt import *
        path = MEDIA_ROOT + 'download_xls/' + request.user.username
        # if not os.path.exists(path):
        mkdir_p(MEDIA_ROOT + 'download_xls')
        os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))

        mkdir_p(path)
        os.popen('chmod 777 %s' % (path))

        w = Workbook()
        sheet = w.add_sheet('feed_trackNo_to_py')

        sheet.write(0, 0, u'订单号')
        sheet.write(0, 1, u'店铺单号')
        sheet.write(0, 2, u'跟踪号')

        # 写数据
        row = 0
        for qs in queryset:
            if qs.pyOrderNumber:

                row = row + 1
                column = 0
                sheet.write(row, column, qs.pyOrderNumber)

                column = column + 1
                sheet.write(row, column, '')

                t_order_track_info_amazon_india_objs = t_order_track_info_amazon_india.objects.filter(
                    AmazonOrderId=qs.AmazonOrderId)
                trackNo = ''
                if t_order_track_info_amazon_india_objs:
                    if isinstance(t_order_track_info_amazon_india_objs,list):
                        trackNo = t_order_track_info_amazon_india_objs[0][0].trackNumber
                    else:
                        trackNo = t_order_track_info_amazon_india_objs[0].trackNumber

                column = column + 1
                sheet.write(row, column, trackNo)
            else:
                messages.error(request,u'导出错误,订单号:%s缺少普源单号'% qs.AmazonOrderId)


        filename = request.user.username + '_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
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

    to_excel.short_description = u'导出回填pyEXCEL'

    def to_csv(self, request, queryset):
        import csv,codecs
        objs = []
        for qs in queryset:
            if qs.pyOrderNumber:
                obj = []
                obj.append(qs.pyOrderNumber)
                obj.append('')
                t_order_track_info_amazon_india_objs = t_order_track_info_amazon_india.objects.filter(
                    AmazonOrderId=qs.AmazonOrderId)
                trackNo = ''
                if t_order_track_info_amazon_india_objs:
                    if isinstance(t_order_track_info_amazon_india_objs,list):
                        trackNo = t_order_track_info_amazon_india_objs[0][0].trackNumber
                    else:
                        trackNo = t_order_track_info_amazon_india_objs[0].trackNumber
                obj.append(trackNo)
                objs.append(obj)


        filename = request.user.username + '_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.csv'
        csvfile_path = MEDIA_ROOT + 'download_xls/' + filename
        with open(csvfile_path, "w") as csvfile:
            csvfile.write(codecs.BOM_UTF8)
            superwriter = csv.writer(csvfile, dialect='excel')
            # superwriter.writerow([u"pyOrderId", u"ShopId", u"trackNumber"])
            superwriter.writerow([u"订单号", u"店铺单号", u"跟踪号"])
            for obj in objs:
                superwriter.writerow(obj)

        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT, BUCKETNAME_XLS)
        bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
        # 删除现有的
        for object_info in oss2.ObjectIterator(bucket,
                                               prefix='%s/%s_' % (request.user.username, request.user.username)):
            bucket.delete_object(object_info.key)
        bucket.put_object(u'%s/%s' % (request.user.username, filename), open(csvfile_path))
        messages.error(request, u'%s%s.%s/%s/%s' % (PREFIX, BUCKETNAME_XLS, ENDPOINT_OUT, request.user.username,
                                                    filename) + u':成功导出,可点击Download下载到本地............................。')

    to_csv.short_description = u'导出回填pyCSV'

    def show_dealResult(self,obj):
        rt = ''
        if obj.dealResult is not None and obj.dealResult.strip() != '':
            if obj.dealAction is not None:
                rt = obj.dealAction + ' '
            rt += obj.dealResult
            if obj.dealResult != 'Success' and obj.dealResult != 'Complete':
                rt += '.<br/>Reason: &nbsp;'+obj.dealResultInfo
        return mark_safe(rt)
    show_dealResult.short_description = u'订单处理结果'

    def feed_trackNo(self, obj):
        rt = ''
        if obj.FulfillmentChannel=='MFN' and obj.OrderStatus!='Pending' and obj.OrderStatus!='Canceled' and obj.applyTracking!= '1':
            rt = u"<a id=feed1_%s style='color:#428bca'>手动申请回填</a><script>$('#feed1_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'手动申请回填',fix:false,shadeClose: true,maxmin:true,area:['400px','300px'],content:'/Project/admin/skuapp/t_order_amazon_india/feed_track/?shopname=%s&order_id=%s',btn:['关闭页面'],end:function(){location.reload();}});});</script>" % (
            str(obj.id), str(obj.id), obj.ShopName, str(obj.id))
        return mark_safe(rt)
    feed_trackNo.short_description = u'手动申请处理'

    list_display = ('AmazonOrderId','OrderStatus','ShopName','show_track_info','show_track_status', 'track_time', 'click_button', 'feed_trackNo','FulfillmentChannel','show_dealResult')

    actions = ['apply_tracks','to_excel', 'download_track_pdf', 'download_price_pdf']

    def download_track_pdf(self, request, queryset):
        trackNumbers = []
        params = {'userName': request.user.username}
        AmazonOrderId = request.GET.get('AmazonOrderId', '')
        AmazonOrderIds = AmazonOrderId.split(',')
        if AmazonOrderIds:
            for amazonOrderId in AmazonOrderIds:
                t_order_track_info_amazon_india_objs = t_order_track_info_amazon_india.objects.filter(
                    AmazonOrderId=amazonOrderId)
                trackNo = ''
                if t_order_track_info_amazon_india_objs.exists():
                    if isinstance(t_order_track_info_amazon_india_objs, list):
                        trackNo = t_order_track_info_amazon_india_objs[0][0].trackNumber
                    else:
                        trackNo = t_order_track_info_amazon_india_objs[0].trackNumber
                trackNumbers.append(trackNo)
        else:
            for qs in queryset:
                t_order_track_info_amazon_india_objs = t_order_track_info_amazon_india.objects.filter(
                    AmazonOrderId=qs.AmazonOrderId)
                trackNo = ''
                if t_order_track_info_amazon_india_objs.exists():
                    if isinstance(t_order_track_info_amazon_india_objs, list):
                        trackNo = t_order_track_info_amazon_india_objs[0][0].trackNumber
                    else:
                        trackNo = t_order_track_info_amazon_india_objs[0].trackNumber
                trackNumbers.append(trackNo)
        filename = 'trackInfoPDF' + '_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.pdf'
        params['trackNumbers'] = trackNumbers
        # messages.error(request, '%s'%params)
        params['filename'] = filename
        download_trackInfo_pdf.delay(params)
        appname = u'%s/%s' % (request.user.username, filename)
        messages.info(request,u'正在生成物流面单PDF文件...请移至下载中心下载该文件,文件名称：%s'%(appname))

    download_track_pdf.short_description = u'下载物流面单'

    def download_price_pdf(self, request, queryset):
        orderNumbers = []
        params = {'userName': request.user.username}
        AmazonOrderId = request.GET.get('AmazonOrderId', '')
        AmazonOrderIds = AmazonOrderId.split(',')
        if AmazonOrderId:
            for amazonOrderId in AmazonOrderIds:
                urder_track_numbers = {'orderId': amazonOrderId}
                t_order_track_info_amazon_india_objs = t_order_track_info_amazon_india.objects.filter(
                    AmazonOrderId=amazonOrderId)
                trackNo = ''
                if t_order_track_info_amazon_india_objs.exists():
                    if isinstance(t_order_track_info_amazon_india_objs, list):
                        trackNo = t_order_track_info_amazon_india_objs[0][0].trackNumber
                    else:
                        trackNo = t_order_track_info_amazon_india_objs[0].trackNumber
                urder_track_numbers['track_number'] = trackNo
                orderNumbers.append(urder_track_numbers)
        else:
            for qs in queryset:
                urder_track_numbers = {'orderId': qs.AmazonOrderId}
                t_order_track_info_amazon_india_objs = t_order_track_info_amazon_india.objects.filter(
                    AmazonOrderId=qs.AmazonOrderId)
                trackNo = ''
                if t_order_track_info_amazon_india_objs.exists():
                    if isinstance(t_order_track_info_amazon_india_objs, list):
                        trackNo = t_order_track_info_amazon_india_objs[0][0].trackNumber
                    else:
                        trackNo = t_order_track_info_amazon_india_objs[0].trackNumber
                urder_track_numbers['track_number'] = trackNo
                orderNumbers.append(urder_track_numbers)

        filename = 'AmazonPricePDF' + '_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.pdf'
        params['orderNumbers'] = orderNumbers
        params['filename'] = filename
        # messages.error(request, '%s'%params)
        download_price_pdf.delay(params)
        appname = u'%s/%s' % (request.user.username, filename)
        messages.info(request,u'正在生成价格面单PDF文件...请移至下载中心下载该文件,文件名称：%s'%(appname))

    download_price_pdf.short_description = u'下载价格面单'

    def get_list_queryset(self,):
        request = self.request
        from django.db.models import Q
        qs = super(t_order_amazon_india_Admin, self).get_list_queryset()
        # qs.filter(UpdateTime__gte='2017-12-04')
        FulfillmentChannel = request.GET.get('FulfillmentChannel', '')
        applyTracking = request.GET.get('applyTracking', '')
        if applyTracking is not None and applyTracking.strip() != '':
            if applyTracking == '0':
                # messages.error(request, u'============%s' % applyTracking)
                qs = qs.filter(Q(applyTracking__isnull=True)| Q(applyTracking=''))
            else:
                qs = qs.filter(applyTracking__exact=applyTracking)
        AmazonOrderId = request.GET.get('AmazonOrderId', '')
        AmazonOrderId = AmazonOrderId.split(',')
        if '' in AmazonOrderId:
            AmazonOrderId = ''
        OrderStatus = request.GET.get('OrderStatus','')
        OrderStatus = OrderStatus.split(',')
        updateTimeStart = request.GET.get('updateTimeStart', '')  # refreshTimeStart
        updateTimeEnd = request.GET.get('updateTimeEnd', '')
        isWarning = request.GET.get('isWarning', '')
        applyTrackNoTimeStart =  request.GET.get('applyTrackNoTimeStart', '')
        applyTrackNoTimeEnd = request.GET.get('applyTrackNoTimeEnd', '')
        if '' in OrderStatus:
            OrderStatus = ''
        #applyTracking
        searchList = {'FulfillmentChannel__exact': FulfillmentChannel, 'OrderStatus__in': OrderStatus,
                        'AmazonOrderId__in': AmazonOrderId,'UpdateTime__gte': updateTimeStart, 'UpdateTime__lt': updateTimeEnd,
                      'applyTrackNoTime__gte': applyTrackNoTimeStart, 'applyTrackNoTime__lt': applyTrackNoTimeEnd}
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    sl[k] = v
        if sl is not None:
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')
        # messages.error(request, u'============%s'%isWarning)
        if isWarning is not None and isWarning.strip() != '':
            if isWarning == '1':
                qs = qs.filter(OrderWarningDays__isnull=False)
                if applyTracking == '1':
                    qs = qs.filter(OrderWarningType='TrackNumberToAmazon')
                    return qs.order_by('OrderWarningDays')
                elif applyTracking == '0':
                    qs = qs.filter(OrderWarningType='ApplyTrackNumber')
                    return qs.order_by('-OrderWarningDays')
            elif isWarning == '2':
                qs = qs.filter(OrderWarningType='NoTrackInfo')
                return qs.order_by('-OrderWarningDays')
            elif isWarning == '3':
                qs = qs.filter(OrderWarningType='feedAmazon')
                return qs.order_by('-OrderWarningDays')
            else:
                return qs.order_by('OrderWarningDays')

        # if isTrack is not None and isTrack.strip() != '':
        #     if isTrack=='0':
        #         qs = qs.filter(Q(trackNumber__isnull=True)| Q(trackNumber=''))
        #     else:
        #         qs = qs.exclude(Q(trackNumber__isnull=True)| Q(trackNumber=''))
        return qs.order_by('LatestShipDate')
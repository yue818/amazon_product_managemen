#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_wish_pb_campaignproductstats_Admin.py
 @time: 2018-05-25 10:13
"""
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.db import connection
from xadmin.layout import Fieldset, Row
from skuapp.table.t_config_online_amazon import t_config_online_amazon
from skuapp.table.t_wish_pb_campaignproductstats import t_wish_pb_campaignproductstats as t_wish_pb
from skuapp.table.t_wish_pb_productdailystats import t_wish_pb_productdailystats
from skuapp.table.t_product_enter_ed import t_product_enter_ed
from chart_app.table.t_chart_wish_listing_refund_statistics import t_chart_wish_listing_refund_statistics as wish_score
from storeapp.models import t_online_info_wish_store
from brick.wish.WishPbAPI import CreateCampaign, UpdateCampaign, UpdateCampaign_running
from datetime import datetime, timedelta, date
import json

class t_wish_pb_campaignproductstats_Admin(object):
    t_wish_pb_left_menu = True
    search_box1_flag = True
    search_wishpb_keywords = True
    t_wishpb_syncdata_flag = True

    def tortInfo(self, TortInfo):
        if TortInfo == 'WY':
            rt = u' <div title="Wish侵权" style="float:left;width: 20px;height: 20px;background-color: #FF3333;text-align: center;line-height: 20px;border-radius: 4px">W</div>'
        elif TortInfo == 'N':
            rt = u' <div title="未侵权" style="float:left;width: 20px;height: 20px;background-color: #66FF66;text-align: center;line-height: 20px;border-radius: 4px">N</div>'
        else:
            rt = u' <div title="其他平台侵权" style="float:left;width: 20px;height: 20px;background-color: #FFCC33;text-align: center;line-height: 20px;border-radius: 4px">O</div>'
        return rt

    def chk_budget(self, campaign_id, max_budget):
        '''红色：总预算-总花费<前一天花费
            黄色：7天平均预算<当前几天平均花费
            绿色：7天平均预算>当前几天平均花费
            '''
        color = '#66FF66'
        objs = t_wish_pb_productdailystats.objects.filter(campaign_id=campaign_id, date_flag=0).order_by('-p_date').values_list('spend', flat=True)
        if objs:
            lastspend = objs[0]
            avgspend = sum(objs)/len(objs)
            totalspend = sum(objs)
            avgbudget = float(max_budget)/7.0

            if max_budget - totalspend < lastspend:
                color = 'red'
            elif avgspend > avgbudget:
                color = 'yellow'

        rt = u'<div title="预算预警标识" style="float:left;width: 20px;height: 20px;background-color: %s;text-align: center;line-height: 20px;border-radius: 4px">B</div>'
        return rt % color


    def show_pic(self, obj):

        score = 'None'
        TortInfo = 'N'
        WishExpress = '[]'

        objs = t_online_info_wish_store.objects.filter(ProductID=obj.product_id).values('WishExpress', 'Rating', 'TortInfo')
        if objs.count() > 0:
            if objs[0]['Rating'] is not None:
                score = objs[0]['Rating']
            TortInfo = objs[0]['TortInfo']
            WishExpress = objs[0]['WishExpress']

        # original medium
        url = u'https://contestimg.wish.com/api/webimage/%s-medium.jpg' % str(obj.product_id)
        rt = '<div style="position:relative; width:120px"><img src="%s" width="120" height="120" alt="无法显示" title="%s"/>' \
             '<span style="position:absolute; right:0; top:0; background-color:rgba(0,250,0,0.2); ' \
             'color:red">%s</span></div>' % (url, url, score)

        h_url = u'https://fancyqube-wish.oss-cn-shanghai.aliyuncs.com/badge.png'
        if WishExpress is not None and WishExpress != '[]':
            rt = rt + ' <div style="float:left"><img src="%s"  width="20" height="20"  alt = "%s"  title="%s" /></div>' % (
            h_url, h_url, WishExpress)
        rt = rt + self.tortInfo(TortInfo)

        if obj.campaign_state == 'STARTED':
            rt = rt + self.chk_budget(obj.campaign_id, obj.max_budget)

        return mark_safe(rt)
    show_pic.short_description = mark_safe('<p style="color:#428bca;text-align:center">图片</p>')

    def getanydata(self, productid):
        cursor = connection.cursor()
        sql = '''select Title,ShopName, DateUploaded,Seller,
                if( min(if(Status='Enabled',Price+Shipping,null))=max(if(Status='Enabled',Price+Shipping,null)),
                min(if(Status='Enabled',Price+Shipping,null)), 
                CONCAT_WS('~',min(if(Status='Enabled',Price+Shipping,null)),max(if(Status='Enabled',Price+Shipping,null)))) as Price,
                GROUP_CONCAT(DISTINCT MainSKU) as SKU
                from t_online_info 
                where ProductID='%s' 
                GROUP BY ProductID'''%(productid,)
        cursor.execute(sql)
        anydata = cursor.fetchone()
        cursor.close()
        return anydata

    def save_models(self):
        try:
            obj = self.new_obj
            request = self.request
            post = request.POST
            # 重定向返回页
            if obj.campaign_state is None or obj.campaign_state == '' or obj.dataflag == 1:
                post['_redirect'] = "/Project/admin/skuapp/t_wish_pb_campaignproductstats/?dataflag=1"
            elif obj.dataflag == 2:
                post['_redirect'] = "/Project/admin/skuapp/t_wish_pb_campaignproductstats/?dataflag=2"
            elif obj.dataflag == 3:
                post['_redirect'] = "/Project/admin/skuapp/t_wish_pb_campaignproductstats/?dataflag=3"
            else:
                post['_redirect'] = "/Project/admin/skuapp/t_wish_pb_campaignproductstats/"

            if obj.campaign_state in ('ENDED', 'CANCELLED'):
                messages.warning(request, u'取消或超过截止日期的活动不能更新数据!')
                return

            # 维护联动值
            obj.StaffID = request.user.first_name
            obj.updatetime = datetime.now()
            # 出错时，保留关键词
            request.session['lastkey'] = obj.keywords

            if obj.sku is None:
                v_productid = obj.product_id
                skuinfo = self.getanydata(v_productid)
                if skuinfo is not None:
                    obj.product_name = skuinfo[0]
                    obj.shopname = skuinfo[1]
                    obj.publish_date = skuinfo[2]
                    obj.seller = skuinfo[3]
                    obj.sales_price = skuinfo[4]
                    obj.sku = skuinfo[5]
                    # 大类 服装
                    if obj.sku is not None:
                        v_mainsku = obj.sku.split(',')[0]
                        t = t_product_enter_ed.objects.filter(MainSKU=v_mainsku).values_list('LargeCategory','ClothingSystem1','ClothingSystem2','ClothingSystem3')

                        if len(t) > 0:
                            obj.LargeCategory = t[0][0]
                            obj.ClothingSystem1 = t[0][1]
                            obj.ClothingSystem2 = t[0][2]
                            obj.ClothingSystem3 = t[0][3]

                    if 'add' in request.path:  # 新插入时才需要做更新
                        pid = t_wish_pb.objects.filter(product_id=v_productid)
                        pidcnt = pid.count()

                        obj.campaign_name = v_productid + '_' + str(pidcnt + 1)
                        obj.dataflag = 2 if pidcnt >= 1 else 1
                        if pidcnt == 1 or (pidcnt > 1 and pid[0].dataflag == 3):  # 连续广告FLAG/停止广告重开
                            t_wish_pb.objects.filter(product_id=v_productid).update(dataflag=2)
                else:
                    if obj.shopname is None or obj.shopname.upper().find('WISH') == -1:
                        messages.error(request, u'请填写卖家简称....')
                        post['_redirect'] = request.path
                        return
                    elif 'add' in request.path:  # 新插入时才需要做更新
                        obj.dataflag = 1
                        obj.campaign_name = v_productid + '_1'

            # 处理参数
            access_token = ''
            config_objs = t_config_online_amazon.objects.filter(Name=obj.shopname, K='access_token')
            if config_objs.exists() and config_objs[0].V != '':
                access_token = config_objs[0].V
            else:
                messages.error(self.request, u'%s 没有access_token信息....' % obj.shopname)
                post['_redirect'] = request.path
                return

            param = {}
            param['access_token'] = access_token
            param['max_budget'] = float(obj.max_budget)
            param['auto_renew'] = True if obj.auto_renew == 'True' else False
            param['campaign_name'] = obj.campaign_name
            param['start_date'] = obj.start_time if isinstance(obj.start_time, unicode) else obj.start_time.strftime('%Y-%m-%d')
            param['end_date'] = obj.end_time.strftime('%Y-%m-%d')
            # products
            param['products'] = [{'product_id': obj.product_id, 'bid': float(obj.bid), 'keywords': obj.keywords.split(',')}]

            # 执行广告操作
            if 'add' in request.path:  # 添加
                try:
                    x = CreateCampaign(param)
                    if x['retcode'] == 0:
                        data = x['data']
                        data = data['data']['Campaign']
                        obj.campaign_id = data['campaign_id']
                        obj.campaign_state = data['campaign_state']
                        obj.CreateUser = request.user.first_name
                        messages.info(request, u'广告创建成功,活动ID:' + obj.campaign_id)

                        obj.save()
                        request.session['lastkey'] = ''
                    else:
                        messages.error(request, u'广告创建失败:' + x['data'])
                        post['_redirect'] = request.path
                except Exception, ex:
                    messages.error(request, u'广告创建失败:' + repr(ex))
            else:  # 更新
                try:
                    param['id'] = obj.campaign_id

                    if obj.campaign_state in ('SAVED', 'STARTED'):  # 预设运行中的广告
                        param.pop('auto_renew')
                        param.pop('campaign_name')
                        param.pop('start_date')
                        param['products'][0].pop('bid')
                        x = UpdateCampaign_running(param)
                    else:
                        x = UpdateCampaign(param)   # 新未处理广告
                    if x['retcode'] == 0:
                        data = x['data']
                        data = data['data']['Campaign']
                        obj.campaign_id = data['campaign_id']
                        obj.campaign_state = data['campaign_state']
                        messages.info(request, u'广告更新成功,活动ID:' + obj.campaign_id)

                        obj.save()
                        request.session['lastkey'] = ''
                    else:
                        messages.error(request, u'广告更新失败:' + x['data'])
                        post['_redirect'] = request.path
                except Exception, ex:
                    messages.error(request, u'广告更新失败:' + repr(ex))

        except Exception, ex:
            messages.error(request, 'SysError:' + repr(ex))

    def show_product_detail(self, obj):
        
        access_token = ''
        config_objs = t_config_online_amazon.objects.filter(Name=obj.shopname, K='access_token')
        if config_objs.exists():
            access_token = config_objs[0].V
        else:
            messages.warning(self.request, '%s without access_token info.' % obj.shopname)

        rt = ''
        if obj.campaign_state in ('SAVED', 'STARTED', 'ENDED', 'STOPPED'):
            rt = '<a href="/Project/admin/skuapp/t_wish_pb_productdailystats/' \
                 '?product_id=%s">业绩查看</a>' %(obj.product_id, )

        if obj.campaign_state in ('NEW', 'PENDING', 'SAVED', 'STARTED'):
            rt = '%s<br/><br/><a href="/Project/admin/skuapp/t_wish_pb_campaignproductstats' \
                 '/%s/update/?state=%s">编辑广告</a>' %(rt, obj.id, obj.campaign_state)

        param2 = {}
        param2['pbid'] = obj.id
        param2['id'] = obj.campaign_id
        param2['access_token'] = access_token
        if obj.campaign_state == 'STARTED':
            rt = """%s<br/><br/><a id="stop_%s">停止广告</a>
                 <script>
                $('#stop_%s').click(function(){ if(confirm('确定要停止此广告吗?')){
                $.ajax({url:"/campaign/stop",type:"POST",contentType:"application/x-www-form-urlencoded:charset=UTF-8",dataType:"json",data:%s,
                success:function(data){if(data.result=="OK"){location.reload(); } else {alert('Fail:'+data.result);}},
                error:function(data){alert('Stop Fail:'+data.result);}}
                );
                }})</script>""" % (rt, obj.id, obj.id, json.dumps(param2))

        if obj.campaign_state in ('NEW', 'PENDING', 'SAVED'):
            rt = """%s<br/><br/><a id="cancel_%s">取消广告</a>
                 <script>
                $('#cancel_%s').click(function(){ if(confirm('确定要取消此广告吗?')){
                $.ajax({url:"/campaign/cancel",type:"POST",contentType:"application/x-www-form-urlencoded:charset=UTF-8",dataType:"json",data:%s,
                success:function(data){if(data.result=="OK"){location.reload(); } else {alert('Fail:'+data.result);}},
                error:function(data){alert('Stop Fail:'+data.result);}}
                );
                }})</script>""" % (rt, obj.id, obj.id, json.dumps(param2))

        if obj.campaign_state in ('NEW', 'SAVED', 'STARTED', 'PENDING'):
            rt = "%s<br/></br><a id=addBudget_%s>添加预算</a>" \
                 "<script>$('#addBudget_%s').on('click',function()" \
                 "{layer.open({type:2,skin:'layui-layer-lan',title:'增加预算',fix:false,shadeClose: true,maxmin:true,area:['400px','250px']," \
                 "content:'/campaign/addBudget/?id=%s&access_token=%s&currBudget=%s',});});" \
                 "</script>" % (rt, obj.id, obj.id, obj.campaign_id, access_token, obj.max_budget)

        return mark_safe(rt)
    show_product_detail.short_description = mark_safe('<p style="color:#428bca;text-align:center;width:90px">活动详情</p>')

    def show_sku_detail(self, obj):

        automated = u'<span>自动广告：否</span>' if obj.Automated == 'False' \
                    else u'<span style="color:red">自动广告：是</span>'
        automated += u',&nbsp&nbsp&nbsp&nbsp<span>重复广告: 否</span>' if obj.auto_renew == 'False' \
                    else u',&nbsp&nbsp&nbsp&nbsp<span style="color:green">重复广告: 是</span>'

        if obj.sku and obj.sku.find(',') >= 0:
            mainsku = """<script type="text/javascript">
            $(document).ready(function(){
              $("#but_msku%s").click(function(){
              $("#dmsku%s").toggle();
              $("#ddmsku%s").toggle();
              });
            });
            </script>
            <p id="dmsku%s" style="float:left">主SKU:%s &nbsp</p>
            <p id="ddmsku%s" hidden="hidden" style="float:left">主SKU:%s &nbsp</p>
            <button type="button" id="but_msku%s" style="width:40px;height:20px;">更多</button>       
            """%(obj.id, obj.id, obj.id, obj.id, obj.sku[:obj.sku.find(',')], obj.id, obj.sku, obj.id)

            rt = u"活动ID:%s<br>产品ID:%s<br>%s<br>刊登时间:%s<br>卖家简称:%s<br>店长/销售员:%s<br>广告创建人:%s<br>%s" % (
                obj.campaign_id, obj.product_id, mainsku, obj.publish_date, obj.shopname, obj.seller, obj.CreateUser, automated)
        else:
            rt = u"活动ID:%s<br>产品ID:%s<br>主SKU:%s<br>刊登时间:%s<br>卖家简称:%s<br>店长/销售员:%s<br>广告创建人:%s<br>%s" % (
                obj.campaign_id,obj.product_id,obj.sku,obj.publish_date,obj.shopname,obj.seller,obj.CreateUser,automated)

        return mark_safe(rt)
    show_sku_detail.short_description = mark_safe('<p style="color:#428bca;text-align:center">详情</p>')

    def show_campaign_date(self, obj):
        rt = u"开始时间:<br>%s<br>结束时间:<br>%s" % (obj.start_time, obj.end_time)
        return mark_safe(rt)
    show_campaign_date.short_description = mark_safe('<p style="color:#428bca;text-align:center;width:80px">活动时间</p>')

    def show_sales_paid(self, obj):
        rt = u'<font color="red">%s</font>' % (obj.sales_paid, )
        return mark_safe(rt)
    show_sales_paid.short_description = mark_safe('<p style="color:red;text-align:center">曝光转化率</p>')

    def show_keywords(self, obj):

        l = obj.keywords.split(',')
        value = '<div>'
        for i in range(len(l) - 1):
            value += '<p>' + l[i] + ',</p>'
        value += '<p>' + l[len(l) - 1] + '</p>' + '</div>'

        if value == '<div><p></p></div>':
            value = ''

        rt = value
        if obj.campaign_state in ('NEW', 'SAVED', 'STARTED', 'PENDING') and rt != '' :

            access_token = ''
            config_objs = t_config_online_amazon.objects.filter(Name=obj.shopname, K='access_token')
            if config_objs.exists():
                access_token = config_objs[0].V
            else:
                messages.warning(self.request, '%s without access_token info.' % obj.shopname)

            rt = value+"<br><a id=translation_%s>翻译</a>" \
                       "<script>$('#translation_%s').on('click',function()" \
                       "{layer.open({type:2,skin:'layui-layer-lan',title:'翻译',fix:false,shadeClose: true,maxmin:true,area:['400px','250px']," \
                       '''content:"/campaign/translation/?id=%s&keywords=%s&access_token=%s",});});''' \
                       "</script>" % (obj.id, obj.id, obj.id, obj.keywords,access_token)
        return mark_safe(rt)
    show_keywords.short_description = mark_safe('<p style="color:#428bca;text-align:center;width:120px">关键词</p>')

    def getparam(self, obj):

        # if obj.auto_renew == 'True' and obj.campaign_state == 'STARTED':
        #     messages.error(self.request, u'%s 已是重复活动,请勿重复设置.' % obj.campaign_id)
        #     return {}

        access_token = ''
        config_objs = t_config_online_amazon.objects.filter(Name=obj.shopname, K='access_token')
        if config_objs.exists() and config_objs[0].V != '':
            access_token = config_objs[0].V
        else:
            messages.error(self.request, u'%s 没有access_token信息.' % obj.campaign_id)
            return {}

        param = {}
        param['access_token'] = access_token
        param['max_budget'] = float(obj.max_budget)
        param['auto_renew'] = True  #默认重复
        param['campaign_name'] = obj.campaign_name
        # products
        param['products'] = [{'product_id': obj.product_id, 'bid': float(obj.bid), 'keywords': obj.keywords.split(',')}]

        # 对活动时间段的处理
        ttoday = date.today()
        x = datetime.now().strftime('%H:%M:%S')
        if obj.campaign_state in ('STARTED', 'SAVED'):
            end_time = datetime.strptime(obj.end_time, '%Y-%m-%d').date()
            end_time_1 = end_time - timedelta(days=1)

            if ttoday < end_time_1:
                param['start_date'] = end_time.strftime('%Y-%m-%d')
                param['end_date'] = (end_time + timedelta(days=7)).strftime('%Y-%m-%d')
            else:  # 正好是结束那天或前一天
                if x >= '15:00:00':
                    param['start_date'] = (ttoday + timedelta(days=2)).strftime('%Y-%m-%d')
                    param['end_date'] = (ttoday + timedelta(days=9)).strftime('%Y-%m-%d')
                else:
                    param['start_date'] = (ttoday + timedelta(days=1)).strftime('%Y-%m-%d')
                    param['end_date'] = (ttoday + timedelta(days=8)).strftime('%Y-%m-%d')
        else:  # ENDED STOPPED
            if x >= '15:00:00':
                param['start_date'] = (ttoday + timedelta(days=2)).strftime('%Y-%m-%d')
                param['end_date'] = (ttoday + timedelta(days=9)).strftime('%Y-%m-%d')
            else:
                param['start_date'] = (ttoday + timedelta(days=1)).strftime('%Y-%m-%d')
                param['end_date'] = (ttoday + timedelta(days=8)).strftime('%Y-%m-%d')

        return param

    actions = ['move_to_stoplist', 'repeat_campaign', ]
    def move_to_stoplist(self, request, objs):
        cnt = 0
        for obj in objs:
            try:
                productid = obj.product_id
                t_wish_pb.objects.filter(product_id=productid).update(dataflag=3, StaffID=request.user.first_name, updatetime=datetime.now())
                cnt += 1
            except Exception, e:
                messages.error(request, repr(e))
                continue

        messages.info(request, u'移动%d条,成功完成%d条.' % (objs.count(), cnt))

    move_to_stoplist.short_description = u'移到停止广告列表'

    def repeat_campaign(self, request, objs):
        cnt = 0
        for obj in objs:
            try:
                if obj.campaign_state not in ('STARTED', 'ENDED', 'STOPPED', 'SAVED'):
                    messages.error(request, u'此活动%s状态为%s,暂不支持重复活动.'%(obj.campaign_id, obj.get_campaign_state_display(),))
                    continue

                param = self.getparam(obj)
                if not param:
                    continue

                try:
                    x = CreateCampaign(param)
                    if x['retcode'] == 0:
                        data = x['data']
                        data = data['data']['Campaign']

                        v_dataflag = obj.dataflag
                        if v_dataflag in (1, 3):
                            v_dataflag = 2
                            t_wish_pb.objects.filter(product_id=obj.product_id).update(dataflag=2)

                        t_wish_pb.objects.create(
                        shopname = obj.shopname,
                        campaign_id = data['campaign_id'],
                        campaign_name = obj.campaign_name,
                        product_id = obj.product_id,
                        product_name = obj.product_name,
                        keywords = obj.keywords,
                        bid = obj.bid,
                        max_budget = obj.max_budget,
                        start_time = param['start_date'],
                        end_time = param['end_date'],
                        auto_renew = str(param['auto_renew']),
                        campaign_state = data['campaign_state'],
                        sku = obj.sku,
                        publish_date = obj.publish_date,
                        sales_price = obj.sales_price,
                        seller = obj.seller,
                        LargeCategory = obj.LargeCategory,
                        ClothingSystem1 = obj.ClothingSystem1,
                        ClothingSystem2 = obj.ClothingSystem2,
                        ClothingSystem3 = obj.ClothingSystem3,
                        operation_remark = u'重复活动',
                        StoreName = obj.StoreName,
                        dataflag = v_dataflag,
                        StaffID = request.user.first_name,
                        CreateUser = request.user.first_name,
                        updatetime = datetime.now()
                        )

                        cnt += 1
                    else:
                        messages.error(request, u'%s创建重复广告失败:%s'% (obj.campaign_id, x['data']))
                except Exception, ex:
                    messages.error(request, u'%s创建重复广告失败:%s'% (obj.campaign_id, repr(ex)))

            except Exception, e:
                messages.error(request, repr(e))
                continue

        messages.info(request, u'选择%d条,成功创建%d条.' % (objs.count(), cnt))

    repeat_campaign.short_description = u'创建重复活动'

    def get_readonly_fields(self):

        fields = super(t_wish_pb_campaignproductstats_Admin, self).get_readonly_fields()

        request = self.request

        campaign_state = request.GET.get('state', '')
        if campaign_state in ('SAVED', 'STARTED'):
            fields = ['shopname', 'product_id', 'start_time', 'auto_renew', 'bid', ]
        elif campaign_state in ('NEW', 'PENDING'):
            fields = ['shopname', ]

        return fields

    list_display_links = ('id',)
    list_display = ('campaign_state', 'show_pic', 'show_sku_detail', 'sales_price', 'bid', 'max_budget',
                    'spend', 'paid_impressions', 'sales', 'gmv', 'spend_gmv', 'sales_paid',
                    'show_campaign_date', 'show_keywords', 'survey_remark', 'operation_remark', 'show_product_detail',)

    list_editable = {'survey_remark', 'operation_remark', 'StoreName'}
    '''list_editable = ('product_id', 'keywords', 'bid', 'max_budget', 'start_time', 'end_time',
                     'auto_renew', 'survey_remark', 'operation_remark')'''

    fields = ('shopname', 'product_id', 'max_budget', 'bid', 'start_time', 'end_time',
              'auto_renew', 'StoreName', 'keywords', 'survey_remark', 'operation_remark'
              )

    form_layout = (
        Fieldset(u'选填信息', Row('shopname')
                 ),
        Fieldset(u'关键信息',
            Row('product_id'),
            Row('max_budget'),
            Row('bid'),
            Row('auto_renew', 'StoreName'),
            Row('start_time', 'end_time'),
            Row('survey_remark', 'operation_remark'),
            css_class='unsort'
        ),
        Fieldset(u'关键词建议', Row('keywords'))
    )

    def getPid_byRating(self, rstart, rend):
        if not rstart and not rend:
            return False
        s1 = {}
        if rstart:
            s1['Rating__gte'] = rstart
        if rend:
            s1['Rating__lte'] = rend

        objs = wish_score.objects.filter(**s1).values('ProductID').distinct()
        if objs.count() == 0:
            return False
        else:
            pids = [obj['ProductID'] for obj in objs]
            return pids

    def getfallpid(self, fall):
        cursor = connection.cursor()
        sql = 'select campaign_id from t_wish_pb_fall_log where fall=%s'% fall
        cursor.execute(sql)
        if cursor.rowcount > 0:
            x = cursor.fetchall()
            x = [y[0] for y in x]
        else:
            x = []

        cursor.close()
        return x


    def get_list_queryset(self):
        request = self.request
        qs = super(t_wish_pb_campaignproductstats_Admin, self).get_list_queryset()
        
        if request.session.get('mycampaign_id', False):
            del request.session['mycampaign_id']
        
        request.session['back_ref'] = request.get_full_path()

        dataflag = request.GET.get('dataflag', '')
        seller = request.GET.get('seller', '')
        createuser = request.GET.get('createuser', '')
        keywords = request.GET.get('keywords', '')
        surveyremark = request.GET.get('surveyremark', '')
        largecategory = request.GET.get('largecate', '')
        cate1 = request.GET.get('cate1', '')
        cate2 = request.GET.get('cate2', '')
        cate3 = request.GET.get('cate3', '')
        cate1 = '' if cate1 == '0' else cate1
        cate2 = '' if cate2 == '0' else cate2
        cate3 = '' if cate3 == '0' else cate3

        campaign_state = request.GET.get('campaign_state', '')
        campaign_state = '' if campaign_state == '' else campaign_state.split(',')

        campaign_id = request.GET.get('campaign_id', '')
        campaign_id = '' if campaign_id == '' else campaign_id.split(',')

        product_id = request.GET.get('product_id', '')
        product_id = '' if product_id == '' else product_id.split(',')
        # 评分的筛选
        rating_Start = request.GET.get('rating_Start', '')
        rating_End = request.GET.get('rating_End', '')
        pids = self.getPid_byRating(rating_Start, rating_End)
        if pids:
            if isinstance(product_id, list):
                product_id = list(set(product_id).intersection(set(pids)))
            else:
                product_id = pids
        # 是否跌停的筛选
        isFall = request.GET.get('isFall', '')
        if isFall:
            cids = self.getfallpid(isFall)
            if isinstance(campaign_id, list):
                campaign_id = list(set(campaign_id).intersection(set(cids)))
            else:
                campaign_id = cids

        SKU = request.GET.get('SKU', '')
        SKU = '' if SKU == '' else SKU.split(',')

        automated = request.GET.get('automated', '')
        auto_renew = request.GET.get('auto_renew', '')

        shopname = request.GET.get('Shopname', '')
        shopname = '' if shopname == '' else shopname.split(',')

        spend_gmv_Start = request.GET.get('spend_gmv_Start', '')
        spend_gmv_End = request.GET.get('spend_gmv_End', '')
        expose_Start = request.GET.get('expose_Start', '')
        expose_End = request.GET.get('expose_End', '')
        time_Start = request.GET.get('time_Start', '')
        time_End = request.GET.get('time_End', '')
        budget_Start = request.GET.get('budget_Start', '')
        budget_End = request.GET.get('budget_End', '')
        paid_Start = request.GET.get('paid_Start', '')
        paid_End = request.GET.get('paid_End', '')
        sales_Start = request.GET.get('sales_Start', '')
        sales_End = request.GET.get('sales_End', '')
        gmv_Start = request.GET.get('gmv_Start', '')
        gmv_End = request.GET.get('gmv_End', '')
        spend_Start = request.GET.get('spend_Start', '')
        spend_End = request.GET.get('spend_End', '')
        pub_Start = request.GET.get('pubtime_Start', '')
        pub_End = request.GET.get('pubtime_End', '')

        searchList = {'dataflag__exact': dataflag,
                      'seller__exact': seller,
                      'CreateUser__exact': createuser,
                      'Automated__exact': automated,
                      'auto_renew__exact': auto_renew,

                      'LargeCategory__exact': largecategory,
                      'ClothingSystem1__exact': cate1,
                      'ClothingSystem2__exact': cate2,
                      'ClothingSystem3__exact': cate3,

                      'shopname__in': shopname,
                      'keywords__icontains': keywords,
                      'survey_remark__icontains': surveyremark,
                      'sku__in': SKU,
                      'campaign_id__in': campaign_id,
                      'product_id__in': product_id,
                      'campaign_state__in': campaign_state,

                      'spend_gmv__gte': spend_gmv_Start,
                      'spend_gmv__lte': spend_gmv_End,

                      'sales_paid__gte': expose_Start,
                      'sales_paid__lte': expose_End,

                      'start_time__gte': time_Start,
                      'start_time__lt': time_End,

                      'max_budget__gte': budget_Start,
                      'max_budget__lte': budget_End,

                      'paid_impressions__gte': paid_Start,
                      'paid_impressions__lte': paid_End,

                      'sales__gte': sales_Start,
                      'sales__lte': sales_End,

                      'gmv__gte': gmv_Start,
                      'gmv__lte': gmv_End,

                      'spend__gte': spend_Start,
                      'spend__lte': spend_End,

                      'publish_date__gte': pub_Start,
                      'publish_date__lt': pub_End,
                      }

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
                ordercol = request.GET.get('o', '')
                if 'sales_price' in ordercol:
                    ordercol = ordercol.replace('sales_price', 'sales_price1').split('.')
                    qs = qs.extra(select={'sales_price1': 'CAST(sales_price as DECIMAL(6,2))'}).order_by(*ordercol)

            except Exception, ex:
                messages.error(request, u'输入的查询数据有误！')

        return qs
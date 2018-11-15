#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_wish_pb_earnings_show_Admin.py
 @time: 2018-07-23 10:58
"""
from django.db import connection
from django.contrib import messages
from django.utils.safestring import mark_safe
from skuapp.table.t_wish_pb_earnings_rep import t_wish_pb_earnings_show, t_wish_pb_earnings_meta
from skuapp.table.t_wish_pb_campaignproductstats import t_wish_pb_campaignproductstats as t_wish_pb
from skuapp.table.t_product_enter_ed import t_product_enter_ed as largeCls
from skuapp.table.t_online_info import t_online_info

class t_wish_pb_earnings_show_Admin(object):
    t_wish_pb_left_menu = True
    search_box_flag = True
    t_wishpb_repdesc_flag = True

    def show_pic(self, obj):
        # original medium
        url = u'https://contestimg.wish.com/api/webimage/%s-medium.jpg' % str(obj.product_id)
        if obj.product_id == u'合计':
            rt = '--'
        else:
            rt = '<img src="%s" width="120" height="120" alt="无法显示" title="%s"/>'% (url, url,)

        return mark_safe(rt)
    show_pic.short_description = mark_safe('<p style="color:#428bca;text-align:center">图片</p>')

    list_display_links = ('id',)
    list_display = ('show_pic', 'product_id', 'pbgmv', 'spend', 'grossprofit', 'gmv', 'earning', 'totearning')

    def check_param(self):

        request = self.request

        currentparam = dict(request.GET)
        if 'o' in currentparam:
            del currentparam['o']
        elif 'p' in currentparam:
            del currentparam['p']

        lastparam = request.session.get('lastparam', False)
        if not lastparam:
            request.session['lastparam'] = currentparam
            return False
        else:
            result = cmp(lastparam, currentparam)

            if result == 0:
                return True
            else:
                request.session['lastparam'] = currentparam
                request.session.set_expiry(3600)
                return False

    def get_list_queryset(self):
        request = self.request
        qs = super(t_wish_pb_earnings_show_Admin, self).get_list_queryset()

        username = request.user.username
        oo = request.GET.get('o', '')
        pp = request.GET.get('p', '')

        if len(request.GET) == 0 or (len(request.GET) == 1 and (oo != '' or pp != '')):
            qs = t_wish_pb_earnings_show.objects.filter(username='default')  # 默认
            if oo != '':  # 点了排序
                oo = oo.split('.')
                qs = qs.order_by(*oo)
            return qs

        elif self.check_param():
            qs = t_wish_pb_earnings_show.objects.filter(username=username)   # 不用重新统计，提高性能
            if oo != '':  # 点了排序
                oo = oo.split('.')
                qs = qs.order_by(*oo)
            return qs

        product_id = []
        mainSKU = []

        x = request.GET.get('product_id', '')
        if x != '':
            product_id.extend(x.split(','))

        else:
            y = request.GET.get('mainSKU', '')
            if y != '':
                mainSKU.extend(y.split(','))

            largecate = request.GET.get('largecate', '')
            if largecate != '':
                y = largeCls.objects.filter(LargeCategory=largecate).values_list('MainSKU')
                z = [obj[0] for obj in y]
                if len(mainSKU) > 0:
                    mainSKU = list(set(mainSKU).intersection(set(z)))   # 取交集
                else:
                    mainSKU = z

            ss = {}
            seller = request.GET.get('seller', '')
            pubtime_Start = request.GET.get('pubtime_Start', '')
            pubtime_End = request.GET.get('pubtime_End', '')
            CreateUser = request.GET.get('CreateUser', '')
            if len(mainSKU) > 0:
                ss['MainSKU__in'] = mainSKU
            if seller != '':
                ss['seller__exact'] = seller
            if pubtime_Start != '':
                ss['DateUploaded__gte'] = pubtime_Start
            if pubtime_End != '':
                ss['DateUploaded__lt'] = pubtime_End

            if len(ss) > 0:
                x = t_online_info.objects.filter(**ss).values_list('ProductID')
                z = [obj[0] for obj in x]
                product_id.extend(z)

            if CreateUser != '':
                x = t_wish_pb.objects.filter(CreateUser=CreateUser).values_list('product_id')
                z = [obj[0] for obj in x]
                if len(product_id) > 0:
                    product_id = list(set(product_id).intersection(set(z)))  # 取交集
                else:
                    product_id = z

        dealdate_Start = request.GET.get('dealdate_Start', '')
        dealdate_End = request.GET.get('dealdate_End', '')

        where = 'where'

        if len(product_id) > 0:
            where += ' product_id in ('+str(product_id)[1:-1].replace('u', '')+')'
        if dealdate_Start != '':
            if where == 'where':
                where += " p_date>='%s'" % dealdate_Start
            else:
                where += " and p_date>='%s'" % dealdate_Start
        if dealdate_End != '':
            if where == 'where':
                where += " p_date<'%s'" % dealdate_End
            else:
                where += " and p_date<'%s'" % dealdate_End
        try:
            #   过滤
            if where == 'where':
                qs = t_wish_pb_earnings_show.objects.filter(username='none')       #取空行
            else:
                #   聚合
                sql = '''select product_id,sum(if(date_flag=0,gmv,0)) as pbgmv,sum(spend) as spend, 
                        sum(if(date_flag=0,grossprofit,0)) as grossprofit,
                        sum(if(date_flag=1,gmv,0)) as gmv,
                        sum(if(date_flag=1,grossprofit,0)) as earning,
                        sum(grossprofit) as totearning
                        from t_wish_pb_earnings_rep 
                        %s group by product_id
                        union all 
                        select '合计' as product_id,sum(if(date_flag=0,gmv,0)) as pbgmv,sum(spend) as spend, 
                        sum(if(date_flag=0,grossprofit,0)) as grossprofit,
                        sum(if(date_flag=1,gmv,0)) as gmv,
                        sum(if(date_flag=1,grossprofit,0)) as earning,
                        sum(grossprofit) as totearning
                        from t_wish_pb_earnings_rep
                        %s
                        ''' % (where, where)

                cursor = connection.cursor()
                cursor.execute(sql)
                objs = cursor.fetchall()
                cursor.close()

                #   删除
                t_wish_pb_earnings_show.objects.filter(username=username).delete()

                earnings_showlist = [t_wish_pb_earnings_show(product_id=obj[0],
                                                             pbgmv=obj[1],
                                                             spend=obj[2],
                                                             grossprofit=obj[3],
                                                             gmv=obj[4],
                                                             earning=obj[5],
                                                             totearning=obj[6],
                                                             username=username) for obj in objs]
                #   重建
                t_wish_pb_earnings_show.objects.bulk_create(earnings_showlist)
                #   查询
                qs = t_wish_pb_earnings_show.objects.filter(username=username)

            #   排序
            if oo != '':  # 点了排序
                oo = oo.split('.')
                qs = qs.order_by(*oo)
            else:
                qs = qs.order_by('-totearning')

        except Exception, ex:
            messages.error(request, 'err:%s' % repr(ex))

        return qs
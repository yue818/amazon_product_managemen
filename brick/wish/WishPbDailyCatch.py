#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: WishPbDailyCatch.py
 @time: 2018-06-01 17:34
"""
import requests
import pymysql
import datetime
from brick.function.updatetasklog import updatetasklog

sql_campaignproductstats = """
INSERT INTO t_wish_pb_campaignproductstats(shopname, campaign_id, campaign_name, product_id, product_name, paid_impressions, spend, sales, gmv, 
last_updated_time, keywords, bid, max_budget, start_time, end_time, auto_renew, campaign_state, spend_gmv, sales_paid, automated) 
VALUES %s
ON DUPLICATE KEY UPDATE 
paid_impressions=VALUES(paid_impressions),
spend=VALUES(spend),
sales=VALUES(sales),
gmv=VALUES(gmv),
last_updated_time=VALUES(last_updated_time),
keywords=VALUES(keywords),
bid=VALUES(bid),
max_budget=VALUES(max_budget),
start_time=VALUES(start_time),
end_time=VALUES(end_time),
auto_renew=VALUES(auto_renew),
campaign_state=VALUES(campaign_state),
spend_gmv=VALUES(spend_gmv),
sales_paid=VALUES(sales_paid),
updatetime=sysdate();"""

sql_productdailystats = """
INSERT INTO t_wish_pb_productdailystats(campaign_id, product_id, p_date, date_flag, impressions, sales, gmv, spend, paid_impressions) 
VALUES %s
ON DUPLICATE KEY UPDATE 
campaign_id=VALUES(campaign_id),
paid_impressions=VALUES(paid_impressions),
spend=VALUES(spend),
sales=VALUES(sales),
gmv=VALUES(gmv),
impressions=VALUES(impressions),
date_flag=VALUES(date_flag),
updatetime=sysdate();"""

sql_updatecancell = """update t_wish_pb_campaignproductstats set campaign_state='CANCELLED', updatetime=sysdate()
where campaign_id in (%s);"""

today = datetime.date.today().strftime('%Y-%m-%d')
yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

def catchExcept(func):
    def wrapper(param, timeout=30):
        try:
            r = func(param, timeout)
            if r.status_code == requests.codes.ok:
                t = r.json()
                if t['code'] == 0:
                    return {'retcode': 0, 'data': t}
                else:  # 返回错误
                    return {'retcode': -1, 'data': t['message']}
            else:  # 连接错误
                if r.status_code == 400:
                    t = r.json()
                    return {'retcode': -1, 'data': t['message']}
                else:
                    return {'retcode': -1, 'data': 'status_code:%s' % (r.status_code,)}

        except Exception, e:  # 系统错误
            return {'retcode': -1, 'data': repr(e)}

    return wrapper


# 抓取活动列表
@catchExcept
def getListCampaigns(param, timeout=30):
    URL = 'https://merchant.wish.com/api/v2/product-boost/campaign/multi-get'
    r = requests.get(URL, params=param, timeout=timeout)
    return r


# 抓取活动下每个产品的表现
@catchExcept
def getProductPerformance(param, timeout=30):
    URL = 'https://merchant.wish.com/api/v2/product-boost/campaign/get-product-stats'
    r = requests.get(URL, params=param, timeout=timeout)
    return r


# 抓取活动下产品每日表现
@catchExcept
def getProductDailyStats(param, timeout=30):
    URL = 'https://merchant.wish.com/api/v2/product-boost/campaign/get-product-daily-stats'
    r = requests.get(URL, params=param, timeout=timeout)
    return r


def get_products_bid(data):
    ps_bid = {}

    for v in data:
        x = v['Product']
        ps_bid[x['product_id']] = x['merchant_bid_rate']

    return ps_bid


def format_v(data):
    t=data[1:-1]
    t=t.replace("u'","'")
    t = t.replace("None", "Null")

    return t


# spend_gmv, sales_paid
def get_spend_gmv(spend, gmv):
    spend = float(spend)
    gmv = float(gmv)
    if spend == 0.0 or spend is None:
        rt = 0.00
    elif gmv == 0.0 or gmv is None:
        rt = None
    else:
        x = round(spend / gmv * 100, 2)
        rt = '%.2f' % (x,)

    return rt


def get_sales_paid(sales, paid):
    sales = float(sales)
    paid = float(paid)
    if sales == 0.0 or sales is None:
        rt = 0.000
    elif paid == 0.0 or paid is None:
        rt = None
    else:
        x = round(sales/paid * 100, 3)
        rt = '%.3f' % (x,)

    return rt


def check_ifrun(state, edate):
    if state in ('NEW', 'SAVED', 'STARTED', 'STOPPED', 'PENDING'):
        return True
    elif state == 'ENDED':
        if edate[:10] in (today, yesterday):
            return True
        else:
            return False
    else:  # CANCELLED
        return True

def analy_ProductPerformance(param, ps_bid, temp_para):
    pperformance = []

    x = getProductPerformance(param)
    if x['retcode'] == 0:
        try:
            data = x['data']['data']
            campaign_id = param['id']
            shopname = temp_para['shopname']
            max_budget = temp_para['max_budget']
            start_time = temp_para['start_time'][:10]
            end_time = temp_para['end_time'][:10]
            auto_renew = temp_para['auto_renew']
            campaign_state = temp_para['campaign_state']
            campaign_name = temp_para['campaign_name']
            automated = temp_para['automated']

            for v in data:
                vv = v['ProductStat']
                spend_gmv = get_spend_gmv(vv['spend'], vv['gmv'])
                sales_paid = get_sales_paid(vv['sales'], vv['paid_impressions'])
                pp = (
                shopname, campaign_id, campaign_name, vv['product_id'], vv['product_name'], vv['paid_impressions'],
                vv['spend'],
                vv['sales'], vv['gmv'], vv['last_updated_time'], ','.join(vv['keywords']), ps_bid[vv['product_id']],
                max_budget, start_time, end_time, auto_renew, campaign_state, spend_gmv, sales_paid, automated
                )

                pperformance.append(pp)

            return (1, pperformance)
        except Exception, ex:
            return (-1, repr(ex))
    else:
        return (-1, x['data'])


def analy_ProductDailyStats(param, ps_bid):
    cperformance = []

    fspend = lambda x: round(float(x), 4)

    for pid in ps_bid.keys():
        param['product_id'] = pid
        x = getProductDailyStats(param)
        if x['retcode'] == 0:
            try:
                data = x['data']['data']
                campaign_id = param['campaign_id']
                st = data['Statistics']

                '''before_campaign = st['before_campaign']
                for v in before_campaign:
                    vv = v['ProductDailyStatistics']
                    cp = (campaign_id, pid, vv['date'], -1, vv['total_impressions'], vv['sales'], vv['gmv'],
                          fspend(vv['spend']), vv['paid_impressions'])
                    cperformance.append(cp)'''

                campaign = st['campaign']
                for v in campaign:
                    vv = v['ProductDailyStatistics']
                    cp = (campaign_id, pid, vv['date'], 0, vv['total_impressions'], vv['sales'], vv['gmv'],
                          fspend(vv['spend']), vv['paid_impressions'])
                    cperformance.append(cp)

                after_campaign = st['after_campaign']
                for v in after_campaign:
                    vv = v['ProductDailyStatistics']
                    cp = (campaign_id, pid, vv['date'], 1, vv['total_impressions'], vv['sales'], vv['gmv'],
                          fspend(vv['spend']), vv['paid_impressions'])
                    cperformance.append(cp)
            except Exception, ex:
                return (-1, repr(ex))
        else:
            return (-1, x['data'])

    return (1, cperformance)


# 解析活动列表
def analy_ListCampaigns(shopname, param):
    x = getListCampaigns(param)

    if x['retcode'] == 0:
        data = x['data']
        data = data['data']

        if len(data)==0:
            return {'shopname':shopname, 'info':'none data'}

        Performance, DailyStats, CancellID = [], [], []
        for d in data:
            campaign = d['Campaign']
            if check_ifrun(campaign['campaign_state'], campaign['end_time']):
                # print shopname, campaign['campaign_id'], campaign['campaign_state'], campaign['start_time'], campaign['end_time']

                ps_bid = get_products_bid(campaign['products'])  # 要价信息
                temp_para = {'shopname': shopname, 'start_time': campaign['start_time'],
                             'end_time': campaign['end_time'], 'campaign_name': campaign['campaign_name'],
                             'auto_renew': campaign['auto_renew'], 'campaign_state': campaign['campaign_state'],
                             'max_budget': campaign['campaign_max_budget'], 'automated': campaign['is_automated_campaign']}

                # 抓取表现信息
                if campaign['campaign_state'] == 'CANCELLED': 
                    CancellID.append(campaign['campaign_id'])
                else:
                    _param={'access_token':param['access_token'],'id':campaign['campaign_id']}
                    x=analy_ProductPerformance(_param, ps_bid, temp_para)
                    if x[0]==1:
                        Performance.extend(x[1])
                    else:
                        print 'Performance', campaign['campaign_id'], x[1]

                if campaign['campaign_state'] not in ('NEW', 'CANCELLED'):
                    _param = {'access_token': param['access_token'], 'campaign_id': campaign['campaign_id']}
                    y = analy_ProductDailyStats(_param, ps_bid)
                    if y[0] == 1:
                        DailyStats.extend(y[1])
                    else:
                        print 'DailyStats', campaign['campaign_id'], y[1]


        return {'shopname':shopname, 'info':'OK', 'Performance':Performance, 'DailyStats':DailyStats, 'CancellID':CancellID }
    else:
        return {'shopname':shopname, 'info':x['data']}


# 多线程
def open_multi_threaded(async_pool, funcname, param):
    results = []

    stime = param['start_time']
    limit = param['limit']
    vlist = param['vlist']

    for shopname, access_token in vlist:
        _param = {'start_time': stime}
        _param['limit'] = limit
        _param['access_token'] = access_token
        result = async_pool.apply_async(funcname, (shopname, _param,))
        # result = funcname(shopname, _param,)
        results.append(result)

    for res in results:
        res.wait()  # 等待线程函数执行完毕
    return results


# 主程序
def run_wishpb():

    from multiprocessing.dummy import Pool as ThreadPool
    taskid = ''
    try:
        onlineConn = pymysql.connect(user="by15161458383", passwd="K120Esc1",
                                     host="rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com", db="hq_db", port=3306,
                                     charset='utf8')

        taskid = updatetasklog(conn=onlineConn, exectype=1)

        cursor1 = onlineConn.cursor()
        cursor2 = onlineConn.cursor()

        num = 40
        stime = (datetime.date.today() - datetime.timedelta(days=8)).strftime('%Y-%m-%d')
        async_pool = ThreadPool(processes=num)
        # and name='Wish-0531' order by 1 LIMIT %s,%s
        cnt = 0
        SQL='''select Name,V 
        from t_config_online_amazon 
        where K='access_token' and V !=''
        order by 1 LIMIT %s,%s '''
        '''and name in (select  shopname from t_wish_pb_campaignproductstats where campaign_state in ('NEW','SAVED','STARTED','STOPPED')) order by 1 LIMIT %s,%s'''
        cursor1.execute(SQL % (cnt, num,))

        while cursor1.rowcount > 0:

            vlist = cursor1.fetchall()
            param = {'start_time': stime, 'limit': 200, 'vlist': vlist}
            results = open_multi_threaded(async_pool, analy_ListCampaigns, param)

            for i in results:
                if i.ready() and i.successful(): # 线程函数是否已经启动了
                    restat = i.get() #{'shopname':shopname, 'info':'OK', 'Performance':Performance, 'DailyStats':DailyStats}
                    if restat['info'] == 'OK':
                        Performance = restat['Performance']
                        DailyStats = restat['DailyStats']
                        CancellID = restat['CancellID']

                        if len(Performance) > 0:
                            v_pperformance=format_v(str(Performance))
                            cursor2.execute(sql_campaignproductstats%(v_pperformance,))

                            if len(DailyStats) > 0:
                                v_cperformance=format_v(str(DailyStats))
                                cursor2.execute(sql_productdailystats%(v_cperformance,))
                        else:
                            print restat['shopname'],'performance empty.'

                        if len(CancellID) > 0:
                            v_cancellid=format_v(str(CancellID))
                            cursor2.execute(sql_updatecancell%(v_cancellid,))

                    else:
                        print restat['shopname'], restat['info']

            onlineConn.commit()
            cnt += num
            cursor1.execute(SQL % (cnt, num,))

        cursor2.execute('call p_update_t_wish_pb_campaign()')  # 更新相关SKU INFO

        updatetasklog(conn=onlineConn, taskid=taskid, exectype=2)
        onlineConn.commit()
        cursor1.close()
        cursor2.close()
        onlineConn.close()
    except Exception, ex:
        updatetasklog(conn=onlineConn, taskid=taskid, exectype=3, msg=repr(ex))


# 执行
if __name__ == '__main__':
    run_wishpb()



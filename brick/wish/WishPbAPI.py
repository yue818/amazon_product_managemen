#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: WishPbAPI.py
 @time: 2018-05-26 9:10
"""

import requests
import json

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
                    return {'retcode': -1, 'data': 'status_code:%s'%(r.status_code, )}

        except Exception, e:  # 系统错误
            return {'retcode': -1, 'data': repr(e)}

    return wrapper

# 创建广告
@catchExcept
def CreateCampaign(param, timeout=30):
    URL = 'https://merchant.wish.com/api/v2/product-boost/campaign/create?access_token=%s'
    access_token = param.pop('access_token')
    url = URL % access_token
    r = requests.post(url, data=json.dumps(param), timeout=timeout)
    return r

# 更新广告
@catchExcept
def UpdateCampaign(param, timeout=30):
    URL = 'https://merchant.wish.com/api/v2/product-boost/campaign/update?access_token=%s'
    access_token = param.pop('access_token')
    url = URL % access_token
    r = requests.post(url, data=json.dumps(param), timeout=timeout)
    return r

# 停止广告
@catchExcept
def StopCampaign(param, timeout=30):
    URL = 'https://merchant.wish.com/api/v2/product-boost/campaign/stop?access_token={0}&id={1}'
    url = URL.format(param['access_token'], param['id'])
    r = requests.post(url, timeout=timeout)
    return r

# 取消广告
@catchExcept
def CancelCampaign(param, timeout=30):
    URL = 'https://merchant.wish.com/api/v2/product-boost/campaign/cancel?access_token={0}&id={1}'
    url = URL.format(param['access_token'], param['id'])
    r = requests.post(url, timeout=timeout)
    return r

# 查询关键词
@catchExcept
def getKeyWords(param, timeout=30):
    URL = 'https://merchant.wish.com/api/v2/product-boost/keyword/search?access_token=%s'
    access_token = param.pop('access_token')
    url = URL % access_token
    r = requests.post(url, data=json.dumps(param), timeout=timeout)
    return r

# 查询最大可用预算
@catchExcept
def GetMaxBudget(access_token, timeout=30):
    URL = 'https://merchant.wish.com/api/v2/product-boost/budget?access_token=%s'
    url = URL % access_token
    r = requests.get(url, timeout=timeout)
    return r

# 加预算
@catchExcept
def AddBudget(param, timeout=30):
    URL = 'https://merchant.wish.com/api/v2/product-boost/campaign/add-budget?access_token=%s&id=%s&amount=%s'
    url = URL % (param['access_token'], param['id'], param['amount'])
    r = requests.post(url, timeout=timeout)
    return r

# 更新在运行中的广告
@catchExcept
def UpdateCampaign_running(param, timeout=30):
    URL = 'https://merchant.wish.com/api/v2/product-boost/campaign/update-running?access_token=%s'
    access_token = param.pop('access_token')
    url = URL % access_token
    r = requests.post(url, data=json.dumps(param), timeout=timeout)
    return r

# 更新关键字
def UpdateKeywords(objs, access_token, keywords):
    obj = objs[0]
    if obj.campaign_state in ('NEW', 'PENDING'):
        param = {}
        param['id'] = obj.campaign_id
        param['access_token'] = access_token
        param['max_budget'] = float(obj.max_budget)
        param['auto_renew'] = True if obj.auto_renew == 'True' else False
        param['campaign_name'] = obj.campaign_name
        # st = datetime.strptime(obj.start_time, "%Y-%m-%d")
        param['start_date'] = obj.start_time
        # et = datetime.strptime(obj.end_time, "%Y-%m-%d")
        param['end_date'] = obj.end_time
        # products
        param['products'] = [{'product_id': obj.product_id, 'bid': float(obj.bid), 'keywords': keywords.split(',')}]
        r = UpdateCampaign(param, timeout=30)
        return r

    elif obj.campaign_state in ('SAVED', 'STARTED'):
        param = {}
        param['id'] = obj.campaign_id
        param['access_token'] = access_token
        param['max_budget'] = float(obj.max_budget)
        param['auto_renew'] = True if obj.auto_renew == 'True' else False
        # et = datetime.strptime(obj.end_time, "%Y-%m-%d")
        param['end_date'] = obj.end_time
        # products
        param['products'] = [{'product_id': obj.product_id,'keywords': keywords.split(',')}]
        
        r = UpdateCampaign_running(param, timeout=30)
        return r

#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: eBay_PLAPI.py
 @time: 2018-08-10 14:57
"""
import base64
import requests
import json
import datetime

from skuapp.table.t_config_store_ebay import t_config_store_ebay
from ebayapp.table.t_developer_info_ebay import t_developer_info_ebay
from ebayapp.table.t_online_info_ebay_campaigns import t_online_info_ebay_campaigns as campaigns

def getRunIP(campaign_id='', shopname=''):

    if not shopname:
        if campaign_id:
            objs = campaigns.objects.filter(Campaign_id=campaign_id).values('ShopName')
            shopname = objs[0]['ShopName']
        else:
            return ''

    objs = t_config_store_ebay.objects.filter(ShopName=shopname).values('appID')
    if objs.exists():
        developer = t_developer_info_ebay.objects.filter(appID=objs[0]['appID']).values('runIP')
        if developer.exists():
            return developer[0]['runIP']
        else:
            return ''
    else:
        return ''

def get_OAuth(appinfo, refresh_token):

    ClientSecretId = appinfo['appid'] + ':' + appinfo['certid']
    base64_ClientSecretId = base64.encodestring(ClientSecretId)
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Basic ' + base64_ClientSecretId.replace("\n", "")}

    body = 'grant_type=refresh_token&refresh_token=%s&scope=https://api.ebay.com/oauth/api_scope/sell.marketing' % refresh_token

    if appinfo['runIP']:
        request_url = 'http://%s:9193/fancyqube/api.ebay.com/identity/v1/oauth2/token'% appinfo['runIP']
    else:
        request_url = 'https://api.ebay.com/identity/v1/oauth2/token'

    try:
        r = requests.post(request_url, data=body, headers=headers, timeout=20)

        if r.status_code == requests.codes.ok:
            t = r.json()
            return {'retcode':0, 'data':t['access_token']}
        else:
            t = r.json()
            return {'retcode':-1, 'data':t['error_description']}
    except Exception,ex:
        return {'retcode':-1, 'data':repr(ex)}

def createCampaign(body, OAuthToken, ShopName):
    '''body = {
    "campaignName": "Fall Sale",
    "startDate": "2016-09-07T21:43:00Z",
    "fundingStrategy": {
        "bidPercentage": "10.0",
        "fundingModel": "COST_PER_SALE"
    },
    "marketplaceId": "EBAY_US"
    "endDate":""
    }'''
    
    headers = {'Accept':'application/json','Content-Type':'application/json'}
    headers['Authorization'] = 'Bearer %s' % OAuthToken

    runIP = getRunIP(shopname=ShopName)
    if runIP:
        request_url = 'http://%s:9193/fancyqube/api.ebay.com/sell/marketing/v1/ad_campaign'% runIP
    else:
        request_url = 'https://api.ebay.com/sell/marketing/v1/ad_campaign'
    try:
        r = requests.post(request_url, data=json.dumps(body), headers=headers, timeout=20)
        if r.status_code == 201:
            # 'Location': 'https://api.ebay.com/sell/marketing/v1/ad_campaign/10509709011'
            Location = r.headers['Location']
            campaign_id = Location.split('/')[-1]
            return {'retcode': 0, 'data': campaign_id}
        else:
            t = r.json()
            #print t
            return {'retcode': -1, 'data': t['errors'][0]['message']}  # longMessage
    except Exception, ex:
        return {'retcode': -1, 'data': repr(ex)}

def manageCampaign(campaign_id, OAuthToken, manageType):

    headers = {'Accept':'application/json','Content-Type':'application/json'}
    headers['Authorization'] = 'Bearer %s' % OAuthToken

    try:
        runIP = getRunIP(campaign_id=campaign_id)
        if runIP:
            url = 'http://%s:9193/fancyqube/api.ebay.com/sell/marketing/v1/ad_campaign'%runIP
        else:
            url = 'https://api.ebay.com/sell/marketing/v1/ad_campaign'

        if manageType.lower() == 'delete':
            request_url = '%s/%s' % (url, campaign_id)
            r = requests.delete(request_url, headers=headers, timeout=20)
        else:  # pause,resume,end
            request_url = '%s/%s/%s' % (url, campaign_id, manageType.lower())
            r = requests.post(request_url, headers=headers, timeout=20)

        if r.status_code == 204:
            return {'retcode': 0, 'data': 'OK'}
        else:
            t = r.json()
            return {'retcode': -1, 'data': t['errors'][0]['message']}
    except Exception, ex:
        return {'retcode': -1, 'data': repr(ex)}

def updateCampaign(campaign_id, OAuthToken, body):

    headers = {'Accept':'application/json','Content-Type':'application/json'}
    headers['Authorization'] = 'Bearer %s' % OAuthToken

    runIP = getRunIP(campaign_id=campaign_id)
    if runIP:
        request_url = 'http://%s:9193/fancyqube/api.ebay.com/sell/marketing/v1/ad_campaign/%s/update_campaign_identification' % (runIP, campaign_id)
    else:
        request_url = 'https://api.ebay.com/sell/marketing/v1/ad_campaign/%s/update_campaign_identification' % campaign_id
    try:
        r = requests.post(request_url, data=json.dumps(body), headers=headers, timeout=20)
        if r.status_code == 204:
            return {'retcode': 0, 'data': 'OK'}
        else:
            t = r.json()
            return {'retcode': -1, 'data': t['errors'][0]['message']}
    except Exception, ex:
        return {'retcode': -1, 'data': repr(ex)}

def bulkCreateAdsByListingId(campaign_id, OAuthToken, body):

    headers = {'Accept':'application/json','Content-Type':'application/json'}
    headers['Authorization'] = 'Bearer %s' % OAuthToken

    runIP = getRunIP(campaign_id=campaign_id)
    if runIP:
        request_url = 'http://%s:9193/fancyqube/api.ebay.com/sell/marketing/v1/ad_campaign/%s/bulk_create_ads_by_listing_id' % (runIP, campaign_id)
    else:
        request_url = 'https://api.ebay.com/sell/marketing/v1/ad_campaign/%s/bulk_create_ads_by_listing_id'% campaign_id
    try:
        r = requests.post(request_url, data=json.dumps(body), headers=headers, timeout=20)
        t = r.json()
        if 'responses' in t:
            return {'retcode': 0, 'data': t['responses']}
        elif 'errors' in t:
            return {'retcode': -1, 'data': t['errors'][0]['message']}
        else:
            return {'retcode': -1, 'data': str(t)}
    except Exception, ex:
        return {'retcode': -1, 'data': repr(ex)}

def bulkDeleteAdsByListingId(campaign_id, OAuthToken, body):

    headers = {'Accept':'application/json','Content-Type':'application/json'}
    headers['Authorization'] = 'Bearer %s' % OAuthToken

    runIP = getRunIP(campaign_id=campaign_id)
    if runIP:
        request_url = 'http://%s:9193/fancyqube/api.ebay.com/sell/marketing/v1/ad_campaign/%s/bulk_delete_ads_by_listing_id' % (runIP, campaign_id)
    else:
        request_url = 'https://api.ebay.com/sell/marketing/v1/ad_campaign/%s/bulk_delete_ads_by_listing_id'% campaign_id
    try:
        r = requests.post(request_url, data=json.dumps(body), headers=headers, timeout=20)
        if r.status_code == 200:
            t = r.json()
            return {'retcode': 0, 'data': t['responses']}
        else:
            t = r.json()
            return {'retcode': -1, 'data': t['errors'][0]['message']}
    except Exception, ex:
        return {'retcode': -1, 'data': repr(ex)}

def bulkUpdateAdsBidByListingId(campaign_id, OAuthToken, body):

    headers = {'Accept':'application/json','Content-Type':'application/json'}
    headers['Authorization'] = 'Bearer %s' % OAuthToken

    runIP = getRunIP(campaign_id=campaign_id)
    if runIP:
        request_url = 'http://%s:9193/fancyqube/api.ebay.com/sell/marketing/v1/ad_campaign/%s/bulk_update_ads_bid_by_listing_id' % (runIP, campaign_id)
    else:
        request_url = 'https://api.ebay.com/sell/marketing/v1/ad_campaign/%s/bulk_update_ads_bid_by_listing_id'% campaign_id
    try:
        r = requests.post(request_url, data=json.dumps(body), headers=headers, timeout=20)
        if r.status_code == 200:
            t = r.json()
            return {'retcode': 0, 'data': t['responses']}
        else:
            t = r.json()
            return {'retcode': -1, 'data': t['errors'][0]['message']}
    except Exception, ex:
        return {'retcode': -1, 'data': repr(ex)}

def createAdByListingId(campaign_id, OAuthToken, body):

    headers = {'Accept':'application/json','Content-Type':'application/json'}
    headers['Authorization'] = 'Bearer %s' % OAuthToken

    runIP = getRunIP(campaign_id=campaign_id)
    if runIP:
        request_url = 'http://%s:9193/fancyqube/api.ebay.com/sell/marketing/v1/ad_campaign/%s/ad' % (runIP, campaign_id)
    else:
        request_url = 'https://api.ebay.com/sell/marketing/v1/ad_campaign/%s/ad'% campaign_id
    try:
        r = requests.post(request_url, data=json.dumps(body), headers=headers, timeout=20)
        if r.status_code == 201:
            Location = r.headers['Location']
            ad_id = Location.split('/')[-1]
            return {'retcode': 0, 'data': ad_id}
        else:
            t = r.json()
            return {'retcode': -1, 'data': t['errors'][0]['message']}
    except Exception, ex:
        return {'retcode': -1, 'data': repr(ex)}

def deleteAd(campaign_id, OAuthToken, ad_id):
    headers = {'Accept':'application/json','Content-Type':'application/json'}
    headers['Authorization'] = 'Bearer %s' % OAuthToken

    runIP = getRunIP(campaign_id=campaign_id)
    if runIP:
        request_url = 'http://%s:9193/fancyqube/api.ebay.com/sell/marketing/v1/ad_campaign/%s/ad/%s' % (runIP, campaign_id, ad_id)
    else:
        request_url = 'https://api.ebay.com/sell/marketing/v1/ad_campaign/%s/ad/%s'% (campaign_id, ad_id)
    try:
        r = requests.delete(request_url, headers=headers, timeout=20)
        if r.status_code == 204:
            return {'retcode': 0, 'data': 'OK'}
        else:
            t = r.json()
            return {'retcode': -1, 'data': t['errors'][0]['message']}
    except Exception, ex:
        return {'retcode': -1, 'data': repr(ex)}

def updateBid(campaign_id, OAuthToken, ad_id, body):

    headers = {'Accept':'application/json','Content-Type':'application/json'}
    headers['Authorization'] = 'Bearer %s' % OAuthToken

    runIP = getRunIP(campaign_id=campaign_id)
    if runIP:
        request_url = 'http://%s:9193/fancyqube/api.ebay.com/sell/marketing/v1/ad_campaign/%s/ad/%s/update_bid' % (runIP, campaign_id, ad_id)
    else:
        request_url = 'https://api.ebay.com/sell/marketing/v1/ad_campaign/%s/ad/%s/update_bid'% (campaign_id, ad_id)
    try:
        r = requests.post(request_url, data=json.dumps(body), headers=headers, timeout=20)
        if r.status_code == 204:
            return {'retcode': 0, 'data': 'OK'}
        else:
            t = r.json()
            return {'retcode': -1, 'data': t['errors'][0]['message']}
    except Exception, ex:
        return {'retcode': -1, 'data': repr(ex)}



if __name__ == '__main__':
    body = {
"requests": [
    {
      "bidPercentage": "5.0",
      "listingId": "232904124610"
    }
  ]
}
    campaign_id = '10544538016'
    token = 'v^1.1#i^1#I^3#f^0#p^3#r^0#t^H4sIAAAAAAAAAOVXa2gUVxTObjarUaOltI21VrZjW6wyu3eeOzu4K2uy0dWYrNnVmoiG2Zk72dHZmWXurEmk4hLEikkR7A8FS430QQuFqpDaQluwWktFaGvxh0WrKAUf/aGgtlBqe2fzcLNSLUboQufPMOeeOfd83/nuveeCgrd2/val23+rc01yDxZAwe1yUVNBrbdmwfRq96yaKlDi4BosvFjw9FVfWYikrJ4T2yDKmQaCvp6sbiCxaAwTecsQTQlpSDSkLESiLYvJ6IpmkfYDMWeZtimbOuGLN4YJKPOMyqmCqlAKo9IsthqjMVNmmJDVdJoVQpwiCADQNI/HEcrDuIFsybDDBA0ogQQCyYAU4EWWFVnGz7NCB+FbDS2kmQZ28QMiUkxXLP5rleT64FQlhKBl4yBEJB5tSrZG442xltTCQEmsyAgPSVuy82j8V4OpQN9qSc/DB0+Dit5iMi/LECEiEBmeYXxQMTqazCOkP0w1ywGWo3iOUUFaBo+HyibTykr2g/NwLJpCqkVXERq2Zvc+jFHMRnoDlO2RrxYcIt7oc14r85KuqRq0wkRscbR9VTLWRviSiYRlbtIUqDhIKYoOsiwIYYwRVUIZnLsuGQoGyI1MNRxvhOiyuRpMQ9Ec2pCvxbQXQ5w3LGeHKWEHO7UarVZUtZ2cSv2EMRbZDqesw3XM2xnDqSzMYip8xc+H12BUFPdk8LhkQSlBqDKywrGMpEhQKJOFs9YfSRoRpzrRRCLg5ALTUi+ZlayN0M7pkgxJGdObz0JLU0SGU2lGUCGp8CGVZEOqSqY5hScpFUIAYToth4T/l0Js29LSeRuOqaR8oAgTr2jMqqhJqmibG6GR6s1BotyzuP2MSKMHhYmMbefEQKC7u9vfzfhNqytAA0AF1qxoTsoZmJWIMV/t4c6kVhSJDPFfSBNtnECY6MEaxJMbXUSkLdbUFksu7Uy1Lo+1jOp3XGaRcus/IE3KZg4mTF2TeysLImMpCcmye5NQ17FhQiCRA/K/hOes9fshOjEQDiLlNL+jOL9sZgOmhPctx9RZzDqAMH7/8AKfKA3RXC6uVFaVezSY1QwyI5k5MtHWSDKcEmRVWVBJOc3KQTbETgixAjdpMuzUKgy1kdf1CeFqhJsqrZIUDdgQzzAkoHmZZFmWI0NBhieDgGZoFaihNC1PCPOKrkorI8UKTJAN4vMdd9BjKDx97nmPgq9B1/CBVHlnzVIT2VCZUOkacFtUWaCcvWZ0q8EPQ/IhJYhbpBCFVQsAmaY5/t9CLjOU9Bb3NZaB8Xe7SFXxofpcQ6DPdQhfD0EAvETNBS94q1d5qqfNQpoN/bgP8SOty8BXFgv6N8LenKRZbq9r7eyDH3aW3CYH14GZY/fJ2mpqasnlEsy+N1JDzaivowQgYNni9ohlOsDce6Me6hnPUy/f1r84fv2TOGFOm3Lr7OVCXd2ieaBuzMnlqqny9Lmqzmzj67rdns/23uhcV79r+lBz7eQ7ZwaWLVtTe/XT5W+cbvdOunF5wZ29711d7NXkyfyVOZt/2fbrwKkZa7ecu/nX+bsBdWD/++6jX3LNP26Vveof72TfPLknVcicf914ld9+bp8ytKMNCu7P55xoj0Vndxlrm8nNB3YN7n+r6e6eKScH9tTOPLL+8rH+0xdeS12Hh3c8OX+f+2KWO7xsdaT9uf7zb7cu/PrbP/vBte8+urpl28HpVwQzc+f2oe8/vnRqqFVY8nN/4WZH84Efnr5+7daxJd8cfffCzuNbj1dPHfjqmH/nK6fqL25IPE9c2i1Napc+GNrsefaJlUfnTTmyftFPJ+rP/n5gVrRnn983XL6/AV5gJZTnDwAA'
    x = bulkCreateAdsByListingId(campaign_id, token, body)

    print x
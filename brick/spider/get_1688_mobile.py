# coding=utf-8


import requests, re, json


def get_1688_mobile(web_url):
    image, title, supplier, price_range = None, None, None, None
    mobile_url = web_url.replace('detail', 'm')
    response = requests.get(mobile_url, timeout=30, verify=False)
    text = response.text
    pattern = r'wingxViewData\[0\]=(.*)</script></div></div>'
    s = re.findall(pattern, text)
    s_dict = json.loads(s[0])
    image_list = s_dict.get('imageList', '')
    if image_list:
        image = image_list[0].get('size310x310URL', '')
    title = s_dict.get('subject', '')
    supplier = s_dict.get('companyName', '')
    price_range_list = s_dict.get('priceDisplay', '')
    price_range = [float(price) for price in price_range_list.split('-')]
    return image, title, supplier, price_range

url_list = [
    'https://detail.1688.com/offer/558669844089.html', 'https://detail.1688.com/offer/568605236387.html',
    'https://detail.1688.com/offer/562437642185.html', 'https://detail.1688.com/offer/555482828214.html',
    'https://detail.1688.com/offer/566776519559.html', 'https://detail.1688.com/offer/549751456325.html'
]

for web_url in url_list:
    image, title, supplier, price_range = get_1688_mobile(web_url)
    print image, title, supplier, price_range
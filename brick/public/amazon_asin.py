#-*-coding:utf-8-*-
import redis as redis
import requests
from bs4 import BeautifulSoup
import re
import pymysql
from datetime import datetime
import random
import logging
import sys
import traceback
import oss2
from multiprocessing import Pool
from multiprocessing import Manager
import functools
import time


logger = logging.getLogger("logger")
formart = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
file_handler = logging.FileHandler('commentLogger.log')
file_handler.setFormatter(formart)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formart)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

ACCESS_KEY_ID= 'LTAIH6IHuMj6Fq2h'
ACCESS_KEY_SECRET = 'N5eWsbw8qBkMfPREkgF2JnTsDASelM'
PREFIX = 'http://'
ENDPOINT = 'vpc100-oss-cn-shanghai.aliyuncs.com'
ENDPOINT_OUT = 'oss-cn-shanghai.aliyuncs.com'
BUCKETNAME_AMAZON  = 'fancyqube-amazon'


#获取一页的内容
def get_one_page(url):
    user_agentList = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
        "Opera/8.0 (Windows NT 5.1; U; en)",
        "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"
    ]
    ua_header = {
        "User-Agent": random.choice(user_agentList)}
    try:
        response = requests.get(url, headers=ua_header)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception,ex:
        logger.info('%s:%s = %s' % (traceback.print_exc(), Exception, ex))
        return None

# 获取产品信息
def get_product_msg(html):
    msg = {}
    pattern = re.compile(
        '''<ul class="a-unordered-list a-nostyle a-horizontal list maintain-height">[\s\S]*?<img alt="([\s\S]*?)" src=[\s\S]*?data-old-hires="([\s\S]*?)"[\s\S]*?<a data-hook="see-all-reviews-link-foot" class="a-link-emphasis a-text-bold" href="([\s\S]*?)">''')

    title = ''
    image = ''
    url = ''

    try:
        title = re.findall(pattern, html)[0][0]
    except Exception,ex:
        logger.info('%s:%s = %s' % (traceback.print_exc(), Exception, ex))

    msg['title'] = title

    try:
        image = re.findall(pattern, html)[0][1]
    except Exception,ex:
        logger.info('%s:%s = %s' % (traceback.print_exc(), Exception, ex))

    msg['image'] = image

    try:
        url = re.findall(pattern, html)[0][2]
    except Exception, ex:
        logger.info('%s:%s = %s' % (traceback.print_exc(), Exception, ex))

    msg['url'] = url

    return msg


# 提取数据
def parse_one_page(html):

    total = []
    try:
        soup = BeautifulSoup(html, "lxml")
        l = soup.findAll('div', {'class': 'a-section review'})
        for i in l :
            dic = {}
            ver = []
            com = []

            star = i.find('span', {'class': 'a-icon-alt'}).string.strip()[:3]
            dic['star'] = star

            comment_title = i.find('a', {'class': 'a-size-base a-link-normal review-title a-color-base a-text-bold'}).string.strip()
            dic['comment_title'] = comment_title

            customer = i.find('a', {'class':'a-size-base a-link-normal author'}).string.strip()
            dic['customer'] = customer

            try:
                p_time = i.find('span', {'class':'a-size-base a-color-secondary review-date'}).string.strip()
                comment_time = datetime.strptime(p_time , "on %B %d, %Y")
                dic['comment_time'] = comment_time
            except Exception,ex:
                logger.info('%s:%s = %s' % (traceback.print_exc(), Exception, ex))

            try:
                comments = i.find('span',{'class':'a-size-base review-text'}).stripped_strings
                for c in comments:
                    com.append(c)
                comment = ' '.join(com)
                dic['comment'] = comment
            except Exception,ex:
                logger.info('%s:%s = %s' % (traceback.print_exc(), Exception, ex))
                dic['comment'] = ''

            try:
                versions = i.find('a', {'class':'a-size-mini a-link-normal a-color-secondary'}).stripped_strings
                for v in versions:
                    ver.append(v)
                for i in ver:
                    if 'Color' in i:
                        dic['color'] = i
                        ver[ver.index(i)] = ''
                for i in ver:
                    if 'Size' in i:
                        dic['si'] = i
                        ver[ver.index(i)] = ''
                if 'color' not in dic.keys():
                    dic['color'] = ''
                if 'si' not in dic.keys():
                    dic['si'] = ''

                other = ' '.join(ver)
                dic['other'] = other
            except Exception,ex:
                dic['color'] = ''
                dic['si'] = ''
                dic['other'] = ''

            total.append(dic)

        return total

    except Exception,ex:
        logger.info('%s:%s = %s' % (traceback.print_exc(), Exception, ex))
        return total

# 获取评论页数
def get_pages(html,url):

    urls = []
    try:
        soup = BeautifulSoup(html, "lxml")
        page = soup.find('ul', {'class':'a-pagination'}).stripped_strings
        pg = []
        for p in page:
            try:
                cp = p.replace(',','')
                pg.append(int(cp))
            except:
                pass
        num = max(pg)+1
        if num >101:
            num = 101
        for i in range (2,num):
            u = url + '&pageNumber=' + str(i)
            urls.append(u)
        return urls
    except Exception,ex:
        logger.info('%s:%s = %s' % (traceback.print_exc(), Exception, ex))
        return urls

# 保存产品图片
def save_image(msg,asin):
    ua_header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"}

    imageurl = ''
    if msg['image']:
        try:
            try:
                response = requests.get(msg['image'], headers=ua_header)
            except Exception, ex:
                logger.info('%s:%s = %s' % (traceback.print_exc(), Exception, ex))
                return imageurl

            auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
            bucket = oss2.Bucket(auth, ENDPOINT, BUCKETNAME_AMAZON)
            bucket.put_object(u'%s/%s.jpg' % ('API', asin), response)
            # 保存图片
            imageurl = u'%s%s.%s/%s/%s.jpg' % (PREFIX, BUCKETNAME_AMAZON, ENDPOINT_OUT, 'API', asin)
            return imageurl
            # with open('img.jpg','ab') as f:
            #     f.write(response.content)
        except Exception,ex:
            logger.info('%s:%s = %s' % (traceback.print_exc(), Exception, ex))
            return imageurl
    else:
        return imageurl


# 保存数据
def write_to_file(imageurl,msg,asin,item):
    # with open("Amazon.txt", 'a', encoding='utf-8') as f:
    #     f.write(json.dumps(item, ensure_ascii=False) + '\n')
    title = msg['title']
    t = datetime.now()
    cnxn = pymysql.connect('hequskuapp.mysql.rds.aliyuncs.com','by15161458383','K120Esc1','hq_db',charset='utf8')
    cursor = cnxn.cursor()

    star = item['star']
    comment_title = item['comment_title']
    customer = item['customer']
    comment_time = item['comment_time']
    color = item['color']
    si = item['si']
    other = item['other']
    comment = item['comment']
    try:
        sql = 'insert into t_amazon_pro_comment(imageurl, title, asin, star, comment_title, customer, comment_time, color, si, other, comment, get_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
        params = (imageurl, title, asin, star, comment_title, customer, comment_time, color, si, other, comment,t)
        cursor.execute(sql, params)
        cnxn.commit()
    except Exception,ex:
        logger.info('%s:%s = %s' % (traceback.print_exc(), Exception, ex))
        pass
    cursor.close()
    cnxn.close()


def Crawlpage(lock, imageurl, msg, asin, counts, url):
    html = get_one_page(url)
    comm = parse_one_page(html)

    for item in comm:
        lock.acquire()
        write_to_file(imageurl,msg,asin,item)
        lock.release()

    time.sleep(0.01)


def get_comments(asin):
    url = "https://www.amazon.com/dp/" + str(asin)
    html = get_one_page(url)
    if html is None:
        return u'faild, please refresh and retry'

    msg = get_product_msg(html)
    s = ''.join(msg.values())
    if not s:
        return u'faild, please refresh and retry'
    print msg

    imageurl = save_image(msg,asin)
    print imageurl

    urls = []
    comment_url = "https://www.amazon.com" + msg['url']
    urls.append(comment_url)
    comm_html = get_one_page(comment_url)
    url_page = get_pages(comm_html,comment_url)
    urls.extend(url_page)
    print urls
    if not urls:
        return u'faild, please refresh and retry'

    counts = float(len(urls)*10)

    manager = Manager()
    lock = manager.Lock()
    newCrawlpage = functools.partial(Crawlpage, lock, imageurl, msg, asin, counts)

    # 创建进程池
    pool = Pool()
    pool.map(newCrawlpage, urls)
    pool.close()
    pool.join()

    logger.removeHandler(file_handler)
    logger.removeHandler(console_handler)
    return u'success'


if __name__ == "__main__":
    asin = raw_input('请输入asin：')
    s = time.time()
    print(get_comments(asin))
    e = time.time()
    print e-s



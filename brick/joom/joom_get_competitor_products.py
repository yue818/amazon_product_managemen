# -*- coding: utf-8 -*-
"""
Installation(This is Linux no window browser)

python package:
    pip install selenium

Linux package:
    Download phantomjs-2.1.1-linux-x86_64.tar.bz2 (22.3 MB) and extract the content.
    Download url: https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
    Linux Env: tar -xvf phantomjs-2.1.1-linux-x86_64.tar.bz2

Linux make soft connection:
    ln -s /where/is/phantomjs /usr/local/bin/phantomjs

PhantomJS website:
    http://phantomjs.org/download.html

"""

from selenium import webdriver
import time
import os
import signal
import psutil


class joom_get_competitor_products():

    def __init__(self):
        self.dr = webdriver.PhantomJS('phantomjs')
        self.dr.implicitly_wait(5)
        self.dr.set_page_load_timeout(10)
        self.dr.set_script_timeout(10)
        self.parent_pid = os.getpid()

    def get_page_info(self, product_id):
        pro_url = "https://www.joom.com/en/products/%s" % product_id
        try:
            self.dr.get(pro_url)
        except Exception as e:
            if str(e) == 'timed out':
                try:
                    self.dr.get(pro_url)
                except Exception:
                    return {'code': -1, 'message': 'Get url timeout'}
            else:
                return {'code': -1, 'message': str(e)}
        # Be sure the page has been loaded completely.
        time.sleep(2)
        return {'code': 0, 'message': ''}

    def get_price_range(self):
        try:
            colors = self.dr.find_elements_by_class_name('_3-Bw4-1XR2ZHUgHcdSg19p')
        except:
            colors = None
        try:
            sizes = self.dr.find_elements_by_class_name('_2I9Zv4I8nOBxhSeTVt0CH-  ')
        except:
            sizes = None
        prices = list()
        # 无变体商品
        if not sizes and not colors:
            try:
                price = self.dr.find_element_by_class_name('m18VbNPeb3lg3plifh4Ph').text.split('$')[-1]
                prices.append(price)
            except:
                pass

        # 只有size属性商品
        if sizes and not colors:
            for size in sizes:
                try:
                    size.click()
                    price = self.dr.find_element_by_class_name('m18VbNPeb3lg3plifh4Ph').text.split('$')[-1]
                    if price not in prices:
                        prices.append(price)
                except:
                    pass

        # 只有color属性商品
        if not sizes and colors:
            for color in colors:
                try:
                    color.click()
                    price = self.dr.find_element_by_class_name('m18VbNPeb3lg3plifh4Ph').text.split('$')[-1]
                    if price not in prices:
                        prices.append(price)
                except:
                    pass

        # size和color属性都有
        if sizes and colors:
            for size in sizes:
                try:
                    size.click()
                    for color in colors:
                        color.click()
                        price = self.dr.find_element_by_class_name('m18VbNPeb3lg3plifh4Ph').text.split('$')[-1]
                        if price not in prices:
                            prices.append(price)
                except:
                    pass

        price_range = list()
        if prices:
            price_list = list(map(lambda x: float(x), prices))
            price_list.sort()
            print 'price_list', price_list
            price_range.append(price_list[0])
            price_range.append(price_list[-1])
        else:
            price_range = ['', '']
        return price_range

    def get_main_image(self):
        main_image = ''
        try:
            image_elements = self.dr.find_elements_by_tag_name('meta')
            for i in image_elements:
                try:
                    image_type = i.get_attribute('property')
                    if image_type == 'og:image':
                        main_image = i.get_attribute('content')
                        break
                except Exception as e:
                    print 'get image error: %s' % e
        except:
            pass
        return main_image

    def get_ratingValue(self):
        ratingvalue = ''
        try:
            elements = self.dr.find_elements_by_class_name('znPTiSqfV_iqvAj_fLC_1')
            for i in elements:
                rv = i.find_element_by_tag_name('span').find_element_by_tag_name('span').text
                if rv:
                    ratingvalue = rv
                    break
        except Exception as e:
            print e

        return ratingvalue

    def close_webdriver(self):
        # self.dr.close()
        try:
            self.dr.quit()
        except Exception:
            pass
        try:
            self.dr.service.stop()
        except Exception:
            pass

        try:
            self.kill_children_process()
        except:
            pass

    def kill_children_process(self, sig=signal.SIGTERM):
        try:
            parent = psutil.Process(self.parent_pid)
        except psutil.NoSuchProcess:
            return
        children = parent.children(recursive=True)
        for process in children:
            if process.name() == 'phantomjs.exe' or process.name() == 'phantomjs':
                process.send_signal(sig)

    def get_free_shipping(self):
        from joom_app.table.t_online_info_joom import t_online_info_joom
        product_ids = t_online_info_joom.objects.filter(Status='True', ReviewState='approved')[:5000].values('ProductID')
        count = 0
        no_get_free_list = list()
        for i in product_ids:
            pro_id = i['ProductID']
            print 'ProductID', pro_id
            self.get_page_info(pro_id)
            time.sleep(1)
            try:
                elements = self.dr.find_element_by_class_name('_2gj4b-PUn53EtKShoiOHdW').find_elements_by_tag_name('span')
            except Exception as e:
                print e
                no_get_free_list.append(pro_id)
                continue
            for j in elements:
                if 'Free shipping' in j.text:
                    print j.text
                    count += 1
                    break

        print 'free count', count
        print 'no_get_free_list num', len(no_get_free_list)
        print 'no_get_free_list', no_get_free_list

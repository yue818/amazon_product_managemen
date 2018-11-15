# -*- coding: utf-8 -*-

from selenium import webdriver
import time
import os
import signal
import psutil


class webdriver_get_page_by_phantomjs():

    def __init__(self):
        self.dr = webdriver.PhantomJS('phantomjs')
        self.dr.implicitly_wait(5)
        self.dr.set_page_load_timeout(10)
        self.dr.set_script_timeout(10)
        self.parent_pid = os.getpid()

    def get_page_info(self, pro_url):
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

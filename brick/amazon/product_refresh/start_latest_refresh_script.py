# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: start_latest_refresh_script.py
 @time: 2018-05-02 17:23
"""  

import os
script_path = r"C:\vps_server"

if os.path.exists(script_path):
    n = 1
    for dir_root, dir_name, file_name in os.walk(script_path, topdown=False):
        print 'loop %s' % str(n)
        print dir_root
        print dir_name
        print file_name
        n += 1
        print


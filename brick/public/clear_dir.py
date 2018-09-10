#-*-coding:utf-8-*-
import os
import shutil
import traceback
"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: clear_dir.py
 @time: 2018/1/5 9:50
"""
def clear_p(current_path):
    try:
        for root, dirs, files in os.walk(current_path):
            for name in files:
                # delete the log and test resultf
                # print root, dirs, files
                del_file = os.path.join(root, name)
                # print del_file
                os.remove(del_file)
                print 'remove file[%s] successfully' % del_file
        shutil.rmtree(current_path)
        print 'remove foler[%s] successfully' % current_path
    except Exception, e:
        traceback.print_exc()
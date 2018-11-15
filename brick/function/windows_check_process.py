#-*- coding:utf-8 -*-

import win32com.client

def check_exsit(process_name):
    WMI = win32com.client.GetObject('winmgmts:')
    processCodeCov = WMI.ExecQuery('select * from Win32_Process where Name="%s"' % process_name)
    if len(processCodeCov) > 0:
        print '%s is exists' % process_name
        return 1
    else:
        print '%s is not exists' % process_name
        return 0

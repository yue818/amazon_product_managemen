#-*-coding:utf-8-*-
"""  
 @desc:  避免魔鬼数字，维护常量，阅读直观
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: const.py
 @time: 2018-05-04 16:56
"""

# 常量定义
class tort(object):
    '''CHECKIN = 0                 # 侵权登记
    WAIT_AUDIT = 1              # 侵权待审核
    WAIT_RECEIVE = 2            # 侵权待领用(审核通过)
    ALREADY_RECEIVE = 3         # 侵权已领用
    REJECT = 9                  # 驳回侵权申请
    DELETE = 10                 # 删除到回收站
    CANCEL_WAIT_AUDIT = 11      # 撤销侵权待审核
    CANCEL_WAIT_RECEIVE = 12    # 撤销侵权待领用(审核通过)
    CANCEL_ALREADY_RECEIVE = 13 # 撤销侵权已领用
    CANCEL_REJECT = 19          # 驳回撤销侵权申请
    HIDE = 20                   # 合并审核后隐藏的数据行
    SYNC = 21                   # 侵权数据导出同步
    CANCEL_SYNC = 22            # 侵权撤销数据导出同步
    '''
    CHECKIN = 0                 # 侵权登记
    WAIT_AUDIT = 1              # 侵权待审核
    TORT_LIST = 2               # 严重侵权(审核通过)
    COM_TORT_LIST = 3           # 一般侵权(审核通过)
    NO_TORT_LIST = 4            # 一般侵权中的不侵权(审核通过)
    REJECT = 9                  # 驳回侵权申请
    DELETE = 10                 # 删除到回收站

    SYNC = 11                   # 严重侵权已导出同步
    SYNC_COM = 12               # 一般侵权已导出同步
    
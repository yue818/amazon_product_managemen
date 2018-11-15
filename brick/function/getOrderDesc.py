# -*- coding: utf-8 -*-
import sys,os
def getOrderDesc(OrderDesc, PODate):
    PODate = str(PODate)
    if OrderDesc is not None and OrderDesc.endswith(PODate):
        x = OrderDesc[OrderDesc.find(':')+1:OrderDesc.find('|')]
    else:
        x = u'无'

    return x

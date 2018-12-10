# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: 20181203.py
 @time: 2018/12/3 17:48
"""
from reportlab.graphics.barcode import code128
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont
# pdfmetrics.registerFont(TTFont('SimSun', 'SimSun.ttf'))
# from pyPdf import PdfFileReader,PdfFileWriter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def create_sku_bar_code(info):
    c = canvas.Canvas('C:\Users\Administrator\Desktop\\' + info+'.pdf')
    print c.getAvailableFonts()

    c.setPageSize((51*mm, 76*mm))

    barcode = code128.Code128(info, barHeight=6.3*mm, barWidth=42*mm)
    barcode.drawOn(c, 6.3*mm, 10*mm)
    # c.drawString(2*mm, 6*mm, '1111') #写名字
    # c.drawString(2 * mm, 6 * mm, info)  # 写名字
    c.showPage()
    c.save()


def create_sku_bar_code1(info):
    c = canvas.Canvas('C:\Users\Administrator\Desktop\\' + info+'.pdf')
    c.setPageSize((76*mm, 51*mm))

    barcode = code128.Code128(info)
    barcode.drawOn(c, 1*mm, 40*mm)

    c.drawString(6.3*mm, 35*mm, info)
    c.drawString(6.3*mm, 30*mm, '1')

    c.showPage()
    c.save()


create_sku_bar_code1('X001KV5H93')


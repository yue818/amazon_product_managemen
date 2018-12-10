# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: 20181204a.py
 @time: 2018/12/4 19:45
"""  
from reportlab.graphics.barcode import code128
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def create_barcodes(code_name):
    c = canvas.Canvas(code_name+".pdf", pagesize=letter)
    c.setFont('Courier', 5)
    margin_x = 7.526
    margin_y = 13.876
    padding_x = 7.526
    font_size = 15
    width, height = letter
    extra_padding = 20

    bars_width = (float(width-margin_x*2)-3*padding_x)/4
    bars_height = float(height-margin_y*2)/15

    bar_height = bars_height - font_size
    #For alphanumeric values, the total number of bars is calculated as:
    #total = (11*string_length+35)
    bar_width = (bars_width-extra_padding)/(len(code_name)*11+35)

    barcode_value = code_name
    barcode128 = code128.Code128(
                            barcode_value,
                            barHeight=bar_height,
                            barWidth=bar_width,
                            humanReadable=True,
                        )

    # for i in range(0,4):
    #     for j in range(0,15):
    #         x = margin_x + i * (bars_width+padding_x)
    #         y = margin_y + j * bars_height
    #         barcode128.drawOn(c, x, y)
    x = margin_x + 0 * (bars_width + padding_x)
    y = margin_y + 14 * bars_height
    barcode128.drawOn(c, x, y)

    # c.drawRightString(x+10, margin_y + 13 * bars_height, 'NEW')

    c.save()


if __name__ == "__main__":
    create_barcodes('X001V1KI3H')
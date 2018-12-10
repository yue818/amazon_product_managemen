# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: 20181204.py
 @time: 2018/12/4 17:35
"""
from reportlab.graphics.barcode import code128
from reportlab.pdfgen import canvas

c = canvas.Canvas("test.pdf")
final_size = 100 # arbitrary
# setting barWidth to 1
initial_width = .1

barcode128 = code128.Code128('111111111', humanReadable=True, barWidth=initial_width,
                             barHeight=1)
# creates the barcode, computes the total size
barcode128._calculate()
# the quiet space before and after the barcode
quiet = barcode128.lquiet + barcode128.rquiet
# total_wid = barWidth*charWid + quiet_space
# char_wid = (total_width - quiet) / bar_width
char_width = (barcode128._width - quiet) / barcode128.barWidth
# now that we have the char width we can calculate the bar width
bar_width = (final_size - quiet) / char_width
# set the new bar width
barcode128.barWidth = bar_width
# re-calculate
barcode128._calculate()

# draw the barcode on the canvas
wid, hgt = barcode128._width, barcode128._height
x_pos = y_pos = final_size # arbitrary
barcode128.drawOn(c, x_pos, y_pos)





# from reportlab.graphics.barcode import code128
# from reportlab.lib.units import mm, cm, inch
# from reportlab.pdfgen import canvas
#
# c = canvas.Canvas("test.pdf")
# c.setPageSize((57*mm,32*mm))
# # barcode = code128.Code128("123456789")
# barcode = code128.Code128("123456789",barHeight=6.3*mm, barWidth = 1.2)
# barcode.drawOn(c, 2*mm, 20*mm)
# c.showPage()
# c.save()

# canvas.saveState()
# canvas.translate(2*cm, 3*cm) # bottom left corner of the barcode
# canvas.scale(15*cm / barcode.width, 2*cm / barcode.height) # resize (15 cm and 2 cm)
# barcode.drawOn(canvas, 0, 0)
# canvas.restoreState()

















# #引入所需要的基本包
# from reportlab.pdfgen import canvas
# from reportlab.graphics.barcode import code39, code128, code93
# from reportlab.graphics.barcode import eanbc, qr, usps
# from reportlab.graphics.shapes import Drawing
# from reportlab.lib.units import mm
# from reportlab.graphics import renderPDF
#
#
# def createBarCodes(c):
#     barcode_value = "1234567890"
#     barcode128 = code128.Code128(barcode_value)
#     codes = [barcode128]
#
#     x = 1 * mm
#     y = 285 * mm
#
#     for code in codes:
#         code.drawOn(c, x, y)
#         y = y - 15 * mm

    # barcode_eanbc8 = eanbc.Ean8BarcodeWidget(barcode_value)
    # d = Drawing(50, 10)
    # d.add(barcode_eanbc8)
    # renderPDF.draw(d, c, 15, 555)

    # draw the eanbc13 code
    # barcode_eanbc13 = eanbc.Ean13BarcodeWidget(barcode_value)
    # d = Drawing(50, 10)
    # d.add(barcode_eanbc13)
    # renderPDF.draw(d, c, 15, 465)

    # draw a QR code
    # qr_code = qr.QrCodeWidget('http://blog.csdn.net/webzhuce')
    # bounds = qr_code.getBounds()
    # width = bounds[2] - bounds[0]
    # height = bounds[3] - bounds[1]
    # d = Drawing(45, 45, transform=[45./width,0,0,45./height,0,0])
    # d.add(qr_code)
    # renderPDF.draw(d, c, 15, 405)


# #定义要生成的pdf的名称
# c=canvas.Canvas("reportlab.pdf")
# #调用函数生成条形码和二维码，并将canvas对象作为参数传递
# createBarCodes(c)
# #showPage函数：保存当前页的canvas
# c.showPage()
# #save函数：保存文件并关闭canvas
# c.save()

























# from reportlab.pdfgen import canvas
# from reportlab.graphics.barcode import code128
# from reportlab.lib.units import mm
# c = canvas.Canvas("BRC.pdf")
# c.setPageSize((76*mm, 51*mm))
# barcode = code128.Code128("X001QIS2DX", barHeight=6.3*mm, barWidth=1.2, quiet=True, lquiet=6.6*mm, rquiet=6.6*mm)
#
# barcode.drawOn(c, 0*mm, (51-6.3-3.2)*mm)
# c.drawString(6.6*mm, (51-6.3-3.2-6.4)*mm, 'X001QIS2DX')
# c.drawString(6.6*mm, (51-6.3-3.2-6.4-6.4)*mm, '100 Sheets 6.3 inches Coppery Leaf and Silver Leaf Foil Paper for Arts, Gilding Crafting, Decoration, Crafts Decoration DIY (Silver)')
# c.showPage()
# c.save()
# import barcode
# Code = barcode.get_barcode_class('code128')
# bar = Code("123456")
# bar.save("barcode")
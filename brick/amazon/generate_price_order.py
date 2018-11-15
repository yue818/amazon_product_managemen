#-*-coding:utf-8-*-
from brick.table.t_sku_color import t_sku_color
from brick.classredis.classsku import classsku
from django.db import connection
from brick.table.t_order_amazon_india import *
from Project.settings import *
import decimal, datetime, traceback, zipfile
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table,TableStyle, Paragraph
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from brick.public.upload_to_oss import upload_to_oss
from skuapp.table.t_download_info import t_download_info
# from Project.settings import *
import time
from brick.table.amzon_india_price_config import amzon_india_price_config
"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: generate_price_order.py
 @time: 2018/1/5 16:34
"""
class generate_price_order():
    def __init__(self):
        pass

    def get_max_price(self, params):
        t_order_amazon_india_obj = t_order_amazon_india(connection)
        order_item_infos = t_order_amazon_india_obj.get_order_item_info_by_orderNumber(orderNumber=params['orderNumber']['orderId'])
        weight = 0
        price = decimal.Decimal("%.2f" % float(0))
        IsCharged = 0
        for order_item_info in order_item_infos:
            if order_item_info:
                SellerSKU = order_item_info['SellerSKU']
                ShopSKU = order_item_info['ShopSKU']
                print '------------SellerSKU: %s, ShopSKU: %s----------------'%(SellerSKU,ShopSKU)
                sellerSKUs = SellerSKU.split('+')
                count = 1
                for sellerSKU in sellerSKUs:
                    print '**********sellerSKU: %s, ShopSKU: %s**********' % (sellerSKU, ShopSKU)
                    if ShopSKU in sellerSKU:
                        sku_count = sellerSKU.split('*')
                        print '============sellerSKU: %s, ShopSKU: %s===========' % (sellerSKU, ShopSKU)
                        if len(sku_count)>1:
                            count = int(sku_count[1])
                            print 'count: %s'%count
                weight += order_item_info['Weight'] * count
                price += order_item_info['CostPrice'] * count
                if order_item_info['IsCharged'] == '1':
                    IsCharged = 1
        max_price = float(0)
        if weight>0 and price>0:
            #EXCHANGE_RATE 汇率
            #TRACK_PRICE_ELEC 带电
            #TRACK_DEAL_WEIGHT 处理克重500
            #PROFIT_RATE 利润率
            # track_price = decimal.Decimal("%.2f" % (params['EXCHANGE_RATE'] * params['TRACK_PRICE_ELEC'])) * weight
            # if IsCharged == 1:
            #     track_price = decimal.Decimal("%.2f" % (params['EXCHANGE_RATE'] * params['TRACK_PRICE_UNELEC'])) * weight
            weight_count = int(weight / params['TRACK_DEAL_WEIGHT'])
            if (weight - params['TRACK_DEAL_WEIGHT']) % params['TRACK_DEAL_WEIGHT'] == 0:
                lastCount = weight_count
            else:
                lastCount = weight_count + 1
            track_deal_price = params['EXCHANGE_RATE'] * lastCount * params['TRACK_DEAL_PRICE']

            all_price = (float(track_deal_price) + (float(1.083325) * float(price) + float(params['TRACK_PRICE_ELEC']) * float(weight)) * float(params['EXCHANGE_RATE']) +
                         float(23.6)) * float(float(1) + float(params['PROFIT_RATE'])) + (float(price) * float(params['EXCHANGE_RATE']))
            max_price = all_price / (0.6705 - 0.3295 * float(params['PROFIT_RATE']))

            # all_price = (float(track_deal_price) + (1.083325 * float(price) + params['TRACK_PRICE_ELEC'] * weight) * params['EXCHANGE_RATE'] +
            #              23.6) * float(1 + params['PROFIT_RATE']) + (float(price) * params['EXCHANGE_RATE'])
            # max_price = all_price / (0.6705 - 0.3295 * float(params['PROFIT_RATE']))
            max_price = (int(max_price) / 10) * 10 + 9
            # max_price = decimal.Decimal("%.2f" % float(4000))*(track_price + decimal.Decimal("%.2f" % track_deal_price)
            #                   + decimal.Decimal("%.2f" % float(1.103))*price_india
            #                   + decimal.Decimal("%.2f" % float(24.6)))/decimal.Decimal("%.2f" % float(1187))
        return max_price

    def data_to_pdf(self, params):
        story=[]
        stylesheet=getSampleStyleSheet()
        normalStyle = stylesheet['Normal']
        rpt_title = '<para autoLeading="off" fontSize=10 align=right>%s<br/><br/></para>'%params['orderNumber']['track_number']
        story.append(Paragraph(rpt_title,normalStyle))
        # 表格数据：用法详见reportlab-userguide.pdf中chapter 7 Table
        component_data = [
            ['Marketed by', params['MARKETED']],
            ['Manufactured by', params['MANUFACTURED']],
            ['MRP(all india)', params['mrp']],
            ['Expiry date', params['expiry_date']],
            ['Customer care number/email id:', params['CUSTOMER_PHONE']],
            ['', params['END_MESSAGE']],
        ]
        # 创建表格对象，并设定各列宽度
        component_table = Table(component_data, colWidths=[200, 250])
        # 添加表格样式
        component_table.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), int(params['TABLE_WIDTH'])),  # 字体大小
            ('ALIGN', (-1, 0), (-2, 0), 'RIGHT'),  # 对齐
            ('VALIGN', (-1, 0), (-2, 0), 'RIGHT'),  # 对齐
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # 设置表格框线为红色，线宽为0.5
        ]))
        story.append(component_table)

        doc = SimpleDocTemplate(params['filepath'])
        doc.build(story)

    def generate_price_info_pdf(self, params):
        t_order_amazon_india_obj = t_order_amazon_india(connection)
        amazon_india_sn =  t_order_amazon_india_obj.getShopNameByOrderId(OrderId=params['orderNumber']['orderId'])
        if amazon_india_sn['code'] <> 0:
            return
        amzon_india_price_config_obj = amzon_india_price_config(connection)
        price_config = amzon_india_price_config_obj.getAmazonPriceCofig(ShopName=amazon_india_sn['data'][0])
        if price_config['code'] <> 0:
            return
        params['EXCHANGE_RATE'] = float(price_config['data']['EXCHANGE_RATE'])
        params['PROFIT_RATE'] = float(price_config['data']['PROFIT_RATE'])
        params['TRACK_PRICE_ELEC'] = float(price_config['data']['TRACK_PRICE_ELEC'])
        params['TRACK_PRICE_UNELEC'] = float(price_config['data']['TRACK_PRICE_UNELEC'])
        params['TRACK_DEAL_WEIGHT'] = decimal.Decimal("%.2f" %float(price_config['data']['TRACK_DEAL_WEIGHT']))
        params['TRACK_DEAL_PRICE'] = float(price_config['data']['TRACK_DEAL_PRICE'])
        params['MARKETED'] = price_config['data']['MARKETED']
        params['MANUFACTURED'] = price_config['data']['MANUFACTURED']
        params['MRP_START'] = price_config['data']['MRP_START']
        params['MRP_END'] = price_config['data']['MRP_END']
        params['CUSTOMER_PHONE'] = price_config['data']['CUSTOMER_PHONE']
        params['END_MESSAGE'] = price_config['data']['END_MESSAGE']
        params['TABLE_WIDTH'] = price_config['data']['TABLE_WIDTH']
        date_time = datetime.datetime.now()
        date_time = date_time + datetime.timedelta(days=365)
        expiry_date = '%s' % datetime.datetime.strftime(date_time, '%B %d, %Y')
        max_price = self.get_max_price(params)
        if max_price>0:
            params['expiry_date'] = expiry_date
            params['mrp'] = params['MRP_START'] + str(max_price) + params['MRP_END']
            self.data_to_pdf(params)

    def fba_data_to_pdf(self, params, result_sku_info):
        c = canvas.Canvas(params['filepath'],pagesize=(1180,380))
        # p.rotate(90)
        c.rect(0.3 * inch, 0.32 * inch, 16.0 * inch, 4.5 * inch, fill=0)#添加边框，左边距，下边距，左边距+边框长，边框高度
        c.setFont("Helvetica", 43)#设置字体，大小
        textobject = c.beginText()
        textobject.setTextOrigin(0.4 * inch, 4.22 * inch)#字体左边距，下边距
        company_first = result_sku_info['company']
        company_end = ''
        if len(result_sku_info['company']) > 23:
            company_first = result_sku_info['company'][:22]
            if len(result_sku_info['company']) > 24:
                if result_sku_info['company'][22] == ' ' or result_sku_info['company'][23] == ' ':
                    company_end = result_sku_info['company'][23:]
                else:
                    company_end = '-' + result_sku_info['company'][23:]
        textobject.textLine('Marketed & Imported By: %s'%company_first)
        textobject.textLine('                                       %s'%company_end)
        textobject.textLine('Weight: %s grams' % str(result_sku_info['weight']))
        textobject.textLine('Color: %s' % result_sku_info['color'])
        textobject.textLine('Date Of Manufacturing: %s' % result_sku_info['expiry_date'])
        textobject.textLine('MRP: RS. %s/-(inclusive of all taxes)' % str(result_sku_info['price']))
        c.drawText(textobject)
        c.showPage()
        c.save()

    def get_price_and_weight_color_by_sku(self,all_skus, params):
        import re
        if len(all_skus) > 1:
            color_map = 'Mixed Color'
        else:
            sku_temp = all_skus.keys()[0]
            if sku_temp[-3:].isalnum():
                sub_temp = re.sub(r'([\d]+)', '', sku_temp[-5:])
                t_sku_color_obj = t_sku_color(connection)
                color_map = t_sku_color_obj.get_color_name_us_by_sku(sub_temp)
                if color_map:
                    color_map = color_map.get('color_name_us','')
                else:
                    color_map = 'Mixed Color'
            else:
                color_map = 'Mixed Color'
        weight = 0
        price = decimal.Decimal("%.2f" % float(0))
        IsCharged = 0
        for sku, sku_values in all_skus.items():
            each_weight = classsku(db_cnxn=connection).get_weight_by_sku(sku)
            each_price = classsku(db_cnxn=connection).get_price_by_sku(sku)
            if each_weight:
                weight += int(float(each_weight) * float(sku_values))
            if each_price:
                price += decimal.Decimal("%.2f" % float(each_price)) * int(sku_values)
            if classsku().get_isCharged_by_sku(sku_values) == '1':
                IsCharged = 1
        max_price = float(0)
        if weight > 0 and price > 0:
            # EXCHANGE_RATE 汇率
            # TRACK_PRICE_ELEC 带电
            # TRACK_DEAL_WEIGHT 处理克重500
            # PROFIT_RATE 利润率
            # track_price = decimal.Decimal("%.2f" % (params['EXCHANGE_RATE'] * params['TRACK_PRICE_ELEC'])) * weight
            # if IsCharged == 1:
            #     track_price = decimal.Decimal("%.2f" % (params['EXCHANGE_RATE'] * params['TRACK_PRICE_UNELEC'])) * weight
            weight_count = int(weight / params['TRACK_DEAL_WEIGHT'])
            if (weight - params['TRACK_DEAL_WEIGHT']) % params['TRACK_DEAL_WEIGHT'] == 0:
                lastCount = weight_count
            else:
                lastCount = weight_count + 1
            track_deal_price = params['EXCHANGE_RATE'] * lastCount * params['TRACK_DEAL_PRICE']
            all_price = (float(track_deal_price) + (1.083325 * float(price) + params['TRACK_PRICE_ELEC'] * weight) * params['EXCHANGE_RATE'] +
                        float(23.6)) * float(1 + params['PROFIT_RATE']) + (float(price) * params['EXCHANGE_RATE'])
            max_price = all_price / (0.6705 - 0.3295 * params['PROFIT_RATE'])
            max_price = (int(max_price) / 10) * 10 + 9
            # max_price = decimal.Decimal("%.2f" % float(4000))*(track_price + decimal.Decimal("%.2f" % track_deal_price)
            #                   + decimal.Decimal("%.2f" % float(1.103))*price_india
            #                   + decimal.Decimal("%.2f" % float(24.6)))/decimal.Decimal("%.2f" % float(1187))
        result_sku_info = {'color': color_map, 'price': max_price, 'weight': weight}
        return result_sku_info

    def zip_ya(self, startdir,file_news):
        # startdir 要压缩的文件夹路径
        # file_news 压缩后文件夹的名字
        try:
            z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)  # 参数一：文件夹名
            for dirpath, dirnames, filenames in os.walk(startdir):
                fpath = dirpath.replace(startdir, '')  # 这一句很重要，不replace的话，就从根目录开始复制
            fpath = fpath and fpath + os.sep or ''  # 这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
            for filename in filenames:
                z.write(os.path.join(dirpath, filename), fpath + filename)
            print ('压缩成功')
            z.close()
            result_msg = 1
        except Exception,e:
            result_msg = -1
        return result_msg

    def generate_fba_price_pdf(self,all_sku_list, upload_path, shopname, timestamp):
        from brick.public.clear_dir import clear_p
        from brick.public.create_dir import mkdir_p
        filePath = '/data/djangostack-1.9.7/apps/django/django_projects/Project/media/Amazon/IN/fba/price/'
        clear_p(filePath)
        mkdir_p(filePath)
        params = {}
        amzon_india_price_config_obj = amzon_india_price_config(connection)
        price_config = amzon_india_price_config_obj.getAmazonPriceCofig(ShopName=shopname)
        if price_config['code'] <> 0:
            return
        params['EXCHANGE_RATE'] = float(price_config['data']['EXCHANGE_RATE'])
        params['PROFIT_RATE'] = float(price_config['data']['PROFIT_RATE'])
        params['TRACK_PRICE_ELEC'] = float(price_config['data']['TRACK_PRICE_ELEC'])
        params['TRACK_PRICE_UNELEC'] = float(price_config['data']['TRACK_PRICE_UNELEC'])
        params['TRACK_DEAL_WEIGHT'] = decimal.Decimal("%.2f" % float(price_config['data']['TRACK_DEAL_WEIGHT']))
        params['TRACK_DEAL_PRICE'] = float(price_config['data']['TRACK_DEAL_PRICE'])
        params['MARKETED'] = price_config['data']['MARKETED']
        params['MANUFACTURED'] = price_config['data']['MANUFACTURED']
        params['MRP_START'] = price_config['data']['MRP_START']
        params['MRP_END'] = price_config['data']['MRP_END']
        params['CUSTOMER_PHONE'] = price_config['data']['CUSTOMER_PHONE']
        params['END_MESSAGE'] = price_config['data']['END_MESSAGE']
        params['TABLE_WIDTH'] = price_config['data']['TABLE_WIDTH']
        count = 1
        for all_skus in all_sku_list:
            for sku,sku_values in all_skus.items():
                result_sku_info = self.get_price_and_weight_color_by_sku(sku_values, params)
                result_sku_info['company'] = params['MARKETED']
                params['filepath'] = filePath + str(count) + '.pdf'
                result_sku_info['expiry_date'] = (datetime.datetime.now() + datetime.timedelta(days=-60)).strftime("%d/%m/%Y")
                self.fba_data_to_pdf(params, result_sku_info)
                count += 1
        new_filePath = filePath[:-1]
        result_msg = self.zip_ya(new_filePath, new_filePath + '.zip')
        if result_msg == 1:
            upload_to_oss_obj = upload_to_oss('fancyqube-download')
            upload_params = {'path': upload_path, 'name': 'FBA_Price_%s.zip'%timestamp, 'byte': open(new_filePath + '.zip'), 'del': 1}
            upload_to_oss_obj.upload_to_oss(upload_params)
            t_download_info.objects.create(appname=upload_path + '/FBA_Price_%s.zip'%timestamp, abbreviation='FBA_Price_%s.zip'%timestamp,
                                           updatetime=datetime.datetime.now(), Belonger=upload_path.split('/')[-1],
                                           Datasource='t_order_amazon_india_fba')




# coding=utf-8

"""
导出wish待铺货表格
"""

from Project.settings import *
# from skuapp.modelsadminx.t_product_Admin import mkdir_p
import oss2
import errno
import re
from xlwt import *
from django.db import connection
from brick.public.generate_shop_code import generate_code_func
from brick.function.generate_random_title import get_new_title
from random import choice
from brick.joom.upload_picture_to_vps import upload_picture_to_vps
from django_redis import get_redis_connection
redis_db = get_redis_connection(alias='product')
from brick.pricelist.calculate_price import calculate_price


PREFIX = 'http://'
ACCESS_KEY_ID = 'LTAIH6IHuMj6Fq2h'
ACCESS_KEY_SECRET = 'N5eWsbw8qBkMfPREkgF2JnTsDASelM'
# ENDPOINT = 'vpc100-oss-cn-shanghai.aliyuncs.com'
ENDPOINT_OUT = 'oss-cn-shanghai.aliyuncs.com'
BUCKETNAME = 'fancyqube-download'


def export_joom_wait_upload_excel(id_list, export_user, export_time, coreWordsList, shopname='joom3', calculate_flag=0):
    cur = connection.cursor()
    profit = get_profit(shopname)
    export_time_format = export_time.strftime('%Y%m%d%H%M%S')

    # 设置redis缓存
    if calculate_flag == 1:
        filename = export_user + '_' + export_time_format + '_max_price' + '.xls'
    else:
        filename = export_user + '_' + export_time_format + '.xls'
    total = len(id_list)
    processed = 0
    set_redis_cache(shopname, filename, total, processed)

    # 先将记录插入到下载中心
    insert_sql = 'insert into t_download_info(appname, abbreviation, updatetime, Belonger, Datasource) values(%s,%s,%s,%s,%s)'
    params = (shopname + '/' + filename, shopname + u'刊登导出', export_time_format, export_user, u'joom刊登导出')
    cur.execute(insert_sql, params)
    connection.commit()

    if len(id_list) == 1:
        sql = 'select MainSKU, Title, Description, Tags, MainImage, ExtraImages, Variants, CoreWords, B_cost_weight' \
              ' from t_templet_joom_wait_upload where id=%s ' % id_list[0]
    else:
        sql = 'select MainSKU, Title, Description, Tags, MainImage, ExtraImages, Variants, CoreWords, B_cost_weight' \
                ' from t_templet_joom_wait_upload where id IN ' + str(tuple(id_list))
    cur.execute(sql)
    infos = cur.fetchall()

    path = MEDIA_ROOT + 'download_xls/' + export_user
    mkdir_p(MEDIA_ROOT + 'download_xls')
    os.popen('chmod 777 %s' % (MEDIA_ROOT + 'download_xls'))

    mkdir_p(path)
    os.popen('chmod 777 %s' % (path))

    w = Workbook()
    sheet = w.add_sheet('joom')

    sheet.write(0, 0, u'JoomSKU')
    sheet.write(0, 1, u'ShopSKU')
    sheet.write(0, 2, u'CostPrice')
    sheet.write(0, 3, u'Weight')
    sheet.write(0, 4, u'Parent Unique ID')
    sheet.write(0, 5, u'Product Name')
    sheet.write(0, 6, u'Description')
    sheet.write(0, 7, u'Tags')
    sheet.write(0, 8, u'Unique ID')
    sheet.write(0, 9, u'Color')
    sheet.write(0, 10, u'Size')
    sheet.write(0, 11, u'Quantity')
    sheet.write(0, 12, u'Price')
    sheet.write(0, 13, u'MSRP')
    sheet.write(0, 14, u'Shipping')
    sheet.write(0, 15, u'Shipping Time')
    sheet.write(0, 16, u'Product Main Image URL')
    sheet.write(0, 17, u'Variant Main Image URL')
    sheet.write(0, 18, u'Extra Image URL1')
    sheet.write(0, 19, u'Extra Image URL2')
    sheet.write(0, 20, u'Extra Image URL3')
    sheet.write(0, 21, u'Extra Image URL4')
    sheet.write(0, 22, u'Extra Image URL5')
    sheet.write(0, 23, u'Extra Image URL6')
    sheet.write(0, 24, u'Extra Image URL7')
    sheet.write(0, 25, u'Extra Image URL8')
    sheet.write(0, 26, u'Extra Image URL9')
    sheet.write(0, 27, u'Extra Image URL10')

    # 写数据
    row = 0

    for info in infos:
        # 生成新标题
        new_title = get_new_title(coreWordsList, info[7], info[1])
        main_image = get_main_image(info[0])
        if main_image == '':
            main_image = info[4]

        variation_image_list = []
        extra_image_list = info[5].split('|')
        b_cost_weight = []

        try:
            variations = eval(info[6])
            for variation in variations:
                variation_image_list.append(variation['Variant']['main_image'])
            b_cost_weight = eval(info[8])
        except:
            pass

        if calculate_flag == 1:
            max_price = get_max_price(variations, profit)

        # 将主图、变种图、副图传参到upload_picture_to_vps， 返回处理后的图片链接，相同的数据格式
        image = {'shopname':shopname, 'main_image':main_image, 'variation_image_list':variation_image_list, 'extra_image_list':extra_image_list}
        result = upload_picture_to_vps(image)

        length = len(variations)
        for i in range(length):
            joom_shopsku = ''

            shopsku = variations[i]['Variant']['sku']
            product_sku = variations[i]['Variant']['productSKU']
            color = variations[i]['Variant']['color']
            size = variations[i]['Variant']['size']
            inventory = variations[i]['Variant']['inventory']
            if calculate_flag == 1:
                price = max_price
            else:
                price = variations[i]['Variant']['price']
            msrp = variations[i]['Variant']['msrp']
            shipping = variations[i]['Variant']['shipping']
            shipping_time = variations[i]['Variant']['shipping_time']

            # 插入到店铺sku申请表
            # insert_banding_apply(shopname, product_sku, joom_shopsku, export_user, export_time_format)

            cost_price = ''
            weight = ''
            try:
                for each in b_cost_weight:
                    if each.has_key(product_sku):
                        weight = each.get(product_sku, '').get('weight', '')
                        cost_price = each.get(product_sku, '').get('cost_price', '')
                        break
            except:
                pass

            row = row + 1
            column = 0
            sheet.write(row, column, joom_shopsku)

            column = column + 1
            sheet.write(row, column, shopsku)

            column = column + 1
            sheet.write(row, column, cost_price)

            column = column + 1
            sheet.write(row, column, weight)

            column = column + 1
            sheet.write(row, column, info[0])

            column = column + 1
            sheet.write(row, column, new_title)

            column = column + 1
            sheet.write(row, column, clean_unknow_code(info[2]))

            column = column + 1
            sheet.write(row, column, info[3])

            column = column + 1
            sheet.write(row, column, product_sku)

            column = column + 1
            sheet.write(row, column, color)

            column = column + 1
            sheet.write(row, column, size)

            column = column + 1
            sheet.write(row, column, inventory)

            column = column + 1
            sheet.write(row, column, price)

            column = column + 1
            sheet.write(row, column, msrp)

            column = column + 1
            sheet.write(row, column, shipping)

            column = column + 1
            sheet.write(row, column, shipping_time)

            column = column + 1
            sheet.write(row, column, result['main_image'])

            column = column + 1
            variation_image = result['variation_image_list'][i]
            if variation_image != -1 and variation_image != 1:
                sheet.write(row, column, variation_image)
            else:
                sheet.write(row, column, '')

            for j in range(10):
                column = column + 1
                try:
                    extra_image = result['extra_image_list'][j]
                    if extra_image != -1 and extra_image != 1:
                        sheet.write(row, column, extra_image)
                    else:
                        sheet.write(row, column, '')
                except:
                    sheet.write(row, column, '')
                    pass

        # 更新redis缓存
        processed += 1
        set_redis_cache(shopname, filename, total, processed)

    w.save(path + '/' + filename)
    os.popen(r'chmod 777 %s' % (path + '/' + filename))

    # 上传oss对象
    auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, ENDPOINT, BUCKETNAME)
    bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)
    # 删除现有的
    for object_info in oss2.ObjectIterator(bucket,
                                           prefix='%s/%s_' % (export_user, export_user)):
        bucket.delete_object(object_info.key)
    bucket.put_object(u'%s/%s' % (shopname, filename), open(path + '/' + filename))
    cur.close()


def get_main_image(mainsku):
    """
    查找joom主图
    :param mainsku: 主SKU
    :return: 主图路径
    """
    cur = connection.cursor()
    sql = 'select WishPic from t_product_mainsku_pic where MainSKU=\"%s\" AND FlagJoom=1' % mainsku
    cur.execute(sql)
    MainImageList = cur.fetchall()

    main_image = ''
    if len(MainImageList) != 0:
        main_image = choice(MainImageList)[0]
    return main_image


def set_redis_cache(shopname, filename, total, processed):
    """
    设置redis缓存
    :param shopname: 店铺名
    :param filename: 文件名
    :param total: 需要下载的总数
    :param processed: 已经下载的数目
    :return:
    """
    name = shopname + '/' + filename
    redis_db.hset(name, 'total', total)
    redis_db.hset(name, 'processed', processed)


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def clean_unknow_code(description):
    """
    清除描述中的未知字符
    :param description: 描述
    :return: 去除未知字符的描述
    """
    pattern = r'\\u[a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9]'
    new_description = ''.join(re.split(pattern, description))
    return new_description


# def insert_banding_apply(shopname, product_sku, joom_shopsku, user, time):
#     """
#     将记录插入到店铺sku申请表
#     :param shopname: 店铺名
#     :param product_sku: 商品sku
#     :param joom_shopsku: joom商品sku
#     :param user: 申请人
#     :param time: 申请时间
#     :return:
#     """
#     cur = connection.cursor()
#     param = (shopname, 'productsku', product_sku, joom_shopsku, user, time, 'notyet', 'never')
#     sql = 'insert into t_use_productsku_apply_for_shopsku(ShopName, ApplyType, ProductSKU, ShopSKU, Applicant, ' \
#           'ApplyTime, BStatus, EStatus) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
#     cur.execute(sql, param)
#     cur.execute('commit;')
#     cur.close()


def get_max_price(variations, profit):
    max_price = 0
    price_list = []
    for variation in variations:
        product_sku = variation['Variant']['productSKU']
        try:
            price = float(variation['Variant']['price'])
        except:
            price = 0
        price_list.append(price)

        calculate_price_obj = calculate_price(SKU=product_sku)
        param = calculate_price_obj.calculate_selling_price(profitRate=profit)
        this_price = param.get('sellingPrice_us', 0)
        if this_price > max_price:
            max_price = this_price

    if max_price == 0:
        return max(price_list)
    else:
        return max_price

def get_profit(shopname):
    cur = connection.cursor()
    sql = 'select profit from t_config_online_ftp where ShopName=%s'
    cur.execute(sql, (shopname,))
    info = cur.fetchone()
    profit = None
    if info:
        if info[0]:
            profit = info[0]
    return profit

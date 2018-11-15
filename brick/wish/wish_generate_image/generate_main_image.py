# coding=utf-8


import time, os, sys, shutil
from datetime import datetime
from compare_image import get_hash, hamming_distance
from download_image import download_image
from db_operation import  DbOperation, connect_mysql


PICTURE_PATH = '/home/picture/'


def update_wish_image(client):
    try:
        cur = client.cursor()
        DbOperation_obj = DbOperation(cur)
        all_sku_pic_list = DbOperation_obj.get_updated_listing_pic()  # 获取最近更新的在线listing
        all_num = len(all_sku_pic_list)
        i = 0
        for single_sku_pic_list in all_sku_pic_list:
            i += 1
            print '--------------------------------------------------------------------------------------There are %s wish listing to be updated, Currently being updated is the %sth......' % (all_num, i)
            main_sku = single_sku_pic_list[0]
            update_modify_flag = 0
            exists_hash_str_list = DbOperation_obj.get_exists_hashstr(main_sku)  # 获取已经存在于图片库的hash
            if not exists_hash_str_list:  # 如果图片库没有改MainSKU图片，则在主图维护表新增此MainSKU
                DbOperation_obj.insert_image_modify(main_sku=main_sku)
            for image_url in single_sku_pic_list[1:]:
                image_path = download_image(image_url, main_sku)  # 下载图片返回图片本机物理地址
                if image_path:
                    current_hash_str = get_hash(image_path) # 得到已下载图片的hash
                else:
                    continue
                similar_flag = 0
                for exists_hash_str in exists_hash_str_list:
                    if not exists_hash_str:     # 如果图片的hash值为空，则不做去重校验，此情况多由于用户上传图片
                        continue
                    hamming_distance_num = hamming_distance(current_hash_str, exists_hash_str)   # 得到汉明距
                    if hamming_distance_num <= 400: # 如果两张图片的汉明距小于400，则图片相似
                        similar_flag = 1
                        break
                if similar_flag == 0:
                    exists_hash_str_list.append(current_hash_str)
                    DbOperation_obj.insert_new_url(main_sku, image_url, current_hash_str)    # 图片库插入一条新纪录
                    update_modify_flag += 1
                else:
                    os.remove(image_path)
            if update_modify_flag > 0:
                DbOperation_obj.sign_modify_update_flag(main_sku)

            delete_empty_folder(main_sku=main_sku)
        cur.close()
    except Exception, e:
        print e

def delete_empty_folder(main_sku):
    """删除空文件夹"""
    try:
        file_path = PICTURE_PATH + main_sku
        if not os.listdir(file_path):
            shutil.rmtree(file_path)
    except:
        pass

if __name__ == "__main__":
    client = connect_mysql()
    while True:
        start = time.time()
        try:
            client.ping()
        except:
            client = connect_mysql()
        update_wish_image(client)
        end = time.time()
        delta = int(end-start)
        now = str(datetime.now())
        print '[%s]  This update took %s seconds, And the next plan will be executed in 4 hours……' % (now, delta)
        time.sleep(6*60*60)
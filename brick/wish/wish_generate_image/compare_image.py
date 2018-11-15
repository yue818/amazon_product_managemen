# coding=utf-8

"""
get_hash：获取图片的hash值
hamming_distance：得到两张图片的相似度
"""

import numpy as np
import cv2


def get_hash(image_path):
    """输入图片路径，返回hash字符串"""
    image_byte = cv2.imread(image_path)
    image_byte_64 = cv2.resize(image_byte, (64, 64))
    image_gray = cv2.cvtColor(image_byte_64, cv2.COLOR_BGR2GRAY)
    # 将灰度图转为浮点型，再进行dct变换
    image_dct = cv2.dct(np.float32(image_gray))
    avreage = np.mean(image_dct)
    hash_str = ''
    for i in range(image_dct.shape[0]):
        for j in range(image_dct.shape[1]):
            if image_dct[i, j] > avreage:
                hash_str += '1'
            else:
                hash_str += '0'
    return hash_str


def hamming_distance(hash_str_1, hash_str_2):
    """计算汉明距离"""
    hamming_distance_num = 0
    length = len(hash_str_1)
    for index in range(length):
        if hash_str_1[index] != hash_str_2[index]:
            hamming_distance_num += 1
    return hamming_distance_num



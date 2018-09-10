# # -*- coding:utf-8 -*-
#
# """
#  @desc:
#  @author: wuchongxiang
#  @site:
#  @software: PyCharm
#  @file: dict_test.py
#  @time: 2018-06-04 13:18
# """
# from django.db import models
#
# class t_templet_amazon_collection_box(object):
#
#     def __init__(self):
#         self.db = 'jshdahsgh'
#
#     a = 'eyeyye'
#     def  test(self):
#         b = 'bbbbb'
#
#
#
#
# obj = t_templet_amazon_collection_box()
#
# print obj.__dict__


matrix = [[1, 2, 3, 4],[5, 6, 7, 8],[9, 10, 11, 12], ]
print matrix
for i in matrix:
    print i

list1 = [ [row[i] for row in matrix] for i in range(4)]
print list1
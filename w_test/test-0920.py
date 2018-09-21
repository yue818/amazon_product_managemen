# coding:utf-8

"""
冒泡排序
1. 外层循环表示比较趟数
2. 内层循环两两比较该趟内需边角的元素

第1趟 将最大值放到最后
第2趟 将次最大值放到倒二位置
……
第n-1趟 将次最小值放到第二位置 完成排序
"""


def bubble_sort(num_list):
    for i in range(1, len(num_list)):
        print '\n原始列表为：%s' % num_list
        print '目前是第 %d 趟比较' % i
        for j in range(len(num_list)-i):
            print ' '*2, '比较 %d 和 %d 元素 => %s 和 %s' % (j, j+1, num_list[j], num_list[j+1])
            if num_list[j] > num_list[j+1]:
                # num_list[j], num_list[j+1] = num_list[j+1], num_list[j]
                num_list[j+1], num_list[j] = num_list[j], num_list[j+1]
                print ' '*4, '满足交换条件，交换后列表为 %s' % num_list
        print '第 %d 趟比较后，列表变为: %s' % (i, num_list)
    return num_list


nums = [9, 8, 7, 6, 5, 4, 3, 2, 1]
bubble_sort(nums)


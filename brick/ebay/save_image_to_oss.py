# coding=utf-8

from brick.function.oss_operation import oss_operation
from get_pic import get_pic


def save_image_to_oss(img_urls):
    """
    将ebay图片上传到OSS上
    :param img_urls: 图片链接列表
    :param img_names: 图片名列表
    """

    BUCKETNAME = 'fancyqube-ebaypic'
    oss = oss_operation(BUCKETNAME)

    for url in img_urls:
        resp = get_pic(url)

        if resp == 'ERROR':
            continue
        else:
            if url.endswith('.JPG'):
                pass
            else:
                url += '.JPG'

            try:
                oss_pic_name = url.split('i.ebayimg.com/')[-1].split('?')[0]
                oss.bucket.put_object(u'%s' % oss_pic_name, resp)
            except Exception, e:
                print 'save_image_to_oss-----------------------', e
                pass
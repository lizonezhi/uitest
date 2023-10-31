#!/usr/bin/env python
# coding=utf-8
from PIL import Image


class ImageUtil:

    def crop(self, x, y, w, h, filename=None, filename_crop=None):
        '''
        filename：原图片  filename_crop：剪切后的图片
        裁剪：传入一个元组作为参数
        元组里的元素分别是：（距离图片左边界距离x， 距离图片上边界距离y，距离图片左边界距离+裁剪框宽度x+w，距离图片上边界距离+裁剪框高度y+h）
        例如：截取图片中一块宽和高都是250的
            x = 100
            y = 100
            w = 250
            h = 250
        '''
        if not filename:
            filename = "screenshot.png"
        im = Image.open(filename)
        # 图片的宽度和高度
        # img_size = im.size
        # print("图片宽度和高度分别是{}".format(img_size))
        region = im.crop((x, y, x + w, y + h))
        if not filename_crop:
            filename_crop = "filename_crop.png"
        return region.save(filename_crop)

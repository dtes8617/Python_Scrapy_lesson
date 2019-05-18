# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

class CraigslistPipeline(object):
    def process_item(self, item, spider):
        os.chdir(r'E:/Users/Jude/Documents/GitHub/Python_Scrapy_lesson/Practice/craigslist/Pictures')
        images_info = item['images']
        for i, image_info in enumerate(images_info):
            image_new_path = './full/' + item['title'][0] + '_image_' + str(i) + '.jpg'
            os.rename(image_info['path'], image_new_path)
        return item

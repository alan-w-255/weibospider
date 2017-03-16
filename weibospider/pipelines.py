# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#import os
#import urllib
#import scrapy
#from scrapy.exceptions import DropItem
#from scrapy.pipelines.images import ImagesPipeline
#
#from weibospider import settings
#
#class WBImgPipeline(ImagesPipeline):
#    def get_media_requests(self, item, info):
#        for image_url in item['image_urls']:
#            yield scrapy.Request(image_url)
    

class WeibospiderPipeline(object):
    def process_item(self, item, spider):
        return item

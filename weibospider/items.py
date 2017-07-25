# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
#from scrapy.pipelines.images import ImagesPipeline


class WeibospiderItem(scrapy.Item):
    # define the fields for your item here like:
    mblog_text = scrapy.Field()
    created_at = scrapy.Field()
    user_id = scrapy.Field()
    user_screen_name = scrapy.Field()
    user_gender = scrapy.Field()
    attitudes_count = scrapy.Field()
    comments_count = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    scheme = scrapy.Field()

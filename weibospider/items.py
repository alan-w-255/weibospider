# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeibospiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    weibo_text = scrapy.Field()
    auther_id = scrapy.Field()
    weibo_date = scrapy.Field()
    #screen_name = scrapy.Field()
    #create_at = scrapy.Field()

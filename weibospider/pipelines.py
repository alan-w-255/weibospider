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

import scrapy
import psycopg2
from weibospider.items import WeibospiderItem
import logging


class PostgreSQLPipeline(object):
    def process_item(self, item, spider):
        conn = psycopg2.connect(database='weibo_crawl_db', user='alan', password='helloalan')
        sql_insert_weibo = '''\
            insert into weibo_crawled_data (itemid, mblog_text, created_at, user_id, user_screen_name, user_gender, attitudes_count, comments_count, image_urls, iamges, scheme) values({itemid}, {mblog_text}, {created_at}, {user_id}, {user_screen_name}, {user_gender}, {attitudes_count}, {comments_count}, {image_urls}, {scheme})
        '''.format(
            itemid=item['itemid'].replace('_-_', '-'),
            mblog_text=item['mblog_text'],
            created_at=item['created_at'],
            user_id=item['user_id'],
            user_screen_name=item['user_screen_name'],
            user_gender=item['user_gender'],
            attitudes_count=item['attitudes_count'],
            comments_count=item['comments_count'],
            image_urls=item['image_urls'],
            scheme=item['scheme']
            )
        try:
            cur = conn.cursor()
            cur.execute(sql_insert_weibo)
            conn.commit()
            logging.debug('Data added to PostgreSQL DB')
        except Exception as e:
            print('insert record into table failed')
            print(e)
        finally:
            if cur:
                cur.close()
        conn.close()
        return item












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

import time
import scrapy
import psycopg2
import base64
from weibospider.items import WeibospiderItem
import logging

class PreProcessPipeline(object):
    """
    格式化日期
    """
    def process_item(self, item, spider):
        if '前' in item['created_at'] or '今天' in item['created_at']:
            item['created_at'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        else:
            t = item['created_at'].split(' ')[0]
            if len(t) == 5:
                t = '2017-' + t
            item['created_at'] = t

        return item


class PostgreSQLPipeline(object):
    def process_item(self, item, spider):
        if item['image_urls']:
            image_urls = str(set(item['image_urls']))
            image_urls = image_urls.replace("'", '"')
        else:
            image_urls = '{}'
        
        mblog_text = base64.b64encode(bytes(item['mblog_text'], 'utf8'))
        mblog_text = mblog_text.decode(encoding='utf8')

        conn = psycopg2.connect(database='weibo_crawl_db', user='alan', password='helloalan')
        sql_insert_weibo = '''\
            insert into weibo_crawled_data (mblog_text, created_at, user_id, user_screen_name, user_gender, attitudes_count, comments_count, image_urls, scheme) values('{mblog_text}', '{created_at}', {user_id}, '{user_screen_name}', '{user_gender}', {attitudes_count}, {comments_count}, '{image_urls}', '{scheme}')
        '''.format(
            mblog_text=mblog_text,
            created_at=item['created_at'],
            user_id=item['user_id'],
            user_screen_name=item['user_screen_name'],
            user_gender=item['user_gender'],
            attitudes_count=item['attitudes_count'],
            comments_count=item['comments_count'],
            image_urls=image_urls,
            scheme=item['scheme']
            )
        print(sql_insert_weibo)
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

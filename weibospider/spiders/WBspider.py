# -*- coding: utf-8 -*-
import json
import scrapy
from weibospider.items import WeibospiderItem

class WbspiderSpider(scrapy.Spider):
    name = "wbspider"

    start_urls=[
        'https://m.weibo.cn/api/container/getIndex?jumpfrom=weibocom&containerid=1008084e073a22a66dfd2fd8a9c2f8defd31d5_-_feed'
    ]


    def _extractCardType9Info(self, card):
        _p_urls = []
        try:
            pics = card['mblog']['pics']
            for _p in pics:
                _p_urls.append(_p['url'])
        except Exception as e:
            pass

        _item = WeibospiderItem()
        _item['scheme'] = card['scheme']
        _item['mblog_text'] = card['mblog']['text']
        _item['created_at'] = card['mblog']['created_at']
        _item['user_id'] = card['mblog']['user']['id']
        _item['user_screen_name'] = card['mblog']['user']['screen_name']
        _item['user_gender'] = card['mblog']['user']['gender']
        _item['user_followers_count'] = card['mblog']['user']['followers_count']
        _item['attitudes_count'] = card['mblog']['attitudes_count']
        _item['comments_count'] = card['mblog']['comments_count']
        _item['image_urls'] = _p_urls

        return _item

    def _createNewRequestUrl(self, since_id):
        url_template = 'https://m.weibo.cn/api/container/getIndex?jumpfrom=weibocom&containerid=1008084e073a22a66dfd2fd8a9c2f8defd31d5_-_feed&since_id={since_id}'
        return url_template.format(since_id=since_id)


    def parse(self, response):
        #assert response.headers.get('Content-Type') == b'application/json; charset=utf-8'

        response_json = json.loads(response.body.decode('utf-8'))
        if response_json['ok'] != 1:
            self.logger.info('未返回期望结果!')
        else:
            # 提取since_id
            try:
                since_id = response_json['data']['pageInfo']['since_id']
                yield scrapy.Request(self._createNewRequestUrl(since_id))
            except KeyError as e:
                pass

            WBCards = response_json['data']['cards']
            for _c in WBCards:
                if _c['card_type'] == '11':
                    for WBCard in _c['card_group']:
                        if WBCard['card_type'] == 9:
                            print('card type 9')
                            # 9 号类型卡片, 微博类型, 提取微博文章信息.
                            yield self._extractCardType9Info(WBCard)
                        else:
                            pass
                else:
                    pass

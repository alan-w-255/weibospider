# -*- coding: utf-8 -*-
import json
import scrapy
from weibospider.items import WeibospiderItem

class WbspiderSpider(scrapy.Spider):
    name = "wbspider"

    start_urls=[
        'http://m.weibo.cn/container/getIndex?type=uid&value=1502844527&containerid=1076031502844527',
        'http://m.weibo.cn/container/getIndex?type=uid&value=2893057857&containerid=1076032893057857',
        'http://m.weibo.cn/container/getIndex?type=uid&value=5688724856&containerid=1076035688724856',
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

    def _createNewRequest(self, user_id, page_num):
        url_template = 'http://m.weibo.cn/container/getIndex?type=uid&value={userid}&containerid=107603{userid}'
        url = None
        if page_num == 1:
            url = url_template.format(userid=user_id)
        else:
            url_template += '&page={page_num}'
            url = url_template.format(userid=user_id, page_num=page_num)
        return url

    def _handleCardType11(self, card):
        # 从card type 11 中获取用户关注账号的id, 生成新的请求的列表
        following_users = []
        newRequests = []
        for _c in card['card_group']:
            if _c['card_type'] == 24:
                for _u in _c['elements']:
                    following_users.append(_u['uid'])
        for _u in following_users:
            newRequests.append(self._createNewRequest(_u, 1))
        return newRequests


    def parse(self, response):
        #assert response.headers.get('Content-Type') == b'application/json; charset=utf-8'

        response_json = json.loads(response.body.decode('utf-8'))
        if response_json['ok'] != 1:
            self.logger.info('未返回期望结果!')
        else:
            WBCards = response_json['data']['cards']
            for WBCard in WBCards:
                if WBCard['card_type'] == 9:
                    # 9 号类型卡片, 微博类型, 提取微博文章信息.

                    yield self._extractCardType9Info(WBCard)
                elif WBCard['card_type'] == 11:
                    # 该用户关注的微博用户的信息
                    for _r in self._handleCardType11(WBCard):
                        yield scrapy.Request(_r)
                else:
                    pass

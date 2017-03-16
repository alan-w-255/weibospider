# -*- coding: utf-8 -*-
import json
import scrapy
import unicodedata
from weibospider.items import WeibospiderItem

class WbspiderSpider(scrapy.Spider):
    name = "wbspider"

    start_urls=[
        'http://m.weibo.cn/container/getIndex?type=uid&value=1239246050&containerid=1076031239246050',
        'http://m.weibo.cn/container/getIndex?uid=3200673035&featurecode=20000180&type=uid&value=1239246050&containerid=1076033200673035',
        'http://m.weibo.cn/container/getIndex?uid=1502739807&featurecode=20000180&type=uid&value=1239246050&containerid=1076031502739807',
    ]

    def create_comment_ajax_requests(self, response: 'cardlist response', page_num):
        """
        根据cardlist response 中 每个card.itemid 返回request for comment 的列表
        """
        def get_commentids(response: 'cardlist response'):
            """
            从cardlistinfo response 中获取每个微博评论页面的id列表
            """
            response_json = json.loads(response.body.decode('utf-8'))
            cards = response_json['cards']
            commentids = []
            for card in cards:
                if card['card_type'] == 9:
                    commentids.append(card['itemid'].split('_-_')[-1])
            return commentids

        def create_msg_url(comment_id, page_num):
            """
            生成评论的ajax url
            """
            url_template = "http://m.weibo.cn/api/comments/show?id={id}&page={page_num}"
            return url_template.format(id=comment_id, page_num=page_num)

        _commentids = get_commentids(response)
        _urls = []
        for _id in _commentids:
            _urls.append(create_msg_url(_id, page_num))

        _req = []
        for u in _urls:
            _req.append(scrapy.Request(url=u, errback=None))

        return _req


    def create_mblog_page_requests(self, response: 'msg_response', page_num):
        """
        根据msg_response返回page=page_num 的request for cardlist
        """

        def get_userids(response):
            """
            从message response 中获取每个评论者的用户id
            """
            response_json = json.loads(response.body.decode('utf-8'))
            if 'data' in response_json:
                msgs = response_json['data']
                userids = []
                for msg in msgs:
                    userids.append(msg['user']['id'])
                return userids
            else:
                return []


        def create_cardlist_url(user_id, page_num):
            """
            生成id 为 user_id用户微博列表的ajax url
            """
            if page_num == 1:
                url_template = 'http://m.weibo.cn/container/getIndex?type=uid&value={userid}&containerid=107603{userid}'
                return url_template.format(userid=user_id)
            else:
                url_template += '&page={page_num}'
                return url_template.format(userid=user_id, page_num=page_num)
                
        _urls = []
        _userids = get_userids(response)
        for _id in _userids:
            _urls.append(create_cardlist_url(_id, page_num))
        _req = []
        for u in _urls:
            _req.append(scrapy.Request(url=u, errback=None))

        return _req


    def parse(self, response):
        #assert response.headers.get('Content-Type') == b'application/json; charset=utf-8'

        response_json = json.loads(response.body.decode('utf-8'))
        _response_type = None
        if 'msg' in response_json:
            _response_type = 'msg'
        elif 'cards' in response_json:
            _response_type = 'cards'

        if _response_type == 'cards':
            comment_ajax_requests = self.create_comment_ajax_requests(response, 1)
            for r in comment_ajax_requests:
                # 添加新的评论列表 请求
                yield r
            cards = response_json['cards']
            for card in cards:
                if card['card_type'] == 9:
                    #WeibospiderItem.itemid = card['itemid']
                    #WeibospiderItem.mblog_text = card['mblog']['text']
                    #WeibospiderItem.created_at = card['mblog']['created_at']
                    #WeibospiderItem.user_id = card['mblog']['user']['id']
                    #WeibospiderItem.user_screen_name = card['mblog']['user']['screen_name']
                    yield {
                        'itemid': card['itemid'],
                        'mblog_text': card['mblog']['text'],
                        'created_at': card['mblog']['created_at'],
                        'user_id': card['mblog']['user']['id'],
                        'user_screen_name': card['mblog']['user']['screen_name'],
                    }
                    print(card['mblog']['text'])
        elif _response_type == 'msg':
            mblog_page_requests = self.create_mblog_page_requests(response, 1)
            for r in mblog_page_requests:
                # 添加新的mblog_page 请求
                yield r
        else:
            pass

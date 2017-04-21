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


    def create_mblog_page_requests(self, response, page_num):
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

            # 提取xhr 中的数据
            cards = response_json['cards']
            for card in cards:
                if card['card_type'] == 9:
                        #get image urls of every mblog
                    _p_urls = []
                    try:
                        pics = card['mblog']['pics']
                        for _p in pics:
                            print(_p['url'])
                            _p_urls.append(_p['url'])
                    except Exception as e:
                        pass

                    _item = WeibospiderItem()
                    _item['itemid'] = card['itemid']
                    _item['scheme'] = card['scheme']
                    _item['mblog_text'] = card['mblog']['text']
                    _item['created_at'] = card['mblog']['created_at']
                    _item['user_id'] = card['mblog']['user']['id']
                    _item['user_screen_name'] = card['mblog']['user']['screen_name']
                    _item['user_gender'] = card['mblog']['user']['gender']
                    _item['attitudes_count'] = card['mblog']['attitudes_count']
                    _item['comments_count'] = card['mblog']['comments_count']
                    _item['image_urls'] = _p_urls

                    yield _item

        elif _response_type == 'msg':
            mblog_page_requests = self.create_mblog_page_requests(response, 1)
            for r in mblog_page_requests:
                # 添加新的mblog_page 请求
                yield r
        else:
            pass

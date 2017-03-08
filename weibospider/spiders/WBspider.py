# -*- coding: utf-8 -*-
import scrapy
from weibospider.items import WeibospiderItem
import json


class WbspiderSpider(scrapy.Spider):
    name = "WBspider"

    weibo_start_url = 'http://m.weibo.cn/container/getIndex?uid=1746664450&luicode=10000011&lfid=1076031746664450&featurecode=20000180&type=uid&value=1746664450&containerid=1076031746664450'

    weibo_start_headers = {
            "Host": "m.weibo.cn",
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
            "Referer": "http://m.weibo.cn/u/1218346612?uid=1218346612&luicode=10000011&lfid=1076031746664450",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "en-US,en;q=0.8",
            "Cookie": "_T_WM=75395c0795ce5d9d2eac9bc00a651e04; M_WEIBOCN_PARAMS=from%3Dfeed%26luicode%3D10000011%26lfid%3D1076031746664450%26fid%3D1005051218346612%26uicode%3D10000011"
        }

        
    def start_requests(self):
        yield scrapy.http.Request(url=self.weibo_start_url, headers=self.weibo_start_headers)


    def create_comment_ajax_url(self, comment_id, page_num):
        """
        生成评论的ajax url
        """
        url_template = "http://m.weibo.cn/api/comments/show?id={id}&page={page_num}"
        return url_template.format(id=comment_id, page_num=page_num)


    def parse(self, response):
        #需要判断返回的是html 还是json
        response_json = None
        Content_Type = response.headers.get('Content-Type')
        if Content_Type == b'text/html; charset=UTF-8':
            pass
        elif Content_Type == b'application/json; charset=utf-8':
            response_json = json.loads(response.body.decode('utf-8'))
        profile_urls = []
        scheme_urls = []
        next_90_page_urls = []
        if response_json is None:
            pass
        else:
            if 'msg' in response_json:
                #微博详情页面的ajax json
                #获取评论者的profile urls
                try:
                    msg_data = response_json['data']
                    profile_urls = [u['user']['profile_url'].replace('\/', '/') for u in msg_data]
                except:
                    pass
            if 'cards' in response_json:
                #微博页面的ajax json
                #获取页面上微博详情的url
                #和90页的微博cardlists
                try:
                    #
                    cards = response_json['cards']
                    for card in cards:
                        if card['card_type'] == 9:
                            scheme_urls.append(card['scheme'])
                            WeibospiderItem.itemid = card['itemid']
                            WeibospiderItem.mblog_text = card['mblog']['text']
                            WeibospiderItem.created_at = card['mblog']['created_at']
                            WeibospiderItem.user_id = card['mblog']['user']['id']
                            WeibospiderItem.user_screen_name = card['mblog']['user']['screen_name']
                            print(scheme_urls)
                except:
                    pass
                

        for scheme in scheme_urls:
            yield scrapy.Request(scheme)
            for prof in profile_urls:
                yield scrapy.Request(prof)








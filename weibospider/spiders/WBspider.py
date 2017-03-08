# -*- coding: utf-8 -*-
import scrapy
from weibospider.items import WeibospiderItem


class WbspiderSpider(scrapy.Spider):
    name = "WBspider"
    allowed_domains = ["http://m.weibo.cn"]
    start_urls = ['http://m.weibo.cn/container/getIndex?uid=1218346612&luicode=10000011&lfid=1076031746664450&type=uid&value=1218346612&containerid=1005051218346612']

    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            "Host": "m.weibo.cn",
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
            "Referer": "http://m.weibo.cn/u/1218346612?uid=1218346612&luicode=10000011&lfid=1076031746664450",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "en-US,en;q=0.8",
            "Cookie": "_T_WM=75395c0795ce5d9d2eac9bc00a651e04; M_WEIBOCN_PARAMS=from%3Dfeed%26luicode%3D10000011%26lfid%3D1076031746664450%26fid%3D1005051218346612%26uicode%3D10000011",
        }
    }

    def parse(self, response):
        print("************************")
        print(response.headers)
        print("************************")

# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Request
from scrapy.contrib.loader import ItemLoader
from xqtest.items import XqtestItem


class XqSpider(scrapy.Spider):
    name = 'xq'
    # allowed_domains = ['https://xueqiu.com/']
    # start_urls = ['http://https://xueqiu.com//']
    headers = {
        'Cache-Control': 'private, no-store, no-cache, must-revalidate, max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
        'Accept': '*/*',
        'Referer': 'https://xueqiu.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Host': 'xueqiu.com',

    }


    def start_requests(self):
        login_url = "https://xueqiu.com/snowman/login"
        return [scrapy.FormRequest(login_url,
                                       headers=self.headers,
                                       callback=self.parse)]
    def parse(self,response):
        url='https://xueqiu.com/v4/statuses/public_timeline_by_category.json?since_id=-1&max_id=-1&count=10&category=-1'
        yield Request(url,callback=self.parse2)

    def parse2(self, response):
        item = json.loads(response.body_as_unicode())
        for i in range(len(item['list'])):
            data_tmp=item['list'][i]

            loader = ItemLoader(item=XqtestItem())
            loader.add_value('title', data_tmp['data'])
            org = loader.load_item()
            yield org



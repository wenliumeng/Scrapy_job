# -*- coding: utf-8 -*-
import scrapy
# import re
from lagou.items import LagouItem
from scrapy import selector
import time


class Lagou1Spider(scrapy.Spider):
    name = "lagou1"
    allowed_domains = ["www.lagou.com"]
    start_urls = ['http://www.lagou.com/']
    u = (
        'http://www.lagou.com/zhaopin/Java/4/?filterOption=3',
        'http://www.lagou.com/zhaopin/Java/5/?filterOption=3',
        'http://www.lagou.com/zhaopin/Java/6/?filterOption=3'
        )

    def start_requests(self):
        for usi in self.u:    
            yield scrapy.Request(usi, meta={'indexs': 'd'}, callback=self.parse, dont_filter=True)

    def parse(self, response):
        sel = selector.Selector(response)
        keyword = sel.response.xpath('//*[@id="keyword"]/@value').extract()
        dd = sel.xpath('//li[@class="con_list_item default_list"]')
        for d in dd:
            position = LagouItem()
            position['type'] = keyword
            print position['type']
            position['index'] = d.xpath('@data-index').extract()
            position['salary'] = d.xpath('@data-salary').extract()
            position['company'] = d.xpath('@data-company').extract()
            position['position'] = d.xpath('div[@class="list_item_top"]/div/div/a/span/em/text()').extract()
            position['positionname'] = d.xpath('@data-positionname').extract()
            position['time'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            yield position

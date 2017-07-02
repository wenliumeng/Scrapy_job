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
    url = start_urls[0]

    def start_requests(self):
        yield scrapy.Request(self.url, callback=self.home_parse, dont_filter=True)

    def home_parse(self, response):
        sel = scrapy.selector.Selector(response)
        dd = sel.xpath("//div[@class='menu_main job_hopping']")
        allurl = dd.xpath("//a/@href").extract()
        i = 1
        for u in allurl:
            # 只爬一页
            # if 'http' in u and 'Java' in u and i < 2:
            if 'http' in u:
                i += 1
                yield scrapy.Request(u, callback=self.parse, dont_filter=True)
                print u
            # else:
            #     print "NOT IS HTTP -----> {0}".format(u)

    def parse(self, response):
        sel = selector.Selector(response)
        keyword = sel.response.xpath('//*[@id="keyword"]/@value').extract()
        dd = sel.xpath('//li[@class="con_list_item default_list"]')
        i = 1
        for d in dd:
            i += 1
            position = LagouItem()
            position['type'] = keyword
            position['index'] = d.xpath('@data-index').extract()
            position['salary'] = d.xpath('@data-salary').extract()
            position['company'] = d.xpath('@data-company').extract()
            position['position'] = d.xpath('div[@class="list_item_top"]/div/div/a/span/em/text()').extract()
            position['positionname'] = d.xpath('@data-positionname').extract()
            position['time'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            yield position
        purl = sel.xpath('//div[@class="pager_container"]/a[last()]/@href').extract()
        if 'http' in purl:
            yield scrapy.Request(purl, callback=self.parse, dont_filter=True)

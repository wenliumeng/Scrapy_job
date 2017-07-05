# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# from lagou.items import LagouItem
from scrapy import log
import pymongo
from scrapy.conf import settings
import string

class LagouPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host=settings['MONGODB_SERVER'], port=settings['MONGODB_PORT'])
        self.client.test.authenticate(settings['MONGODB_USER'], settings['MONGODB_PSW'])
        self.db = self.client[settings['MONGODB_DB']]
        # self.coll = self.db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        # w = open('position', 'a')
        # w.write(str(dict(item)) + "\n")
        # w.close()
        log.msg("position added to file!!!", level=log.DEBUG, spider=spider)
        post_item = dict(item)
        if post_item.get('type')[0] not in self.db.collection_names('false'):
            self.db.create_collection(post_item.get('type')[0])
        self.db[post_item.get('type')[0].encode('utf-8')].insert(post_item)
        # self.db[str(dict(item).get('type'))].insert(post_item)
        return item

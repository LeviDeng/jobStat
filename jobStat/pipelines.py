# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
import codecs
import pymongo

class jobStatPipeline(object):

    def __init__(self):
        con=pymongo.MongoClient('localhost',27017)
        self.coll=con['jobs51']['jobs']

    def process_item(self, item, spider):
        line = json.dumps(dict(item))
        line=line.decode('unicode_escape').strip()
        self.coll.save(json.loads(line))
        return item
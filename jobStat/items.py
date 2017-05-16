# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Urls(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = scrapy.Field()

class workDetails(scrapy.Item):
    url = scrapy.Field()
    workName = scrapy.Field()
    salary = scrapy.Field()
    workYears = scrapy.Field()
    degree = scrapy.Field()
    jobType = scrapy.Field()
    jobid = scrapy.Field()
    comType = scrapy.Field()
    comName = scrapy.Field()
    comIndustry = scrapy.Field()
    employNums = scrapy.Field()
    date = scrapy.Field()
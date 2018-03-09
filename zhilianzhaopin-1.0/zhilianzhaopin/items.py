# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhilianzhaopinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    company = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    start_date = scrapy.Field()
    experience = scrapy.Field()
    count = scrapy.Field()
    site = scrapy.Field()
    nature = scrapy.Field()
    edu = scrapy.Field()
    type = scrapy.Field()
    # people_num = scrapy.Field()

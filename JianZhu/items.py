# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JianzhuItem(scrapy.Item):
    url = scrapy.Field()
    company_name  = scrapy.Field()
    project_name = scrapy.Field()
    project_code = scrapy.Field()
    project_address = scrapy.Field()
    date = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    intro = scrapy.Field()
    reference_number = scrapy.Field()
    reward_department = scrapy.Field()
    registration_department = scrapy.Field()
    telephone = scrapy.Field()

    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


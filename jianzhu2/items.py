# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JianzhuItem(scrapy.Item):
    originalurl = scrapy.Field()
    name = scrapy.Field()
    zizhiname = scrapy.Field()
    zizhileibie = scrapy.Field()
    zhengshuhao = scrapy.Field()
    fazhengriqi = scrapy.Field()
    youxiaoqi = scrapy.Field()
    fazhengjigou = scrapy.Field()

    # intro = scrapy.Field()
    # reference_number = scrapy.Field()
    # reward_department = scrapy.Field()
    # registration_department = scrapy.Field()
    # telephone = scrapy.Field()
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

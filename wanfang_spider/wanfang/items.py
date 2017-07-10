# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WanfangItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    # 点击量与下载量
    click = scrapy.Field()
    down = scrapy.Field()
    # 描述
    des = scrapy.Field()
    # 论文作者等信息
    zuozhe = scrapy.Field()
    kanming = scrapy.Field()
    yingwenkanming = scrapy.Field()
    keyword = scrapy.Field()
    lanmuname = scrapy.Field()
    doi = scrapy.Field()
    # 参考引用文献
    cankao = scrapy.Field()
    yinzheng = scrapy.Field()
    # 相似文献等
    sswenxian = scrapy.Field()
    sswaiwen = scrapy.Field()
    sshuiyi = scrapy.Field()
    ssxuewei = scrapy.Field()

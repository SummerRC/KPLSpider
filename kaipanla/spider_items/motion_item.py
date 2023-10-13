# -*- coding: utf-8 -*-
# @Time : 2023/10/13 18:13
# @Author : SummerRC
import scrapy


class MotionItem(scrapy.Item):
    # 市场情绪的综合强度
    zhqd = scrapy.Field()
    # 当下情绪强度对应的时间戳，eg: 2023-10-01 21:24:55
    timestamp = scrapy.Field()
    # 是否是交易时间，值为1或者0
    is_trade_time = scrapy.Field()
    # 数据生成的时间
    data_crawl_timestamp = scrapy.Field()

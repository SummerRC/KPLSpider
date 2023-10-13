# -*- coding: utf-8 -*-
# @Time : 2023/10/13 18:14
# @Author : SummerRC
import scrapy


class DaBanItem(scrapy.Item):
    # 今日涨停家数
    tZhangTing = scrapy.Field()
    # 昨日涨停家数
    lZhangTing = scrapy.Field()
    # 今日封板率
    tFengBan = scrapy.Field()
    # 昨日封板率
    lFengBan = scrapy.Field()
    # 今日跌停家数
    tDieTing = scrapy.Field()
    # 昨日跌停家数
    lDieTing = scrapy.Field()
    # 上涨家数
    SZJS = scrapy.Field()
    # 下跌家数
    XDJS = scrapy.Field()
    # 平盘家数
    PPJS = scrapy.Field()
    # 综合强度
    ZHQD = scrapy.Field()

    # 昨日涨停今表现
    ZRZTJ = scrapy.Field()
    # 昨日连板今表现
    ZRLBJ = scrapy.Field()
    # 上证量能
    szln = scrapy.Field()
    # 全市场量能
    qscln = scrapy.Field()
    # 上证昨日总量能
    s_zrcs = scrapy.Field()
    # 全市场昨日总量能
    q_zrcs = scrapy.Field()
    # 接口返回的交易日期
    Day = scrapy.Field()
    # 数据生成的时间
    data_crawl_timestamp = scrapy.Field()

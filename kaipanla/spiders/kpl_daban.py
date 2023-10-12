import logging
import time
import scrapy
from scrapy import Selector

from kaipanla.StockUtils import StockUtils
from kaipanla.items import MotionItem, DaBanItem


class KPLDaBanSpider(scrapy.Spider):
    name = 'KPLDaBanSpider'
    allowed_domains = ['longhuvip.com']
    start_urls = [
        'https://apphq.longhuvip.com',
    ]

    def start_requests(self):
        return [
            scrapy.FormRequest("https://apphq.longhuvip.com/w1/api/index.php",
                               formdata={'apiv': 'w33', 'PhoneOSNew': '1', 'VerSion': '5.11.0.6', 'c': 'Index',
                                         'a': 'GetInfo', 'View': '2,3,4,5,7,8,9,10',
                                         'UserID': '1946772', 'Token': '9bf32d78fc9def555f62b8aad16f1b26'},
                               callback=self.parse_motion)
        ]

    def parse_motion(self, response):
        sel = Selector(response)
        da_ban_item = DaBanItem()
        # 获取打扮板数据所在的Json
        da_ban_list = sel.response.json()['DaBanList']
        da_ban_item['tZhangTing'] = da_ban_list['tZhangTing']
        da_ban_item['lZhangTing'] = da_ban_list['tZhangTing']
        da_ban_item['tFengBan'] = da_ban_list['tFengBan']
        da_ban_item['lFengBan'] = da_ban_list['lFengBan']
        da_ban_item['tDieTing'] = da_ban_list['tDieTing']
        da_ban_item['lDieTing'] = da_ban_list['lDieTing']
        da_ban_item['SZJS'] = da_ban_list['SZJS']
        da_ban_item['XDJS'] = da_ban_list['XDJS']
        da_ban_item['PPJS'] = da_ban_list['PPJS']
        da_ban_item['ZHQD'] = da_ban_list['ZHQD']
        da_ban_item['ZRZTJ'] = da_ban_list['ZRZTJ']
        da_ban_item['ZRLBJ'] = da_ban_list['ZRLBJ']
        da_ban_item['szln'] = da_ban_list['szln']
        da_ban_item['qscln'] = da_ban_list['qscln']
        da_ban_item['s_zrcs'] = da_ban_list['s_zrcs']
        da_ban_item['q_zrcs'] = da_ban_list['q_zrcs']
        da_ban_item['Day'] = sel.response.json()['Day']

        # 打印数据
        self.log("今日涨停家数:" + str(da_ban_item['tZhangTing']), logging.DEBUG)
        self.log("今日封板率:" + str(da_ban_item['tFengBan']), logging.DEBUG)
        yield da_ban_item


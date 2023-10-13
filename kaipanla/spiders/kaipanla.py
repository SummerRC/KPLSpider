import datetime
import logging
import time
import scrapy
from scrapy import Selector

from kaipanla.StockUtils import StockUtils
from kaipanla.items import MotionItem


class KaiPanLaSpider(scrapy.Spider):
    name = 'kaipanla'
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
        motion_item = MotionItem()
        # 获取市场情绪所在的Json
        da_ban_list = sel.response.json()['DaBanList']
        # 获取市场的综合情绪
        zhqx = da_ban_list['ZHQD']
        motion_item['zhqd'] = zhqx
        motion_item['timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        motion_item['data_crawl_timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        motion_item['is_trade_time'] = 1 if StockUtils.a_stock_is_trade_time() else 0
        # 打印数据
        self.log("综合强度:" + str(zhqx), logging.DEBUG)
        self.log("时间戳:" + str(motion_item.get('timestamp')), logging.DEBUG)
        yield motion_item


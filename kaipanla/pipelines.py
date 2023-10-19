import datetime
import logging

from kaipanla.db.db_helper_daban import DaBanDbHelper
from kaipanla.db.db_helper_zhqd import ZhqdDbHelper
from kaipanla.spiders.kaipanla import KaiPanLaSpider
from kaipanla.spiders.kpl_daban import KPLDaBanSpider
from kaipanla.utils.stock_utils import StockUtils


class KaipanlaPipeline:

    def __init__(self):
        self.data = []

    # 爬虫开启的时候会执行一次
    def open_spider(self, spider):
        pass

    # 爬虫结束的时候会执行一次
    def close_spider(self, spider):
        pass

    # 每拿到一条数据都会执行一次
    def process_item(self, item, spider):
        if isinstance(spider, KaiPanLaSpider):
            self.save_data(item, spider)
            return item
        else:
            # 如果不是这个Spider的爬虫就返回item交给其他管道处理
            return item

    # 如果是非交易日，直接丢弃数据，不重复存储
    # 如果是交易日：
    #       1、交易时间，直接存储抓取的数据即可
    #       2、下午一点前的非交易时间，丢弃数据（可继续细分）
    #       3、下午三点后的非交易时间，需要将timestamp修改为当日的15点，并保存当日的最终数据
    def save_data(self, item, spider):
        # 1、非交易日，不抓数据，因为已在交易日抓取过
        if StockUtils.today_is_a_stock_trade_day() is False:
            return

        # 2、交易日，分情况抓取数据
        is_trade_time = item.get('is_trade_time', 0)
        # 2.1、交易时间，数据正确，后面直接存储即可
        if is_trade_time == 1:
            spider.log("当前属于交易时间！", logging.DEBUG)
            self.insert_to_db(item, spider)
        # 2.2、交易日的非交易时间，分情况处理
        # 2.2.1 处于下午一点前的非交易时间，丢弃数据
        elif StockUtils.time_is_before_13_clock():
            spider.log("当前属于下午一点前的非交易时间，丢弃数据！", logging.DEBUG)
        # 2.2.1 处于下午一点后的非交易时间，即三点收盘后，是当天的最终数据，需要存储
        else:
            spider.log("当前属于下午3点收盘后的非交易时间，修正timestamp！", logging.DEBUG)
            today = datetime.datetime.now().date()
            timestamp = datetime.datetime.strptime(str(today) + ' 15:00:00', '%Y-%m-%d %H:%M:%S')
            item["timestamp"] = timestamp
            self.insert_to_db(item, spider)

    # 插入到两个表中
    def insert_to_db(self, item, spider):
        # 情绪为0的数据视为异常数据，不执行插入操作
        if int(item['zhqd']) == 0:
            return

        db_helper = ZhqdDbHelper()
        db_helper.insert_to_db(item, spider)

        db_daban_helper = DaBanDbHelper()
        db_daban_helper.insert_to_db(item, spider)


class KPLDaBanPipeline:

    def __init__(self):
        self.data = []

    # 爬虫开启的时候会执行一次
    def open_spider(self, spider):
        pass

    # 爬虫结束的时候会执行一次
    def close_spider(self, spider):
        pass

    # 每拿到一条数据都会执行一次
    def process_item(self, item, spider):
        if isinstance(spider, KPLDaBanSpider):
            self.save_data(item, spider)
            return item
        else:
            # 如果不是这个Spider的爬虫就返回item交给其他管道处理
            return item

    def save_data(self, item, spider):
        need_insert_to_db = StockUtils.today_is_a_stock_trade_day() & StockUtils.time_is_after_15_clock()
        spider.log("need_insert_to_db: " + str(need_insert_to_db))
        if need_insert_to_db is True:
            # 交易日且是收盘时间才插入数据到数据库中
            self.insert_to_db(item, spider)

    # 插入到两个表中
    def insert_to_db(self, item, spider):
        # 情绪为0的数据视为异常数据，不执行插入操作
        if int(item['ZHQD']) == 0:
            return

        db_helper = DaBanDbHelper()
        db_helper.insert_to_db(item, spider)



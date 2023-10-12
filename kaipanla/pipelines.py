# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import configparser
import datetime
import logging
import pymysql

from kaipanla.StockUtils import StockUtils


class KaipanlaPipeline:

    def __init__(self):

        conf = configparser.ConfigParser()
        conf.read('config.ini')
        # config_db_name = 'PROD_DATABASE'
        config_db_name = 'DEV_DATABASE'
        db_address = conf.get(config_db_name, 'HOST')
        db_port = int(conf.get(config_db_name, 'PORT'))
        db_user = conf.get(config_db_name, 'USER')
        db_password = conf.get(config_db_name, 'PASSWORD')
        db_name = conf.get(config_db_name, 'DBNAME')
        db_charset = conf.get(config_db_name, 'CHARSET')

        self.conn = pymysql.connect(host=db_address, port=db_port,
                                    user=db_user, password=db_password,
                                    database=db_name, charset=db_charset)

        self.cursor = self.conn.cursor()
        self.data = []

    # 爬虫开启的时候会执行一次
    def open_spider(self, spider):
        pass

    # 爬虫结束的时候会执行一次
    def close_spider(self, spider):
        self.close_db()

    # 关闭数据库
    def close_db(self):
        # 关闭游标
        self.cursor.close()
        # 关闭连接
        self.conn.close()

    # 每拿到一条数据都会执行一次
    def process_item(self, item, spider):
        if self.update_timestamp(item, spider):
            # 数据更新成功才插入数据到数据库中
            self.insert_to_db(item, spider)

        return item

    # 如果是非交易日，直接丢弃数据，不重复抓取
    # 如果是交易日：
    #       1、交易时间，直接使用抓取的数据即可
    #       2、下午一点前的非交易时间，丢弃数据（可继续细分）
    #       3、下午三点后的非交易时间，需要将timestamp修改为当日的15点，并保存当日的最终数据
    def update_timestamp(self, item, spider):
        # 1、非交易日，不抓数据，因为已在交易日抓取过
        if StockUtils.today_is_a_stock_trade_day() is False:
            return False

        # 2、交易日，分情况抓取数据
        update_suc = True
        is_trade_time = item.get('is_trade_time', 0)
        # 2.1、交易时间，数据正确，后面直接存储即可
        if is_trade_time == 1:
            spider.log("当前属于交易时间！", logging.DEBUG)
        # 2.2、交易日的非交易时间，分情况处理
        # 2.2.1 处于下午一点前的非交易时间，丢弃数据
        elif StockUtils.time_is_before_13_clock():
            spider.log("当前属于下午一点前的非交易时间，丢弃数据！", logging.DEBUG)
            update_suc = False
        # 2.2.1 处于下午一点后的非交易时间，即三点收盘后，是当天的最终数据，需要存储
        else:
            spider.log("当前属于下午3点收盘后的非交易时间，修正timestamp！", logging.DEBUG)
            today = datetime.datetime.now().date()
            timestamp = datetime.datetime.strptime(str(today) + ' 15:00:00', '%Y-%m-%d %H:%M:%S')
            item["timestamp"] = timestamp

        return update_suc

    # 插入到两个表中
    def insert_to_db(self, item, spider):
        # 情绪为0的数据视为异常数据，不执行插入操作
        if int(item['zhqd']) == 0:
            return

        self.insert_to_table_zhqd(item, spider)
        self.insert_to_table_zhqd_unique(item, spider)

    # 会重复插入
    def insert_to_table_zhqd(self, item, spider):
        try:
            self.cursor.execute(
                'insert into kaipanla_zhqd (zhqd, timestamp, is_trade_time, data_crawl_timestamp) '
                'value (%s, %s, %s, %s)',
                (item['zhqd'], item['timestamp'], item['is_trade_time'], item['data_crawl_timestamp'])
            )
            self.conn.commit()
        except Exception as e:
            spider.log("kaipanla_zhqd表数据插入失败, exception info: " + str(e), logging.ERROR)
            # 失败后的回滚操作
            self.conn.rollback()
        else:  # 如果没有异常
            spider.log("kaipanla_zhqd表数据插入成功", logging.DEBUG)
        finally:
            pass

    # 不会重复插入 timestamp字段设置了唯一性，已存在的情况下会插入失败
    def insert_to_table_zhqd_unique(self, item, spider):
        try:
            self.cursor.execute(
                'insert into kaipanla_zhqd_unique (zhqd, timestamp, is_trade_time, data_crawl_timestamp) '
                'value (%s, %s, %s, %s)',
                (item['zhqd'], item['timestamp'], item['is_trade_time'], item['data_crawl_timestamp'])
            )
            self.conn.commit()
        except Exception as e:
            spider.log("kaipanla_zhqd_unique表数据插入失败, exception info: " + str(e), logging.ERROR)
            # 失败后的回滚操作
            self.conn.rollback()
        else:  # 如果没有异常
            spider.log("kaipanla_zhqd_unique表数据插入成功", logging.DEBUG)
        finally:
            pass

    # 如果当天是休息日，该方法获取最近的交易日的日期的timestamp（要排除掉调休的周六周日）
    def get_previous_workday_timestamp(self):
        # 最近的一个工作日
        previous_work_day = StockUtils.get_previous_work_day()
        # 返回星期几（数字0 代表周一）
        week_day = previous_work_day.weekday()
        if week_day < 5:    # 小于5 代表是周一到周五的工作日
            timestamp = datetime.datetime.strptime(str(previous_work_day) + ' 15:00:00', '%Y-%m-%d %H:%M:%S')
            return timestamp
        else:               # 周六周日，应该返回周六周日之前的最近一个周一到周五的工作日
            return 0

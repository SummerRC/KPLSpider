import configparser
import logging

import pymysql


class ZhqdDbHelper:

    def insert_to_db(self, item, spider):
        self._init_db()
        self._insert_to_target_table(item, spider, self.db_table_name_zhqd)
        self._insert_to_target_table(item, spider, self.db_table_name_zhqd_unique)
        self._close_db()

    def _init_db(self):
        conf = configparser.ConfigParser()
        conf.read('config.ini')
        config_db_name = conf.get("CHANGE_DB", "CONFIG_DB_NAME")
        db_address = conf.get(config_db_name, 'HOST')
        db_port = int(conf.get(config_db_name, 'PORT'))
        db_user = conf.get(config_db_name, 'USER')
        db_password = conf.get(config_db_name, 'PASSWORD')
        db_name = conf.get(config_db_name, 'DBNAME')
        db_charset = conf.get(config_db_name, 'CHARSET')
        self.db_table_name_zhqd = conf.get("DB_TABLE_NAME", 'ZHQD')
        self.db_table_name_zhqd_unique = conf.get("DB_TABLE_NAME", 'ZHQD_UNIQUE')

        self.conn = pymysql.connect(host=db_address, port=db_port,
                                    user=db_user, password=db_password,
                                    database=db_name, charset=db_charset)
        self.cursor = self.conn.cursor()

    def _insert_to_target_table(self, item, spider, db_table_name):
        query = "insert into %s (zhqd, timestamp, is_trade_time, data_crawl_timestamp) value (%s, %s, %s, %s)"
        args = (db_table_name, item['zhqd'], item['timestamp'], item['is_trade_time'], item['data_crawl_timestamp'])
        try:
            self.cursor.execute(query, args)
            self.conn.commit()
        except Exception as e:
            spider.log(db_table_name + "表数据插入失败, exception info: " + str(e), logging.ERROR)
            # 失败后的回滚操作
            self.conn.rollback()
        else:  # 如果没有异常
            spider.log(db_table_name + "表数据插入成功", logging.DEBUG)
        finally:
            pass

    # 会重复插入
    def _insert_to_table_zhqd(self, item, spider):
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
    def _insert_to_table_zhqd_unique(self, item, spider):
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

    # 关闭数据库
    def _close_db(self):
        # 关闭游标
        self.cursor.close()
        # 关闭连接
        self.conn.close()
import logging

from kaipanla.db.db_helper import DbHelper


class ZhqdDbHelper(DbHelper):

    def insert_to_db(self, item, spider):
        self._init_db()
        self._insert_to_target_table(item, spider, self.config_helper.db_table_name_zhqd)
        self._insert_to_target_table(item, spider, self.config_helper.db_table_name_zhqd_unique)
        self._close_db()

    def _init_db(self):
        super()._init_db()

    # 注意：timestamp字段设置了唯一性的表不会重复插入，所以已存在的情况下会插入失败，避免数据重复
    def _insert_to_target_table(self, item, spider, db_table_name):
        sql = "insert into %s (zhqd, timestamp, is_trade_time, data_crawl_timestamp) value (%s, '%s', %s, '%s')" % \
            (db_table_name, item['zhqd'], item['timestamp'], item['is_trade_time'], item['data_crawl_timestamp'])
        spider.log("sql: " + sql, logging.DEBUG)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            spider.log(db_table_name + "表数据插入失败, exception info: " + str(e), logging.ERROR)
            # 失败后的回滚操作
            self.conn.rollback()
        else:  # 如果没有异常
            spider.log(db_table_name + "表数据插入成功", logging.DEBUG)
        finally:
            pass

    # 关闭数据库
    def _close_db(self):
        # 关闭游标
        self.cursor.close()
        # 关闭连接
        self.conn.close()
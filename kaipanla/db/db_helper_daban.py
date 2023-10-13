import logging

from kaipanla.db.db_helper import DbHelper


class DaBanDbHelper(DbHelper):

    def insert_to_db(self, item, spider):
        self._init_db()
        self._insert_to_target_table(item, spider)
        self._close_db()

    def _init_db(self):
        super()._init_db()

    def _insert_to_target_table(self, item, spider):
        sql = ("insert into %s (tZhangTing, lZhangTing, tFengBan, lFengBan, tDieTing, lDieTing, SZJS, XDJS, PPJS, "
                 "ZHQD, ZRZTJ, ZRLBJ, szln, qscln, s_zrcs, q_zrcs, Day, data_crawl_timestamp) "
                 "value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s', '%s')"
               % (self.config_helper.db_table_name_da_ban, item['tZhangTing'], item['lZhangTing'], item['tFengBan'],
                  item['lFengBan'], item['tDieTing'], item['lDieTing'], item['SZJS'], item['XDJS'], item['PPJS'],
                  item['ZHQD'], item['ZRZTJ'],  item['ZRLBJ'], item['szln'], item['qscln'], item['s_zrcs'],
                  item['q_zrcs'], item['Day'], item['data_crawl_timestamp']))
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            spider.log(self.config_helper.db_table_name_da_ban + "表数据插入失败, exception info: " + str(e), logging.ERROR)
            # 失败后的回滚操作
            self.conn.rollback()
        else:  # 如果没有异常
            spider.log(self.config_helper.db_table_name_da_ban + "表数据插入成功", logging.DEBUG)
        finally:
            pass

    # 关闭数据库
    def _close_db(self):
        # 关闭游标
        self.cursor.close()
        # 关闭连接
        self.conn.close()
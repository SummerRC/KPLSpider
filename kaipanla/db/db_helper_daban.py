import configparser
import logging

import pymysql


class DaBanDbHelper:

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
        self.db_table_name_da_ban = conf.get("DB_TABLE_NAME", 'DA_BAN_LIST')

        self.conn = pymysql.connect(host=db_address, port=db_port,
                                    user=db_user, password=db_password,
                                    database=db_name, charset=db_charset)
        self.cursor = self.conn.cursor()

    def _insert_to_target_table(self, item, spider):
        query = ("insert into %s (tZhangTing, tZhangTing, tFengBan, lFengBan, tDieTing, lDieTing, SZJS, XDJS, PPJS, "
                 "ZHQD, ZRZTJ, ZRLBJ, szln, qscln, s_zrcs, q_zrcs, Day) "
                 "value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        args = (self.db_table_name_da_ban, item['tZhangTing'], item['tZhangTing'], item['tFengBan'], item['lFengBan'],
                item['tDieTing'], item['lDieTing'], item['SZJS'], item['XDJS'], item['PPJS'], item['ZHQD'],
                item['ZRZTJ'],  item['ZRLBJ'], item['szln'], item['qscln'], item['s_zrcs'], item['q_zrcs'], item['Day'])
        try:
            self.cursor.execute(query, args)
            self.conn.commit()
        except Exception as e:
            spider.log(self.db_table_name_da_ban + "表数据插入失败, exception info: " + str(e), logging.ERROR)
            # 失败后的回滚操作
            self.conn.rollback()
        else:  # 如果没有异常
            spider.log(self.db_table_name_da_ban + "表数据插入成功", logging.DEBUG)
        finally:
            pass

    # 关闭数据库
    def _close_db(self):
        # 关闭游标
        self.cursor.close()
        # 关闭连接
        self.conn.close()
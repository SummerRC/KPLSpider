import time
import configparser
from datetime import datetime

import pymysql


class DBUtils:
    zhqd = [32, 42, 53, 34, 59, 40, 35, 36, 33, 33, 43, 34, 61, 45, 32, 49, 56, 37, 35, 33,
         34, 34, 34, 29, 44, 24, 39, 30, 28, 56, 32, 40, 44, 31, 44, 25, 53, 74, 50, 37,
         42, 60, 37, 53, 22, 45, 52, 35, 27, 31, 47, 48, 27, 23, 25, 56, 38, 39, 54, 59]

    date = ["2023-7-7", '2023-7-10', "2023-7-11", "2023-7-12", "2023-7-13", "2023-7-14", '2023-7-17', '2023-7-18', "2023-7-19", '2023-7-20',
            '2023-7-21', "2023-7-24", "2023-7-25", "2023-7-26", "2023-7-27", '2023-7-28', "2023-7-31", '2023-8-1', "2023-8-2", '2023-8-3',
            '2023-8-4', "2023-8-7", '2023-8-8', '2023-8-9', "2023-8-10", "2023-8-11", '2023-8-14', "2023-8-15", "2023-8-16", '2023-8-17',
            "2023-8-18", "2023-8-21", "2023-8-22", "2023-8-23", "2023-8-24", "2023-8-25", "2023-8-28", "2023-8-29", '2023-8-30', '2023-8-31',
            "2023-9-1", "2023-9-4", "2023-9-5", "2023-9-6", "2023-9-7", "2023-9-8", "2023-9-11", "2023-9-12", "2023-9-13", "2023-9-14",
            "2023-9-15", "2023-9-18", '2023-9-19', "2023-9-20", "2023-9-21", "2023-9-22", "2023-9-25", '2023-9-26', "2023-9-27", '2023-9-28']

    zhqd_timestamps = []

    def __init__(self):

        conf = configparser.ConfigParser()
        conf.read('config.ini')
        config_db_name = conf.get("CHANGE_DB", "CONFIG_DB_NAME")
        db_address = conf.get(config_db_name, 'HOST')
        db_port = int(conf.get(config_db_name, 'PORT'))
        db_user = conf.get(config_db_name, 'USER')
        db_password = conf.get(config_db_name, 'PASSWORD')
        db_name = conf.get(config_db_name, 'DBNAME')
        db_charset = conf.get(config_db_name, 'CHARSET')

        self.conn = pymysql.connect(host=db_address, port=db_port, user=db_user, password=db_password, database=db_name,
                                    charset=db_charset)
        self.cursor = self.conn.cursor()

    def insert_to_db(self):
        if len(self.zhqd_timestamps) == 0:
            self.package_data()
        if len(self.zhqd_timestamps) == 0:
            return
        self.write_to_db()

    def package_data(self):
        i = 0
        while i < 60:
            timestamp = datetime.strptime(self.date[i] + ' 15:00:00', '%Y-%m-%d %H:%M:%S')
            self.zhqd_timestamps.append((self.zhqd[i], str(timestamp), '0', time.localtime()))
            i = i + 1

    def write_to_db(self):
        self.cursor.executemany(
            'insert into kaipanla_zhqd (zhqd, timestamp, is_trade_time, data_crawl_timestamp)'
            ' value (%s, %s, %s, %s)',
            self.zhqd_timestamps
        )
        self.conn.commit()
        self.conn.close()


utils = DBUtils()
utils.insert_to_db()
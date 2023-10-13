import pymysql

from kaipanla.utils.config_helper import ConfigHelper


class DbHelper:
    def _init_db(self):
        self.config_helper = ConfigHelper()
        self.conn = pymysql.connect(host=self.config_helper.db_address, port=self.config_helper.db_port,
                                    user=self.config_helper.db_user, password=self.config_helper.db_password,
                                    database=self.config_helper.db_name, charset=self.config_helper.db_charset)
        self.cursor = self.conn.cursor()
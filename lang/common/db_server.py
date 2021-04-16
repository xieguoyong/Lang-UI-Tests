from lang.common.ini_read import *
import pymysql
from sshtunnel import SSHTunnelForwarder


class DBServer(object):
    """数据库连接信息"""
    def __init__(self, db_name):
        """ssh连接跳板机"""
        self.ssh_address = ini_options("ssh", "ssh_address", ini_name="db")
        self.ssh_port = ini_options("ssh", "ssh_port", ini_name="db")
        self.ssh_username = ini_options("ssh", "ssh_username", ini_name="db")
        self.ssh_password = ini_options("ssh", "ssh_password", ini_name="db")
        self.ssh_pkey = ini_options("ssh", "ssh_pkey", ini_name="db")
        self.remote_bind_address = ini_options("ssh", "remote_bind_address", ini_name="db")
        self.remote_bind_port = ini_options("ssh", "remote_bind_port", ini_name="db")

        self.ssh_server = SSHTunnelForwarder(ssh_address_or_host=(self.ssh_address, int(self.ssh_port)),
                                             ssh_username=self.ssh_username,
                                             ssh_password=self.ssh_password,
                                             ssh_pkey=self.ssh_pkey,
                                             remote_bind_address=(self.remote_bind_address, int(self.remote_bind_port)))
        self.ssh_server.start()

        """数据库连接"""
        self.host = ini_options("db", "host", ini_name="db")
        self.user = ini_options("db", "user", ini_name="db")
        self.passwd = ini_options("db", "passwd", ini_name="db")
        self.port = self.ssh_server.local_bind_port

        self.db_name = db_name

        self.conn = pymysql.connect(host=self.host,
                                    port=self.port,
                                    user=self.user,
                                    passwd=self.passwd,
                                    db=self.db_name)
        self.cursor = self.conn.cursor()

    def select_sql(self, sql):
        """查询"""
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        """查询完关闭游标、数据库连接和ssh连接"""
        self.cursor.close()
        self.conn.close()
        self.ssh_server.stop()
        return data

    def update_sql(self, sql):
        """更新"""
        self.cursor.execute(sql)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        self.ssh_server.stop()

# sql = "SELECT * from tb_balance WHERE pfid=1049688;"
# DBServer('db_billing').select_sql(sql)

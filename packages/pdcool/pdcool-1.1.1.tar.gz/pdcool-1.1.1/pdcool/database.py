#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import pymysql
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger()


class DBUtil:
    def __init__(self):
        self.username = os.getenv("MYSQL_USERNAME")
        self.password = os.getenv("MYSQL_PASSWORD")
        self.host = os.getenv("MYSQL_HOST")
        self.port = int(os.getenv("MYSQL_PORT"))
        self.database = os.getenv("MYSQL_DATABASE")

    def conn(self):
        self.db = pymysql.connect(
            user=self.username,
            passwd=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )
        self.cursor = self.db.cursor()

    def close(self):
        self.cursor.close()
        self.db.close()

    def queryone(self, sql):
        self.conn()
        logger.debug(sql)
        self.cursor.execute(sql)
        res = self.cursor.fetchone()
        self.close()
        return res

    def query(self, sql):
        self.conn()
        logger.debug(sql)
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        self.close()
        return res

    def show(self, sql):
        self.conn()
        logger.debug(sql)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        self.close()
        for row in rows:
            print(row)

    def __execute(self, sql):
        self.conn()
        logger.debug(sql)
        count = self.cursor.execute(sql)
        self.db.commit()
        self.close()
        return count

    def insert(self, sql):
        return self.__execute(sql)

    def update(self, sql):
        return self.__execute(sql)

    def delete(self, sql):
        return self.__execute(sql)

    def execute(self, sql):
        self.conn()
        logger.debug(sql)
        self.cursor.execute(sql)
        self.db.commit()
        self.close()

    def execute_list(self, sql_list):
        self.conn()
        for sql in sql_list:
            logger.debug(sql)
            self.cursor.execute(sql)
        self.db.commit()
        self.close()

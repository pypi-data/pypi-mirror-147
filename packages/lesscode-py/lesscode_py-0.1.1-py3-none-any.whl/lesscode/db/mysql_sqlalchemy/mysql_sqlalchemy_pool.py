# -*- coding: utf-8 -*-
# author:chao.yy
# email:yuyc@ishangqi.com
# date:2022/2/17 2:45 下午
# Copyright (C) 2022 The lesscode Team
import asyncio

import pymysql
from dbutils.pooled_db import PooledDB
from tornado_sqlalchemy import SQLAlchemy

from lesscode.db.base_connection_pool import BaseConnectionPool
import aiomysql


class MysqlSqlAlchemyPool(BaseConnectionPool):
    """
    mysql 数据库链接创建类
    """

    async def create_pool(self):
        """
        创建mysql 异步连接池
        :return:
        """
        if self.conn_info.async_enable:
            mysql_url = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(
                self.conn_info.user, self.conn_info.password, self.conn_info.host, self.conn_info.port,
                self.conn_info.db_name)
            pool = SQLAlchemy(mysql_url, engine_options={"echo": True, "pool_recycle": 3600})
            return pool
        else:
            raise NotImplementedError

    def sync_create_pool(self):
        mysql_url = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(
            self.conn_info.user, self.conn_info.password, self.conn_info.host, self.conn_info.port,
            self.conn_info.db_name)
        pool = SQLAlchemy(mysql_url, engine_options={"echo": True, "pool_recycle": 3600})
        return pool

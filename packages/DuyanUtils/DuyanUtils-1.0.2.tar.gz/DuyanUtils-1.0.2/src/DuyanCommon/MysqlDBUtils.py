import re

import pymysql
import loguru

from DuyanCommon.CommonUtls import Entity, EntityPage

logger = loguru.logger

try:
    """支持DBUtils>=2.0以上版本"""
    from dbutils.pooled_db import PooledDB

    DB_VERSION = PooledDB.version
    logger.info("当前DBUtils版本-{}", DB_VERSION)
except Exception as e:
    """用于兼容DBUtils<2.0以下版本"""
    DB_VERSION = PooledDB.version
    logger.warning("当前DBUtil[{}]版本过低...请适当升级版本至最新版", DB_VERSION)
    from DBUtils.PooledDB import PooledDB

from Error import VersionLowError, PageError, SizeError, ParamError, SQLFormatError, SQLNotInsertError, \
    SQLNotDeleteError, SQLNotUpdateError, SQLNotSelectError


class MySQLDBClient(object):

    def __init__(self, host, user_name, password, db_name, port: int = 3306, mincached=1, maxcached=2,
                 maxshared=0, maxconnections=5, blocking=False,
                 maxusage=50, setsession=None, reset=True,
                 failures=None, ping=1,
                 *args, **kwargs):
        self.pool_db_version = PooledDB.version
        self.pool = PooledDB(pymysql,
                             host=host or "",
                             user=user_name or "",
                             passwd=password or "",
                             db=db_name or "",
                             port=port or 3306,
                             mincached=mincached,
                             maxcached=maxcached,
                             maxshared=maxshared,
                             maxconnections=maxconnections,
                             blocking=blocking,
                             maxusage=maxusage,
                             setsession=setsession,
                             reset=reset,
                             failures=failures,
                             ping=ping)

    def select_one(self, sql: str, *args, **kwargs) -> Entity:
        if not sql.rstrip().lower().startswith("select"):
            raise SQLNotSelectError(sql)
        conn = None
        cursor = None
        try:
            conn = self.pool.connection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            self.__execute__(cursor, sql, *args, **kwargs)
            result = cursor.fetchone()
            logger.debug(f"<== Total:{result and 1 or 0}")
            return Entity(data=result) if result is not None else None
        except Exception as e:
            loguru.logger.exception(e)
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def select_page(self, sql: str, page: int, size: int, *args, **kwargs) -> EntityPage:
        """
            分页查询
        :param sql: 基础sql
        :param page: 页码
        :param size: 一页展示条数
        :param args: sql 变量
        :param kwargs: sql 变量
        :return:
        """
        if not sql.rstrip().lower().startswith("select"):
            raise SQLNotSelectError(sql)
        if page is None or page < 0:
            raise PageError
        if size is None or size <= 0:
            raise SizeError
        if "group by " in sql.lower():
            raise SQLFormatError(sql)
        data = self.select(sql + f" limit {page * size} , {size}", *args, **kwargs)
        # 这里去统计组装 count 的语句
        r = re.search(r"([\s\n]from[\s\n]).*", sql.lower())
        if r is None:
            raise SQLFormatError(sql)
        # 找到 from 后面的语句后 组装 count
        _sql = "SELECT COUNT(1) as c " + sql[-len(r.group()):]
        total = self.count(_sql, *args, **kwargs)
        return EntityPage.build_obj(data, page, size, total)

    def count(self, sql: str, *args, **kwargs) -> int:
        res_obj = self.select_one(sql, *args, **kwargs)
        return res_obj.c if res_obj is not None else 0

    def select(self, sql: str, *args, **kwargs) -> list[Entity]:
        if not sql.rstrip().lower().startswith("select"):
            raise SQLNotSelectError(sql)
        conn = None
        cursor = None
        try:
            conn = self.pool.connection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            self.__execute__(cursor, sql, *args, **kwargs)
            result = cursor.fetchall()
            logger.debug(f"<== Total:{result and len(result) or 0}")
            return Entity.build_list(result)
        except Exception as e:
            logger.exception(e)
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def insert(self, sql: str, *args, **kwargs) -> int:
        """执行插入"""
        if not sql.rstrip().lower().startswith("insert"):
            raise SQLNotInsertError(sql)
        return self.execute(sql, *args, **kwargs)

    def delete(self, sql, *args, **kwargs) -> int:
        if not sql.rstrip().lower().startswith("delete"):
            raise SQLNotDeleteError(sql)
        return self.execute(sql, *args, **kwargs)

    def update(self, sql, *args, **kwargs) -> int:
        if not sql.rstrip().lower().startswith("update"):
            raise SQLNotUpdateError(sql)
        return self.execute(sql, *args, **kwargs)

    def execute(self, sql, *args, **kwargs) -> int:
        """
            执行器 主要处理 update delete insert 的语句
        :param sql:
        :param args:
        :param kwargs:
        :return:
        """
        conn = None
        cursor = None
        try:
            conn = self.pool.connection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            self.__execute__(cursor, sql, *args, **kwargs)
            result = cursor.rowcount
            conn.commit()
            logger.debug(f"<== Total:{result or 0}")
            return result or 0
        except Exception as e:
            logger.exception(e)
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def insert_many(self, sql, args=None) -> int:
        """
            批量插入
        :param sql: sql 格式
        :param args:
        :return:
        """
        if not sql.rstrip().lower().startswith("select"):
            raise SQLNotInsertError(sql)
        conn = None
        cursor = None
        try:
            conn = self.pool.connection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            rowcount = self.__executemany__(cursor, sql, args)
            conn.commit()
            return rowcount
        except Exception as e:
            loguru.logger.exception(e)
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    @staticmethod
    def __execute__(cursor, sql, *args, **kwargs):
        """
            底层调用sql的方法
        :param cursor: 游标
        :param sql:  执行sql
        :param args:  参数
        :param kwargs: 参数
        :return:
        """
        _sql_format = sql.format(*args, **kwargs)
        logger.debug(f"==> Preparing:{sql}")
        if args is not None and len(args):
            logger.debug(f"==> Parameters:{args}")
        elif kwargs is not None and len(kwargs):
            logger.debug(f"==> Parameters:{kwargs}")
        cursor.execute(_sql_format)

    @staticmethod
    def __executemany__(cursor, sql, args=None) -> int:
        """
            底层调用 批量插入的sql方法
        :param cursor:  游标
        :param sql: insert 语句
        :param args: 数据
        :return:
        """
        logger.debug(f"==> Preparing:{sql}")
        if args is not None and len(args):
            logger.debug(f"==> Parameters:{args}")
        rowcount = cursor.executemany(sql, args=args)
        logger.debug(f"<== Total:{rowcount}")
        return rowcount


if __name__ == "__main__":
    client = MySQLDBClient(host="127.0.0.7", password="admin123", user_name="root", db_name="videoxt")
    print(client.select_page("select * from blogger where id >{0}", 4, 10, 100000))

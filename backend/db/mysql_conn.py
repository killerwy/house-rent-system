import pymysql
from pymysql.err import OperationalError
from config import MYSQL_CONFIG
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 数据库连接池（简化版，生产可使用DBUtils）
class MySQLConnection:
    @classmethod
    def _get_new_conn(cls):
        """新建数据库连接"""
        try:
            conn = pymysql.connect(**MYSQL_CONFIG)
            return conn
        except OperationalError as e:
            logger.error(f"数据库连接失败: {e}")
            raise e

    @classmethod
    def execute_sql(cls, sql, params=None, fetch_type="none"):
        """
        执行SQL语句
        :param sql: SQL语句
        :param params: 参数列表
        :param fetch_type: none(执行)/one(单条)/all(所有)/count(计数)
        :return: 执行结果
        """
        conn = None
        cursor = None
        try:
            conn = cls._get_new_conn()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            # 执行SQL
            affected_rows = cursor.execute(sql, params or ())
            
            # 根据返回类型处理结果
            if fetch_type == "none":
                result = affected_rows
            elif fetch_type == "one":
                result = cursor.fetchone()
            elif fetch_type == "all":
                result = cursor.fetchall()
            elif fetch_type == "count":
                result = cursor.rowcount
            else:
                result = None
            
            conn.commit()
            return result
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"执行SQL失败: {sql} | 参数: {params} | 错误: {e}")
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @classmethod
    def call_procedure(cls, proc_name, params=None):
        """调用存储过程"""
        conn = None
        cursor = None
        try:
            conn = cls._get_new_conn()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.callproc(proc_name, params or ())
            result = cursor.fetchall()
            conn.commit()
            return result
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"调用存储过程失败: {proc_name} | 参数: {params} | 错误: {e}")
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
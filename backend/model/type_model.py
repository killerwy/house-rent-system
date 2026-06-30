"""户型模型"""
from db.mysql_conn import MySQLConnection

class HouseTypeModel:
    @staticmethod
    def get_type_list():
        """查询所有户型"""
        sql = "SELECT * FROM house_type ORDER BY type_id DESC"
        return MySQLConnection.execute_sql(sql, fetch_type="all")

    @staticmethod
    def add_type(type_name, area_range, remark=""):
        """新增户型"""
        sql = """
        INSERT INTO house_type(type_name, area_range, remark) 
        VALUES (%s, %s, %s)
        """
        return MySQLConnection.execute_sql(sql, (type_name, area_range, remark))

    @staticmethod
    def update_type(type_id, type_name, area_range, remark=""):
        """修改户型"""
        sql = """
        UPDATE house_type 
        SET type_name=%s, area_range=%s, remark=%s 
        WHERE type_id=%s
        """
        return MySQLConnection.execute_sql(sql, (type_name, area_range, remark, type_id))

    @staticmethod
    def delete_type(type_id):
        """删除户型（需确保无房源关联）"""
        # 检查是否有关联房源
        check_sql = "SELECT COUNT(*) as total FROM house WHERE type_id = %s"
        check_result = MySQLConnection.execute_sql(check_sql, (type_id,), fetch_type="one")
        if check_result["total"] > 0:
            return -1  # 有关联数据，禁止删除
        # 执行删除
        sql = "DELETE FROM house_type WHERE type_id = %s"
        return MySQLConnection.execute_sql(sql, (type_id,))

    @staticmethod
    def get_type_by_id(type_id):
        """根据ID查询户型"""
        sql = "SELECT * FROM house_type WHERE type_id = %s"
        return MySQLConnection.execute_sql(sql, (type_id,), fetch_type="one")
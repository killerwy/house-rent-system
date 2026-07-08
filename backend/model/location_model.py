"""区域模型"""
from db.mysql_conn import MySQLConnection

class LocationModel:
    @staticmethod
    def get_or_create(province, city, county):
        """
        根据省市区获取loc_id，不存在则自动插入（利用唯一键去重，并发安全）
        返回 loc_id
        """
        # 无则插入，有则忽略
        insert_sql = "INSERT IGNORE INTO location(province, city, county) VALUES (%s, %s, %s)"
        MySQLConnection.execute_sql(insert_sql, (province, city, county))
        # 查询返回对应ID
        query_sql = "SELECT loc_id FROM location WHERE province = %s AND city = %s AND county = %s"
        result = MySQLConnection.execute_sql(query_sql, (province, city, county), fetch_type="one")
        return result["loc_id"]

    @staticmethod
    def get_location_by_id(loc_id):
        """根据ID查询区域信息"""
        sql = "SELECT * FROM location WHERE loc_id = %s"
        return MySQLConnection.execute_sql(sql, (loc_id,), fetch_type="one")

    @staticmethod
    def count_house_by_loc(loc_id):
        """统计指定区域下关联的房源数量"""
        sql = "SELECT COUNT(*) as total FROM house WHERE loc_id = %s"
        result = MySQLConnection.execute_sql(sql, (loc_id,), fetch_type="one")
        return result["total"] if result else 0

    @staticmethod
    def delete_location(loc_id):
        """删除区域记录（仅当无房源关联时调用）"""
        sql = "DELETE FROM location WHERE loc_id = %s"
        return MySQLConnection.execute_sql(sql, (loc_id,))
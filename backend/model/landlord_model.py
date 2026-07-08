"""房东模型"""
from db.mysql_conn import MySQLConnection
from util.page_util import build_page_sql, get_total_count

class LandlordModel:
    @staticmethod
    def get_landlord_list(offset, size, keyword=""):
        """分页查询房东（支持手机号/姓名搜索）"""
        # 基础查询SQL
        base_sql = """
        SELECT * FROM landlord 
        WHERE land_name LIKE %s OR land_phone LIKE %s OR land_idcard LIKE %s
        ORDER BY land_id DESC
        """
        # 计数SQL
        count_sql = """
        SELECT COUNT(*) as total FROM landlord 
        WHERE land_name LIKE %s OR land_phone LIKE %s OR land_idcard LIKE %s
        """
        # 处理搜索关键词
        like_keyword = f"%{keyword}%"
        params = (like_keyword, like_keyword, like_keyword)
        
        # 分页查询
        page_sql = build_page_sql(base_sql, offset, size)
        list_data = MySQLConnection.execute_sql(page_sql, params, fetch_type="all")
        # 总条数
        total = get_total_count(count_sql, params)
        
        return total, list_data

    @staticmethod
    def add_landlord(land_name, land_phone, land_idcard="", land_address=""):
        """新增房东"""
        sql = """
        INSERT INTO landlord(land_name, land_phone, land_idcard, land_address) 
        VALUES (%s, %s, %s, %s)
        """
        return MySQLConnection.execute_sql(sql, (land_name, land_phone, land_idcard, land_address))

    @staticmethod
    def update_landlord(land_id, land_name, land_phone, land_idcard="", land_address=""):
        """修改房东"""
        sql = """
        UPDATE landlord 
        SET land_name=%s, land_phone=%s, land_idcard=%s, land_address=%s 
        WHERE land_id=%s
        """
        return MySQLConnection.execute_sql(sql, (land_name, land_phone, land_idcard, land_address, land_id))

    @staticmethod
    def delete_landlord(land_id):
        """删除房东（检查关联房源）"""
        # 检查关联房源
        check_sql = "SELECT COUNT(*) as total FROM house WHERE land_id = %s"
        check_result = MySQLConnection.execute_sql(check_sql, (land_id,), fetch_type="one")
        if check_result["total"] > 0:
            return -1
        # 执行删除
        sql = "DELETE FROM landlord WHERE land_id = %s"
        return MySQLConnection.execute_sql(sql, (land_id,))

    @staticmethod
    def get_landlord_by_id(land_id):
        """根据ID查询房东"""
        sql = "SELECT * FROM landlord WHERE land_id = %s"
        return MySQLConnection.execute_sql(sql, (land_id,), fetch_type="one")
    
    @staticmethod
    def get_landlord_by_phone(phone):
        """根据手机号查询房东"""
        sql = "SELECT * FROM landlord WHERE land_phone = %s"
        return MySQLConnection.execute_sql(sql, (phone,), fetch_type="one")
    
    @staticmethod
    def get_landlord_by_idcard(idcard):
        """根据身份证号查询房东"""
        sql = "SELECT * FROM landlord WHERE land_idcard = %s"
        return MySQLConnection.execute_sql(sql, (idcard,), fetch_type="one")
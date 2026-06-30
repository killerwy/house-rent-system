"""房源模型"""
from db.mysql_conn import MySQLConnection
from util.page_util import build_page_sql, get_total_count

class HouseModel:
    @staticmethod
    def get_house_list(offset, size, keyword="", status=-1):
        """分页查询房源（支持房号/地址搜索、状态筛选）"""
        # 构建查询条件
        where_conditions = []
        params = []
        # 搜索关键词
        if keyword:
            where_conditions.append("(house_no LIKE %s OR address LIKE %s)")
            like_keyword = f"%{keyword}%"
            params.extend([like_keyword, like_keyword])
        # 状态筛选
        if status != -1:
            where_conditions.append("house_status = %s")
            params.append(status)
        # 拼接WHERE子句
        where_sql = " WHERE " + " AND ".join(where_conditions) if where_conditions else ""
        
        # 基础SQL
        base_sql = f"""
        SELECT h.*, ht.type_name, l.land_name, l.land_phone 
        FROM house h
        LEFT JOIN house_type ht ON h.type_id = ht.type_id
        LEFT JOIN landlord l ON h.land_id = l.land_id
        {where_sql}
        ORDER BY h.house_id DESC
        """
        # 计数SQL
        count_sql = f"""
        SELECT COUNT(*) as total FROM house h
        {where_sql}
        """
        
        # 分页查询
        page_sql = build_page_sql(base_sql, offset, size)
        list_data = MySQLConnection.execute_sql(page_sql, params, fetch_type="all")
        # 总条数
        total = get_total_count(count_sql, params)
        
        return total, list_data

    @staticmethod
    def add_house(house_no, type_id, land_id, address, area, rent_price, deposit, facilities="", status=0):
        """新增房源"""
        sql = """
        INSERT INTO house(house_no, type_id, land_id, address, area, rent_price, deposit, facilities, house_status) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        return MySQLConnection.execute_sql(sql, (house_no, type_id, land_id, address, area, rent_price, deposit, facilities, status))

    @staticmethod
    def update_house(house_id, house_no, type_id, land_id, address, area, rent_price, deposit, facilities="", status=0):
        """修改房源"""
        sql = """
        UPDATE house 
        SET house_no=%s, type_id=%s, land_id=%s, address=%s, area=%s, rent_price=%s, deposit=%s, facilities=%s, house_status=%s 
        WHERE house_id=%s
        """
        return MySQLConnection.execute_sql(sql, (house_no, type_id, land_id, address, area, rent_price, deposit, facilities, status, house_id))

    @staticmethod
    def delete_house(house_id):
        """删除房源（检查关联合同）"""
        # 检查关联合同
        check_sql = "SELECT COUNT(*) as total FROM rent_contract WHERE house_id = %s"
        check_result = MySQLConnection.execute_sql(check_sql, (house_id,), fetch_type="one")
        if check_result["total"] > 0:
            return -1
        # 执行删除
        sql = "DELETE FROM house WHERE house_id = %s"
        return MySQLConnection.execute_sql(sql, (house_id,))

    @staticmethod
    def get_house_by_id(house_id):
        """根据ID查询房源"""
        sql = """
        SELECT h.*, ht.type_name, l.land_name, l.land_phone 
        FROM house h
        LEFT JOIN house_type ht ON h.type_id = ht.type_id
        LEFT JOIN landlord l ON h.land_id = l.land_id
        WHERE h.house_id = %s
        """
        return MySQLConnection.execute_sql(sql, (house_id,), fetch_type="one")
    
    @staticmethod
    def get_house_by_no(house_no):
        """根据房号查询房源"""
        sql = "SELECT * FROM house WHERE house_no = %s"
        return MySQLConnection.execute_sql(sql, (house_no,), fetch_type="one")
    
    @staticmethod
    def update_house_status(house_id, status):
        """更新房源状态"""
        sql = "UPDATE house SET house_status = %s WHERE house_id = %s"
        return MySQLConnection.execute_sql(sql, (status, house_id))
    
    @staticmethod
    def get_type_by_id(type_id):
        """根据ID查询房源"""
        sql = "SELECT * FROM house_type WHERE type_id = %s"
        return MySQLConnection.execute_sql(sql, (type_id,), fetch_type="one")
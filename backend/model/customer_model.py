"""租客模型"""
from db.mysql_conn import MySQLConnection
from util.page_util import build_page_sql, get_total_count

class CustomerModel:
    @staticmethod
    def get_customer_list(offset, size, keyword=""):
        """分页查询租客（支持姓名/手机号搜索）"""
        # 基础SQL
        base_sql = """
        SELECT * FROM customer 
        WHERE cust_name LIKE %s OR cust_phone LIKE %s 
        ORDER BY cust_id DESC
        """
        # 计数SQL
        count_sql = """
        SELECT COUNT(*) as total FROM customer 
        WHERE cust_name LIKE %s OR cust_phone LIKE %s
        """
        # 处理关键词
        like_keyword = f"%{keyword}%"
        params = (like_keyword, like_keyword)
        
        # 分页查询
        page_sql = build_page_sql(base_sql, offset, size)
        list_data = MySQLConnection.execute_sql(page_sql, params, fetch_type="all")
        # 总条数
        total = get_total_count(count_sql, params)
        
        return total, list_data

    @staticmethod
    def add_customer(cust_name, cust_phone, cust_idcard="", work_unit=""):
        """新增租客"""
        sql = """
        INSERT INTO customer(cust_name, cust_phone, cust_idcard, work_unit) 
        VALUES (%s, %s, %s, %s)
        """
        return MySQLConnection.execute_sql(sql, (cust_name, cust_phone, cust_idcard, work_unit))

    @staticmethod
    def update_customer(cust_id, cust_name, cust_phone, cust_idcard="", work_unit=""):
        """修改租客"""
        sql = """
        UPDATE customer 
        SET cust_name=%s, cust_phone=%s, cust_idcard=%s, work_unit=%s 
        WHERE cust_id=%s
        """
        return MySQLConnection.execute_sql(sql, (cust_name, cust_phone, cust_idcard, work_unit, cust_id))

    @staticmethod
    def delete_customer(cust_id):
        """删除租客（检查关联合同）"""
        # 检查关联合同
        check_sql = "SELECT COUNT(*) as total FROM rent_contract WHERE cust_id = %s"
        check_result = MySQLConnection.execute_sql(check_sql, (cust_id,), fetch_type="one")
        if check_result["total"] > 0:
            return -1
        # 执行删除
        sql = "DELETE FROM customer WHERE cust_id = %s"
        return MySQLConnection.execute_sql(sql, (cust_id,))

    @staticmethod
    def get_customer_by_id(cust_id):
        """根据ID查询租客"""
        sql = "SELECT * FROM customer WHERE cust_id = %s"
        return MySQLConnection.execute_sql(sql, (cust_id,), fetch_type="one")
    
    @staticmethod
    def get_customer_by_phone(phone):
        """根据手机号查询租客"""
        sql = "SELECT * FROM customer WHERE cust_phone = %s"
        return MySQLConnection.execute_sql(sql, (phone,), fetch_type="one")
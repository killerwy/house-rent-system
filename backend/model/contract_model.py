"""租赁合同模型"""
from db.mysql_conn import MySQLConnection
from util.page_util import build_page_sql, get_total_count

class ContractModel:
    @staticmethod
    def get_contract_list(offset, size, keyword="", status=-1):
        """分页查询合同（支持房号/租客姓名搜索、状态筛选）"""
        # 构建条件
        where_conditions = []
        params = []
        if keyword:
            where_conditions.append("(h.house_no LIKE %s OR c.cust_name LIKE %s)")
            like_keyword = f"%{keyword}%"
            params.extend([like_keyword, like_keyword])
        if status != -1:
            where_conditions.append("rc.contract_status = %s")
            params.append(status)
        where_sql = " WHERE " + " AND ".join(where_conditions) if where_conditions else ""
        
        # 基础SQL
        base_sql = f"""
        SELECT rc.*, h.house_no, c.cust_name, c.cust_phone, u.real_name as operator_name
        FROM rent_contract rc
        LEFT JOIN house h ON rc.house_id = h.house_id
        LEFT JOIN customer c ON rc.cust_id = c.cust_id
        LEFT JOIN sys_user u ON rc.operator_id = u.user_id
        {where_sql}
        ORDER BY rc.contract_id DESC
        """
        # 计数SQL
        count_sql = f"""
        SELECT COUNT(*) as total FROM rent_contract rc
        LEFT JOIN house h ON rc.house_id = h.house_id
        LEFT JOIN customer c ON rc.cust_id = c.cust_id
        {where_sql}
        """
        
        # 分页查询
        page_sql = build_page_sql(base_sql, offset, size)
        list_data = MySQLConnection.execute_sql(page_sql, params, fetch_type="all")
        total = get_total_count(count_sql, params)
        
        return total, list_data

    @staticmethod
    def add_contract(house_id, cust_id, start_date, end_date, real_rent, operator_id):
        """新增租赁合同（出租登记）"""
        sql = """
        INSERT INTO rent_contract(house_id, cust_id, start_date, end_date, real_rent, contract_status, operator_id) 
        VALUES (%s, %s, %s, %s, %s, 0, %s)
        """
        return MySQLConnection.execute_sql(sql, (house_id, cust_id, start_date, end_date, real_rent, operator_id))

    @staticmethod
    def return_house(contract_id, return_date):
        """退租登记（更新合同状态+归还日期）"""
        sql = """
        UPDATE rent_contract 
        SET contract_status=1, return_date=%s 
        WHERE contract_id=%s
        """
        return MySQLConnection.execute_sql(sql, (return_date, contract_id))

    @staticmethod
    def get_contract_by_id(contract_id):
        """根据ID查询合同"""
        sql = """
        SELECT rc.*, h.house_no, h.address, c.cust_name, c.cust_phone, u.real_name as operator_name
        FROM rent_contract rc
        LEFT JOIN house h ON rc.house_id = h.house_id
        LEFT JOIN customer c ON rc.cust_id = c.cust_id
        LEFT JOIN sys_user u ON rc.operator_id = u.user_id
        WHERE rc.contract_id = %s
        """
        return MySQLConnection.execute_sql(sql, (contract_id,), fetch_type="one")
    
    @staticmethod
    def get_contract_by_house(house_id, status=0):
        """查询房屋当前有效的租赁合同"""
        sql = """
        SELECT * FROM rent_contract 
        WHERE house_id = %s AND contract_status = %s
        """
        return MySQLConnection.execute_sql(sql, (house_id, status), fetch_type="one")
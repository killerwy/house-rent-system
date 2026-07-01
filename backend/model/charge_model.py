"""收费记录模型"""
from db.mysql_conn import MySQLConnection
from util.page_util import build_page_sql, get_total_count

class ChargeModel:
    @staticmethod
    def get_charge_list(offset, size, keyword="", charge_type=-1):
        """分页查询收费记录（支持合同ID、收费类型筛选）"""
        # 构建条件
        where_conditions = []
        params = []
        if keyword:
            where_conditions.append("(cr.contract_id LIKE %s OR c.cust_name LIKE %s)")
            like_keyword = f"%{keyword}%"
            params.extend([like_keyword, like_keyword])
        if charge_type != -1:
            where_conditions.append("charge_type = %s")
            params.append(charge_type)
        where_sql = " WHERE " + " AND ".join(where_conditions) if where_conditions else ""
        
        # 基础SQL
        base_sql = f"""
        SELECT cr.*, rc.contract_id, h.province, h.city, h.county, h.address, c.cust_name 
        FROM charge_record cr
        LEFT JOIN rent_contract rc ON cr.contract_id = rc.contract_id
        LEFT JOIN house h ON rc.house_id = h.house_id
        LEFT JOIN customer c ON rc.cust_id = c.cust_id
        {where_sql}
        ORDER BY cr.charge_id DESC
        """
        # 计数SQL
        count_sql = f"""
        SELECT COUNT(*) as total FROM charge_record cr
        LEFT JOIN rent_contract rc ON cr.contract_id = rc.contract_id
        LEFT JOIN customer c ON rc.cust_id = c.cust_id
        {where_sql}
        """
        
        # 分页查询
        page_sql = build_page_sql(base_sql, offset, size)
        list_data = MySQLConnection.execute_sql(page_sql, params, fetch_type="all")
        total = get_total_count(count_sql, params)
        
        return total, list_data

    @staticmethod
    def add_charge(contract_id, charge_type, charge_money, remark=""):
        """新增收费记录"""
        sql = """
        INSERT INTO charge_record(contract_id, charge_type, charge_money, remark) 
        VALUES (%s, %s, %s, %s)
        """
        return MySQLConnection.execute_sql(sql, (contract_id, charge_type, charge_money, remark))

    @staticmethod
    def get_charge_by_id(charge_id):
        """根据ID查询收费记录"""
        sql = "SELECT * FROM charge_record WHERE charge_id = %s"
        return MySQLConnection.execute_sql(sql, (charge_id,), fetch_type="one")
    
    @staticmethod
    def get_charge_by_contract(contract_id):
        """查询合同所有收费记录"""
        sql = "SELECT * FROM charge_record WHERE contract_id = %s ORDER BY charge_time DESC"
        return MySQLConnection.execute_sql(sql, (contract_id,), fetch_type="all")
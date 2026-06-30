"""员工用户模型"""
from db.mysql_conn import MySQLConnection
from util.page_util import build_page_sql, get_total_count

class UserModel:
    @staticmethod
    def get_user_list(offset, size, keyword=""):
        """分页查询员工（支持账号/姓名搜索）"""
        base_sql = """
        SELECT u.*, r.role_name 
        FROM sys_user u
        LEFT JOIN sys_role r ON u.role_id = r.role_id
        WHERE u.username LIKE %s OR u.real_name LIKE %s
        ORDER BY u.user_id DESC
        """
        count_sql = """
        SELECT COUNT(*) as total FROM sys_user u
        WHERE u.username LIKE %s OR u.real_name LIKE %s
        """
        like_keyword = f"%{keyword}%"
        params = (like_keyword, like_keyword)
        
        page_sql = build_page_sql(base_sql, offset, size)
        list_data = MySQLConnection.execute_sql(page_sql, params, fetch_type="all")
        total = get_total_count(count_sql, params)
        
        return total, list_data

    @staticmethod
    def add_user(username, password, real_name, phone, role_id):
        """新增员工（密码加密）"""
        sql = """
        INSERT INTO sys_user(username, password, real_name, phone, role_id) 
        VALUES (%s, %s, %s, %s, %s)
        """
        return MySQLConnection.execute_sql(sql, (username, password, real_name, phone, role_id))

    @staticmethod
    def update_user(user_id, real_name, phone, role_id):
        """修改员工信息（不修改密码）"""
        sql = """
        UPDATE sys_user 
        SET real_name=%s, phone=%s, role_id=%s 
        WHERE user_id=%s
        """
        return MySQLConnection.execute_sql(sql, (real_name, phone, role_id, user_id))

    @staticmethod
    def update_password(user_id, new_password):
        """修改密码（加密）"""
        sql = "UPDATE sys_user SET password = %s WHERE user_id = %s"
        return MySQLConnection.execute_sql(sql, (new_password, user_id))

    @staticmethod
    def delete_user(user_id):
        """删除员工（禁止删除管理员）"""
        # 检查是否是管理员
        check_sql = "SELECT role_id FROM sys_user WHERE user_id = %s"
        user = MySQLConnection.execute_sql(check_sql, (user_id,), fetch_type="one")
        if user and user["role_id"] == 1:
            return -1  # 禁止删除超级管理员
        # 检查是否有操作记录
        check_contract = "SELECT COUNT(*) as total FROM rent_contract WHERE operator_id = %s"
        contract_count = MySQLConnection.execute_sql(check_contract, (user_id,), fetch_type="one")
        if contract_count["total"] > 0:
            return -2  # 有操作记录，禁止删除
        # 执行删除
        sql = "DELETE FROM sys_user WHERE user_id = %s"
        return MySQLConnection.execute_sql(sql, (user_id,))

    @staticmethod
    def get_user_by_id(user_id):
        """根据ID查询员工"""
        sql = """
        SELECT u.*, r.role_name 
        FROM sys_user u
        LEFT JOIN sys_role r ON u.role_id = r.role_id
        WHERE u.user_id = %s
        """
        return MySQLConnection.execute_sql(sql, (user_id,), fetch_type="one")
    
    @staticmethod
    def get_user_by_username(username):
        """根据账号查询员工（登录用）"""
        sql = "SELECT * FROM sys_user WHERE username = %s"
        return MySQLConnection.execute_sql(sql, (username,), fetch_type="one")
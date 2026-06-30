"""分页工具"""

def get_page_params(request):
    """解析分页参数"""
    page = request.args.get("page", 1, type=int)
    size = request.args.get("size", 10, type=int)
    # 计算偏移量
    offset = (page - 1) * size
    return page, size, offset

def build_page_sql(base_sql, offset, size):
    """构建分页SQL"""
    return f"{base_sql} LIMIT {offset}, {size}"

def get_total_count(count_sql, params=None):
    """获取总条数"""
    from db.mysql_conn import MySQLConnection
    result = MySQLConnection.execute_sql(count_sql, params, fetch_type="one")
    return result.get("total", 0) if result else 0
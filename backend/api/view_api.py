"""视图查询接口：查询 v_house_all_info 视图，展示地址、房东、状态等信息"""
from flask import Blueprint, request
from db.mysql_conn import MySQLConnection
from util.response_util import success, page_success
from util.page_util import get_page_params, build_page_sql, get_total_count
from util.auth_util import permission_required

view_api = Blueprint("view_api", __name__, url_prefix="/api/view")

@view_api.route("/houseAll", methods=["GET"])
@permission_required("view")
def get_house_all_view():
    """查询房屋总览视图（地址+房东+状态），支持分页、关键词搜索"""
    page, size, offset = get_page_params(request)
    keyword = request.args.get("keyword", "")
    
    # 构建查询条件
    where_sql = ""
    params = []
    if keyword:
        where_sql = " WHERE 房屋地址 LIKE %s OR 房东姓名 LIKE %s "
        like_key = f"%{keyword}%"
        params = [like_key, like_key, like_key]
    
    # 基础查询SQL（基于视图）
    base_sql = f"SELECT * FROM v_house_all_info {where_sql}"
    count_sql = f"SELECT COUNT(*) as total FROM v_house_all_info {where_sql}"
    
    # 分页查询
    page_sql = build_page_sql(base_sql, offset, size)
    list_data = MySQLConnection.execute_sql(page_sql, params, fetch_type="all")
    total = get_total_count(count_sql, params)
    
    return page_success(total, list_data)
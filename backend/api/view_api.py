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
    status = request.args.get("status", "").strip()
    type_name = request.args.get("type_name", "").strip()
    province = request.args.get("province", "").strip()
    city = request.args.get("city", "").strip()
    county = request.args.get("county", "").strip()

    # 构建查询条件
    where_conditions = []
    params = []
    # 省精确筛选
    if province:
        where_conditions.append("省份 = %s")
        params.append(province)
    # 市精确筛选
    if city:
        where_conditions.append("城市 = %s")
        params.append(city)
    # 区县精确筛选
    if county:
        where_conditions.append("区县 = %s")
        params.append(county)
    # 户型筛选
    if type_name:
        where_conditions.append("户型 = %s")
        params.append(type_name)
    # 状态筛选
    if status:
        where_conditions.append("房屋状态 = %s")
        params.append(status)
    if keyword:
        where_conditions.append("(省份 LIKE %s OR 城市 LIKE %s OR 区县 LIKE %s OR 房屋地址 LIKE %s OR 房东姓名 LIKE %s)")
        like_key = f"%{keyword}%"
        params.extend([like_key, like_key, like_key, like_key, like_key])
    
    # 拼接WHERE
    where_sql = " WHERE " + " AND ".join(where_conditions) if where_conditions else ""
    base_sql = f"SELECT * FROM v_house_all_info {where_sql}"
    count_sql = f"SELECT COUNT(*) as total FROM v_house_all_info {where_sql}"
    
    # 分页查询
    page_sql = build_page_sql(base_sql, offset, size)
    list_data = MySQLConnection.execute_sql(page_sql, params, fetch_type="all")
    total = get_total_count(count_sql, params)
    
    return page_success(total, list_data)
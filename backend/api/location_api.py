"""省市区地址接口"""
from flask import Blueprint, request
from util.response_util import success
from util.auth_util import permission_required
from db.mysql_conn import MySQLConnection

location_api = Blueprint("location_api", __name__, url_prefix="/api/location")

# 获取所有省份
@location_api.route("/province/list", methods=["GET"])
@permission_required("common")
def get_province_list():
    sql = "SELECT DISTINCT province FROM location WHERE province != '' ORDER BY province"
    data = MySQLConnection.execute_sql(sql, [], fetch_type="all")
    res = [{"name": row["province"]} for row in data]
    return success(data=res)

# 获取城市（可传province筛选对应省的城市）
@location_api.route("/city/list", methods=["GET"])
@permission_required("common")
def get_city_list():
    province = request.args.get("province", "").strip()
    sql = "SELECT DISTINCT city FROM location WHERE city != ''"
    params = []
    if province:
        sql += " AND province = %s"
        params.append(province)
    sql += " ORDER BY city"
    data = MySQLConnection.execute_sql(sql, params, fetch_type="all")
    res = [{"name": row["city"]} for row in data]
    return success(data=res)

# 获取区县（可传province、city筛选）
@location_api.route("/county/list", methods=["GET"])
@permission_required("common")
def get_county_list():
    province = request.args.get("province", "").strip()
    city = request.args.get("city", "").strip()
    sql = "SELECT DISTINCT county FROM location WHERE county != ''"
    params = []
    if province:
        sql += " AND province = %s"
        params.append(province)
    if city:
        sql += " AND city = %s"
        params.append(city)
    sql += " ORDER BY county"
    data = MySQLConnection.execute_sql(sql, params, fetch_type="all")
    res = [{"name": row["county"]} for row in data]
    return success(data=res)
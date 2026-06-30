"""数据统计接口：调用存储过程统计各户型出租数量"""
from flask import Blueprint
from db.mysql_conn import MySQLConnection
from util.response_util import success
from util.auth_util import permission_required

stat_api = Blueprint("stat_api", __name__, url_prefix="/api/stat")

@stat_api.route("/rentByType", methods=["GET"])
@permission_required("stat")
def stat_rent_by_type():
    """统计各户型出租数量（调用存储过程 proc_stat_rent_by_type）"""
    # 调用存储过程
    result = MySQLConnection.call_procedure("proc_stat_rent_by_type")
    return success(data=result, msg="户型出租统计查询成功")
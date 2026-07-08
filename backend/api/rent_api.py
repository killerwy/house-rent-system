"""租赁业务接口：出租登记、退租归还、合同管理"""
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from model.rent_model import RentModel
from model.house_model import HouseModel
from model.customer_model import CustomerModel
from util.response_util import success, fail, page_success
from util.page_util import get_page_params
from util.auth_util import permission_required

rent_api = Blueprint("rent_api", __name__, url_prefix="/api/rent")

@rent_api.route("/list", methods=["GET"])
@permission_required("rent")
def get_rent_list():
    """分页查询租赁合同"""
    page, size, offset = get_page_params(request)
    keyword = request.args.get("keyword", "")
    status = request.args.get("status", -1, type=int)
    
    total, list_data = RentModel.get_rent_list(offset, size, keyword, status)
    return page_success(total, list_data)

@rent_api.route("/add", methods=["POST"])
@permission_required("rent")
def add_rent():
    """房屋出租登记：新增租赁合同，触发器自动更新房屋状态为已租"""
    data = request.get_json()
    house_id = data.get("house_id")
    cust_id = data.get("cust_id")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    real_rent = data.get("real_rent")
    
    # 参数校验
    if not all([house_id, cust_id, start_date, end_date, real_rent]):
        return fail(msg="必填信息不能为空", code=400)
    
    # 校验房屋是否存在且可租
    house = HouseModel.get_house_by_id(house_id)
    if not house:
        return fail(msg="房源不存在", code=400)
    if house["house_status"] != 0:
        return fail(msg="该房屋当前非空置状态，无法出租", code=400)
    
    # 校验租客是否存在
    if not CustomerModel.get_customer_by_id(cust_id):
        return fail(msg="租客不存在", code=400)
    
    # 校验日期合法性
    if start_date >= end_date:
        return fail(msg="到期日期必须晚于起租日期", code=400)
    
    # 获取当前操作人ID
    operator_id = get_jwt_identity()
    
    # 新增合同（数据库触发器自动更新房屋状态）
    result = RentModel.add_rent(house_id, cust_id, start_date, end_date, real_rent, operator_id)
    if result > 0:
        return success(msg="出租登记成功，房屋状态已自动更新为已出租")
    else:
        return fail(msg="出租登记失败")

@rent_api.route("/return", methods=["POST"])
@permission_required("rent")
def return_house():
    """退租归还登记：更新合同状态，触发器自动将房屋改为空置"""
    data = request.get_json()
    rent_id = data.get("rent_id")
    return_date = data.get("return_date")
    
    if not rent_id or not return_date:
        return fail(msg="合同ID和归还日期不能为空", code=400)
    
    # 校验合同是否存在且处于租住中
    rent = RentModel.get_rent_by_id(rent_id)
    if not rent:
        return fail(msg="租赁合同不存在", code=400)
    if rent["rent_status"] == 1:
        return fail(msg="该合同已办理退租", code=400)
    
    # 执行退租
    result = RentModel.return_house(rent_id, return_date)
    if result > 0:
        return success(msg="退租登记成功，房屋状态已自动更新为空置")
    else:
        return fail(msg="退租登记失败")

@rent_api.route("/<int:rent_id>", methods=["GET"])
@permission_required("rent")
def get_rent_detail(rent_id):
    """查询合同详情"""
    rent = RentModel.get_rent_by_id(rent_id)
    if rent:
        return success(data=rent)
    else:
        return fail(msg="租赁合同不存在")
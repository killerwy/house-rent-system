"""房源/户型管理接口"""
from flask import Blueprint, request
from model.house_model import HouseModel
from model.type_model import HouseTypeModel
from util.response_util import success, fail, page_success
from util.page_util import get_page_params
from util.auth_util import permission_required

house_api = Blueprint("house_api", __name__, url_prefix="/api/house")

# ---------------------- 户型管理 ----------------------
@house_api.route("/type/list", methods=["GET"])
@permission_required("house")
def get_type_list():
    """查询所有户型"""
    data = HouseTypeModel.get_type_list()
    return success(data=data)

@house_api.route("/type/add", methods=["POST"])
@permission_required("house")
def add_type():
    """新增户型"""
    data = request.get_json()
    type_name = data.get("type_name")
    area_range = data.get("area_range")
    remark = data.get("remark", "")
    
    if not type_name:
        return fail(msg="户型名称不能为空", code=400)
    
    result = HouseTypeModel.add_type(type_name, area_range, remark)
    if result > 0:
        return success(msg="新增户型成功")
    else:
        return fail(msg="新增户型失败")

@house_api.route("/type/<int:type_id>", methods=["GET"])
@permission_required("house")
def get_type_detail(type_id):
    data = HouseTypeModel.get_type_by_id(type_id)
    if data:
        return success(data=data)
    return fail("户型不存在")

@house_api.route("/type/update", methods=["POST"])
@permission_required("house")
def update_type():
    """修改户型"""
    data = request.get_json()
    type_id = data.get("type_id")
    type_name = data.get("type_name")
    area_range = data.get("area_range")
    remark = data.get("remark", "")
    
    if not type_id or not type_name:
        return fail(msg="必填参数不能为空", code=400)
    
    result = HouseTypeModel.update_type(type_id, type_name, area_range, remark)
    if result > 0:
        return success(msg="修改户型成功")
    else:
        return fail(msg="修改户型失败")

@house_api.route("/type/delete/<int:type_id>", methods=["DELETE"])
@permission_required("house")
def delete_type(type_id):
    """删除户型"""
    result = HouseTypeModel.delete_type(type_id)
    if result == -1:
        return fail(msg="该户型有关联房源，禁止删除", code=400)
    elif result > 0:
        return success(msg="删除户型成功")
    else:
        return fail(msg="删除户型失败")

# ---------------------- 房源管理 ----------------------
@house_api.route("/list", methods=["GET"])
@permission_required("house")
def get_house_list():
    """分页查询房源"""
    page, size, offset = get_page_params(request)
    keyword = request.args.get("keyword", "")
    status = request.args.get("status", -1, type=int)
    
    total, list_data = HouseModel.get_house_list(offset, size, keyword, status)
    return page_success(total, list_data)

@house_api.route("/add", methods=["POST"])
@permission_required("house")
def add_house():
    """新增房源"""
    data = request.get_json()
    house_no = data.get("house_no")
    type_id = data.get("type_id")
    land_id = data.get("land_id")
    address = data.get("address")
    area = data.get("area")
    rent_price = data.get("rent_price")
    deposit = data.get("deposit")
    facilities = data.get("facilities", "")
    status = data.get("status", 0)
    
    # 校验参数
    required = [house_no, type_id, land_id, address, area, rent_price, deposit]
    if not all(required):
        return fail(msg="必填参数不能为空", code=400)
    
    # 检查房号是否重复
    if HouseModel.get_house_by_no(house_no):
        return fail(msg="房号已存在", code=400)
    
    # 新增
    result = HouseModel.add_house(house_no, type_id, land_id, address, area, rent_price, deposit, facilities, status)
    if result > 0:
        return success(msg="新增房源成功")
    else:
        return fail(msg="新增房源失败")

@house_api.route("/update", methods=["POST"])
@permission_required("house")
def update_house():
    """修改房源"""
    data = request.get_json()
    house_id = data.get("house_id")
    house_no = data.get("house_no")
    type_id = data.get("type_id")
    land_id = data.get("land_id")
    address = data.get("address")
    area = data.get("area")
    rent_price = data.get("rent_price")
    deposit = data.get("deposit")
    facilities = data.get("facilities", "")
    status = data.get("status", 0)
    
    required = [house_id, house_no, type_id, land_id, address, area, rent_price, deposit]
    if not all(required):
        return fail(msg="必填参数不能为空", code=400)
    
    # 检查房号是否重复（排除自身）
    house = HouseModel.get_house_by_no(house_no)
    if house and house["house_id"] != int(house_id):
        return fail(msg="房号已存在", code=400)
    
    # 修改
    result = HouseModel.update_house(house_id, house_no, type_id, land_id, address, area, rent_price, deposit, facilities, status)
    if result > 0:
        return success(msg="修改房源成功")
    else:
        return fail(msg="修改房源失败")

@house_api.route("/delete/<int:house_id>", methods=["DELETE"])
@permission_required("house")
def delete_house(house_id):
    """删除房源"""
    result = HouseModel.delete_house(house_id)
    if result == -1:
        return fail(msg="该房源有关联租赁合同，禁止删除", code=400)
    elif result > 0:
        return success(msg="删除房源成功")
    else:
        return fail(msg="删除房源失败")

@house_api.route("/<int:house_id>", methods=["GET"])
@permission_required("house")
def get_house_detail(house_id):
    """查询房源详情"""
    house = HouseModel.get_house_by_id(house_id)
    if house:
        return success(data=house)
    else:
        return fail(msg="房源不存在")
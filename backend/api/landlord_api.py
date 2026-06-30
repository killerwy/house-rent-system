"""房东管理接口"""
from flask import Blueprint, request
from model.landlord_model import LandlordModel
from util.response_util import success, fail, page_success
from util.page_util import get_page_params
from util.auth_util import permission_required

landlord_api = Blueprint("landlord_api", __name__, url_prefix="/api/landlord")

@landlord_api.route("/list", methods=["GET"])
@permission_required("landlord")
def get_landlord_list():
    """分页查询房东"""
    page, size, offset = get_page_params(request)
    keyword = request.args.get("keyword", "")
    
    total, list_data = LandlordModel.get_landlord_list(offset, size, keyword)
    return page_success(total, list_data)

@landlord_api.route("/add", methods=["POST"])
@permission_required("landlord")
def add_landlord():
    """新增房东"""
    data = request.get_json()
    land_name = data.get("land_name")
    land_phone = data.get("land_phone")
    land_idcard = data.get("land_idcard", "")
    land_address = data.get("land_address", "")
    
    # 参数校验
    if not land_name or not land_phone:
        return fail(msg="姓名和手机号不能为空", code=400)
    
    # 检查手机号是否重复
    if LandlordModel.get_landlord_by_phone(land_phone):
        return fail(msg="该手机号已存在", code=400)
    
    # 执行新增
    result = LandlordModel.add_landlord(land_name, land_phone, land_idcard, land_address)
    if result > 0:
        return success(msg="新增房东成功")
    else:
        return fail(msg="新增房东失败")

@landlord_api.route("/update", methods=["POST"])
@permission_required("landlord")
def update_landlord():
    """修改房东信息"""
    data = request.get_json()
    land_id = data.get("land_id")
    land_name = data.get("land_name")
    land_phone = data.get("land_phone")
    land_idcard = data.get("land_idcard", "")
    land_address = data.get("land_address", "")
    
    if not land_id or not land_name or not land_phone:
        return fail(msg="必填参数不能为空", code=400)
    
    # 校验手机号是否重复（排除自身）
    exist = LandlordModel.get_landlord_by_phone(land_phone)
    if exist and exist["land_id"] != int(land_id):
        return fail(msg="该手机号已被其他房东使用", code=400)
    
    result = LandlordModel.update_landlord(land_id, land_name, land_phone, land_idcard, land_address)
    if result > 0:
        return success(msg="修改房东成功")
    else:
        return fail(msg="修改房东失败")

@landlord_api.route("/delete/<int:land_id>", methods=["DELETE"])
@permission_required("landlord")
def delete_landlord(land_id):
    """删除房东"""
    result = LandlordModel.delete_landlord(land_id)
    if result == -1:
        return fail(msg="该房东有关联房源，禁止删除", code=400)
    elif result > 0:
        return success(msg="删除房东成功")
    else:
        return fail(msg="删除房东失败")

@landlord_api.route("/<int:land_id>", methods=["GET"])
@permission_required("landlord")
def get_landlord_detail(land_id):
    """查询房东详情"""
    landlord = LandlordModel.get_landlord_by_id(land_id)
    if landlord:
        return success(data=landlord)
    else:
        return fail(msg="房东不存在")
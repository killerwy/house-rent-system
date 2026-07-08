"""租客管理接口"""
import re
from flask import Blueprint, request
from model.customer_model import CustomerModel
from util.response_util import success, fail, page_success
from util.page_util import get_page_params
from util.auth_util import permission_required

customer_api = Blueprint("customer_api", __name__, url_prefix="/api/customer")

PHONE_REG = re.compile(r'(^\d{8}$)|(^\d{11}$)')
IDCARD_REG = re.compile(r'(^\d{15}$)|(^\d{17}[\dX]$)')

@customer_api.route("/list", methods=["GET"])
@permission_required("customer")
def get_customer_list():
    """分页查询租客"""
    page, size, offset = get_page_params(request)
    keyword = request.args.get("keyword", "")
    
    total, list_data = CustomerModel.get_customer_list(offset, size, keyword)
    return page_success(total, list_data)

@customer_api.route("/add", methods=["POST"])
@permission_required("customer")
def add_customer():
    """新增租客"""
    data = request.get_json()
    cust_name = data.get("cust_name")
    cust_phone = data.get("cust_phone")
    cust_idcard = data.get("cust_idcard", "")
    work_unit = data.get("work_unit", "")
    
    if not cust_name or not cust_phone:
        return fail(msg="姓名和手机号不能为空", code=400)
    
    # 手机号校验
    if not PHONE_REG.match(cust_phone):
        return fail(msg="手机号必须为8或11位数字", code=400)
    # 身份证校验（允许空字符串，不填写不校验）
    if cust_idcard and not IDCARD_REG.match(cust_idcard):
        return fail(msg="身份证号必须为15位数字或18位数字(末位可为X)", code=400)

    # 手机号唯一性校验
    if CustomerModel.get_customer_by_phone(cust_phone):
        return fail(msg="该手机号已存在", code=400)
    
    # 身份证号唯一性校验
    if CustomerModel.get_customer_by_idcard(cust_idcard):
        return fail(msg="该身份证号已存在", code=400)
    
    result = CustomerModel.add_customer(cust_name, cust_phone, cust_idcard, work_unit)
    if result > 0:
        return success(msg="新增租客成功")
    else:
        return fail(msg="新增租客失败")

@customer_api.route("/update", methods=["POST"])
@permission_required("customer")
def update_customer():
    """修改租客信息"""
    data = request.get_json()
    cust_id = data.get("cust_id")
    cust_name = data.get("cust_name")
    cust_phone = data.get("cust_phone")
    cust_idcard = data.get("cust_idcard", "")
    work_unit = data.get("work_unit", "")
    
    if not cust_id or not cust_name or not cust_phone:
        return fail(msg="必填信息不能为空", code=400)
    
    # 手机号校验
    if not PHONE_REG.match(cust_phone):
        return fail(msg="手机号必须为8或11位数字", code=400)
    # 身份证校验（允许空字符串，不填写不校验）
    if cust_idcard and not IDCARD_REG.match(cust_idcard):
        return fail(msg="身份证号必须为15位数字或18位数字(末位可为X)", code=400)
    
    # 手机号唯一性校验（排除自身）
    exist = CustomerModel.get_customer_by_phone(cust_phone)
    if exist and exist["cust_id"] != int(cust_id):
        return fail(msg="该手机号已被其他租客使用", code=400)
    
    # 身份证号唯一性校验（排除自身）
    exist = CustomerModel.get_customer_by_idcard(cust_idcard)
    if exist and exist["cust_id"] != int(cust_id):
        return fail(msg="该身份证号已被其他租客使用", code=400)
    
    result = CustomerModel.update_customer(cust_id, cust_name, cust_phone, cust_idcard, work_unit)
    if result > 0:
        return success(msg="修改租客成功")
    else:
        return fail(msg="修改租客失败")

@customer_api.route("/delete/<int:cust_id>", methods=["DELETE"])
@permission_required("customer")
def delete_customer(cust_id):
    """删除租客"""
    result = CustomerModel.delete_customer(cust_id)
    if result == -1:
        return fail(msg="该租客有关联租赁合同，禁止删除", code=400)
    elif result > 0:
        return success(msg="删除租客成功")
    else:
        return fail(msg="删除租客失败")

@customer_api.route("/<int:cust_id>", methods=["GET"])
@permission_required("customer")
def get_customer_detail(cust_id):
    """查询租客详情"""
    customer = CustomerModel.get_customer_by_id(cust_id)
    if customer:
        return success(data=customer)
    else:
        return fail(msg="租客不存在")
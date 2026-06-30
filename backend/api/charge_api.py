"""收费管理接口：租金、押金、中介费登记与查询"""
from flask import Blueprint, request
from model.charge_model import ChargeModel
from model.contract_model import ContractModel
from util.response_util import success, fail, page_success
from util.page_util import get_page_params
from util.auth_util import permission_required

charge_api = Blueprint("charge_api", __name__, url_prefix="/api/charge")

@charge_api.route("/list", methods=["GET"])
@permission_required("charge")
def get_charge_list():
    """分页查询收费记录"""
    page, size, offset = get_page_params(request)
    contract_id = request.args.get("contract_id", -1, type=int)
    charge_type = request.args.get("charge_type", -1, type=int)
    
    total, list_data = ChargeModel.get_charge_list(offset, size, contract_id, charge_type)
    return page_success(total, list_data)

@charge_api.route("/add", methods=["POST"])
@permission_required("charge")
def add_charge():
    """新增收费记录：1=租金 2=押金 3=中介费"""
    data = request.get_json()
    contract_id = data.get("contract_id")
    charge_type = data.get("charge_type")
    charge_money = data.get("charge_money")
    remark = data.get("remark", "")
    
    # 参数校验
    if not all([contract_id, charge_type, charge_money]):
        return fail(msg="必填参数不能为空", code=400)
    
    # 校验收费类型
    if charge_type not in [1, 2, 3]:
        return fail(msg="收费类型不合法", code=400)
    
    # 校验金额
    if float(charge_money) <= 0:
        return fail(msg="收费金额必须大于0", code=400)
    
    # 校验合同是否存在
    if not ContractModel.get_contract_by_id(contract_id):
        return fail(msg="关联租赁合同不存在", code=400)
    
    # 新增收费记录
    result = ChargeModel.add_charge(contract_id, charge_type, charge_money, remark)
    if result > 0:
        return success(msg="收费登记成功")
    else:
        return fail(msg="收费登记失败")

@charge_api.route("/<int:charge_id>", methods=["GET"])
@permission_required("charge")
def get_charge_detail(charge_id):
    """查询收费记录详情"""
    charge = ChargeModel.get_charge_by_id(charge_id)
    if charge:
        return success(data=charge)
    else:
        return fail(msg="收费记录不存在")

@charge_api.route("/contract/<int:contract_id>", methods=["GET"])
@permission_required("charge")
def get_charge_by_contract(contract_id):
    """查询指定合同的所有收费记录"""
    data = ChargeModel.get_charge_by_contract(contract_id)
    return success(data=data)
"""员工管理接口"""
import re
from flask import Blueprint, request
from model.user_model import UserModel
from util.response_util import success, fail, page_success
from util.page_util import get_page_params
from util.auth_util import permission_required

user_api = Blueprint("user_api", __name__, url_prefix="/api/user")

PHONE_REG = re.compile(r'(^\d{8}$)|(^\d{11}$)')
IDCARD_REG = re.compile(r'(^\d{15}$)|(^\d{17}[\dX]$)')

@user_api.route("/list", methods=["GET"])
@permission_required("all")  # 仅超级管理员可访问
def get_user_list():
    """分页查询员工"""
    page, size, offset = get_page_params(request)
    keyword = request.args.get("keyword", "")
    total, list_data = UserModel.get_user_list(offset, size, keyword)
    return page_success(total, list_data)

@user_api.route("/add", methods=["POST"])
@permission_required("all")
def add_user():
    """新增员工"""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    real_name = data.get("real_name")
    phone = data.get("phone")
    idcard = data.get("idcard")
    role_id = data.get("role_id")
    
    # 校验参数
    if not username or not password or not real_name or not role_id:
        return fail(msg="必填信息不能为空", code=400)
    
    # 手机号校验
    if not PHONE_REG.match(phone):
        return fail(msg="手机号必须为8或11位数字", code=400)
    # 身份证校验（允许空字符串，不填写不校验）
    if idcard and not IDCARD_REG.match(idcard):
        return fail(msg="身份证号必须为15位数字或18位数字(末位可为X)", code=400)
    
    # 检查账号是否已存在
    if UserModel.get_user_by_username(username):
        return fail(msg="账号已存在", code=400)
    
    # 校验手机号重复
    if phone and UserModel.get_user_by_phone(phone):
        return fail(msg="该手机号已被注册", code=400)
    
    # 校验身份证重复
    if idcard and UserModel.get_user_by_idcard(idcard):
        return fail(msg="该身份证号已被注册", code=400)

    # 新增
    result = UserModel.add_user(username, password, real_name, phone, idcard, role_id)
    if result > 0:
        return success(msg="新增员工成功")
    else:
        return fail(msg="新增员工失败")

@user_api.route("/update", methods=["POST"])
@permission_required("all")
def update_user():
    """修改员工"""
    data = request.get_json()
    user_id = data.get("user_id")
    real_name = data.get("real_name")
    phone = data.get("phone")
    idcard = data.get("idcard")
    role_id = data.get("role_id")
    
    if not user_id or not real_name or not role_id:
        return fail(msg="必填信息不能为空", code=400)
    
    # 手机号校验
    if not PHONE_REG.match(phone):
        return fail(msg="手机号必须为8或11位数字", code=400)
    # 身份证校验（允许空字符串，不填写不校验）
    if idcard and not IDCARD_REG.match(idcard):
        return fail(msg="身份证号必须为15位数字或18位数字(末位可为X)", code=400)
    
    exist = UserModel.get_user_by_phone(phone)
    if exist and exist["user_id"] != int(user_id):
        return fail(msg="该手机号已被其他员工使用", code=400)
    
    exist = UserModel.get_user_by_idcard(idcard)
    if exist and exist["user_id"] != int(user_id):
            return fail(msg="该身份证号已被其他员工使用", code=400)

    result = UserModel.update_user(user_id, real_name, phone, idcard, role_id)
    if result > 0:
        return success(msg="修改员工成功")
    else:
        return fail(msg="修改员工失败")

@user_api.route("/updatePwd", methods=["POST"])
@permission_required("all")
def update_password():
    """修改密码"""
    data = request.get_json()
    user_id = data.get("user_id")
    new_password = data.get("new_password")
    
    if not user_id or not new_password:
        return fail(msg="必填信息不能为空", code=400)
    
    result = UserModel.update_password(user_id, new_password)
    if result > 0:
        return success(msg="密码修改成功")
    else:
        return fail(msg="密码修改失败")

@user_api.route("/delete/<int:user_id>", methods=["DELETE"])
@permission_required("all")
def delete_user(user_id):
    """删除员工"""
    result = UserModel.delete_user(user_id)
    if result == -1:
        return fail(msg="禁止删除超级管理员", code=400)
    elif result == -2:
        return fail(msg="该员工有操作记录，禁止删除", code=400)
    elif result > 0:
        return success(msg="删除员工成功")
    else:
        return fail(msg="删除员工失败")

@user_api.route("/<int:user_id>", methods=["GET"])
@permission_required("all")
def get_user_detail(user_id):
    """查询员工详情"""
    user = UserModel.get_user_by_id(user_id)
    if user:
        return success(data=user)
    else:
        return fail(msg="员工不存在")
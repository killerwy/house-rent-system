"""登录认证接口"""
from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from model.user_model import UserModel
from util.auth_util import verify_password
from util.response_util import success, fail

auth_api = Blueprint("auth_api", __name__, url_prefix="/api/auth")

@auth_api.route("/login", methods=["POST"])
def login():
    """登录接口"""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    # 校验参数
    if not username or not password:
        return fail(msg="账号/密码不能为空", code=400)
    
    # 查询用户
    user = UserModel.get_user_by_username(username)
    if not user:
        return fail(msg="账号不存在", code=401)
    
    # 校验密码
    if not verify_password(password, user["password"]):
        return fail(msg="密码错误", code=401)
    
    # 生成JWT token
    access_token = create_access_token(identity=str(user["user_id"]))
    
    return success(data={
        "token": access_token,
        "user_info": {
            "user_id": user["user_id"],
            "username": user["username"],
            "real_name": user["real_name"],
            "role_id": user["role_id"]
        }
    }, msg="登录成功")

@auth_api.route("/info", methods=["GET"])
def get_user_info():
    """获取当前用户信息"""
    from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = UserModel.get_user_by_id(user_id)
        if not user:
            return fail(msg="用户不存在", code=401)
        return success(data={
            "user_id": user["user_id"],
            "username": user["username"],
            "real_name": user["real_name"],
            "phone": user["phone"],
            "role_id": user["role_id"],
            "role_name": user["role_name"]
        })
    except Exception as e:
        return fail(msg=f"获取用户信息失败：{str(e)}", code=401)
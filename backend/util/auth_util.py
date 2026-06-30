"""权限校验工具：密码加密、JWT校验、角色权限"""
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from config import ROLE_PERMISSIONS
from db.mysql_conn import MySQLConnection
from util.response_util import fail

def verify_password(plain_password: str, db_password: str) -> bool:
    """验证密码"""
    return plain_password == db_password

def check_permission(required_permission: str):
    """
    校验角色权限
    :param required_permission: 需要的权限标识（如house/rent/backup）
    :return: 有权限返回True，无权限返回False
    """
    try:
        # 验证token
        verify_jwt_in_request()
        # 获取当前用户ID
        user_id = int(get_jwt_identity())
        # 查询用户角色
        sql = "SELECT role_id FROM sys_user WHERE user_id = %s"
        user_role = MySQLConnection.execute_sql(sql, (user_id,), fetch_type="one")
        if not user_role:
            return False
        
        role_id = user_role["role_id"]
        # 超级管理员拥有所有权限
        if ROLE_PERMISSIONS.get(role_id) == ["all"]:
            return True
        # 校验权限
        return required_permission in ROLE_PERMISSIONS.get(role_id, [])
    except Exception as e:
        print(f"数据库连接异常，权限校验中断: {e}")
        raise Exception("数据库服务异常，请稍后重试")
    except Exception as e:
        print(f"权限校验失败: {e}")
        return False

def permission_required(required_permission: str):
    """
    装饰器：接口权限校验
    :param required_permission: 需要的权限标识
    """
    def decorator(f):
        def wrapper(*args, **kwargs):
            try:
                if not check_permission(required_permission):
                    return fail(msg="无操作权限", code=403)
            except Exception as e:
                return fail(msg=str(e), code=500)
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator
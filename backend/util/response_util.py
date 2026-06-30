"""统一返回格式工具"""

def success(data=None, msg="操作成功"):
    """成功返回"""
    return {
        "code": 200,
        "msg": msg,
        "data": data or {}
    }

def fail(msg="操作失败", code=500, data=None):
    """失败返回"""
    return {
        "code": code,
        "msg": msg,
        "data": data or {}
    }

def page_success(total, list, msg="查询成功"):
    """分页成功返回"""
    return {
        "code": 200,
        "msg": msg,
        "data": {
            "total": total,
            "list": list
        }
    }
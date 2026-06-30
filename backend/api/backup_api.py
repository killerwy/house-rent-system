"""数据库备份与恢复接口：仅超级管理员可访问"""
from flask import Blueprint, request
from db.backup_tool import BackupTool
from config import BACKUP_PATH
from util.response_util import success, fail
from util.auth_util import permission_required
import os

backup_api = Blueprint("backup_api", __name__, url_prefix="/api/backup")

@backup_api.route("/list", methods=["GET"])
@permission_required("all")
def get_backup_list():
    """获取所有备份文件列表"""
    files = BackupTool.list_backup_files()
    return success(data=files)

@backup_api.route("/doBackup", methods=["POST"])
@permission_required("all")
def do_backup():
    """执行一键数据库备份"""
    result = BackupTool.backup_database()
    if result["status"] == "success":
        return success(data={
            "file_name": result["file_name"],
            "file_path": result["file_path"]
        }, msg="数据库备份成功")
    else:
        return fail(msg=f"备份失败：{result.get('error', '未知错误')}")

@backup_api.route("/doRestore", methods=["POST"])
@permission_required("all")
def do_restore():
    """执行数据库恢复"""
    data = request.get_json()
    file_name = data.get("file_name")
    
    if not file_name:
        return fail(msg="备份文件名不能为空", code=400)
    
    # 拼接完整路径，防止路径穿越
    file_path = os.path.join(BACKUP_PATH, file_name)
    # 安全校验：确保文件在备份目录内
    if not os.path.realpath(file_path).startswith(os.path.realpath(BACKUP_PATH)):
        return fail(msg="非法的备份文件路径", code=400)
    
    result = BackupTool.restore_database(file_path)
    if result["status"] == "success":
        return success(msg="数据库恢复成功")
    else:
        return fail(msg=f"恢复失败：{result.get('error', '未知错误')}")
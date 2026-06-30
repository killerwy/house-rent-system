import os
import subprocess
import time
import logging
from config import MYSQL_CONFIG, BACKUP_PATH

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BackupTool:
    @staticmethod
    def backup_database():
        """手动备份数据库，返回备份文件路径"""
        # 备份文件名：house_rent_20260601_120000.sql
        backup_filename = f"house_rent_{time.strftime('%Y%m%d_%H%M%S')}.sql"
        backup_filepath = os.path.join(BACKUP_PATH, backup_filename)
        
        # 构建mysqldump命令
        cmd = [
            "mysqldump",
            "-h", MYSQL_CONFIG["host"],
            "-P", str(MYSQL_CONFIG["port"]),
            "-u", MYSQL_CONFIG["user"],
            f"-p{MYSQL_CONFIG['password']}",
            MYSQL_CONFIG["database"],
            "--default-character-set=utf8mb4",
            ">", backup_filepath
        ]
        # 拼接命令（兼容Windows/Linux）
        cmd_str = " ".join(cmd)
        
        try:
            # 执行备份命令
            subprocess.run(cmd_str, shell=True, check=True, capture_output=True, text=True)
            logger.info(f"数据库备份成功: {backup_filepath}")
            return {
                "status": "success",
                "file_path": backup_filepath,
                "file_name": backup_filename
            }
        except subprocess.CalledProcessError as e:
            logger.error(f"备份失败: {e.stderr}")
            return {
                "status": "failed",
                "error": e.stderr
            }

    @staticmethod
    def restore_database(backup_filepath):
        """恢复数据库"""
        if not os.path.exists(backup_filepath):
            return {"status": "failed", "error": "备份文件不存在"}
        
        # 构建恢复命令
        cmd = [
            "mysql",
            "-h", MYSQL_CONFIG["host"],
            "-P", str(MYSQL_CONFIG["port"]),
            "-u", MYSQL_CONFIG["user"],
            f"-p{MYSQL_CONFIG['password']}",
            MYSQL_CONFIG["database"],
            "--default-character-set=utf8mb4",
            "<", backup_filepath
        ]
        cmd_str = " ".join(cmd)
        
        try:
            subprocess.run(cmd_str, shell=True, check=True, capture_output=True, text=True)
            logger.info(f"数据库恢复成功: {backup_filepath}")
            return {"status": "success"}
        except subprocess.CalledProcessError as e:
            logger.error(f"恢复失败: {e.stderr}")
            return {"status": "failed", "error": e.stderr}

    @staticmethod
    def list_backup_files():
        """列出所有备份文件"""
        if not os.path.exists(BACKUP_PATH):
            return []
        # 只筛选.sql备份文件，按时间倒序
        files = [f for f in os.listdir(BACKUP_PATH) if f.endswith(".sql")]
        files.sort(reverse=True)
        return [
            {
                "file_name": f,
                "file_path": os.path.join(BACKUP_PATH, f),
                "create_time": time.ctime(os.path.getctime(os.path.join(BACKUP_PATH, f)))
            }
            for f in files
        ]
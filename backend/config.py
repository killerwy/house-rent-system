import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库配置
MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", 3306)),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "your_mysql_password"),
    "database": os.getenv("MYSQL_DB", "house_rent"),
    "charset": "utf8mb4",
    "autocommit": True
}

# JWT配置
JWT_SECRET_KEY = os.getenv("JWT_SECRET", "house_rent_2026_course_design_secure_123456789abc")
JWT_ACCESS_TOKEN_EXPIRES = 3600 * 8  # token有效期8小时

# 备份配置
BACKUP_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "backup")
# 确保备份目录存在
if not os.path.exists(BACKUP_PATH):
    os.makedirs(BACKUP_PATH)

# 角色权限映射
ROLE_PERMISSIONS = {
    1: ["all"],  # 超级管理员
    2: ["house", "landlord", "customer", "rent", "charge", "stat", "view"],  # 中介员工
    3: ["view", "stat"]  # 只读员工
}
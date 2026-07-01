"""Flask项目入口：注册蓝图、配置JWT、启动服务"""
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES

# 导入所有蓝图
from api.auth_api import auth_api
from api.user_api import user_api
from api.house_api import house_api
from api.landlord_api import landlord_api
from api.customer_api import customer_api
from api.rent_api import rent_api
from api.charge_api import charge_api
from api.stat_api import stat_api
from api.view_api import view_api
from api.backup_api import backup_api
from api.address_api import address_api

# 初始化Flask应用
app = Flask(__name__)

# 配置JWT
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = JWT_ACCESS_TOKEN_EXPIRES
jwt = JWTManager(app)

# 启用跨域
CORS(app, supports_credentials=True)

# 注册蓝图
app.register_blueprint(auth_api)
app.register_blueprint(user_api)
app.register_blueprint(house_api)
app.register_blueprint(landlord_api)
app.register_blueprint(customer_api)
app.register_blueprint(rent_api)
app.register_blueprint(charge_api)
app.register_blueprint(stat_api)
app.register_blueprint(view_api)
app.register_blueprint(backup_api)
app.register_blueprint(address_api)

# 根路径测试
@app.route("/")
def index():
    return {
        "code": 200,
        "msg": "二手房中介管理系统（租房版）后端服务运行正常",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    # 启动服务，默认端口5000，开启调试模式（生产环境需关闭）
    app.run(host="0.0.0.0", port=5000, debug=True)
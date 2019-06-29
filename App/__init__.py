from flask import Flask
from App.views import blue
from App.exts import init_exts


def create_app():
    app = Flask(__name__)

    # 配置数据库
    # mysql
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:CooL1995BoY@localhost:3306/blog'

    # 禁止‘追踪修改’
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY']='ASDc25'
    # 修改成开发环境
    app.config['ENV'] = 'development'

    # 注册蓝图
    app.register_blueprint(blue)

    # 初始化插件
    init_exts(app)

    return app


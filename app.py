# app.py

from flask import Flask
from extensions import db, migrate
from views import views
import os

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'your_secret_key'  # 替换为您的秘密密钥
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'your_db.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 确保 instance 文件夹存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass  # Instance 文件夹已经存在

    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)

    # 注册蓝图
    app.register_blueprint(views)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

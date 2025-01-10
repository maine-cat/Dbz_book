# create_db_book.py

from app import create_app
from extensions import db
from models import TacticsBook, Category

app = create_app()

with app.app_context():
    db.create_all()
    print("数据库和表格创建成功！")

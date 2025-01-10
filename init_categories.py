# init_categories.py

from app import create_app
from extensions import db
from models import Category

app = create_app()

with app.app_context():
    # 清空现有类别
    db.session.query(Category).delete()
    
    # 创建主类别
    main_category_economy = Category(name='经济')
    main_category_map = Category(name='地图')
    main_category_lineup = Category(name='阵容')  # 新增主类别“阵容”

    db.session.add_all([main_category_economy, main_category_map, main_category_lineup])
    db.session.commit()

    # 创建子类别
    sub_categories = [
        # 经济类子类别
        Category(name='eco', parent=main_category_economy),
        Category(name='强起', parent=main_category_economy),
        Category(name='长枪局', parent=main_category_economy),
        Category(name='手枪局', parent=main_category_economy),  # 为“经济”添加子类别“手枪局”

        # 地图类子类别
        Category(name='Inferno', parent=main_category_map),
        Category(name='Dust2', parent=main_category_map),
        Category(name='Mirage', parent=main_category_map),
        Category(name='Vertigo', parent=main_category_map),
        Category(name='Ancient', parent=main_category_map),
        Category(name='Anubis', parent=main_category_map),

        # 阵容类子类别
        Category(name='警察', parent=main_category_lineup),  # 为“阵容”添加子类别“警察”
        Category(name='匪徒', parent=main_category_lineup),  # 为“阵容”添加子类别“匪徒”
    ]

    db.session.add_all(sub_categories)
    db.session.commit()

    print("类别初始化完成！")

# models.py

from extensions import db

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)

    parent = db.relationship('Category', remote_side=[id], backref='subcategories')

    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

    def __repr__(self):
        if self.parent:
            return f'<Category {self.parent.name} > {self.name}>'
        return f'<Category {self.name}>'

class TacticsBook(db.Model):
    __tablename__ = 'tactics_book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    modified_by = db.Column(db.String(100), nullable=False)

    # 新增三个外键，分别关联到“经济”、“地图”、“阵容”的子类别
    economic_category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    map_category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    lineup_category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    # 三个关系，分别对应不同类型的类别
    economic_category = db.relationship('Category', foreign_keys=[economic_category_id])
    map_category = db.relationship('Category', foreign_keys=[map_category_id])
    lineup_category = db.relationship('Category', foreign_keys=[lineup_category_id])

    def __init__(self, title, content, modified_by, economic_category, map_category, lineup_category):
        self.title = title
        self.content = content
        self.modified_by = modified_by
        self.economic_category = economic_category
        self.map_category = map_category
        self.lineup_category = lineup_category

    def __repr__(self):
        return f'<TacticsBook {self.title}>'

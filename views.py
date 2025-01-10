# views.py

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from extensions import db
from models import TacticsBook, Category
from forms import TacticsForm

views = Blueprint('views', __name__)

# 首页路由
@views.route('/', methods=['GET', 'POST'])
def index():
    form = TacticsForm()
    
    # 获取所有主类别
    main_categories = Category.query.filter_by(parent_id=None).all()
    
    # 获取对应的子类别
    economic_main = Category.query.filter_by(name='经济').first()
    map_main = Category.query.filter_by(name='地图').first()
    lineup_main = Category.query.filter_by(name='阵容').first()
    
    # 设置选择字段的选项
    form.economic_category.choices = [(str(cat.id), cat.name) for cat in economic_main.subcategories]
    form.map_category.choices = [(str(cat.id), cat.name) for cat in map_main.subcategories]
    form.lineup_category.choices = [(str(cat.id), cat.name) for cat in lineup_main.subcategories]
    
    if form.validate_on_submit():
        # 获取选择的类别
        selected_economic = Category.query.get(int(form.economic_category.data))
        selected_map = Category.query.get(int(form.map_category.data))
        selected_lineup = Category.query.get(int(form.lineup_category.data))
        
        tactics = TacticsBook(
            title=form.title.data,
            content=form.content.data,
            modified_by=form.modified_by.data,
            economic_category=selected_economic,
            map_category=selected_map,
            lineup_category=selected_lineup
        )
        db.session.add(tactics)
        db.session.commit()
        flash('策略本内容已保存！', 'success')
        return redirect(url_for('views.index'))
    
    # 处理筛选逻辑
    economic_filter = request.args.get('economic_category', type=int)
    map_filter = request.args.get('map_category', type=int)
    lineup_filter = request.args.get('lineup_category', type=int)
    
    query = TacticsBook.query
    
    if economic_filter:
        query = query.filter_by(economic_category_id=economic_filter)
    if map_filter:
        query = query.filter_by(map_category_id=map_filter)
    if lineup_filter:
        query = query.filter_by(lineup_category_id=lineup_filter)
    
    tactics = query.order_by(TacticsBook.id.desc()).all()
    
    return render_template('index.html', tactics=tactics, form=form)

# API 路由用于获取子类别（可选，如果需要动态加载）
@views.route('/subcategories/<int:main_category_id>')
def get_subcategories(main_category_id):
    sub_categories = Category.query.filter_by(parent_id=main_category_id).all()
    sub_cat_list = [{'id': cat.id, 'name': cat.name} for cat in sub_categories]
    return jsonify(sub_cat_list)

# 查看单个策略本
@views.route('/view/<int:tactics_id>')
def view_tactic(tactics_id):
    tactics = TacticsBook.query.get_or_404(tactics_id)
    return render_template('view.html', tactics=tactics)

# 编辑策略本内容
@views.route('/edit/<int:tactics_id>', methods=['GET', 'POST'])
def edit(tactics_id):
    tactics = TacticsBook.query.get_or_404(tactics_id)
    form = TacticsForm(obj=tactics)
    
    # 获取对应的主类别
    economic_main = Category.query.filter_by(name='经济').first()
    map_main = Category.query.filter_by(name='地图').first()
    lineup_main = Category.query.filter_by(name='阵容').first()
    
    # 设置选择字段的选项
    form.economic_category.choices = [(str(cat.id), cat.name) for cat in economic_main.subcategories]
    form.map_category.choices = [(str(cat.id), cat.name) for cat in map_main.subcategories]
    form.lineup_category.choices = [(str(cat.id), cat.name) for cat in lineup_main.subcategories]
    
    if form.validate_on_submit():
        # 获取选择的类别
        selected_economic = Category.query.get(int(form.economic_category.data))
        selected_map = Category.query.get(int(form.map_category.data))
        selected_lineup = Category.query.get(int(form.lineup_category.data))
        
        tactics.title = form.title.data
        tactics.content = form.content.data
        tactics.modified_by = form.modified_by.data
        tactics.economic_category = selected_economic
        tactics.map_category = selected_map
        tactics.lineup_category = selected_lineup
        db.session.commit()
        flash('策略本内容已更新！', 'success')
        return redirect(url_for('views.view_tactic', tactics_id=tactics.id))
    
    return render_template('edit.html', form=form, tactics=tactics)

# 删除策略本
@views.route('/delete/<int:tactics_id>', methods=['POST'])
def delete(tactics_id):
    tactics = TacticsBook.query.get_or_404(tactics_id)
    db.session.delete(tactics)
    db.session.commit()
    flash('策略本已删除。', 'success')
    return redirect(url_for('views.index'))

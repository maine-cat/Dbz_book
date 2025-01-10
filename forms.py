# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired

class TacticsForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired()])
    content = TextAreaField('内容', validators=[DataRequired()])
    modified_by = StringField('修改人', validators=[DataRequired()])
    
    # 新增三个选择字段，分别对应不同类型的类别
    economic_category = SelectField('经济类别', choices=[], validators=[DataRequired()])
    map_category = SelectField('地图类别', choices=[], validators=[DataRequired()])
    lineup_category = SelectField('阵容类别', choices=[], validators=[DataRequired()])
    
    submit = SubmitField('保存')

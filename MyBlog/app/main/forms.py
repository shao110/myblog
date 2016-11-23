from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_pagedown.fields import PageDownField
from ..models import Category

class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PostForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    body = PageDownField("Body", validators=[DataRequired()])
    summary = PageDownField('Summary', validators=[DataRequired()])
    category = SelectField('Category', coerce=int)
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.tag)
                                 for category in Category.query.order_by(Category.tag).all()]

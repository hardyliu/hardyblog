from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField,HiddenField,PasswordField,BooleanField,SelectField,ValidationError
from wtforms.validators import DataRequired, Email, Length, Optional, URL

from hardyblog.models import Category

class CommentForm(FlaskForm):
    author = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 254)])
    site = StringField('Site', validators=[Optional(), URL(), Length(0, 255)])
    body = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField()
    
class AdminCommentForm(CommentForm):
    author = HiddenField()
    email = HiddenField()
    site = HiddenField() 


class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField()

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('Name already in use.')

class AdminLoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(4,25)])
    password = PasswordField('Password',validators=[DataRequired(),Length(4,25)])
    remember = BooleanField('Remember me')
    login = SubmitField('Log in')
    
    
class SettingsForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(),Length(4,25)])
    blog_title = StringField('Blog Title',validators=[DataRequired(),Length(4,25)])
    blog_sub_title = StringField('Blog Sub Title')
    about = TextAreaField('About Page')
    submit = SubmitField('Submit')
    
    
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 60)])
    category = SelectField('Category', coerce=int, default=1)
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField()  
    
    def __init__(self,*args,**kwargs):
        super(PostForm,self).__init__(*args,**kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(Category.name).all()]
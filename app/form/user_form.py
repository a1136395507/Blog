# config=utf-8
from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired('username is null')])
    password = PasswordField('password', validators=[DataRequired('password is null')])


class RegisterForm(Form):
    username = StringField("username", validators=[DataRequired('username is null')])
    company_name = StringField('company_name', validators=[DataRequired()])
    phone = IntegerField('Phone', validators=[DataRequired()])
    expire_time = StringField("expire_time", validators=[DataRequired('用户到期时间为空')])
    count = IntegerField('count', validators=[DataRequired("用户调用接口次数为空")])
    submit = SubmitField("login")

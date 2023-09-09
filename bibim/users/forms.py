from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, SubmitField, 
                     BooleanField, PasswordField)
from wtforms.validators import Email, DataRequired, EqualTo, Length, ValidationError
from bibim.models import User
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from bibim.main.utils import file_max_size

class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField('email', validators=[Email(), DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('register') 

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose another one.')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose another one.')

class LoginForm(FlaskForm):
    email = StringField('email', validators=[Email(), DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    about = TextAreaField('Bio')
    picture = FileField('Profile Picture', validators=[FileAllowed(['jpeg', 'png']), file_max_size(10)])
    submit = SubmitField('Make changes')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken.')
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken.')
            
   

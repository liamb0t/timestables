from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, SubmitField, 
                     BooleanField, PasswordField, MultipleFileField, SelectField)
from wtforms.validators import Email, DataRequired, EqualTo, Length, ValidationError
from bibim.models import User
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    about = TextAreaField('About')
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update Account')

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
            

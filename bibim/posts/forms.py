from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import (StringField, TextAreaField, SubmitField, 
                     BooleanField, PasswordField, MultipleFileField, SelectField)
from wtforms.validators import Email, DataRequired, EqualTo, Length, ValidationError
import random


class PostForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()], render_kw={"placeholder": None})
    submit = SubmitField('Post')

class FollowForm(FlaskForm):
    submit = SubmitField('Follow')

class MessageForm(FlaskForm):
    body = TextAreaField('Message', validators=[DataRequired(), Length(min=0, max=140)], render_kw={"placeholder": 'Message...'})
    submit = SubmitField('Send message')
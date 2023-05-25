from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, SubmitField, 
                     BooleanField, PasswordField, MultipleFileField, SelectField, HiddenField,
                     IntegerField)
from wtforms.validators import Email, DataRequired, EqualTo, Length, ValidationError
from wtforms_components import DateField



class MeetingForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], render_kw={'placeholder': 'Title'})
    content = TextAreaField('Description', validators=[DataRequired()], render_kw={'placeholder': 'Text'})
    location = StringField('Location', validators=[DataRequired()], render_kw={'placeholder': 'Meeting location'})
    time = DateField()
    files = MultipleFileField('Attachments')
    fee = IntegerField('Fee', render_kw={'placeholder': 'Please enter a number'})
    capacity = IntegerField('Capacity', render_kw={'placeholder': 'Please enter a number'})
    level = HiddenField()
    tag = SelectField('Type of Meeting', choices=[(x, x) for x in ['Select a tag', 'Language exchange', 'Music',
                                                                              'Social', 'Sports', 'Band',
                                                                              'Arts & Culture', 'Travel'
                                                                            ]])
    submit = SubmitField('Create Meeting') 

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()], render_kw={'placeholder': 'Add a comment...'})
    reply_id = HiddenField('reply_id')
    submit = SubmitField('')
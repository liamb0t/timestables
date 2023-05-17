from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, SubmitField,
                     BooleanField, PasswordField, MultipleFileField, SelectField, HiddenField)
from wtforms.validators import Email, DataRequired, EqualTo, Length, ValidationError

class MaterialForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], render_kw={'placeholder': 'Title'})
    grade = SelectField('Grade')
    content = TextAreaField('Description', validators=[DataRequired()], render_kw={'placeholder': 'Text'})
    files = MultipleFileField('Attachments')
    publisher = SelectField('Publisher')
    level = HiddenField()
    lesson = SelectField('Lesson', choices=[], validate_choice=False)
    material_type = SelectField('Type of Material', choices=[(x, x) for x in ['Select a tag', 'Bomb game', 'Writing game',
                                                                              'Reading game', 'Review game', 'Intro PPT',
                                                                              'Words in songs', 'Non-tech game'
                                                                            ]])
    submit = SubmitField('Create Material') 

class SelectForm(FlaskForm):
    publisher = SelectField('Publisher', choices=[(x, x) for x in ['All', 'YBM Choi 2015', 'YBM Kim 2015',
                                                                              'Cheonjae', 'Daegyo', 'Donga',
                                                                            ]])
    lesson = SelectField('Lesson', choices=['All'])
    type = SelectField('Type of Material', choices=[(x, x) for x in ['Any', 'Bomb game', 'Writing game',
                                                                              'Reading game', 'Review game', 'Intro PPT',
                                                                              'Words in songs', 'Non-tech game'
                                                                            ]])
    submit = SubmitField('Filter')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()], render_kw={'placeholder': 'Add a comment...'})
    reply_id = HiddenField('reply_id')
    submit = SubmitField('')
from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, SubmitField,
                     BooleanField, PasswordField, MultipleFileField, SelectField, HiddenField)
from wtforms.validators import Email, DataRequired, EqualTo, Length, ValidationError
from flask_ckeditor import CKEditorField

class MaterialForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], render_kw={'placeholder': 'Title'})
    grade = SelectField('Grade', validators=[DataRequired()])
    content = CKEditorField('Content', render_kw={'placeholder': 'Text'})
    files = MultipleFileField('Attachments')
    publisher = SelectField('Publisher')
    level = HiddenField()
    lesson = SelectField('Lesson', choices=[], validate_choice=False)
    material_type = SelectField('Type of Material', validators=[DataRequired()], choices=[(x, x) for x in ['Select a tag', 'Bomb game', 'Writing game',
                                                                              'Reading game', 'Review game', 'Intro PPT',
                                                                              'Words in songs', 'Non-tech game'
                                                                            ]])
    submit = SubmitField('Create Material') 

class SelectForm(FlaskForm):
    grade = SelectField('Grade', choices=[('0', 'Grade'), ('All', 'All'), ('1', 'Grade 1'), ('2', 'Grade 2'), ('3', 'Grade 3'), ('4', 'Grade 4'),
                                          ('5', 'Grade 5'), ('6', 'Grade 6'), ('7', 'Kindergarten'), 
                                          ('1', 'Afterschool'), ('1', 'Phonics'),])
    
    publisher = SelectField('Publisher', choices=[(x, x) for x in ['Textbook', 'All', 'YBM Choi ', 'YBM Kim ',
                                                                              'Cheonjae', 'Daegyo', 'Donga',
                                                                            ]])
    lesson = SelectField('Lesson', choices=['Lesson', 'All'])
    type = SelectField('Type of Material', choices=[(x, x) for x in ['Material Type', 'Any', 'Bomb game', 'Writing game',
                                                                              'Reading game', 'Review game', 'Intro PPT',
                                                                              'Words in songs', 'Non-tech game'
                                                                            ]])
    submit = SubmitField('Filter')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()], render_kw={'placeholder': 'Add a comment...'})
    reply_id = HiddenField('reply_id')
    submit = SubmitField('')
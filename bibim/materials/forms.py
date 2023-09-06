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
    publisher = SelectField('Publisher', validate_choice=False)
    level = HiddenField()
    lesson = SelectField('Lesson', choices=[], validate_choice=False)
    material_type = SelectField('Type of Material', validate_choice=False, choices=[(x, x) for x in ['Select a tag', 'Bomb game', 'Writing game',
                                                                              'Reading game', 'Review game', 'Intro PPT',
                                                                              'Words in songs', 'Non-tech game'
                                                                            ]])
    submit = SubmitField('Create Material') 

    def validate_grade(self, grade):
      if grade.data == '0':
        raise ValidationError('Please select a valid option.')
      
    def validate_material_type(self, material_type):
      if material_type.data == 'Select a tag':
        raise ValidationError('Please select at least one tag.')

class SelectForm(FlaskForm):
    grade = SelectField('Grade', choices=[])
    
    publisher = SelectField('Publisher', choices=['Textbook', 'All'])
    lesson = SelectField('Lesson', choices=['Lesson', 'All'], validate_choice=False)
    type = SelectField('Type of Material', choices=[(x, x) for x in ['Material Type', 'Any', 'Bomb game', 'Writing game',
                                                                              'Reading game', 'Review game', 'Intro PPT',
                                                                              'Words in songs', 'Non-tech game'
                                                                            ]])
    submit = SubmitField('Filter')

class CommentForm(FlaskForm):
    content = StringField('Comment', validators=[DataRequired()], render_kw={'placeholder': 'Add a comment...'})
    reply_id = HiddenField('reply_id')
    submit = SubmitField('Send  ')
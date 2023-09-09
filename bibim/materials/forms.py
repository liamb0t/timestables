from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField,
                    MultipleFileField, SelectField, HiddenField)
from wtforms.validators import DataRequired, ValidationError
from flask_ckeditor import CKEditorField
from bibim.main.utils import total_files_max_size
from flask_wtf.file import FileAllowed

allowed_extensions = [
    'jpeg', 'jpg', 'png', 'gif',  # Image formats
    'ppt', 'pptx',                # Presentation formats
    'mp4', 'mp3', 'wav', 'mov',   # Audio/Video formats
    'pdf',                        # Document format
    'doc', 'docx',                # Word document formats
    'xls', 'xlsx',                # Excel formats
    'zip', 'rar'                  # Archive formats
]

class MaterialForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], render_kw={'placeholder': 'Title'})
    grade = SelectField('Grade', validators=[DataRequired()])
    content = CKEditorField('Content', render_kw={'placeholder': 'Text'})
    files = MultipleFileField('Attachments', validators=[FileAllowed(allowed_extensions), total_files_max_size(500)])
    publisher = SelectField('Publisher', validate_choice=False)
    level = HiddenField()
    lesson = SelectField('Lesson', choices=[], validate_choice=False)
    material_type = SelectField('Type of Material', validate_choice=False, choices=[(x, x) for x in ['Select a tag', 'Bomb game', 'Writing',
                                                                              'Reading', 'Speaking', 'Listening', 'Review', 
                                                                              'Intro PPT', 'Phonics', 'Multi-skill', 'Worksheets',
                                                                              'Words in songs', 'Non-tech'
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
    type = SelectField('Type of Material', choices=[(x, x) for x in ['Material Type', 'Any', 'Bomb game', 'Writing',
                                                                              'Reading', 'Speaking', 'Listening', 'Review', 
                                                                              'Intro PPT', 'Phonics', 'Multi-skill', 'Worksheets',
                                                                              'Words in songs', 'Non-tech'
                                                                            ]])
    submit = SubmitField('Filter')

class CommentForm(FlaskForm):
    content = StringField('Comment', validators=[DataRequired()], render_kw={'placeholder': 'Add a comment...'})
    reply_id = HiddenField('reply_id')
    submit = SubmitField('Send  ')
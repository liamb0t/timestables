from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, SubmitField, 
                     BooleanField, PasswordField, MultipleFileField, SelectField, HiddenField,
                     IntegerField, TimeField, FileField)
from wtforms.validators import Email, DataRequired, EqualTo, Length, ValidationError
from wtforms_components import DateField
from flask_wtf.file import FileAllowed



class MeetingForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], render_kw={'placeholder': 'Event name'})
    content = TextAreaField('Description', validators=[DataRequired()], render_kw={'placeholder': 'Text'})
    location = StringField('Location', validators=[DataRequired()], render_kw={'placeholder': 'Meeting location'})
    start_date = DateField()
    start_time = TimeField()
    end_date = DateField()
    end_time = TimeField()
    cover_pic = FileField()
    files = MultipleFileField('Attachments', 
                            validators=[FileAllowed(['jpg', 'png', 'mp4', 'mp3', 'ppt'])])
    fee = IntegerField('Fee', render_kw={'placeholder': 'Fee'})
    capacity = IntegerField('Capacity', render_kw={'placeholder': 'Maximum number of attendees'})
    tag = SelectField('Type of Meeting', choices=[(x, x) for x in ['Select a tag', 'Language exchange', 'Music',
                                                                              'Social', 'Sports', 'Band',
                                                                              'Arts & Culture', 'Travel'
                                                                            ]])
    submit = SubmitField('Create Meeting') 

    def validate_my_file(self, field):
        max_size = 1000 * 1024 * 1024

        if field.data and len(field.data.read()) > max_size:
            raise ValidationError('File size exceeds the maximum limit.')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()], render_kw={'placeholder': 'Add a comment...'})
    reply_id = HiddenField('reply_id')
    submit = SubmitField('')

class SelectForm(FlaskForm):
    grade = SelectField('Location', choices=[('0', 'Location'), ('All', 'All'), ('1', 'Gyeonggi-do'), ('2', 'Gangwon-do'), ('3', 'Chungcheongbuk-do'), ('4', 'Chungnam-do'),
                                          ('5', 'Gyeongsang-do'), ('6', 'Jeollabuk-do'), ('7', 'Gyeongsangnam-do'), 
                                          ('1', 'Jeollanam-do'), ('1', 'Jeju-do'),])
    
    publisher = SelectField('Publisher', choices=[(x, x) for x in ['City', 'All', 'YBM Choi ', 'YBM Kim ',
                                                                              'Cheonjae', 'Daegyo', 'Donga',
                                                                            ]])
    type = SelectField('Type of Meeting', choices=[(x, x) for x in ['Meeting Type', 'All', 'Sports', 'Social',
                                                                              'Outdoors', 'Language', 'Cultural',
                                                                              'Art', 'Hobbies', 'Others'
                                                                            ]])
    submit = SubmitField('Filter')
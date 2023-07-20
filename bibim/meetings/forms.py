from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, SubmitField, 
                     BooleanField, SearchField, MultipleFileField, SelectField, HiddenField,
                     IntegerField, TimeField, FileField)
from wtforms.validators import Email, DataRequired, EqualTo, Length, ValidationError, Optional
from wtforms_components import DateField
from flask_wtf.file import FileAllowed



class MeetingForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], render_kw={'placeholder': 'Event name'})
    content = TextAreaField('Description', validators=[DataRequired()], render_kw={'placeholder': 'Text'})
    location = StringField('Location', validators=[DataRequired()], render_kw={'placeholder': 'Place name'})
    start_date = DateField(validators=[DataRequired()])
    start_time = TimeField(validators=[DataRequired()])
    end_date = DateField(validators=[Optional()])
    end_time = TimeField(validators=[Optional()])
    cover_pic = FileField()
    lat = HiddenField('lat', validators=[Optional()])
    lng = HiddenField('lng', validators=[Optional()])
    address = HiddenField('address')
    files = MultipleFileField('Attachments', 
                            validators=[FileAllowed(['jpg', 'png', 'mp4', 'mp3', 'ppt'])])
    fee = IntegerField('Fee', validators=[Optional()], render_kw={'placeholder': 'Participation fee in ₩'})
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

class FilterForm(FlaskForm):
    type = SelectField('Type of Meeting', validators=[Optional()], choices=[(x, x) for x in ['Meeting Type', 'All', 'Sports', 'Social',
                                                                              'Outdoors', 'Language', 'Cultural',
                                                                              'Art', 'Hobbies', 'Others'
                                                                            ]])
    search = SearchField('Search', validators=[Optional()], render_kw={'placeholder': 'City, province...'})
    submit = SubmitField('Filter')



   
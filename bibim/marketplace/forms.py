from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, SubmitField, 
                     BooleanField, SearchField, MultipleFileField, SelectField, HiddenField,
                     IntegerField, TimeField, FileField)
from wtforms.validators import Email, DataRequired, EqualTo, Length, ValidationError, Optional
from wtforms_components import DateField
from flask_wtf.file import FileAllowed

class AdForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], render_kw={'placeholder': 'Title'})
    content = TextAreaField('Description', validators=[DataRequired()], render_kw={'placeholder': 'Description'})
    cover_pic = FileField()
    address = HiddenField('address')
    files = MultipleFileField('Photos (.jpg, and .png)', 
                            validators=[FileAllowed(['jpg', 'png', ])])
    fee = IntegerField('Fee', validators=[Optional()], render_kw={'placeholder': 'Price ₩'})
    tag = SelectField('Category', choices=[(x, x) for x in ['Category', 'Home', 'Books',
                                                                              'Sports', 'Electronics', 'Music',
                                                                              'Clothes', 'Appliances', 'Other goods '
                                                                            ]])
    submit = SubmitField('Post my ad') 

    def validate_my_file(self, field):
        max_size = 1000 * 1024 * 1024

        if field.data and len(field.data.read()) > max_size:
            raise ValidationError('File size exceeds the maximum limit.')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()], render_kw={'placeholder': 'Add a comment...'})
    reply_id = HiddenField('reply_id')
    submit = SubmitField('')

class FilterForm(FlaskForm):
    type = SelectField('Category', validators=[Optional()], choices=[(x, x) for x in ['Category', 'All', 'House', 'Books',
                                                                              'Sports', 'Electronics', 'Appliances',
                                                                              'Clothes', 'Kids stuff', 'Others'
                                                                            ]])
    search = SearchField('Search', validators=[Optional()], render_kw={'placeholder': 'Search...'})
    submit = SubmitField('Filter')



   
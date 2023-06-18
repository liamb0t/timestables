import datetime
import os
import secrets
from flask import current_app

def date_member_since(date_joined):
    join_date = date_joined.date()
    today = datetime.date.today()

    delta = today - join_date
    years = delta.days // 365
    months = (delta.days % 365) // 30
    days = delta.days 

    if years > 0:
        time_string = f"Member for {years}, {months} months"
    elif years == 0 and months > 0:
        time_string = f"Member for {months} months"
    elif days <= 1:
        time_string = "Member since today"
    else:
        time_string = f"Member for {days} days"

    return time_string

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/pics', picture_fn)
    form_picture.save(picture_path)

    return picture_fn
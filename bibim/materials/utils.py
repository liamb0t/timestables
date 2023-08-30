import secrets
import os 
from flask import current_app
from bibim import db
from bibim.models import File, Textbook, Lesson

def get_file_size(file_path):

    bytes = os.path.getsize(file_path)
    kb = bytes / 1024
    mb = bytes / (1024 * 1024)
    gb = mb / 1024

    return (int(gb), "GB") if mb > 1000 else (int(mb), "MB") if kb > 1000 else (int(kb), "KB")

def save_file(form_file, post, post_type):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_file.filename)
    fn = random_hex + f_ext
    path = os.path.join(current_app.root_path, 'uploads', fn)
    form_file.save(path)
    if post_type == 'material':
        upload = File(filename=fn, filepath=path, filetype=f_ext, files_material=post)
    elif post_type == 'meeting':
        upload = File(filename=fn, filepath=path, filetype=f_ext, files_meeting=post)
    db.session.add(upload)

def get_publishers(level):
    if level == 'elementary':
        return [('0', 'Select a textbook'), ('Daegyo', 'Daegyo'), ('Cheonjae', 'Cheonjae'), ('YBM KIM', 'YBM Kim'), ('YBM Choi', 'YBM Choi'), ('Dong-A', 'Dong-A')]
    elif level == 'middle':
        return [('0', 'Select a textbook'), ('1', 'Dong-A Lee'), ('2', 'Dong-A Kim'), ('3', 'YBM Kim'), ('4', 'YBM Choi'), ('5', 'Dong-A')]
    else:
        return
    
def get_grades(level):
    if level == 'elementary':
        return [('0', 'Select Grade'), ('1', '1st Grade'), ('2', '2nd Grade'), 
                ('3', '3rd Grade'), ('4', '4th Grade'), ('5', '5th Grade'), ('6', '6th Grade')]
    elif level == 'middle':
        return [('0', 'Select Grade'), ('1', '1st Grade'), ('2', '2nd Grade'), 
                ('3', '3rd Grade')]
    elif level == 'high':
        return [('0', 'Select Grade'), ('1', '1st Grade'), ('2', '2nd Grade'), 
                ('3', '3rd Grade')]
    elif level == 'question':
        return [('0', 'Select category'), ('classroom', 'Classroom'), ('visa', 'Visa'), 
                ('coteaching', 'Co-teachers'), ('epik', 'EPIK'), ('hagwon', 'Hagwon'), 
                ('new', 'New teachers'), ('accommodation', 'Accommodation'), ('contracts', 'Contracts'), ('other', 'Other'), ]
    else:
        return

def update_textbooks_db():
    file_path = os.path.join(current_app.root_path, 'textbooks.txt')
    with open(file_path, 'r') as f:
        lines = f.read().split('\n\n')  # split by empty lines, so each item in `lines` is a textbook

        for textbook_data in lines:
            textbook_lines = textbook_data.split('\n')  # split by newline to get individual lines
            level, grade, publisher = textbook_lines[0].split(',')  # split the first line by comma to get these values
            lesson_titles = textbook_lines[1:]  # the rest of the lines are lesson titles

            textbook = Textbook(level=level, grade=grade, publisher=publisher)
            db.session.add(textbook)
            db.session.flush()  # So that we get the id of the newly created textbook

            for title in lesson_titles:
                split_title = title.split(':', 1)[-1].strip()
                lesson = Lesson(title=split_title, textbook_id=textbook.id)
                db.session.add(lesson)
            
            db.session.commit()

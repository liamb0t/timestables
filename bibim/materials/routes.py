from flask import Blueprint, url_for, redirect, render_template, flash, request, jsonify, abort
from flask_login import current_user, login_required
from bibim import db
from bibim.materials.forms import CommentForm
from bibim.materials.forms import MaterialForm, SelectForm
from bibim.models import Material, Tag, Comment, Like, tags_table, Textbook, Notification, Post, Meeting
from bibim.materials.utils import update_textbooks_db, get_publishers, get_grades, save_file, get_file_size
from bibim.posts.utils import post_timestamp
from sqlalchemy import func
import datetime

materials = Blueprint('materials', __name__)

@materials.route("/update_textbooks")
@login_required
def update_textbooks():
    try:
        update_textbooks_db()
        return redirect(url_for('main.home'))
    except Exception as e:
        print('Error updating textbooks:', e)
        return redirect(url_for('main.home'))

@materials.route("/get_lessons/<string:level>/<string:grade>/<string:publisher>")
@login_required
def get_lesson_choices(level, grade, publisher):
    textbook = Textbook.query.filter_by(publisher=publisher, level=level, grade=grade).first()
    lesson_choices = None
    # If no textbook found, return an error response
    if textbook is not None:
        lesson_choices = [(lesson.id, lesson.title) for lesson in textbook.lessons]

    return jsonify({
        'lesson_choices': lesson_choices
    })

@materials.route("/materials/<string:level>", methods=['GET', 'POST'])
def load_materials(level):
    page = request.args.get('page', 1, type=int)
    materials = Material.query.filter_by(level=level)
    form = SelectForm()
    publishers = Textbook.query.with_entities(Textbook.publisher).filter(Textbook.level == level).distinct().all()
    form.publisher.choices = ['Textbook', 'All'] + [publisher[0] for publisher in publishers]
    form.grade.choices = get_grades(level)
    
    if form.validate_on_submit():
        filter = request.args.get('f', 1, type=str)
        grade = form.grade.data
        publisher = form.publisher.data
        lesson = form.lesson.data
        material_type = form.type.data

        if grade != 'All' and grade != '0':
            materials = materials.filter_by(grade=grade)
        if publisher != 'All' and publisher != 'Textbook':
            tag = Tag.query.filter_by(tagname=publisher).first()
            if tag:
                materials = materials.filter(Material.material_tag.contains(tag))
            else:
                materials = materials.filter_by(grade=999)
        if lesson != 'All' and lesson != 'Lesson':
            materials = materials.filter_by(lesson_id=lesson)
        if material_type != 'Any' and material_type != 'Material Type':
            tag = Tag.query.filter_by(tagname=material_type).first()
            if tag:
                materials = materials.filter(Material.material_tag.contains(tag))
            else:
                materials = materials.filter_by(grade=999)
        if filter:
            if filter == 'new':
                materials = materials.order_by(Material.date_posted.desc())
            elif filter == 'old':
                materials = materials.order_by(Material.date_posted.asc())
            elif filter == 'comments':
                materials = materials.join(Material.comments, isouter=True)\
                            .group_by(Material)\
                            .order_by(func.count(Comment.id).desc())
            elif filter == 'likes':
                materials = materials.join(Material.likes, isouter=True)\
                            .group_by(Material)\
                            .order_by(func.count(Like.id).desc())
            elif filter == 'liked':
                materials = materials.join(Material.likes, isouter=True)\
                            .group_by(Material).filter(Like.user_id==current_user.id)\
                            .order_by(func.count(Comment.id).desc())
        else:
            print(form.errors)
    
    materials = materials.order_by(Material.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('materials.html', materials=materials, level=level, form=form, post_timestamp=post_timestamp)


@materials.route("/materials/liked", methods=['GET', 'POST'])
def liked_materials():
    page = request.args.get('page', 1, type=int)
    materials = Material.query.join(Material.likes, isouter=True)\
                        .group_by(Material).filter(Like.user_id==current_user.id, Material.level!='question', Material.level!='community')\
                        .order_by(Like.date_created.desc()).paginate(page=page, per_page=10)
    return render_template('liked_materials.html', materials=materials, post_timestamp=post_timestamp)


@materials.route("/material/<int:material_id>", methods=["POST", "GET"])
@login_required
def material(material_id):
    comment_form = CommentForm()
    material = Material.query.get_or_404(material_id)
    comments = Comment.query.filter_by(material_id=material_id).filter_by(parent=None).order_by(Comment.date_posted.asc())
    return render_template('material.html', material=material, comment_form=comment_form, 
                            get_file_size=get_file_size, post_timestamp=post_timestamp, likes=len(material.likes),
                            comments=comments)

@materials.route("/material/<int:material_id>/comment", methods=["POST"])
@login_required
def material_comment(material_id):
    data = request.get_json()
    content = data["textAreaData"]
    parent_id = data["parent_id"]
    material = Material.query.get(material_id)
    comment = Comment(content=content, material=material, commenter=current_user)
    if parent_id:
        parent_comment = Comment.query.filter_by(id=parent_id).first()
        if parent_comment:
            comment.parent = parent_comment
    comment.save()
    if material.creator != current_user and not comment.parent:
        n = Notification(name='material_comment', comment_id=comment.id, user_id=material.user_id, material_id=material.id)
        db.session.add(n)
        db.session.commit()
    if material.creator != current_user and comment.parent:
        n = Notification(name='reply', comment_id=comment.id, user_id=comment.parent.id, material_id=material.id)
        db.session.add(n)
        db.session.commit()
    return jsonify({
        'content': comment.content,
        'date_posted': post_timestamp(comment.date_posted),
        'author': current_user.username,
        'parent': parent_comment.commenter.username if parent_id else None, 
        'pic': current_user.image_file,
    })

@materials.route("/materials/new/<string:level>", methods=['GET','POST'])
@login_required
def create_material(level):
    form = MaterialForm(level=level)
    publishers = Textbook.query.with_entities(Textbook.publisher).filter(Textbook.level == level).distinct().all()
    form.publisher.choices = [publisher[0] for publisher in publishers]
    form.grade.choices = get_grades(level)
    del form.grade.choices[1]
    if form.validate_on_submit():
        tagnames = [form.publisher.data, form.material_type.data]
        material = Material(title=form.title.data, level=level, grade=form.grade.data, 
                            content=request.form.get('ckeditor'), creator=current_user)
        if level == 'question' or level == 'community':
            material.section = form.grade.data
        if form.lesson.data:
            material.lesson_id = form.lesson.data
        for tagname in tagnames:
            if tagname is not None:
                tag = Tag.query.filter_by(tagname=tagname).first()
                if not tag:
                    tag = Tag(tagname=tagname)
                material.tags.append(tag)
        db.session.add(material)
        if form.files.data:
            for file in form.files.data:
                if file.filename != '':
                    save_file(file, material, 'material')
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('materials.material', material_id=material.id))
    else:
        print(form.errors)
    return render_template('create_material.html', title='New Material', form=form, level=level, legend=level)

@materials.route("/material/edit/<int:material_id>", methods=['GET','POST'])
@login_required
def edit_material(material_id):
    material = Material.query.filter_by(id=material_id).first()
    if material.creator != current_user:
        abort(403)
    form = MaterialForm(obj=material)
    form.publisher.choices = get_publishers(material.level)
    form.grade.choices = get_grades(material.level)
    if form.validate_on_submit():
        tagnames = [form.publisher.data, form.lesson.data, form.material_type.data]
        material.title = form.title.data
        material.content = request.form.get('ckeditor')
        material.grade = form.grade.data 
        material.tags = []
        for tagname in tagnames:
            if tagname is not None and tagname not in material.tags:
                tag = Tag.query.filter_by(tagname=tagname).first()
                if not tag:
                    tag = Tag(tagname=tagname)
                material.tags.append(tag)   
        if form.files.data:
            for file in form.files.data:
                if file.filename != '':
                    save_file(file, material, 'material')
        db.session.commit()
        flash('Your post has been succesfully updated!', 'success')
        return redirect(url_for('materials.material', material_id=material.id))
    elif request.method == 'GET':
        form.publisher.choices = get_publishers(material.level)
        form.grade.choices = get_grades(material.level)
        
        for t in material.tags:
            print(t.tagname)
            if t.tagname in ['Daegyo', 'Cheonjae']:
                form.publisher.data = t.tagname
            elif t.tagname in ['Lesson1 ']:
                form.lesson.data = t.tagname
            elif t.tagname in ['Writing game', 'Bomb Game', 'Reading game']:
                form.material_type.data = t.tagname
    return render_template('edit_material.html', title='Edit Material', form=form, level=material.level, legend=material.level, material=material)

@materials.route("/like-material/<int:material_id>")
@login_required
def like_material(material_id):
    material = Material.query.filter_by(id=material_id).first_or_404()
    if current_user.has_liked_material(material):
        current_user.unlike_material(material)
    else:
        current_user.like_material(material)
    return jsonify({
        'liked': current_user.has_liked_material(material)
    })

@materials.route("/material/<int:material_id>/delete", methods=['POST', 'GET'])
@login_required
def delete_material(material_id):
    material = Material.query.get_or_404(material_id)
    level = material.level
    if material.creator != current_user:
        abort(403)

    tags = db.session.query(tags_table).filter_by(material_id=material.id).all()
    for tag in tags:
        db.session.execute(tags_table.delete().where(tags_table.c.tag_id==tag[0]).where(tags_table.c.material_id==tag[1]))

    db.session.commit()
    db.session.delete(material)
    db.session.commit()
    flash('Your material has been deleted!', 'success')
    return redirect(url_for('materials.load_materials', level=level))


@materials.route('/questions', methods=["POST", "GET"])
def questions():
    page = request.args.get('page', 1, type=int)
    type = request.args.get('type', '')
    questions = Material.query.filter_by(level='question')
    current_datetime = datetime.datetime.utcnow()
    popular_posts = Post.query.join(Post.likes, isouter=True)\
                            .group_by(Post)\
                            .order_by(func.count(Like.id).desc()).limit(5)
    popular_materials = Material.query.join(Material.likes, isouter=True)\
                            .group_by(Material).filter(Material.level != 'question')\
                            .order_by(func.count(Like.id).desc()).limit(5)
    upcoming_meetings =  Meeting.query.filter(Meeting.start_date >= current_datetime.date(),).all()
    recent_questions = Material.query.filter_by(level='question').limit(5)
    if type:
            questions = Material.query.filter_by(level='question', section=type)
    questions = questions.order_by(Material.date_posted.desc()).paginate(page=page, per_page=15)
    return render_template('questions.html', questions=questions, post_timestamp=post_timestamp,
                           popular_posts=popular_posts, popular_materials=popular_materials, upcoming_meetings=upcoming_meetings,
                           recent_questions=recent_questions)


@materials.route('/community', methods=["POST", "GET"])
def forum(): 
    page = request.args.get('page', 1, type=int)
    board = request.args.get('b', '')
    if board:
        posts = Material.query.filter_by(level='community', section=board).order_by(Material.date_posted.desc()).paginate(page=page, per_page=15)
    else:
        posts = Material.query.filter_by(level='community').order_by(Material.date_posted.desc()).paginate(page=page, per_page=15)
    return render_template('forum.html', posts=posts, section=board, post_timestamp=post_timestamp)
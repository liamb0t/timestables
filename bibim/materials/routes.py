import os 
from flask import Blueprint, url_for, redirect, render_template, flash, request, jsonify
from flask_login import current_user, login_required
from bibim import db
from bibim.materials.forms import CommentForm
from bibim.materials.forms import MaterialForm, SelectForm
from bibim.models import Material, File, Tag, Comment
from werkzeug.utils import secure_filename
from bibim.materials.utils import textbooks_elem, get_publishers, get_grades, save_file, get_file_size
from bibim.posts.utils import post_timestamp

materials = Blueprint('materials', __name__)

@materials.route("/get_lessons/<string:level>/<int:grade>/<string:publisher>")
@login_required
def get_lesson_choices(level, grade, publisher):    
    lesson_choices = textbooks_elem[publisher][str(grade)]
    formatted_lesson_choices = [(key, value) for key, value in lesson_choices.items()]
    
    return jsonify({
        'lesson_choices': formatted_lesson_choices
    })

@materials.route("/materials/<string:level>", methods=['GET', 'POST'])
def load_materials(level):
    page = request.args.get('page', 1, type=int)
    grade = request.args.get('grade', type=int)
    materials = Material.query.filter_by(level=level)
    if grade:
        materials = materials.filter_by(grade=grade)
    form = SelectForm()
    if form.validate_on_submit():
        publisher = form.publisher.data
        lesson = form.lesson.data
        material_type = form.type.data
        if publisher != 'All':
            tag = Tag.query.filter_by(tagname=publisher).first()
            if tag:
                materials = materials.filter(Material.material_tag.contains(tag))
        if lesson != 'All':
            tag = Tag.query.filter_by(tagname=lesson).first()
            if tag:
                materials = materials.filter(Material.material_tag.contains(tag))
        if material_type != 'Any':
            tag = Tag.query.filter_by(tagname=material_type).first()
            if tag:
                materials = materials.filter(Material.material_tag.contains(tag))
    materials = materials.order_by(Material.date_posted.desc()).paginate(page=page, per_page=15)
    return render_template('materials.html', materials=materials, level=level, form=form, post_timestamp=post_timestamp)

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
    if material.creator != current_user:
        material.creator.add_notification('material_comment', comment.id)
    return jsonify({
        'content': comment.content,
        'date_posted': post_timestamp(comment.date_posted),
        'author': current_user.username,
        'parent': parent_comment.commenter.username if parent_id else None
    })

@materials.route("/materials/new/<string:level>", methods=['GET','POST'])
@login_required
def create_material(level):
    form = MaterialForm(level=level)
    form.publisher.choices = get_publishers(level)
    form.grade.choices = get_grades(level)
    if form.validate_on_submit():
        tagnames = [form.publisher.data, form.lesson.data, form.material_type.data]
        material = Material(title=form.title.data, level=level, grade=form.grade.data, 
                            content=form.content.data, creator=current_user)
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
                    save_file(file, material)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('materials.material', material_id=material.id))
    return render_template('create_material.html', title='New Material', form=form, level=level, legend=level)

@materials.route("/like-material/<int:material_id>")
@login_required
def like_material(material_id):
    material = Material.query.filter_by(id=material_id).first_or_404()
    if current_user.has_liked_material(material):
        current_user.unlike_material(material)  
        db.session.commit()
    else:
        like = current_user.like_material(material)
        db.session.commit()
        if material.creator != current_user:
            material.author.add_notification('material_like', like.id)
    return jsonify({
        'liked': current_user.has_liked_material(material)
    })

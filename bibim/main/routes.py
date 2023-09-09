from flask import Blueprint, redirect, render_template, flash, url_for, request, send_file, jsonify, abort
from flask_login import current_user, login_user, logout_user, login_required
from bibim.models import Post, User, Material, File, Comment, Notification, Like, Meeting
from bibim.main.forms import LoginForm, RegistrationForm, ResetPasswordForm, RequestResetForm
from bibim.main.utils import send_reset_email, prompts, send_verification_email
from bibim.posts.forms import PostForm, EditForm
from bibim.posts.utils import post_timestamp
from bibim import bcrpyt, db
import datetime
from sqlalchemy import or_, func
from random import choice
import zipfile
import io
import os 
import bleach

main = Blueprint('main', __name__)

@main.route("/search", methods=['GET', 'POST'])
def search():
    search_query = request.args.get('q', '')
    type = request.args.get('type', '')
    results = None
    if type:
        if type == 'materials':
            results = Material.query.filter(or_(Material.title.ilike(f'%{search_query}%'),
                            Material.content.ilike(f'%{search_query}%'))).filter(Material.level != 'question').all()
        if type == 'posts' and not results:
            results = Post.query.filter(Post.content.ilike(f'%{search_query}%')).all()
        if type == 'users':
            results = User.query.filter(User.username.ilike(f'%{search_query}%')).all()
        if type == 'meetings':
            results = Meeting.query.filter(or_(Meeting.title.ilike(f'%{search_query}%'),
                            Meeting.content.ilike(f'%{search_query}%'))).all()
        if type == 'questions':
            results = Material.query.filter_by(level='question').filter(or_(Material.title.ilike(f'%{search_query}%'),
                            Material.content.ilike(f'%{search_query}%'))).all()
        if type == 'comments':
            results = Comment.query.filter(Comment.content.ilike(f'%{search_query}%')).all()
    else:
        results = Post.query.filter(Post.content.ilike(f'%{search_query}%')).all()
    return render_template('search.html', results=results, query=search_query, type=type if type else None,
                           post_timestamp=post_timestamp)

@main.route("/")
def landing():
    return render_template('landing_page.html')


@main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and current_user.verified:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrpyt.check_password_hash(user.password, form.password.data):
            if user.verified:
                login_user(user)
                return redirect(url_for('main.home'))
            else:
                flash('Please confirm your email address to login.', 'danger')
                return redirect(url_for('main.login'))  
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)


@main.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated and current_user.verified:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrpyt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        send_verification_email(user)
        flash(f'An email has been sent with instructions to confirm your email address.', 'info')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)


@main.route("/reset_password", methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('main.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@main.route("/reset_password/<token>", methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('main.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrpyt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        flash(f'Your password has been reset!', 'success')
        return redirect(url_for('main.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

@main.route('/confirm_email/<token>')
def confirm_email(token):
    user = User.verify_email_token(token)
    if user is None:
        flash('The confirmation link is invalid or has expired.', 'danger')
    else:
        user.verified = True
        db.session.commit()
        flash('Your email has been confirmed. You can now log in!', 'success')
    return redirect(url_for('main.login'))

@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.landing'))
 
@main.route("/home", methods=["POST", "GET"])
@login_required
def home():
    current_datetime = datetime.datetime.utcnow()
    post_form = PostForm()
    edit_form = EditForm()
    placeholder =  choice(prompts)
    if not current_user.is_anonymous:
        post_form.content.render_kw['placeholder'] = f"{current_user.username}, {placeholder[0].lower()}{placeholder[1:]}"
    else:
        post_form.content.render_kw['placeholder'] = placeholder
    # code for announcement bar
    popular_posts = Post.query.join(Post.likes, isouter=True)\
                            .group_by(Post)\
                            .order_by(func.count(Like.id).desc()).limit(5)
    popular_materials = Material.query.join(Material.likes, isouter=True)\
                            .group_by(Material).filter(Material.level != 'question')\
                            .order_by(func.count(Like.id).desc()).limit(5)
    upcoming_meetings =  Meeting.query.filter(Meeting.start_date >= current_datetime.date(),).all()
    recent_questions = Material.query.filter_by(level='question').limit(5)
    if post_form.validate_on_submit():
        post_content = post_form.content.data
        linkified_content = bleach.linkify(post_content)
        post = Post(content=linkified_content, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('home.html', post_form=post_form, edit_form=edit_form, popular_posts=popular_posts, 
                           popular_materials=popular_materials, timestamper=post_timestamp, 
                           upcoming_meetings=upcoming_meetings, recent_questions=recent_questions, type=type)

@main.route("/download/<int:file_id>", methods=["GET"])
@login_required
def download(file_id):
    file = File.query.get(file_id)
    if file:
        return send_file(file.filepath, as_attachment=True)
    else:
        return 'File not found'
    
@main.route("/download_all/<int:material_id>", methods=["GET"])
def download_all(material_id):
    material = Material.query.get(material_id)
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zipf:
        for file in material.files:
            file_name = os.path.basename(file.filepath)
            zipf.write(file.filepath, file_name)

    memory_file.seek(0)

    return send_file(memory_file, as_attachment=True, download_name=f"{material.title}.zip")

@main.route("/like-comment/<int:comment_id>")
@login_required
def like_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first_or_404()
    if current_user.has_liked_comment(comment):
        current_user.unlike_comment(comment)  
        db.session.commit()
    else:
        like = current_user.like_comment(comment)
        db.session.commit()
        if current_user != comment.commenter:
            n = Notification(name='comment_like', like_id=like.id, user_id=comment.commenter.id, comment_id=comment.id)
            db.session.add(n)
            db.session.commit()
    return jsonify({
        'liked': current_user.has_liked_comment(comment)
    })


@main.route("/comment/delete/<int:comment_id>", methods=["POST"])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first_or_404()
    if comment.commenter != current_user:
        abort(403)
    for n in comment.notifications:
        if n:   
            db.session.delete(n)
            db.session.commit()
    comment.deleted = True
    db.session.commit()
    return jsonify({
        'message': 'Your comment has been deleted.'
    })


@main.route("/open_notification/<int:id>", methods=["POST"])
@login_required
def open_notification(id):
    notification = Notification.query.filter_by(id=id).first_or_404()
    notification.read = True
    db.session.commit()
    return jsonify({
        'success': 'nice'
    }) 


@main.route("/get_messages/<int:user_id>")
@login_required
def get_messages(user_id):
    messages = current_user.get_messages(user_id)
    return jsonify({
        'conversation': [m.serialize() for m in messages]
    })
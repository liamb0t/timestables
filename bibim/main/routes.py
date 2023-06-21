from flask import Blueprint, redirect, render_template, flash, url_for, request, send_file, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from bibim.models import Post, User, Material, File, Comment, Notification
from bibim.main.forms import LoginForm, RegistrationForm, SearchForm, ResetPasswordForm, RequestResetForm
from bibim.main.utils import send_reset_email
from bibim.posts.forms import PostForm
from bibim import bcrpyt, db, app
import datetime
from sqlalchemy import or_
from random import choice
import zipfile
import io
import os 

main = Blueprint('main', __name__)

prompts = [
    "Share a recent lesson plan you've used in your classroom and how it went.",
    "Have you tried any new teaching strategies or techniques lately? Tell us about it.",
    "What are some of the biggest challenges you face as an English teacher in Korea?",
    "How do you incorporate Korean culture into your English lessons?",
    "Share a funny or interesting story from your time teaching in Korea.",
    "How do you keep your students motivated to learn English?",
    "What are your favorite resources for teaching English as a foreign language?",
    "Have you attended any professional development workshops or conferences recently? What did you learn?",
    "How do you use technology in your English lessons?",
    "What advice would you give to new English teachers in Korea?"
]

@app.context_processor
def inject():
    return dict(search_form=SearchForm())

@main.route("/search", methods=['GET', 'POST'])
def search():
    search_query = request.form.get('query')
    posts = Material.query.filter(or_(Material.title.ilike(f'%{search_query}%'),
                              Material.content.ilike(f'%{search_query}%'))).all()
    return render_template('search.html', posts=posts)

@main.route("/")
def landing():
    return render_template('landing_page.html')

@main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrpyt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            nextpage = request.args.get('next')
            flash('Login succesful', 'success')
            return redirect(url_for(nextpage)) if nextpage else redirect(url_for('main.home'))
        else:
            flash('Login unsuccesful. Please check your email and password details.')
       
   
    return render_template('login.html', form=form)


@main.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrpyt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Account successfully created for {form.username.data}!', 'success')
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



@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.landing'))
 
@main.route("/home", methods=["POST", "GET"])
@login_required
def home():
    post_form = PostForm()
    placeholder =  choice(prompts)
    if not current_user.is_anonymous:
        post_form.content.render_kw['placeholder'] = f"{current_user.username}, {placeholder[0].lower()}{placeholder[1:]}"
    else:
        post_form.content.render_kw['placeholder'] = placeholder
    # code for announcement bar
    today = datetime.date.today()
    popular_posts = Post.query.filter(db.func.date(Post.date_posted) == today).order_by(Post.date_posted.desc()).limit(5).all()
    if post_form.validate_on_submit():
        post = Post(content=post_form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('home.html', post_form=post_form, popular_posts=popular_posts)

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
            comment.commenter.add_notification('comment_like', like.id)
    return jsonify({
        'liked': current_user.has_liked_comment(comment)
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
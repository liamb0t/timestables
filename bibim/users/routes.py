from flask import Blueprint, render_template, url_for, flash, redirect, request, jsonify
from flask_login import current_user, login_required
from bibim import db
from bibim.users.forms import UpdateAccountForm
from bibim.posts.forms import FollowForm
from bibim.models import User, Post, Material, Comment
from bibim.users.utils import date_member_since, save_picture

users = Blueprint('users', __name__)

@users.route("/follow/<string:username>", methods=['GET','POST'])
@login_required
def follow(username):
    form = FollowForm()
    if form.validate_on_submit:
        user = User.query.filter_by(username=username).first()
        if user == current_user:
            return redirect(url_for('home'))
        current_user.following.append(user)
        db.session.commit()
        return redirect(url_for('users.user_profile', username=username))

@users.route("/unfollow/<string:username>", methods=['GET', 'POST'])
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return redirect(url_for('home'))
    if user == current_user:
        return redirect(url_for('home'))
    current_user.following.remove(user)
    db.session.commit()
    return redirect(url_for('users.user_profile', username=username))

@users.route("/users/<string:username>")
def user_profile(username):
    form = FollowForm()
    user = User.query.filter_by(username=username).first_or_404()
    followers = user.followers.all()
    following = user.following.all()
    followers_count = len(user.followers.all())
    following_count = len(user.following.all())
    member_time = date_member_since(user.date_joined)
    return render_template('user_profile.html', user=user, form=form, followers_count=followers_count, 
                           following_count=following_count, member_time=member_time, 
                           followers=followers, following=following)

@users.route("/users/<string:username>")
def edit_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('edit_profile.html', user=user)


@users.route("/users/<string:username>/<string:contents>")
def user_contents(username, contents):
    if contents == 'posts':
        contents = Post.query.filter_by(author=username).all()
    elif contents == 'materials':
        contents = Material.query.filter_by(creator=username).all()
    elif contents == 'comments':
        contents = Comment.query.filter_by(commenter=username).all()
    else:
        return redirect(url_for('main.home'))
    return jsonify({
        'contents': contents,
    })

@users.route("/users/<string:username>/followers")
def followers(username):
    user = User.query.filter_by(username=username).first_or_404()
    followers = user.followers.all()
    return render_template('followers.html', followers=followers)

@users.route("/users/<string:username>/following")
def following(username):
    user = User.query.filter_by(username=username).first_or_404()
    following = user.following.all()
    return render_template('followers.html', following=following)

@users.route("/users")
def display_users():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    order_by = User.karma.desc()
    users = User.query.order_by(order_by).paginate(page=page, per_page=per_page)

    return render_template('users.html', users=users, datemember=date_member_since)


@users.route("/account", methods=['GET', 'POST'])
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about = form.about.data
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.user_profile', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about.data = current_user.about
    return render_template('account.html', form=form)
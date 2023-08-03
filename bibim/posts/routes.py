from flask import Blueprint, url_for, redirect, request, jsonify, flash, render_template, abort
from flask_login import current_user, login_required
from bibim import db
from bibim.posts.forms import PostForm, MessageForm, EditForm
from bibim.models import Post, Comment, User, Message, Notification
from bibim.materials.forms import CommentForm
import datetime
from bibim.posts.utils import post_timestamp

posts = Blueprint('posts', __name__)

@posts.route("/posts/<int:page>", methods=["POST", "GET"])
def load_posts(page):
    posts_per_page = 5
    offset = (page - 1) * posts_per_page
    posts = Post.query.order_by(Post.date_posted.desc()).offset(offset).limit(posts_per_page).all()
    return jsonify({
        'posts':  [post.serialize() for post in posts]
    })

@posts.route("/like-post/<int:post_id>")
@login_required
def like_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if current_user.has_liked_post(post):
        current_user.unlike_post(post)
    else:
        current_user.like_post(post)
    return jsonify({
        'liked': current_user.has_liked_post(post)
    })

@posts.route("/post/<int:post_id>/comment", methods=["POST"])
@login_required
def post_comment(post_id):
    data = request.get_json()
    content = data["textAreaData"]
    parent_id = data["parent_id"]
    post = Post.query.get(post_id)
    comment = Comment(content=content, post=post, commenter=current_user)
    if parent_id:
        parent_comment = Comment.query.filter_by(id=parent_id).first()
        if parent_comment:
            comment.parent = parent_comment
    comment.save()
    if parent_id:
        n = Notification(name='reply', user_id=comment.parent.user_id, comment_id=comment.id, post_id=post.id)
        db.session.add(n)
    if post.author != current_user:
        n = Notification(name='post_comment', user_id=post.user_id, comment_id=comment.id, post_id=post.id)
        db.session.add(n)
    db.session.commit()
    return jsonify({
        'id': comment.id,
        'content': comment.content,
        'date_posted': post_timestamp(comment.date_posted),
        'author': current_user.username,
        'parent': parent_comment.commenter.username if parent_id else None,
        'pic': current_user.image_file,
    })


@posts.route("/inbox", methods=["GET", "POST"])
@login_required
def inbox():
    form = MessageForm()
    user_id = request.args.get('user')
    conversations = current_user.get_conversations()
    user = None
    if user_id:
        user = User.query.filter_by(id=user_id).first_or_404()
        messages = current_user.get_messages(user_id)
    else:
        messages = None

    if request.method == 'POST':
        user_id = request.args.get('user')
        user = User.query.filter_by(id=user_id).first_or_404()

        if form.validate_on_submit():
            new_messages_count = user.new_messages()
            msg = Message(author=current_user, recipient=user,
                        body=form.body.data)
            user.add_notification('unread_message_count', msg.id, new_messages_count + 1, )
            db.session.add(msg)
            db.session.commit()
            flash(('Your message has been sent.'), 'success')
            return redirect(url_for('posts.inbox', user=user_id))
    
    return render_template('inbox.html', messages=messages, conversations=conversations, form=form, 
                           user=user if user else None, post_timestamp=post_timestamp)


@posts.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.order_by(Notification.timestamp.desc())
    return jsonify({
        'notifications': [n.serialize() for n in notifications if n.name != 'unread_message_count'],
        'unread_message_count': current_user.new_messages(),
    })

@posts.route('/message/<int:msg_id>', methods=["POST"])
@login_required
def message(msg_id):
    message = Message.query.filter_by(id=msg_id).first()
    message.read = True
    db.session.commit()
    return jsonify({
        'success': 'message read'
    })

@posts.route('/post/<int:post_id>', methods=["POST", "GET"])
def post(post_id):
    form = CommentForm()
    post = Post.query.filter_by(id=post_id).first_or_404()
    if post:
        comments = Comment.query.filter_by(post_id=post.id).filter_by(parent=None).order_by(Comment.date_posted.asc())
    return render_template('post.html', post=post, comments=comments, post_timestamp=post_timestamp,
                           form=form)

@posts.route('/post/<int:post_id>/edit', methods=["POST", "GET"])
def edit_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if post.author != current_user:
        abort(403)
    form = EditForm()
    if form.validate_on_submit():
        post.content = form.editor_content.data
        db.session.commit()
        flash('Your post has been sucessfully updated!', 'success')
    return redirect(url_for('main.home'))

@posts.route('/post/<int:post_id>/delete', methods=["POST", "GET"])
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been removed.', 'success')
    return redirect(url_for('main.home'))



from flask import Blueprint, url_for, redirect, request, jsonify, render_template, flash
from flask_login import current_user, login_required
from bibim import db
from bibim.models import Comment, Meeting, Like, Notification, Classified
from bibim.marketplace.forms import CommentForm, AdForm, FilterForm
from bibim.posts.utils import post_timestamp
from bibim.materials.utils import save_file, get_file_size
from sqlalchemy import func, or_

marketplace = Blueprint('marketplace', __name__)

@marketplace.route("/marketplace", methods=['GET', 'POST'])
def load_ads():
    form = FilterForm()
    page = request.args.get('page', 1, type=int)
    classifieds = Classified.query
    if form.validate_on_submit():
        filter = request.args.get('f', 1, type=str)
        if form.type.data:
            meeting_type = form.type.data
            if meeting_type != 'All' and meeting_type != 'Meeting Type':
                classifieds = classifieds.filter_by(tag=meeting_type)
        if filter:
            if filter == 'new':
                classifieds = classifieds.order_by(Classified.date_posted.desc())
            elif filter == 'old':
                classifieds = classifieds.order_by(Classified.date_posted.asc())
            elif filter == 'comments':
                classifieds = classifieds.join(Classified.comments, isouter=True)\
                            .group_by(Classified)\
                            .order_by(func.count(Comment.id).desc())
            elif filter == 'likes':
                classifieds = classifieds.join(Classified.likes, isouter=True)\
                            .group_by(Classified)\
                            .order_by(func.count(Like.id).desc())
        if form.search.data:
            query = form.search.data
            classifieds = Classified.query.filter(or_(Classified.title.ilike(f'%{query}%'),
                        Classified.address.ilike(f'%{query}%')))
    classifieds = classifieds.paginate(page=page, per_page=15)
    return render_template('marketplace.html', classifieds=classifieds, form=form)

@marketplace.route("/marketplace/<int:ad_id>", methods=["POST", "GET"])
@login_required
def ad(ad_id):
    comment_form = CommentForm()
    ad = Classified.query.get_or_404(ad_id)
    comments = Comment.query.filter_by(classified_id=ad_id).filter_by(parent=None).order_by(Comment.date_posted.asc())
    return render_template('ad.html', ad=ad, comment_form=comment_form, 
                            get_file_size=get_file_size, post_timestamp=post_timestamp, likes=len(ad.likes),
                            comments=comments)

@marketplace.route("/marketplace/<int:ad_id>/comment", methods=["POST"])
@login_required
def ad_comment(ad_id):
    data = request.get_json()
    content = data["textAreaData"]
    parent_id = data["parent_id"]
    ad = Classified.query.get(ad_id)
    comment = Comment(content=content, ad=ad, commenter=current_user)
    if parent_id:
        parent_comment = Comment.query.filter_by(id=parent_id).first()
        if parent_comment:
            comment.parent = parent_comment

    comment.save()
    if ad.advertiser != current_user and not comment.parent:
        n = Notification(name='meeting_comment', comment_id=comment.id, user_id=ad.user_id, ad_id=ad.id)
        db.session.add(n)
        db.session.commit()
    elif ad.advertiser != current_user and comment.parent:
        n = Notification(name='reply', comment_id=comment.id, user_id=comment.parent.id, ad_id=ad.id)
        db.session.add(n)
        db.session.commit()
    return jsonify({
        'content': comment.content,
        'date_posted': post_timestamp(comment.date_posted),
        'author': current_user.username,
        'parent': parent_comment.commenter.username if parent_id else None
    })

@marketplace.route("/marketplace/new/", methods=['GET','POST'])
@login_required
def create_ad():
    form = AdForm()
    if form.validate_on_submit():
        ad = Classified(title=form.title.data, fee=form.fee.data, 
                            content=form.content.data, advertiser=current_user, 
                            tag=form.tag.data)
        db.session.add(ad)
        if form.files.data:
            for file in form.files.data:
                if file.filename != '':
                    save_file(file, ad, 'meeting')
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('marketplace.ad', ad_id=ad.id))
    else:
        print(form.errors)
    return render_template('create_ad.html', title='New meeting', form=form)

@marketplace.route("/like-ad/<int:ad_id>")
@login_required
def like_ad(ad_id):
    ad = Classified.query.filter_by(id=ad_id).first_or_404()
    if current_user.has_liked_ad(ad):
        current_user.unlike_ad(ad)  
        db.session.commit()
    else:
        like = current_user.like_ad(ad)
        db.session.commit()
        if ad.advertiser != current_user:
            n = Notification(name='ad_like', like_id=like.id, user_id=ad.user_id, ad_id=ad.id)
            db.session.add(n)
            db.session.commit()
    return jsonify({
        'liked': current_user.has_liked_ad(ad)
    })

@marketplace.route("/marketplace/edit/<int:ad_id>")
@login_required
def edit_ad(ad_id):
    ad = Classified.query.filter_by(id=ad_id).first_or_404()
    if current_user.has_liked_ad(ad):
        current_user.unlike_ad(ad)  
        db.session.commit()
    else:
        like = current_user.like_ad(ad)
        db.session.commit()
        if ad.advertiser != current_user:
            n = Notification(name='ad_like', like_id=like.id, user_id=ad.user_id, ad_id=ad.id)
            db.session.add(n)
            db.session.commit()
    return jsonify({
        'liked': current_user.has_liked_ad(ad)
    })


@marketplace.route("/marketplace/delete/<int:ad_id>")
@login_required
def delete_ad(ad_id):
    ad = Classified.query.filter_by(id=ad_id).first_or_404()
    if current_user.has_liked_ad(ad):
        current_user.unlike_ad(ad)  
        db.session.commit()
    else:
        like = current_user.like_ad(ad)
        db.session.commit()
        if ad.advertiser != current_user:
            n = Notification(name='ad_like', like_id=like.id, user_id=ad.user_id, ad_id=ad.id)
            db.session.add(n)
            db.session.commit()
    return jsonify({
        'liked': current_user.has_liked_ad(ad)
    })
from flask import Blueprint, url_for, redirect, request, jsonify, render_template, flash
from flask_login import current_user, login_required
from bibim import db
from bibim.models import Comment, Meeting, Like, Notification
from bibim.meetings.forms import CommentForm, MeetingForm, FilterForm
from bibim.posts.utils import post_timestamp
from bibim.materials.utils import save_file, get_file_size
from bibim.users.utils import save_picture
from sqlalchemy import func, or_

meetings = Blueprint('meetings', __name__)

@meetings.route("/meetings", methods=['GET', 'POST'])
def load_meetings():
    form = FilterForm()
    page = request.args.get('page', 1, type=int)
    meetings = Meeting.query
    if form.validate_on_submit():
        filter = request.args.get('f', 1, type=str)
        if form.type.data:
            meeting_type = form.type.data
            if meeting_type != 'All' and meeting_type != 'Meeting Type':
                meetings = meetings.filter_by(tag=meeting_type)
        if filter:
            if filter == 'new':
                meetings = meetings.order_by(Meeting.date_posted.desc())
            elif filter == 'old':
                meetings = meetings.order_by(Meeting.date_posted.asc())
            elif filter == 'comments':
                meetings = meetings.join(Meeting.comments, isouter=True)\
                            .group_by(Meeting)\
                            .order_by(func.count(Comment.id).desc())
            elif filter == 'likes':
                meetings = meetings.join(Meeting.likes, isouter=True)\
                            .group_by(Meeting)\
                            .order_by(func.count(Like.id).desc())
        if form.search.data:
            query = form.search.data
            meetings = Meeting.query.filter(or_(Meeting.title.ilike(f'%{query}%'),
                        Meeting.address.ilike(f'%{query}%')))
    meetings = meetings.paginate(page=page, per_page=15)
    return render_template('meetings.html', meetings=meetings, form=form)
                
   
    
    meetings = Meeting.query.order_by(Meeting.date_posted.desc()).paginate(page=page, per_page=15)
    return render_template('meetings.html', meetings=meetings, post_timestamp=post_timestamp, form=form, filter_form=search_form)

@meetings.route("/meeting/<int:meeting_id>", methods=["POST", "GET"])
@login_required
def meeting(meeting_id):
    comment_form = CommentForm()
    meeting = Meeting.query.get_or_404(meeting_id)
    comments = Comment.query.filter_by(meeting_id=meeting_id).filter_by(parent=None).order_by(Comment.date_posted.asc())
    return render_template('meeting.html', meeting=meeting, comment_form=comment_form, 
                            get_file_size=get_file_size, post_timestamp=post_timestamp, likes=len(meeting.likes),
                            comments=comments)

@meetings.route("/meeting/<int:meeting_id>/comment", methods=["POST"])
@login_required
def meeting_comment(meeting_id):
    data = request.get_json()
    content = data["textAreaData"]
    parent_id = data["parent_id"]
    meeting = Meeting.query.get(meeting_id)
    comment = Comment(content=content, meeting=meeting, commenter=current_user)
    if parent_id:
        parent_comment = Comment.query.filter_by(id=parent_id).first()
        if parent_comment:
            comment.parent = parent_comment

    comment.save()
    if meeting.organizer != current_user and not comment.parent:
        n = Notification(name='meeting_comment', comment_id=comment.id, user_id=meeting.user_id, meeting_id=meeting.id)
        db.session.add(n)
        db.session.commit()
    elif meeting.organizer != current_user and comment.parent:
        n = Notification(name='reply', comment_id=comment.id, user_id=comment.parent.id, meeting_id=meeting.id)
        db.session.add(n)
        db.session.commit()
    return jsonify({
        'content': comment.content,
        'date_posted': post_timestamp(comment.date_posted),
        'author': current_user.username,
        'parent': parent_comment.commenter.username if parent_id else None
    })

@meetings.route("/meetings/new/", methods=['GET','POST'])
@login_required
def create_meeting():
    form = MeetingForm()
    if form.validate_on_submit():
        meeting = Meeting(title=form.title.data, fee=form.fee.data, capacity=form.capacity.data,
                            content=form.content.data, organizer=current_user, location=form.location.data, 
                            tag=form.tag.data, start_time=form.start_time.data, start_date=form.start_date.data,
                            lat=float(form.lat.data), lng=float(form.lng.data), address=form.address.data)
        if form.cover_pic.data:
            cover_pic = save_picture(form.cover_pic.data)
            meeting.cover_pic = cover_pic
        db.session.add(meeting) 
        if form.files.data:
            for file in form.files.data:
                if file.filename != '':
                    save_file(file, meeting, 'meeting')
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('meetings.meeting', meeting_id=meeting.id))
    else:
        print(form.errors)
    return render_template('create_meeting.html', title='New meeting', form=form)

@meetings.route("/like-meeting/<int:meeting_id>")
@login_required
def like_meeting(meeting_id):
    meeting = Meeting.query.filter_by(id=meeting_id).first_or_404()
    if current_user.has_liked_meeting(meeting):
        current_user.unlike_meeting(meeting)  
        db.session.commit()
    else:
        like = current_user.like_meeting(meeting)
        db.session.commit()
        if meeting.organizer != current_user:
            n = Notification(name='meeting_like', like_id=like.id, user_id=meeting.user_id, meeting_id=meeting.id)
            db.session.add(n)
            db.session.commit()
    return jsonify({
        'liked': current_user.has_liked_meeting(meeting)
    })

@meetings.route("/going/<int:meeting_id>", methods=["POST", "GET"])
@login_required
def going(meeting_id):
    meeting = Meeting.query.filter_by(id=meeting_id).first()
    is_attending = meeting.is_attending(current_user)
    if is_attending:
        meeting.remove(current_user)
    else:
        meeting.add(current_user)
    db.session.commit()
    return jsonify({
        'going': is_attending
    })

from flask import Blueprint, url_for, redirect, request, jsonify, render_template, flash
from flask_login import current_user, login_required
from bibim import db
from bibim.models import Post, Comment, Meeting, Tag
from bibim.meetings.forms import CommentForm, MeetingForm
from bibim.posts.utils import post_timestamp
from bibim.materials.utils import save_file, get_file_size

meetings = Blueprint('meetings', __name__)

@meetings.route("/meetings", methods=['GET', 'POST'])
def load_meetings():
    page = request.args.get('page', 1, type=int)
    meetings = Meeting.query.order_by(Meeting.date_posted.desc()).paginate(page=page, per_page=15)
    return render_template('meetings.html', meetings=meetings, post_timestamp=post_timestamp)

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
    meeting = meeting.query.get(meeting_id)
    comment = Comment(content=content, meeting=meeting, commenter=current_user)
    if parent_id:
        parent_comment = Comment.query.filter_by(id=parent_id).first()
        if parent_comment:
            comment.parent = parent_comment

    comment.save()
    if meeting.creator != current_user and not comment.parent:
        meeting.creator.add_notification('meeting_comment', comment.id)
    elif meeting.creator != current_user and comment.parent:
        meeting.creator.add_notification('comment_reply', comment.id)
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
                            tag=form.tag.data, time=form.time.data)
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
        if meeting.creator != current_user:
            meeting.author.add_notification('meeting_like', like.id)
    return jsonify({
        'liked': current_user.has_liked_meeting(meeting)
    })

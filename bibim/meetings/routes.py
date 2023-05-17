from flask import Blueprint, url_for, redirect, request, jsonify, render_template
from flask_login import current_user, login_required
from bibim import db
from bibim.posts.forms import PostForm
from bibim.models import Post, Comment

meetings = Blueprint('meetings', __name__)

@meetings.route("/meetings")
def load_meetings():
    return render_template('meetings.html')

@meetings.route("/meetings/new")
def new_meeting():
    return render_template('create_meeting.html')

from bibim import db, login_manager
from flask_login import UserMixin, current_user
from datetime import datetime
from bibim.posts.utils import post_timestamp
import json
from time import time

@login_manager.user_loader
def load_user(user_id):
    return User.query.get((int(user_id)))

follower = db.Table('follower',
                    db.Column('follower_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'), primary_key=True))

tags_table = db.Table('tags_table',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('material_id', db.Integer, db.ForeignKey('material.id'), primary_key=True))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    karma = db.Column(db.Integer, nullable=False, default=0)
    about = db.Column(db.String(120))
    last_message_read_time = db.Column(db.DateTime)
    
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='commenter', lazy=True)
    materials = db.relationship('Material', backref='creator')
    notifications = db.relationship('Notification', backref='user',
                                    lazy='dynamic')
    followers = db.relationship('User', secondary='follower', 
                                 primaryjoin=(id==follower.c.followed_id), 
                                 secondaryjoin=(id==follower.c.follower_id), 
                                 backref=db.backref('following', lazy='dynamic'), 
                                 lazy='dynamic')
    messages_sent = db.relationship('Message',
                                    foreign_keys='Message.sender_id',
                                    backref='author', lazy='dynamic')
    messages_received = db.relationship('Message',
                                        foreign_keys='Message.recipient_id',
                                        backref='recipient', lazy='dynamic')
    liked = db.relationship('Like', foreign_keys='Like.user_id', backref='user', lazy='dynamic')

    def like_post(self, post):
        like = Like(user_id=self.id, post_id=post.id)
        db.session.add(like)

    def unlike_post(self, post):
        Like.query.filter_by(
            user_id=self.id,
            post_id=post.id).delete()

    def has_liked_post(self, post):
        return Like.query.filter(
            Like.user_id == self.id,
            Like.post_id == post.id).count() > 0    
    
    def like_material(self, material):
        like = Like(user_id=self.id, material_id=material.id)
        db.session.add(like)

    def unlike_material(self, material):
        Like.query.filter_by(
            user_id=self.id,
            material_id=material.id).delete()

    def has_liked_material(self, material):
        return Like.query.filter(
            Like.user_id == self.id,
            Like.material_id == material.id).count() > 0   

    def like_comment(self, comment):
        like = Like(user_id=self.id, comment_id=comment.id)
        db.session.add(like)

    def unlike_comment(self, comment):
        Like.query.filter_by(
            user_id=self.id,
            comment_id=comment.id).delete()

    def has_liked_comment(self, comment):
        return Like.query.filter(
            Like.user_id == self.id,
            Like.comment_id == comment.id).count() > 0    
    
    def new_messages(self):
        print([msg.id for msg in Message.query.filter_by(recipient=self).filter(
            Message.read == False).all()])
        return Message.query.filter_by(recipient=self).filter(
            Message.read == False).count()
    
    def add_notification(self, name, data):
        self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json = json.dumps(data), user=self)
        db.session.add(n)
        return n
    
    def serialize(self):
        return({
            "username": self.username,
            "profile_pic": self.image_file,
            "followed": True if current_user in self.followers else False
        })

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    likes = db.relationship('Like', backref='post')
    comments = db.relationship('Comment', backref='post')

    def __repr__(self):
        return f"Post('{self.id}', '{self.date_posted}')"
    
    def serialize(self):
        payload = {
            "id": self.id,
            "author": self.author.username,
            "profile_pic": self.author.image_file,
            "date_posted": post_timestamp(self.date_posted),
            "content": self.content,
            "likes": len(self.likes),
            "likers": [User.query.filter_by(id=like.user_id).first().serialize() for like in self.likes],
            "comments": [comment.serialize() for comment in self.comments] if len(self.comments) > 0 else None,
        }
        
        if not current_user.is_anonymous:
            payload["liked"] = True if current_user.has_liked_post(self) else False
        return payload
    
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))

class Comment(db.Model):
    _N = 6

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(280))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    path = db.Column(db.Text, index=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'))
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'))

    likes = db.relationship('Like', backref='comment')
    replies = db.relationship(
        'Comment', backref=db.backref('parent', remote_side=[id]),
        lazy='dynamic'
    )

    def __repr__(self):
        return f"Comment('{self.id}', '{self.commenter.username}', '{self.parent}')"

    def likes_count(self):
        return len([likes for likes in self.likes])
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        prefix = self.parent.path if self.parent else ''
        self.path = f'{prefix}{self.id:0{self._N}d}'
        db.session.commit()

    def level(self):
        return len(self.path) // self._N - 1
    
    def get_replies(self):
        replies = Comment.query.filter(Comment.path.like(self.path + '%'), Comment.id != self.id).all()
        return replies

    def serialize(self):
        return {
            "id": self.id,
            "author": self.commenter.username,
            "content": self.content,
            "date_posted": post_timestamp(self.date_posted),
            "likes": self.likes,
            "replies": [reply.serialize() for reply in self.get_replies()],
            "likes_count": self.likes_count(),
        }

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String, nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    tags = db.relationship('Tag', secondary='tags_table', backref=db.backref('tag_materials', lazy='dynamic'), lazy='joined')
    comments = db.relationship('Comment', backref='material')
    files = db.relationship('File', backref='files_material', lazy=True)
    likes = db.relationship('Like', backref='material')
    
    def likes_count(self):
        return len([likes for likes in self.likes])

    def comments_count(self):
        return len([comment for comment in self.comments])

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tagname = db.Column(db.String(50), unique=True)

    material_id = db.Column(db.Integer, db.ForeignKey('material.id'))
    materials = db.relationship('Material', secondary='tags_table', 
                                backref=db.backref('material_tag', lazy='dynamic'))

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filetype = db.Column(db.String(50), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), nullable=False)

    def __repr__(self):
        return f"File('{self.filename}', '{self.file_type}')"

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='meeting')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    read = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"Message {self.body}"
    
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)

    def get_data(self):
        return json.loads(str(self.payload_json))
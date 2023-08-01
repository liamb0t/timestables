from sqlalchemy import or_
from bibim import db, login_manager
from flask_login import UserMixin, current_user
from flask import current_app
from datetime import datetime
from bibim.posts.utils import post_timestamp
import json
from time import time
from itsdangerous import URLSafeTimedSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get((int(user_id)))

follower = db.Table('follower',
                    db.Column('follower_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'), primary_key=True))

tags_table = db.Table('tags_table',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('material_id', db.Integer, db.ForeignKey('material.id'), primary_key=True))

going_table = db.Table('going_table',
                    db.Column('meeting_id', db.Integer, db.ForeignKey('meeting.id'), primary_key=True),
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True))

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
    last_seen = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='commenter', lazy=True)
    materials = db.relationship('Material', backref='creator')
    meetings = db.relationship('Meeting', backref='organizer')
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

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}, salt='reset-password-salt')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
           user_id = s.loads(token, salt='reset-password-salt')['user_id']
        except:
           return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    def like_post(self, post):
        like = Like(user_id=self.id, post_id=post.id)
        db.session.add(like)
        return like

    def unlike_post(self, post):
        Notification.query.filter_by(
            name='post_like',
            user_id=post.user_id,
            id=self.id).delete()
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
        return like

    def unlike_material(self, material):
        Notification.query.filter_by(
            name='material_like',
            user_id=self.id,
            id=self.id).delete()
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
        return like

    def unlike_comment(self, comment):
        Notification.query.filter_by(
            name='comment_like',
            user_id=self.id,
            id=self.id).delete()
        Like.query.filter_by(
            user_id=self.id,
            comment_id=comment.id).delete()

    def has_liked_comment(self, comment):
        return Like.query.filter(
            Like.user_id == self.id,
            Like.comment_id == comment.id).count() > 0    
    
    def new_messages(self):
        return Message.query.filter_by(recipient=self).filter(
            Message.read == False).count()
    
    def get_messages(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        return Message.query.filter(or_(
            (Message.author == user) & (Message.recipient == self),
            (Message.author == self) & (Message.recipient == user)
        )).order_by(Message.timestamp.asc()).all()
    
    def my_meetings(self):
        current_datetime = datetime.utcnow()
        going_meetings = Meeting.query.filter(
        Meeting.going.any(id=self.id),
        Meeting.start_date >= current_datetime.date(),
        Meeting.start_time >= current_datetime.time()
        ).all()
        return going_meetings

    def new_notifications(self):
        return Notification.query.filter_by(user_id=self.id).filter(
            Notification.read == False, Notification.name != 'unread_message_count').count()
    
    def add_notification(self, name, data, related_id):
        n = Notification(name=name, payload_json=json.dumps(data), user=self, related_id=related_id)
        db.session.add(n)
        db.session.commit()
        return n
    
    def active_since(self):
        return post_timestamp(self.last_seen)
    
    def get_conversations(self):
        contacts = (
            User.query
            .join(Message, or_(User.id == Message.sender_id, User.id == Message.recipient_id))
            .filter(or_(Message.sender_id == self.id, Message.recipient_id == self.id))
            .filter(User.id != self.id)  # Exclude the current user
            .order_by(Message.timestamp.desc())
            .distinct()
            .all()
        )
        return contacts
    
    def get_last_message_time(self):
        last_message = (
            Message.query
            .filter(or_(Message.sender_id == self.id, Message.recipient_id == self.id))
            .order_by(Message.timestamp.desc())
            .first()
        )
        if last_message:
            time_ago = post_timestamp(last_message.timestamp)
            return time_ago
        else:
            return None
        
    def get_last_message(self):
        last_message = (
            Message.query
            .filter(or_(Message.sender_id == self.id, Message.recipient_id == self.id))
            .order_by(Message.timestamp.desc())
            .first()
        )
        print('last', last_message)
        return last_message
    
    def serialize(self):
        return({
            "username": self.username,
            "pic": self.image_file,
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
    
    def likes_count(self):
        return len([like for like in self.likes])
    
    def comments_count(self):
        return len([comment for comment in self.comments])
    
    def serialize(self):
        payload = {
            "current_user": current_user.username,
            "id": self.id,
            "author": self.author.username,
            "pic": self.author.image_file,
            "date_posted": post_timestamp(self.date_posted),
            "content": self.content,
            "likes": len(self.likes),
            "likers": [User.query.filter_by(id=like.user_id).first().serialize() for like in self.likes],
            "comments": [comment.serialize() for comment in self.comments if not comment.parent] if len(self.comments) > 0 else None,
        }
        
        if not current_user.is_anonymous:
            payload["liked"] = True if current_user.has_liked_post(self) else False
        return payload
    
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'))
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def serialize(self):
        return {
            'author': self.user.username,
            'date': self.date_created,
        }

class Comment(db.Model):
    _N = 6

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(280), nullable=False)
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
    
    def get_post(self):
        return (self.post_id, 'post') if self.post_id else (self.material_id, 'material')
    
    def get_username(self):
        user = User.query.filter_by(id=self.user_id).first()
        return user.username if user else None

    def likes_count(self):
        return len([likes for likes in self.likes])
    
    def replies_count(self):
        return len([r for r in self.replies])
    
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
            "likes": [like.serialize() for like in self.likes],
            "replies": [reply.serialize() for reply in self.get_replies()],
            "likes_count": self.likes_count(),
            "liked": True if current_user.has_liked_comment(self) else False,
            "replies_count": self.replies_count(),
            "pic": self.commenter.image_file,
            "parent": self.parent.get_username() if self.parent else None
        }

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String, nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))

    tags = db.relationship('Tag', secondary='tags_table', backref=db.backref('tag_materials', lazy='dynamic'), lazy='joined')
    comments = db.relationship('Comment', backref='material')
    files = db.relationship('File', backref='files_material', lazy=True)
    likes = db.relationship('Like', backref='material')

    def serialize(self):
        return {
            'id': self.id,
            'author': self.creator.username,
            'title': self.title,
            'content': self.content,
            'timestamp': post_timestamp(self.date_posted),
        }
    
    def likes_count(self):
        return len([likes for likes in self.likes])

    def comments_count(self):
        return len([comment for comment in self.comments])
    
    def lesson_title(self):
        return Lesson.query.filter_by(id=self.lesson_id).first_or_404().title

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

    material_id = db.Column(db.Integer, db.ForeignKey('material.id'))
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'))

    def __repr__(self):
        return f"File('{self.filename}', '{self.file_type}')"

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    end_time = db.Column(db.Time)
    fee = db.Column(db.Integer, nullable=False, default=0)
    capacity = db.Column(db.Integer, nullable=False)
    tag = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    address = db.Column(db.String(150))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='meeting')
    files = db.relationship('File', backref='files_meeting', lazy=True)
    likes = db.relationship('Like', backref='meeting')
    going = db.relationship('User', secondary='going_table', backref=db.backref('going', lazy='dynamic'), lazy='joined')

    def likes_count(self):
        return len([likes for likes in self.likes])

    def comments_count(self):
        return len([comment for comment in self.comments])
    
    def add(self, user):
        if user not in self.going:
            self.going.append(user)

    def remove(self, user):
        if user in self.going:
            self.going.remove(user)

    def is_attending(self, user):
        return True if user in self.going else False

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    read = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"Message {self.body}"
    
    def serialize(self):
        return {
            'current_user': current_user.username,
            'id': self.id,
            'sender': self.author.username,
            'recipient': self.recipient.username,
            'content': self.body,
            'date': self.timestamp,
            'read': self.read,
        }
    
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    related_id = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.Float, index=True, default=time)
    read = db.Column(db.Boolean, nullable=False, default=False)
    payload_json = db.Column(db.Text)

    def get_data(self):
        return json.loads(str(self.payload_json))
    
    def new_notifications(self):
        return Notification.query.filter_by(user_id=current_user).filter(
            Notification.read == False).count()
    
    def serialize(self):
        data = self.get_data()

        if self.name == 'post_comment':

            comment = Comment.query.filter_by(id=data).first()
            post = comment.post

            return {
                'id': self.id,
                'type': self.name,
                'sent_data': comment.serialize(),
                'user_data': post.serialize(),
                'timestamp': self.timestamp,
                'html': 'commented on your post',
                'url': f'/post/{post.id}',
                'read': self.read,
            }
        
        elif self.name == 'post_like':

            like = Like.query.filter_by(id=data).first()
            post = like.post

            return {
                'id': self.id,
                'type': self.name,
                'sent_data': like.serialize(),
                'user_data': post.serialize(),
                'timestamp': self.timestamp,
                'html': 'liked your post',
                'url': f'/post/{post.id}',
                'read': self.read,
            }
        
        elif self.name == 'comment_like':

            like = Like.query.filter_by(id=data).first()
            comment = like.comment
            post_id, link = comment.get_post()

            return {
                'id': self.id,
                'type': self.name,
                'sent_data': like.serialize(),
                'user_data': comment.serialize(),
                'timestamp': self.timestamp,
                'html': 'liked your comment',
                'url': f'/{link}/{post_id}',
                'read': self.read,
            }
        
        elif self.name == 'comment_reply':

            reply = Comment.query.filter_by(id=data).first()
            comment = reply.parent
            post_id, link = comment.get_post()

            return {
                'id': self.id,
                'type': self.name,
                'sent_data': reply.serialize(),
                'user_data': comment.serialize(),
                'timestamp': self.timestamp,
                'html': 'replied to your comment',
                'url': f'/{link}/{post_id}',
                'read': self.read,
            }
        
        elif self.name == 'material_like':

            like = Like.query.filter_by(id=data).first()
            material = like.material

            return {
                'id': self.id,
                'type': self.name,
                'sent_data': like.serialize(),
                'user_data': material.serialize(),
                'timestamp': self.timestamp,
                'html': 'liked your post',
                'url': f'/material/{material.id}',
                'read': self.read,
            }
        
        elif self.name == 'material_comment':

            comment = Comment.query.filter_by(id=data).first()
            material = comment.material

            return {
                'id': self.id,
                'type': self.name,
                'sent_data': comment.serialize(),
                'user_data': material.serialize(),
                'timestamp': self.timestamp,
                'html': 'commented on your post',
                'url': f'/material/{material.id}',
                'read': self.read,
            }

class Textbook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(60), nullable=False)
    publisher = db.Column(db.String(120), nullable=False)
    grade = db.Column(db.Integer, nullable=False)

    # This will contain the list of lessons for this textbook
    lessons = db.relationship('Lesson', backref='textbook', lazy=True)
        
class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    textbook_id = db.Column(db.Integer, db.ForeignKey('textbook.id'), nullable=False)
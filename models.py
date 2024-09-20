from random import choice
from string import ascii_uppercase

from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

connections = db.Table('connections',
    db.Column('user1_id', db.String(16), db.ForeignKey('user.name')),
    db.Column('user2_id', db.String(16), db.ForeignKey('user.name'))
)

liked_posts = db.Table('liked_posts',
    db.Column('user_id', db.String(16), db.ForeignKey('user.name')),
    db.Column('post_id', db.String(8), db.ForeignKey('post.id'))
)

class User(db.Model):
    __tablename__ = 'user'

    name = db.Column(db.String(16), primary_key=True)
    password = db.Column(db.String(164))
    pfp = db.Column(db.String(200))
    info = db.Column(db.String(100), default="Hello!")
    connections = db.relationship(
        'User',
        secondary=connections,
        primaryjoin=(connections.c.user1_id == name),
        secondaryjoin=(connections.c.user2_id == name),
        backref=db.backref('connected_with', lazy='dynamic'),
        lazy='dynamic'
    )
    posts = db.relationship(
        'Post',
        backref='author',
        lazy=True
    )
    liked_posts = db.relationship(
        'Post',
        secondary=liked_posts,
        backref='liked_by',
        lazy='dynamic'
    )
    comments = db.relationship(
        'Comment',
        backref='author',
        lazy=True
    )
    def __init__(self, name, password,pfp="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS_txpHEl3CRozi3qkGKtr7amKDkW5wF3YGCQ&s"):
        self.name = name                                                                                                                                                
        self.password = password
        self.pfp=pfp
    
    def getpass(self):
        return self.password
    
    def gen_code(self):
        while True:
            code = ""
            for _ in range(8):
                code+=choice(ascii_uppercase)
            if db.session.query(Post).filter_by(id=code).first() is None:
                return code
    def connect(self, user):
        if not self.is_connected(user):
            self.connections.append(user)
            user.connections.append(self)
            db.session.commit()

    def disconnect(self, user):
        if self.is_connected(user):
            self.connections.remove(user)
            user.connections.remove(self)
            db.session.commit()

    def is_connected(self, user):
        return self.connections.filter(connections.c.user2_id == user.name).count() > 0

    def get_connections(self):
        return self.connections.all()
    
    def add_post(self, link,content=""):
        self.posts.append(Post(self.gen_code(), self.name, link, content))

    def get_posts(self):
        return self.posts

    def get_feed(self, page=1, per_page=7):
        connection_names = [connection.name for connection in self.connections.all()]
        feed_posts = (
            db.session.query(Post)
            .filter(Post.name.in_(connection_names))
            .order_by(Post.creation_time.desc()) 
            .paginate(page=page, per_page=per_page, error_out=False)
        )
        return feed_posts                                                                                                                                                                       
    
    def to_dict(self):
        return {"name" : self.name ,
                "pfp" : self.pfp,
                "connections" : len(self.connections.all()),
                "posts" : len(self.posts),
                "likes" : len(self.liked_posts.all()),
                "info" : self.info,
                "comments_count" : len(self.comments)
                }
    
    def like_post(self,post):
        if post not in self.liked_posts:
            self.liked_posts.append(post)
            post.likes+=1
            db.session.commit()
        else:
            self.liked_posts.remove(post)
            post.likes -= 1
            db.session.commit()        
    
    def get_liked_posts(self):
        return [self.liked_posts.all()[i].to_dict() for i in range(len(self.liked_posts.all())-1,-1,-1)]

class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(16), db.ForeignKey('user.name'))
    link  = db.Column(db.String(100))
    content = db.Column(db.String(500))
    creation_time = db.Column(db.DateTime, default=func.now())
    likes=db.Column(db.Integer,default=0)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def __init__(self, id, name, link=None, content=""):
        self.id=id
        self.name=name 
        self.link=link
        self.content= content 

    def ret_name(self):
        return self.name 

    def add_comment(self, user, content):
        new_comment = Comment(user_id=user.name, post_id=self.id, content=content)
        db.session.add(new_comment)
        db.session.commit()

    def get_comments(self):
        return [comment.to_dict() for comment in self.comments.all()]

    def to_dict(self):
        return {
            "name": self.name,
            "link": self.link,
            "content": self.content,
            "pfp": db.session.query(User).filter_by(name=self.name).first().pfp,
            "time": self.creation_time,
            "likes": self.likes,
            "id": self.id,
            "comments_count":len(self.comments.all())
        }

class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(16), db.ForeignKey('user.name'))
    post_id = db.Column(db.String(8), db.ForeignKey('post.id'))
    content = db.Column(db.String(500))
    creation_time = db.Column(db.DateTime, default=func.now())

    def to_dict(self):
        user = db.session.query(User).filter_by(name=self.user_id).first()
        
        return {
            "id": self.id,
            "user_name":user.name ,
            "pfp" : user.pfp,
            "post_id": self.post_id,
            "content": self.content,
            "creation_time": self.creation_time
        }

if __name__ == '__main__':
    from flask import Flask             
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "IDK123"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    db.init_app(app)
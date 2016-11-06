from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date
from database import Base
from flask_login import UserMixin

# class Anonymous(AnonymousUserMixin):
#   def __init__(self):
#     self.username = 'Guest'

class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), unique=True)
    email = Column(String(50), unique=True)
    birth_date = Column(Date)
    password = Column(String(50), nullable=False)

    def __init__(self, name, email, birth_date, password):
        self.name = name
        self.email = email
        self.birth_date = birth_date
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % (self.name)

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), )
    user = relationship(User)
    title = Column(String(140))
    content = Column(String(5000))
    date_created = Column(Date, default=date.today())
    is_visible = Column(Boolean, default=True)

class Picture(Base):
    __tablename__ = 'pictures'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'), )
    post = relationship(Post)
    filename = Column(String(100))

class Avatar(Base):
    __tablename__ = 'avatars'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), )
    user = relationship(User)
    filename = Column(String(100))
    #
    # def __init__(self, filename='None'):
    #     self.user =
    #     self.filename = filename



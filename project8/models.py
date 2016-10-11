# -*- coding: utf-8 -*-

from datetime import date
from app import db

__author__ = 'sobolevn'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    birth_date = db.Column(db.Date)

    def __init__(self, username='', email='', birth_date=None):
        self.username = username
        self.email = email

        if birth_date is not None:
            self.birth_date = birth_date

    def __repr__(self):
        return '<User %r>' % self.username

    def __str__(self):
        return repr(self)



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), )
                         # index=True)  # now let's test it.
    user = db.relationship(
        'User', backref=db.backref('posts', lazy='dynamic')
    )
    title = db.Column(db.String(140), unique=True)
    content = db.Column(db.String(3000))

    # sub_title = db.Column(db.String(140), unique=True)

    date_created = db.Column(db.Date, default=date.today())
    is_visible = db.Column(db.Boolean, default=True)

    def __init__(self, title='', content='', user=None,
                 date_created=None, is_visible=None):
        self.title = title
        self.content = content
        self.user = user

        if date_created is not None:
            self.date_created = date_created

        if is_visible is not None:
            self.is_visible = is_visible

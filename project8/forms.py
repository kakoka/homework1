# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, validators, DateField  # , SelectField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtf_tinymce.forms.fields import TinyMceField
# from sqlalchemy import orm
from functools import partial
from models import User
from app import db

__author__ = 'kakoka'

# def users_list(columns=None):
#     u = User.query
#     if columns:
#         u = u.options(orm.load_only(*columns))
#     return u

def getUserFactory(columns=None):
    return partial(users_list, columns=columns)

class BlogPostForm(FlaskForm):
    title = StringField(label='Title', validators=[
        validators.Length(min=4, max=140),
    ])
    content = TinyMceField(label='Article Text',
                        validators=[validators.length(min=10, max=5000)],
                        tinymce_options={'toolbar': 'undo | redo | bold italic | link | code',
                                                                'height': '200',
                                                                'width': '500'}
    )
    #author = QuerySelectField(query_factory=getUserFactory(['id', 'username']), get_label='username')

    author = QuerySelectField('username', query_factory=lambda: db.session.query(User), get_pk=lambda a: a.id,
                     get_label=lambda a: a.username)

class AddUserForm(FlaskForm):
    username = StringField(label='Username', validators=[
        validators.Length(min=4, max=140),
    ])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    birth_date = DateField('Birth Date YYYY-MM-DD', format='%Y-%m-%d', validators=(validators.Optional(),))

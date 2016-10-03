# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, validators, ValidationError, TextField, BooleanField, PasswordField
from wtforms.validators import Required
from wtf_tinymce.forms.fields import TinyMceField

__author__ = 'sobolevn'


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[validators.email()])
    password = PasswordField('New Password')
    #remember_me = BooleanField('Remember me', default=False)


class BlogPostForm(FlaskForm):
    title = StringField(label='Title', validators=[
        validators.Length(min=4, max=140),
    ])
    text = TinyMceField(label='Article Text', tinymce_options={'toolbar': 'bold italic | link | code'}
    )
    author = StringField(label='Author', validators=[
         validators.Length(min=10, max=3500),
     ])

# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, validators, DateField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError

# query select field - поле формы заполняется запросом к таблице БД,
# NB! тут нужно использовать отслеживание сессий, иначе не получается
# записывать в БД, ругается на неправильную сессию

from wtforms_sqlalchemy.fields import QuerySelectField
from flask_sqlalchemy_session import current_session

# Это для загрузки картинок

from flask_wtf.file import FileField, FileAllowed, FileRequired

# это для того, что бы можно было редактировать текст удобно - поле со встроенным TinyMCE

from wtf_tinymce.forms.fields import TinyMceField

# это наши модели

from models import User, Post, Picture

__author__ = 'kakoka'

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
    # выбираем из таблицы пользователей всех пользователей
    # get_pk - ключ, который потом записывается в полу user_id таблицы posts

    author = QuerySelectField(
        label='username',
        query_factory=lambda: current_session.query(User),
        get_pk=lambda item: item.id,
        get_label=lambda item: item.name,
        allow_blank=True,
        blank_text='select user'
    )


class AddUserForm(FlaskForm):
    username = StringField(label='Username', validators=[
        validators.Length(min=4, max=140),
    ])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    birth_date = DateField('Birth Date YYYY-MM-DD', format='%Y-%m-%d', validators=(validators.Optional(),))
    password = PasswordField('Enter your password')
    confirm = PasswordField('Enter your pass again')

class UploadAvatar(FlaskForm):
    user = QuerySelectField(
        label='username',
        query_factory=lambda: current_session.query(User),
        get_pk=lambda item: item.id,
        get_label=lambda item: item.name,
        allow_blank=True,
        blank_text='select user'
    )
    upload = FileField('image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])

class SelectUserProfile(FlaskForm):
    user = QuerySelectField(
        label='username',
        query_factory=lambda: current_session.query(User).all(),
        get_pk=lambda item: item.id,
        get_label=lambda item: item.name,
        allow_blank=True,
        blank_text='select user'
    )

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    remember_me = BooleanField()

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                           Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
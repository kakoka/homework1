# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.ext.sqlalchemy.orm import model_form
import config

__author__ = 'sobolevn'

app = Flask(__name__, template_folder='templates')
app.config.from_object(config)
db = SQLAlchemy(app)
db.create_all()

def create_app():
    @app.route('/', methods=['GET', 'POST'])
    def index():
        from models import Post
        post_form_class = model_form(Post, base_class=FlaskForm, db_session=db.session)
        if request.method == 'POST':
            # For full example:
            # http://flask.pocoo.org/snippets/60/

            # alternative:
            # https://wtforms-alchemy.readthedocs.org/en/latest/introduction.html
            # user = User.query.filter_by(username='sobolevn').first()
            # print("{} is creating a new {}'th post!".format(
            #     user.username, len(user.posts.all()) + 1))
            form = post_form_class(request.form)
            if form.validate():
                post = Post(**form.data)
                print(post)
                db.session.add(post)
                db.session.commit()
                flash('Post created!')
            else:
                flash('Form is not valid! Post was not created.')
        else:
            form = post_form_class()
        posts = Post.query.all()
        #db.create_all()
        return render_template('home.html', form=form, posts=posts)

    @app.route('/add_user', methods=['GET', 'POST'])
    def add_user():
        from models import User
        user_form_class = model_form(User, base_class=FlaskForm, db_session=db.session)
        if request.method == 'POST':
            u_form = user_form_class(request.form, exclude=['POSTS'])
            #print(u_form)
            if u_form.validate():
                print(u_form.data)
                print(u_form.data['email'])
                print(u_form.data['username'])
                print(u_form.data['birth_date'])
                user = User()
                user.email = u_form.data['email']
                user.username = u_form.data['username']
                user.birth_date = u_form.data['birth_date']
                print(user)
                db.session.add(user)
                db.session.commit()
                flash('new User created!')
            else:
                flash('Form is not valid! User was not created.')
        else:
            u_form = user_form_class()
        user = User.query.all()
        #db.create_all()
        return render_template('add_user.html', form=u_form, users=user)
    return app

if __name__ == '__main__':

    create_app().run()

# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, flash, redirect, url_for, send_from_directory

# bootstrap и TinyMCE
from flask_bootstrap import Bootstrap
from wtf_tinymce import wtf_tinymce

from database import Base, db_session, init_db

# отслеживание сессий
from flask_sqlalchemy_session import flask_scoped_session, current_session
from werkzeug import secure_filename

import config

from models import Post, User, Avatar
from forms import BlogPostForm, AddUserForm, UploadAvatar, SelectUserProfile
from logger import my_cool_logger
__author__ = 'kakoka'

app = Flask(__name__, template_folder='templates', static_folder='upload')
app.config.from_object(config)
init_db()
db = flask_scoped_session(db_session, app)
Bootstrap(app)
wtf_tinymce.init_app(app)

def create_app():
    @app.route('/post', methods=['GET', 'POST'])
    @my_cool_logger()
    def post():
        form = BlogPostForm(request.form)
        if request.method == 'POST':
            if form.validate():
                post = Post(user=form.author.data, title=form.title.data, content=form.content.data)
                current_session.add(post)
                current_session.commit()
                flash('Post created!')
                return redirect(url_for('post'))
            else:
                flash('Form is not valid! Post was not created.')
        posts = current_session.query(Post).all()
        return render_template('post.html', form=form, posts=posts)


    @app.route('/user', methods=['GET', 'POST'])
    @my_cool_logger()
    def user():
        form = AddUserForm(request.form)
        if request.method == 'POST':
            if form.validate():
                user = User(name=form.username.data, email=form.email.data, birth_date=form.birth_date.data, password=form.password.data)
                current_session.add(user)
                current_session.commit()
                flash('New user created!')
                return redirect(url_for('user'))
            else:
                flash('Form is not valid! User was not created.')
        all_users = current_session.query(User).all()

        return render_template('user.html', form=form, user=all_users)

    @app.route('/avatar', methods=['GET', 'POST'])
    @my_cool_logger()
    def avatar():
        form = UploadAvatar()
        if request.method == 'POST':
            if form.validate():
                avatar_f = Avatar(user=form.user.data, filename=form.upload.data.filename) #, avatar=form.author.data)
                f_name = secure_filename(form.upload.data.filename)
                form.upload.data.save('upload/avatar/' + f_name)
                current_session.add(avatar_f)
                current_session.commit()
                flash('avatar uploaded!')
                return redirect(url_for('avatar'))
            else:
                flash('Form is not valid!')
        all_avatars = current_session.query(Avatar).all()

        return render_template('avatar.html', form=form, avatars=all_avatars)


    @app.route('/profile', methods=['GET', 'POST'])
    @my_cool_logger()
    def profile():
        form = SelectUserProfile(request.form)
        if request.method == 'POST':
            if form.validate():
                q = current_session.query(Post).filter(Post.user == form.user.data).all()
                print(form.user.data)
                a = current_session.query(Avatar).join(User).filter(Avatar.user == form.user.data).all()
                u = current_session.query(User).join(Avatar).filter(Avatar.user == form.user.data).all()
                return render_template('all_posts.html', form=form, posts=q, avatar=a, users=u)
        else:
            q = current_session.query(Post).all()
            return render_template('all_posts.html', form=form, posts=q)

    @app.route('/upload/<path:filename>')
    @my_cool_logger()
    def download_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'],
                                   filename, as_attachment=True)

    return app

if __name__ == '__main__':

    create_app().run()

# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from wtf_tinymce import wtf_tinymce
import config

__author__ = 'sobolevn'

app = Flask(__name__, template_folder='templates')
app.config.from_object(config)
db = SQLAlchemy(app)
db.create_all()
Bootstrap(app)
wtf_tinymce.init_app(app)

def create_app():
    # @app.route('/', methods=['GET', 'POST'])
    # def index():
    # #     from models import Post
    #     post_form_class = model_form(Post, base_class=FlaskForm, db_session=db.session)
    #     if request.method == 'POST':
    #         form = post_form_class(request.form)
    #         if form.validate():
    #             post = Post(**form.data)
    #             print(post)
    #             db.session.add(post)
    #             db.session.commit()
    #             flash('Post created!')
    #         else:
    #             flash('Form is not valid! Post was not created.')
    #     else:
    #         form = post_form_class()
    #     posts = Post.query.all()
    #     #db.create_all()

        # return render_template('home.html', form=form, posts=posts)
    #
    @app.route('/post_with_form', methods=['GET', 'POST'])
    def post_with_form():
        from models import Post, User
        from forms import BlogPostForm
        form = BlogPostForm(request.form)
        if request.method == 'POST':
            print(form.author.data)
            #print(User.query.get(form.author.data))
            if form.validate():
                post = Post(user=form.author.data, title=form.title.data, content=form.content.data) #, form.author.data)
                # print(form.author.data)
                # print(post)
                db.session.add(post)
                db.session.commit()
                flash('Post created!')
                return redirect(url_for('post_with_form'))
            else:
                flash('Form is not valid! Post was not created.')
        posts = Post.query.all()
        #print(posts)
        return render_template('post_with_form.html', form=form, posts=posts)


    @app.route('/usr_with_forms', methods=['GET', 'POST'])
    def usr_with_forms():
        from models import User
        from forms import AddUserForm
        form = AddUserForm(request.form)
        if request.method == 'POST':
            if form.validate():
                user = User(form.username.data, form.email.data, form.birth_date.data)
                db.session.add(user)
                db.session.commit()
                flash('new User created!')
                return redirect(url_for('usr_with_forms'))
            else:
                flash('Form is not valid! User was not created.')
        all_users = User.query.all()
        print(all_users)
        return render_template('usr_with_forms.html', form=form, user=all_users)
    return app

if __name__ == '__main__':

    create_app().run()

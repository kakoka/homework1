# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, redirect, url_for

from flask_bootstrap import Bootstrap
from wtf_tinymce import wtf_tinymce
from flask_login import LoginManager

import config
from forms import BlogPostForm
from models import Storage, BlogPostModel, User


import logging

logger = logging.getLogger(__name__)


__author__ = 'sobolevn'




def create_app():

    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config)
    wtf_tinymce.init_app(app)
    Bootstrap(app)

    # @app.route('/', methods=['GET', 'POST'])
    # def login():
    #     error = None
    #     if request.method == 'POST':
    #         if request.form['username'] != 'admin' or request.form['password'] != 'admin':
    #             error = 'Invalid Credentials. Please try again.'
    #         else:
    #             return redirect('/blog')
    #     return render_template('login.html', error=error)

    @app.route('/', methods=['GET', 'POST'])
    def home():
        storage = Storage()
        all_items = storage.items

        if request.method == 'POST':
            form = BlogPostForm(request.form)
            if form.validate():
                model = BlogPostModel(form.data)
                all_items.append(model)
            else:
                logger.error('Someone have submitted an incorrect form!')
        else:
            form = BlogPostForm()

        return render_template(
            # '_base_boots.html',
            'home.html',
            form=form,
            items=all_items,
        )
    return app

if __name__ == '__main__':

    create_app().run()

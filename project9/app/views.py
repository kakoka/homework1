from flask import Blueprint, url_for, flash, request, jsonify, redirect, render_template, send_from_directory
from models import Post, User, Avatar
from forms import BlogPostForm, AddUserForm, UploadAvatar, SelectUserProfile, LoginForm
from logger import my_cool_logger
from flask_sqlalchemy_session import current_session
from werkzeug import secure_filename

from flask_login import login_user, logout_user, login_required, current_user, LoginManager

# from app import db

__author__ = 'kakoka'

main_route = Blueprint('main_route', __name__)

post_route = Blueprint('post_route', __name__, url_prefix='/post') #, template_folder='templates')
user_route = Blueprint('user_route', __name__, url_prefix='/user')
avatar_route = Blueprint('avatar_route', __name__, url_prefix='/avatar')
profile_route = Blueprint('profile_route', __name__, url_prefix='/profile')
upload_route = Blueprint('upload_route', __name__, url_prefix='/upload')
login_route = Blueprint('login_route', __name__, url_prefix='/login')
logout_route = Blueprint('logout_route', __name__, url_prefix='/logout')



@main_route.route('/', methods=['GET'])
@login_required
@my_cool_logger()
def main_test():
    urls = {
        'username': current_user.__repr__(),
        'local': url_for('.main_test'),
        'post': url_for('post_route.post'),
        'user': url_for('user_route.user'),
        'avatar': url_for('avatar_route.avatar'),
        'profile': url_for('profile_route.profile'),
        'login': url_for('login_route.login')
    }
    return jsonify(urls)

@post_route.route('/', methods=['GET', 'POST'])
# @login_required
@my_cool_logger()
def post():
    form = BlogPostForm(request.form)
    if request.method == 'POST':
        if form.validate():
            post = Post(user=form.author.data, title=form.title.data, content=form.content.data)
            current_session.add(post)
            current_session.commit()
            flash('Post created!')
            return redirect(url_for('post_route.post'))
        else:
            flash('Form is not valid! Post was not created.')
    posts = current_session.query(Post).all()
    return render_template('post.html', form=form, posts=posts)

# user path
@user_route.route('/', methods=['GET', 'POST'])
@my_cool_logger()
def user():
    form = AddUserForm(request.form)
    if request.method == 'POST':
        if form.validate():
            user = User(name=form.username.data, email=form.email.data, birth_date=form.birth_date.data, password=form.password.data)
            current_session.add(user)
            current_session.commit()
            flash('New user created!')
            return redirect(url_for('user_route.user'))
        else:
            flash('Form is not valid! User was not created.')
    all_users = current_session.query(User).all()

    return render_template('user.html', form=form, user=all_users)

@avatar_route.route('/', methods=['GET', 'POST'])
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

@profile_route.route('/', methods=['GET', 'POST'])
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

@upload_route.route('/upload/<path:filename>')
@my_cool_logger()
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename, as_attachment=True)

@login_route.route('/', methods=['GET', 'POST'])
@my_cool_logger()
def login():
    form = LoginForm()
    # registered_user = None
    if form.validate_on_submit():
        user = current_session.query(User).filter(User.name == form.username.data).first() #, User.password == form.password.data).first()
        print('USER!!!', user)
        if user:
            flash(u'Logged in as %s' % form.username.data)
            user.is_authenticated = True
            # session['user_id'] = form.username.id
            login_user(user, remember=True)
            return redirect(url_for('main_route.main_test'))
        flash(u'Un Successfully un logged in as %s' % form.username.data)
        # session['user_id'] = form.user.id
        # print(session['user_id'])

        return redirect(url_for('login_route.login'))
    return render_template('login.html', form=form)

@logout_route.route("/", methods=["GET"])
@login_required
def logout():
    user = current_user
    user.is_authenticated = False
    logout_user()
    return render_template("logout.html")

# @nickname_route.route('/user/<nickname>')
# @login_required
# def user(nickname):
#     user = User.query.filter_by(nickname=nickname).first()
#     if user == None:
#         flash('User ' + nickname + ' not found.')
#         return redirect(url_for('index'))
#     posts = [
#         {'author': user, 'body': 'Test post #1'},
#         {'author': user, 'body': 'Test post #2'}
#     ]
#     return render_template('user.html',
#                            user=user,
#                    posts=posts)


# @login_route.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'GET':
#         return render_template('register.html')
#     user = User(request.form['username'], request.form['password'], request.form['email'])
#     db.session.add(user)
#     db.session.commit()
#     flash('User successfully registered')
#     return redirect(url_for('login'))


# @login_route.route('/', methods=['GET', 'POST'])
# def login():
#     if request.method == 'GET':
#         return render_template('login.html')
#     return redirect(url_for('index'))
from flask import Blueprint, url_for, flash, request, jsonify, redirect, render_template, send_from_directory
from models import Post, User, Avatar
from forms import BlogPostForm, AddUserForm, UploadAvatar, SelectUserProfile, LoginForm
from logger import my_cool_logger
from flask_sqlalchemy_session import current_session
from werkzeug import secure_filename

from flask_login import login_user, logout_user, login_required, current_user, LoginManager

__author__ = 'kakoka'



main_route = Blueprint('main_route', __name__)
posts_route = Blueprint('posts_route', __name__, url_prefix='/posts') #, template_folder='templates')
user_route = Blueprint('user_route', __name__, url_prefix='/user')
ajax_route = Blueprint('ajax_rote', __name__, url_prefix='/ajax')
profile_route = Blueprint('profile_route', __name__, url_prefix='/profile')

upload_route = Blueprint('upload_route', __name__, url_prefix='/upload')

login_route = Blueprint('login_route', __name__, url_prefix='/login')
logout_route = Blueprint('logout_route', __name__, url_prefix='/logout')



@main_route.route('/', methods=['GET'])
@login_required
@my_cool_logger()
def main_test():
    urls = {
        'username': current_user.name,
        'local': url_for('.main_test'),
        'posts': url_for('posts_route.post'),
        'user': url_for('user_route.user'),
        'profile': url_for('profile_route.profile'),
        'login': url_for('login_route.login')
    }
    return jsonify(urls)

#show all posts
@posts_route.route('/', methods=['GET', 'POST'])
@my_cool_logger()
def post():
    if request.method == 'GET':
        posts = current_session.query(Post).all()
        return render_template('all_posts.html', posts=posts)

# add user's path
@user_route.route('/', methods=['GET', 'POST'])
@login_required
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

@profile_route.route('/', methods=['GET', 'POST'])
@profile_route.route('/<int:id>', methods=['GET', 'POST'])
@login_required
#@my_cool_logger()
def profile(id):
    form = BlogPostForm()
    if id == current_user.id and request.method == 'GET':
        posts = current_session.query(Post).filter(Post.user == current_user).all()
        return render_template('post.html', form=form, posts=posts)

    elif request.method == 'POST' and id == current_user.id and form.validate():
        post = Post(user=current_user, title=form.title.data, content=form.content.data)
        current_session.add(post)
        current_session.commit()
        flash('post_created')
        route_to = '/profile/' + str(current_user.id)
        return redirect(route_to)
    else:
        return redirect(url_for('login_route.login'))

@profile_route.route('/avatar', methods=['GET', 'POST'])
def avatar():
    pass
# # @profile_route.route('/avatar', methods=['GET', 'POST'])
# @login_required
# @my_cool_logger()
# def avatar():
#     form = UploadAvatar()
#     if id == current_user.id:
#         if request.method == 'POST':
#             if form.validate():
#                 avatar_f = Avatar(user=current_user, filename=form.upload.data.filename) #, avatar=form.author.data)
#                 f_name = secure_filename(form.upload.data.filename)
#                 form.upload.data.save('upload/avatar/' + f_name)
#                 current_session.add(avatar_f)
#                 current_session.commit()
#                 flash('avatar uploaded!')
#                 route_to = '/profile/' + str(current_user.id)
#                 return redirect(url_for(route_to))
#             else:
#                 flash('Form is not valid!')
#     all_avatars = current_session.query(Avatar).all()
#
#     return render_template('avatar.html', form=form, avatars=all_avatars)
#ajax
@ajax_route.route('/', methods=['GET', 'POST'])
@login_required
@my_cool_logger()
def ajax():
    form = BlogPostForm()
    if request.method == 'POST': # and form.validate():
        post = Post(user=current_user, title=form.title.data, content=form.content.data)
        print(post)
        current_session.add(post)
        current_session.commit()
        return jsonify(post.title, post.content, current_user.name) #{'success':True}), 200, {'ContentType':'application/json'} #, 'Post created!'
    if request.method == 'GET':
        return jsonify(current_user.name)
    return 'Invalid form'

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
            flash(u'Logged in as %s' % current_user.name)
            user.is_authenticated = True
            # session['user_id'] = form.username.id
            login_user(user, remember=True)
            route_to = '/profile/' + str(current_user.id)
            print(route_to)
            return redirect(route_to)
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
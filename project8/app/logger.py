from datetime import datetime
from functools import wraps
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.update({
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///db/logger.db',
    'SQLALCHEMY_TRACK_MODIFICATIONS': True,
    'DEBUG': True,
})
db = SQLAlchemy(app)


class UserRequest(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    ip = db.Column('ip', db.String(15))
    date_created = db.Column('date_created', db.DateTime(), default=datetime.now())
    url = db.Column('url', db.String(50))

    location_id = db.Column(db.Integer, db.ForeignKey('user_location.id'), )
    location = db.relationship(
        'UserLocation', backref=db.backref('requests', lazy='dynamic')
    )

    def __init__(self, ip, url, user_location=None):
        self.ip = ip
        self.url = url
        self.location = user_location


class UserLocation(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    lat = db.Column('lat', db.Float)
    lon = db.Column('lon', db.Float)
    city_name = db.Column('city_name', db.String(100))
    country_name = db.Column('country_name', db.String(100))

    def __init__(self, lat=None, lon=None, city_name=None, country_name=None):
        self.lat = lat
        self.lon = lon
        self.city_name = city_name
        self.country_name = country_name

def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance

def my_cool_logger():
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            url_address = request.path
            if app.debug:
                ip = request.environ.get(
                    'X-REMOTE_ADDR', request.remote_addr)
            else:
                ip = request.remote_addr

            if request.method == 'GET':
                user_location = get_or_create(
                    db.session, UserLocation,
                    lat=54.170,
                    lon=81.890,
                    city_name='Moscow',
                    country_name='Russia',
                )
                user_request = UserRequest(ip, url_address, user_location=user_location)
                db.session.add(user_request)
                db.session.commit()
            ret = f(*args, **kwargs)
            return ret
        return wrapped
    return decorator

@app.route('/')
@my_cool_logger()
def index():
    return 'index'


@app.route('/home')
@my_cool_logger()
def home():
    return 'home'


if __name__ == '__main__':
    db.create_all()
    app.run()
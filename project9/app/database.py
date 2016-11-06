from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///db/blog.db')
engine.echo = True

db_session = sessionmaker(autocommit=False,
                         autoflush=False,
                         bind=engine)

Base = declarative_base()

def init_db():
    from models import User, Post, Picture
    Base.metadata.create_all(bind=engine)
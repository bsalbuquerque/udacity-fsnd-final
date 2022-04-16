import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint

db = SQLAlchemy()
db_path = os.environ['DATABASE_URL']
migrate = Migrate()


def setup_db(app, database_path=db_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["DEBUG"] = True
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)


'''
Drops database tables and start with
one row for Movies and Actors to unittests

'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

    actor = Actor(
        name='Tom Hanks',
        age=65,
        gender='f'
    )

    movie = Movie(
        name='Fink',
        year=2021
    )

    actor.insert()
    movie.insert()


'''
Movies

'''


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    casting = db.relationship('Cast', backref=db.backref('movies'), cascade='all, delete-orphan', lazy=True)

    def __init__(self, name, year):
        self.name = name
        self.year = year

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'release': self.year
        }


'''
Actors

'''


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(1), nullable=False)
    casting = db.relationship('Cast', backref=db.backref('actors'), cascade='all, delete-orphan', lazy=True)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }


'''
Casts
Relationship between Movies and Actors
'''


class Cast(db.Model):
    __tablename__ = 'casts'
    __table_args__ = (UniqueConstraint('movie_id', 'actor_id'), )

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)
    actor_id = Column(Integer, ForeignKey('actors.id'), nullable=False)

    def __init__(self, movie_id, actor_id):
        self.movie_id = movie_id
        self.actor_id = actor_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'movie_id': self.movie_id,
            'actor_id': self.actor_id
        }

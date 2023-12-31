from flask_sqlalchemy import SQLAlchemy

db_orm = SQLAlchemy()

users_and_movies = db_orm.Table('user_movie',
                                db_orm.Column('user_id', db_orm.Integer, db_orm.ForeignKey('user.id')),
                                db_orm.Column('movie_id', db_orm.Integer, db_orm.ForeignKey('movie.id')),
                                db_orm.Column('user_rating', db_orm.Integer),
                                db_orm.Column('watched', db_orm.String, default='no'))


class User(db_orm.Model):
    __tablename__ = "user"

    id = db_orm.Column(db_orm.Integer, primary_key=True, autoincrement=True)
    name = db_orm.Column(db_orm.String, nullable=False)
    password = db_orm.Column(db_orm.String)
    movie = db_orm.relationship("Movie", secondary=users_and_movies, back_populates="user")


class Movie(db_orm.Model):
    __tablename__ = "movie"

    id = db_orm.Column(db_orm.Integer, primary_key=True, autoincrement=True)
    name = db_orm.Column(db_orm.String, nullable=False)
    rating = db_orm.Column(db_orm.Integer)
    year = db_orm.Column(db_orm.Integer)
    poster = db_orm.Column(db_orm.String)
    page = db_orm.Column(db_orm.String)
    director = db_orm.Column(db_orm.String)
    user = db_orm.relationship("User", secondary=users_and_movies, back_populates="movie")


class Reviews(db_orm.Model):
    __tablename__ = "reviews"

    id = db_orm.Column(db_orm.Integer, primary_key=True, autoincrement=True)
    movie_id = db_orm.Column(db_orm.Integer, db_orm.ForeignKey('movie.id'))
    user_id = db_orm.Column(db_orm.Integer, db_orm.ForeignKey('user.id'))
    review = db_orm.Column(db_orm.String)

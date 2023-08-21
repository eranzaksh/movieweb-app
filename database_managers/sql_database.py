from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
users_and_movies = db.Table('user_movie',
                            db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                            db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')))


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String)
    movie = db.relationship("Movie", secondary=users_and_movies, back_populates="user")


class Movie(db.Model):
    __tablename__ = "movie"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer)
    year = db.Column(db.Integer)
    poster = db.Column(db.String)
    page = db.Column(db.String)
    director = db.Column(db.String)
    user = db.relationship("User", secondary=users_and_movies, back_populates="movie")


# user1 = User(
#     name="eran",
#     password="123qweasdx"
# )
# movie1 = Movie(
#     name="titanic",
#     rating=8,
#     year=1999,
#     poster="test",
#     page="test",
#     director="someone"
# )


# user1.movie.append(movie1)


# with app.app_context():
#     db.session.add(user1)
#     db.session.commit()

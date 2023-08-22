from flask_sqlalchemy import SQLAlchemy


db_orm = SQLAlchemy()

users_and_movies = db_orm.Table('user_movie',
                                db_orm.Column('user_id', db_orm.Integer, db_orm.ForeignKey('user.id')),
                                db_orm.Column('movie_id', db_orm.Integer, db_orm.ForeignKey('movie.id')))


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

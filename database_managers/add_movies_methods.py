class MovieAlreadyExists(Exception):
    pass


class NotFoundException(Exception):
    pass


class AddMovieMethods:
    def __init__(self):
        pass

    @staticmethod
    def generating_new_movie(name, movies_list, movie_data, rating, year, poster, imdb_page, director):
        movie_id = len(movies_list)
        for movie in movies_list:
            if movie_id == movie['id']:
                movie_id += 1
        for movie in movies_list:
            if name.lower() in movie["name"].lower():
                raise MovieAlreadyExists
        if 'Error' in movie_data:
            raise NotFoundException("Movie not found!")
        new_movie = {"id": movie_id, "name": movie_data["Title"], 'rating': float(movie_data[rating]),
                     'year': movie_data[year],
                     'poster': movie_data[poster], 'page': movie_data[imdb_page], 'director': movie_data[director]}
        return new_movie

    @staticmethod
    def add_movie_to_user(users, user_id, new_movie):
        for user in users:
            if user['id'] == user_id:
                user['movies'].append(new_movie)

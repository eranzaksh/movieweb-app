class MovieAlreadyExists(Exception):
    pass


class NotFoundException(Exception):
    pass


class AddMovieMethods:
    def __init__(self):
        pass

    @staticmethod
    def generating_new_movie(name, movies_list, movie_data, rating, year, poster, imdb_page, director):
        """
        Generating new_movie and movie id for the "add_movie" function
        Return the movie dictionary
        """
        movie_id = 0
        if movies_list:
            movie = max(movies_list, key=lambda x: x['id'])
            movie_id = movie['id'] + 1
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
        """
        Appending the new movie to the users movie list
        """
        for user in users:
            if user['id'] == str(user_id):
                user['movies'].append(new_movie)

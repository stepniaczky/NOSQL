import uuid

from typing import List
from src.models import Movie, Ticket
from src.db import get_collection


class MovieManager:

    @staticmethod
    def add_movie(title, genre, min_age, hall, free_slots):
        if not 1 <= hall <= 5:
            print('Błędny numer sali!')
            return
        
        movie_collection = get_collection('movies')
        if movie_collection.find_one({'hall': hall}) is not None:
            print('Podana sala jest zajęta!')
            return

        new_movie = Movie(title=title, genre=genre,
                        min_age=min_age, hall=hall, free_slots=free_slots)

        movie_collection.insert_one(new_movie.__dict__())
        print('Pomyslnie dodano film o UUID: {}'.format(new_movie._id))
        
    @staticmethod
    def delete_movie(_id) -> None:
        _id = str(_id) if isinstance(_id, uuid.UUID) else _id
        
        movie_collection = get_collection('movies')
        movie = movie_collection.find_one({'_id': _id})
        if movie is None:
            print('Film o takim id nie istnieje!')
            return
        
        ticket_collection = get_collection('tickets')
        ticket = ticket_collection.find_one({'movie_id': _id})
        if ticket is not None:
            print('Nie można usunąć filmu, który posiada bilet!')
            return
        
        movie_collection.delete_one({'_id': _id})
        print('Pomyslnie usunieto film o UUID: {}'.format(_id))

    @staticmethod
    def get_movie(**query) -> Movie or None:
        if not set(query.keys()).issubset(set(['_id', 'title', 'genre', 'min_age', 'hall'])):
            print('Niepoprawne zapytanie!')
            return
        
        if '_id' in query.keys():
            query['_id'] = str(query['_id']) if isinstance(query['_id'], uuid.UUID) else query['_id']
        
        movie_collection = get_collection('movies')
        res_list = list(movie_collection.find(query))
        
        if len(res_list) == 0:
            print('Film o wskazanych parametrach nie istnieje!')
            return
        
        if len(res_list) > 1:
            print('Zapytanie zwróciło więcej niż jeden film!')
            return
        
        movie = res_list[0]
        return Movie(**movie)

    @staticmethod
    def get_all_movies() -> List[Movie]:
        movie_collection = get_collection('movies')
        movies_cursor = movie_collection.find()
        
        movies = []
        for movie in movies_cursor:
            movies.append(Movie(**movie))
        
        return movies

    @staticmethod
    def get_size() -> int:
        movie_collection = get_collection('movies')
        return movie_collection.count_documents({})
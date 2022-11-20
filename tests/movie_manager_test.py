import unittest
import os

from src.db import config
from src.managers.movie_manager import MovieManager

config('.env.test')
movie_manager = MovieManager()


class MovieManagerTest(unittest.TestCase):
    def setUp(self) -> None:
        movie = movie_manager.get_movie(hall=1)
        if movie is not None:
            movie_manager.delete_movie(_id=movie._id)
            movie = movie_manager.get_movie(_id=movie._id)
            self.assertIsNone(movie)

    def test_movie_add(self):
        movie = movie_manager.get_movie(hall=1)
        self.assertIsNone(movie)

        movie_manager.add_movie('Pulp Fiction', 'Dramat', 18, 1, 10)

        movie = movie_manager.get_movie(hall=1)
        self.assertIsNotNone(movie)

        movie_manager.delete_movie(_id=movie._id)

    def test_remove_movie(self):
        movie_manager.add_movie('Pulp Fiction', 'Dramat', 18, 1, 10)
        movie = movie_manager.get_movie(hall=1)
        self.assertIsNotNone(movie)

        movie_manager.delete_movie(_id=movie._id)
        movie = movie_manager.get_movie(hall=1)
        self.assertIsNone(movie)


if __name__ == '__main__':
    unittest.main()

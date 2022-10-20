import unittest

from src.db import get_engine_from_env, init_db, get_session

engine = get_engine_from_env()
init_db(engine)
session = get_session(engine)


class AddMovieTest(unittest.TestCase):
    def setUp(self):
        self.xd = 'xd'

    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()

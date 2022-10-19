from typing import List

from sqlalchemy import select
from sqlalchemy.engine import Row
from sqlalchemy.orm import sessionmaker

from src.models import Movie


class MovieManager:
    halls = [True for i in range(5)]

    def __init__(self, session):
        self.session: sessionmaker = session

    def add_movie(self):
        with self.session() as session:
            movies_table = Movie.__table__
            query: list[Row] = session.execute(select(movies_table)).all()
            print(query)

        if not any(self.halls):
            print('Nie ma wolnych sal!')

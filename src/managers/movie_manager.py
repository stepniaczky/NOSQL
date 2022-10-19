from sqlalchemy import insert, select

from src.models import Movie

movies_table = Movie.__table__


class MovieManager:
    def __init__(self, session):
        self.session = session

    def add_movie(self, title, genre, min_age, hall, free_slots):
        if not 1 <= hall <= 5:
            print('Błędny numer sali!')
            return

        with self.session() as session:
            select_response = session.execute(select(movies_table)).all()

            for row in select_response:
                if hall == row.hall:
                    print('Podana sala jest zajęta!')
                    return

            new_movie = Movie(title=title, genre=genre, min_age=min_age, hall=hall, free_slots=free_slots)

            session.add(new_movie)
            session.commit()

    def delete_movie(self, movie_id):
        with self.session() as session:
            res = session.query(Movie).filter(Movie.id == movie_id).delete()

            if not res:
                print('Film o takim id nie istnieje!')
                return

            session.commit()

    def get_movie(self, movie_id):
        with self.session() as session:
            movie = session.query(Movie).get(movie_id)

            if movie is None:
                print('Film o takim id nie istnieje!')

            return movie

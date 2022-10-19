from typing import Any
from sqlalchemy import Column, Integer, String, Boolean, null, ARRAY

from src.models.base import Base


class Movie(Base):
    __tablename__ = 'movies'
    __mapper_args__ = {
        'polymorphic_on': 'type',
        'polymorphic_identity': 'movie',
    }

    id = Column(Integer, primary_key=True, autoincrement='auto')
    title = Column(String, nullable=False)
    genre = Column(String)
    min_age = Column(Integer)
    hall = Column(Integer)
    free_slots = Column(ARRAY(Boolean))

    def __init__(self, title, genre=null, min_age=null, hall=null, free_slots=null, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.title = title
        self.genre = genre
        self.min_age = min_age
        self.hall = hall
        self.free_slots = free_slots

    def __repr__(self):
        return "<Movie(title='%s', genre='%s', min_age='%s', hall='%s', free_slots='%s')>" % (
            self.title,
            self.genre,
            self.min_age,
            self.hall,
            self.free_slots)

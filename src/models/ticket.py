from datetime import datetime, date
import sqlalchemy

from typing import Any

from sqlalchemy import Column, Numeric, Integer, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship

from src.constants.table_names import TICKETS, MOVIES, CLIENTS
from src.models import Base


class Ticket(Base):
    __tablename__ = TICKETS

    id = Column(Integer, primary_key=True)
    base_price = Column(Numeric, nullable=False)
    date = Column(Date, nullable=False)

    client_id = Column(Integer, ForeignKey(f'{CLIENTS}.id'))
    client = relationship('Client', backref='ticket')

    movie_id = Column(Integer, ForeignKey(f'{MOVIES}.id'))
    movie = relationship('Movie', backref='ticket')

    def __init__(self, id, base_price, client_id=None, movie_id=None, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.id = id
        self.base_price = base_price
        self.date = date.today()
        self.client_id = client_id
        self.movie_id = movie_id

    def __repr__(self):
        return "<Ticket(base_price='%s', date='%s', client_id='%s', movie_id='%s')>" % (
            self.base_price,
            self.date,
            self.client_id,
            self.movie_id)

from typing import Any
from sqlalchemy import Column, Integer, ForeignKey, Date, Numeric
from sqlalchemy.orm import relationship

from src.models.base import Base


class Ticket(Base):
    __tablename__ = 'tickets'
    __mapper_args__ = {
        'polymorphic_on': 'type',
        'polymorphic_identity': 'ticket',
    }

    id = Column(Integer, primary_key=True)
    base_price = Column(Numeric, nullable=False)
    date = Column(Date, nullable=False)

    client_id = Column(Integer, ForeignKey('clients.id'))
    client = relationship('Client', backref='ticket')

    movie_id = Column(Integer, ForeignKey('movies.id'))
    movie = relationship('Movie', backref='ticket')

    def __init__(self, base_price, date, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.base_price = base_price
        self.date = date

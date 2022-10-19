from typing import Any
from sqlalchemy import Column, Integer, String, Numeric

from src.models.base import Base


class Address(Base):
    __tablename__ = 'addresses'
    __mapper_args__ = {
        'polymorphic_on': 'type',
        'polymorphic_identity': 'address',
    }

    id = Column(Integer, primary_key=True)
    city = Column(String, nullable=False)
    street = Column(String, nullable=False)
    number = Column(Numeric, nullable=False)

    def __init__(self, city, street, number, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.city = city
        self.street = street
        self.number = number

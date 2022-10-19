from typing import Any

from sqlalchemy import Column, Integer, String, Numeric

from src.constants.table_names import ADDRESSES
from src.models.base import Base


class Address(Base):
    __tablename__ = ADDRESSES

    id = Column(Integer, primary_key=True, autoincrement='auto')
    city = Column(String, nullable=False)
    street = Column(String, nullable=False)
    number = Column(Numeric, nullable=False)

    def __init__(self, city, street, number, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.city = city
        self.street = street
        self.number = number

    def __repr__(self):
        return "<Address(city='%s', street='%s', number='%s')>" % (
            self.city,
            self.street,
            self.number)
    
    def __str__(self):
        return f"City: {self.city}, Street: {self.street} {self.number} "

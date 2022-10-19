from abc import abstractmethod
from datetime import date
from typing import Any

from sqlalchemy import Column, Integer, String, Numeric

from src.constants.table_names import CLIENT_TYPES
from src.models import Base


class ClientType(Base):
    __tablename__ = CLIENT_TYPES

    id = Column(Integer, primary_key=True, autoincrement='auto')
    type = Column(String, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': CLIENT_TYPES,
        'polymorphic_on': type
    }

    def __init__(self, is_premium, birth_date, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        if is_premium:
            return Premium()
        age = self.age(birth_date)
        if age < 5 or age > 65:
            return Reduced()
        else:
            return Normal()

    def __repr__(self):
        return "<Client(type='%s')>" % (
            self.type)
        
    @abstractmethod
    def apply_discount():
        pass
    
    @staticmethod
    def age(birth_date):
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age


class Reduced(ClientType):
    __mapper_args__ = {
        "polymorphic_identity": "reduced",
    }
    
    
    def apply_discount(price):
        return 0.5 * price


class Normal(ClientType):
    __mapper_args__ = {
        "polymorphic_identity": "normal",
    }


    def apply_discount(price):
        return price

class Premium(ClientType):
    __mapper_args__ = {
        "polymorphic_identity": "premium",
    }
    
    def apply_discount(price):
        return 0.1 * price
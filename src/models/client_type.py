from abc import abstractmethod
from typing import Any

from sqlalchemy import Column, Integer, String, Numeric

from src.constants.table_names import CLIENT_TYPES
from src.models import Base


class ClientType(Base):
    __tablename__ = CLIENT_TYPES

    id = Column(Integer, primary_key=True, autoincrement='auto')
    type = Column(String, nullable=False, default="normal")

    __mapper_args__ = {
        'polymorphic_identity': CLIENT_TYPES,
        'polymorphic_on': type
    }

    def __init__(self, type, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.type = type

    def __repr__(self):
        return "<Client(type='%s')>" % (
            self.type)
        
    @abstractmethod
    def apply_discount():
        pass


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
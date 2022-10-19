from abc import abstractmethod
from typing import Any

from sqlalchemy import Column, Integer, String

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

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return "<Client(type='%s')>" % self.type

    @abstractmethod
    def apply_discount(self, price):
        pass


class NormalClientType(ClientType):
    __mapper_args__ = {
        "polymorphic_identity": "client_type_normal",
    }

    def apply_discount(self, price):
        return price


class ReducedClientType(ClientType):
    __mapper_args__ = {
        "polymorphic_identity": "client_type_reduced",
    }

    def apply_discount(self, price):
        return price * 0.5


class PremiumClientType(ClientType):
    __mapper_args__ = {
        "polymorphic_identity": "client_type_premium",
    }

    def apply_discount(self, price):
        return price * 0.1

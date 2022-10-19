from typing import Any

from sqlalchemy import Column, Integer, String

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


class Reduced(ClientType):
    __mapper_args__ = {
        "polymorphic_identity": "reduced",
    }


class Normal(ClientType):
    __mapper_args__ = {
        "polymorphic_identity": "normal",
    }


class Premium(ClientType):
    __mapper_args__ = {
        "polymorphic_identity": "premium",
    }
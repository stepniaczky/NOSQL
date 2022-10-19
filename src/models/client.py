from typing import Any
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship

from src.models.base import Base


class Client(Base):
    __tablename__ = 'clients'
    __mapper_args__ = {
        'polymorphic_on': 'type',
        'polymorphic_identity': 'client',
    }

    id = Column(Integer, primary_key=True, autoincrement='auto')
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    is_premium = Column(Boolean, nullable=False, default=False)
    client_type = Column(String, nullable=False, default="normal")

    address_id = Column(Integer, ForeignKey('addresses.id'))
    address = relationship('Address', backref='client')

    def __init__(self, name, last_name, birth_date, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.name = name
        self.last_name = last_name
        self.birth_date = birth_date

    def __repr__(self):
        return "<Client(first_name='%s', last_name='%s', birth_date='%s', is_premium='%s', client_type='%', address_id='%')>" % (
            self.first_name,
            self.last_name,
            self.birth_date,
            self.is_premium,
            self.client_type,
            self.address_id)

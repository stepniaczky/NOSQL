from typing import Any

from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.constants.table_names import CLIENTS, CLIENT_TYPES, ADDRESSES
from src.models import Base


class Client(Base):
    __tablename__ = CLIENTS

    id = Column(Integer, primary_key=True)
    pesel = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)

    client_type_id = Column(Integer, ForeignKey(f'{CLIENT_TYPES}.id'))
    client_type = relationship('ClientType', backref='client')

    address_id = Column(Integer, ForeignKey(f'{ADDRESSES}.id'))
    address = relationship('Address', backref='client')

    def __init__(self, id, pesel, first_name, last_name, birth_date, client_type_id, client_type, address_id, address, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.id = id
        self.pesel = pesel
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.client_type_id = client_type_id
        self.client_type = client_type
        self.address_id = address_id
        self.address = address

    def __repr__(self):
        return "<Client(client_id='%s', first_name='%s', last_name='%s', birth_date='%s', client_type_id='%s', " \
               "address_id='%s')>" % (
                   self.id,
                   self.first_name,
                   self.last_name,
                   self.birth_date,
                   self.client_type_id,
                   self.address_id)

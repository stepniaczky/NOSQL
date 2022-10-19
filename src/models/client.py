from typing import Any

from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.constants.table_names import CLIENTS, CLIENT_TYPES, ADDRESSES
from src.models import Base


class Client(Base):
    __tablename__ = CLIENTS

    client_id = Column(Integer, primary_key=True, autoincrement='auto')
    pesel = Column(Integer, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    is_premium = Column(Boolean, nullable=False, default=False)

    client_type_id = Column(Integer, ForeignKey(f'{CLIENT_TYPES}.id'))
    client_type = relationship('ClientType', backref='client')

    address_id = Column(Integer, ForeignKey(f'{ADDRESSES}.id'))
    address = relationship('Address', backref='client')

    def __init__(self, client_id, first_name, last_name, birth_date, is_premium, client_type_id = None, address_id = None, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.client_id = client_id
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.is_premium = is_premium
        self.client_type_id = client_type_id
        self.address_id = address_id
        

    def __repr__(self):
        return "<Client(client_id='%s', first_name='%s', last_name='%s', birth_date='%s', is_premium='%s', client_type_id='%s', " \
               "address_id='%s')>" % (
                   self.client_id,
                   self.first_name,
                   self.last_name,
                   self.birth_date,
                   self.is_premium,
                   self.client_type_id,
                   self.address_id)

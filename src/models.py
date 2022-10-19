from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, Date, Boolean, ForeignKey, null, ARRAY
from sqlalchemy.orm import relationship
from typing import Any

from src.constants.table_names import TableName

Base = declarative_base()


class Address(Base):
    __tablename__ = TableName.ADDRESSES

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


class ClientType(Base):
    __tablename__ = TableName.CLIENT_TYPES

    id = Column(Integer, primary_key=True, autoincrement='auto')
    type = Column(String, nullable=False, default="normal")

    __mapper_args__ = {
        'polymorphic_identity': 'client_types',
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


class Client(Base):
    __tablename__ = TableName.CLIENTS

    client_ID = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    is_premium = Column(Boolean, nullable=False, default=False)
    client_type_id = Column(Integer, ForeignKey('client_types.id'))
    client_type = relationship('ClientType', backref='client')

    address_id = Column(Integer, ForeignKey('addresses.id'))
    address = relationship('Address', backref='client')

    def __init__(self, first_name, last_name, birth_date, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date

    def __repr__(self):
        return "<Client(first_name='%s', last_name='%s', birth_date='%s', is_premium='%s', client_type='%', address_id='%')>" % (
            self.first_name,
            self.last_name,
            self.birth_date,
            self.is_premium,
            self.client_id,
            self.address_id)


class Movie(Base):
    __tablename__ = TableName.MOVIES

    id = Column(Integer, primary_key=True, autoincrement='auto')
    title = Column(String, nullable=False)
    genre = Column(String)
    min_age = Column(Integer)
    hall = Column(Integer)
    free_slots = Column(ARRAY(Boolean))

    def __init__(self, title, genre=null, min_age=null, hall=null, free_slots=null, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.title = title
        self.genre = genre
        self.min_age = min_age
        self.hall = hall
        self.free_slots = free_slots

    def __repr__(self):
        return "<Movie(title='%s', genre='%s', min_age='%s', hall='%s', free_slots='%s')>" % (
            self.title,
            self.genre,
            self.min_age,
            self.hall,
            self.free_slots)


class Ticket(Base):
    __tablename__ = TableName.TICKETS

    id = Column(Integer, primary_key=True, autoincrement='auto')
    base_price = Column(Numeric, nullable=False)
    date = Column(Date, nullable=False)

    client_id = Column(Integer, ForeignKey('clients.client_ID'))
    client = relationship('Client', backref='ticket')

    movie_id = Column(Integer, ForeignKey('movies.id'))
    movie = relationship('Movie', backref='ticket')

    def __init__(self, base_price, date, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.base_price = base_price
        self.date = date

    def __repr__(self):
        return "<Ticket(base_price='%s', date='%s', client_id='%s', movie_id='%s')>" % (
            self.base_price,
            self.date,
            self.client_id,
            self.movie_id)

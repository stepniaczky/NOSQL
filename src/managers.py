from sqlalchemy import insert, update, delete

from models import Client, Address, ClientType, Movie, Ticket


class clientManager():
    def add_client(first_name, last_name, birth_date, is_premium, client_ID, city, street, number):
        client = Client(first_name, last_name, birth_date, is_premium)
        address = Address(city, street, number)

        # new_address = (
        #     insert(Address.__tablename__).
        #     values(city= )
        # )

        # stmt = (
        #     insert(Client.__tablename__).
        #     values(name='username', fullname='Full Username')
        # )

    def remove_client():
        ...

    def get_client():
        ...

    def get_all_clients():
        ...


class movieManager():
    ...


class ticketManager():
    ...

from typing import List
from src.models import Client, Address

from sqlalchemy.engine import Row


class ClientManager:
    user_table = Client.__tablename__

    def __init__(self, sessionmaker):
        self.sessionmaker = sessionmaker

    def add_client(self, client_id, first_name, last_name, birth_date, is_premium, city, street, number):
        # cliet_type = ClientType(birth_date)
        # address_id = None
        print("CFFFFFFFFFFFFFFFFFFF")

        with self.sessionmaker() as session:
            addresses = session.query(Address).all()
            print(addresses)
            address = Address(city=city, street=street, number=number)
            session.add(address)
            session.commit()
            # session.flush()
            # session.refresh()
            # address_id = address.id
            # except Exception as e:
            #     session.rollback()

        # client = Client(client_id, first_name, last_name, birth_date, is_premium, )

        # with self.sessionmaker() as session:
        #     try:
        #         client_type_id = ClientType.query.filter_by(type=cliet_type.type).one().id
        #         client = Client(client_id, first_name, last_name, birth_date, is_premium, client_type_id, address_id)
        #         session.add(client)
        #         session.commit()
        #     except Exception as e:
        #         session.rollback()

    def remove_client(self, client_id):
        with self.sessionmaker() as session:
            try:
                obj = Client.query.filter_by(client_id=client_id).one()
                session.delete(obj)
                session.commit()
            except Exception as e:
                session.rollback()

    def get_client(self, client_id):
        with self.sessionmaker() as session:
            client = session.query(Client).get(client_id)

            if client is None:
                print('Klient o takim id nie istnieje!')

            return client

    def get_all_clients(self):
        with self.sessionmaker() as session:
            clients = session.query(Client).all()
            return clients

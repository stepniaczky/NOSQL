from src.helpers.get_age import get_age
from src.models import Client, Address
from src.models.client_type import PremiumClientType, NormalClientType, ReducedClientType, ClientType


class ClientManager:
    def __init__(self, sessionmaker):
        self.sessionmaker = sessionmaker

    def add_client(self, pesel, first_name, last_name, birth_date, is_premium, city, street, number):
        with self.sessionmaker() as session:
            new_address = Address(city=city, street=street, number=number)

            session.add(new_address)
            session.commit()
            session.refresh(new_address)

            new_client_type = ReducedClientType()

            age = get_age(birth_date)

            if is_premium:
                new_client_type = PremiumClientType()
            elif 5 < age < 65:
                new_client_type = NormalClientType()

            client_type_res = session.query(ClientType).filter(ClientType.type == new_client_type.type).first()

            if not client_type_res:
                session.add(new_client_type)
                session.commit()
                session.refresh(new_client_type)

            client_type_to_set = client_type_res if client_type_res else new_client_type

            new_client = Client(pesel=pesel, first_name=first_name, last_name=last_name, birth_date=birth_date,
                                client_type_id=client_type_to_set.id, client_type=client_type_to_set,
                                address_id=new_address.id, address=new_address)
            session.add(new_client)
            session.commit()

    def remove_client(self, client_id):
        with self.sessionmaker() as session:
            delete_response = session.query(Client).filter(Client.id == client_id).delete()

            if not delete_response:
                print('Klient o takim id nie istnieje!')
                return

            session.commit()

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

from src.helpers.get_age import get_age
from src.models import Client, Address, Ticket
from src.models.client_type import PremiumClientType, NormalClientType, ReducedClientType, ClientType


class ClientManager:
    def __init__(self, sessionmaker):
        self.sessionmaker = sessionmaker

    def add_client(self, pesel, first_name, last_name, birth_date, is_premium, city, street, number):
        with self.sessionmaker() as session:
            if len(pesel) != 11:
                print("Pesel musi mieć 11 znaków!")
                return

            if pesel in [client.pesel for client in session.query(Client).all()]:
                print('Klient o takim peselu już istnieje!')
                return

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

            client_type_res = session.query(ClientType).filter(
                ClientType.type == new_client_type.type).first()

            if not client_type_res:
                session.add(new_client_type)
                session.commit()
                session.refresh(new_client_type)

            client_type_to_set = client_type_res if client_type_res else new_client_type

            id = 1
            while True:
                if session.query(Client).get(id) is None:
                    break
                id += 1

            new_client = Client(id=id, pesel=pesel, first_name=first_name, last_name=last_name, birth_date=birth_date,
                                client_type_id=client_type_to_set.id, client_type=client_type_to_set,
                                address_id=new_address.id, address=new_address)
            session.add(new_client)
            session.commit()

    def remove_client(self, id):
        with self.sessionmaker() as session:
            ticket = session.query(Ticket).filter(
                Ticket.client_id == id).first()
            if ticket is not None:
                print('Nie można usunąć klienta, który posiada bilet!')
                return

            client = session.query(Client).get(id)
            if client is None:
                print('Klient o takim id nie istnieje!')
                return

            address_id = client.address_id

            delete_user = session.query(
                Client).filter(Client.id == id).delete()

            delete_address = session.query(
                Address).filter(Address.id == address_id).delete()

            session.commit()

    def get_client(self, id):
        with self.sessionmaker() as session:
            client = session.query(Client).get(id)

            if client is None:
                print('Klient o takim id nie istnieje!')

            return client

    def get_all_clients(self):
        with self.sessionmaker() as session:
            clients = session.query(Client).all()
            return clients

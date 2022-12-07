import uuid
import json
import asyncio

from typing import List

from src.decorators.client_manager import add_client_decorator, get_client_decorator, remove_client_decorator, \
    update_client_decorator
from src.models import Client, Address, PremiumClientType, NormalClientType, ReducedClientType
from src.db import get_collection, hash_prefix, get_redis_client


class ClientManager:
    @staticmethod
    @add_client_decorator
    def add_client(pesel, first_name, last_name, birth_date, is_premium, city, street, number) -> Client | None:
        if len(pesel) != 11:
            print("Pesel musi mieć 11 znaków!")
            return

        address = Address(city=city, street=street, number=number)
        client_type = None

        if is_premium:
            client_type = PremiumClientType()
        elif 5 < Client.get_age(birth_date) < 65:
            client_type = NormalClientType()
        else:
            client_type = ReducedClientType()

        client = Client(pesel=pesel, first_name=first_name, last_name=last_name, birth_date=birth_date,
                        client_type=client_type, address=address, is_premium=is_premium)

        client_collection = get_collection('clients')
        if client_collection.find_one({'pesel': pesel}) is not None:
            print('Klient o takim peselu już istnieje!')
            return

        client_collection.insert_one(client.__dict__())
        print('Pomyslnie dodano klienta o UUID: {}'.format(client._id))
        return client

    @staticmethod
    @remove_client_decorator
    def remove_client(_id):
        _id = str(_id) if isinstance(_id, uuid.UUID) else _id
        client_collection = get_collection('clients')
        client = client_collection.find_one({'_id': _id})
        if client is None:
            print('Klient o takim id nie istnieje!')
            return

        ticket_collection = get_collection('tickets')
        ticket = ticket_collection.find_one({'client_id': _id})
        if ticket is not None:
            print('Nie można usunąć klienta, który posiada bilet!')
            return

        client_collection.delete_one({'_id': _id})
        print('Pomyslnie usunieto klienta o UUID: {}'.format(_id))
        return _id

    @staticmethod
    @get_client_decorator
    def get_client(**query) -> Client or None:
        if not set(query.keys()).issubset(
                set(['_id', 'pesel', 'first_name', 'last_name', 'birth_date', 'client_type', 'address', 'is_premium'])):
            print('Niepoprawne zapytanie!')
            return

        if 'address' in query:
            if not set(query['address'].keys()).issubset(set(['city', 'street', 'number'])):
                print('Niepoprawny adres w zapytaniu!')
                return

        if 'client_type' in query:
            if not set(query['client_type'].keys()).issubset(set(['type'])):
                print('Niepoprawny typ klienta w zapytaniu!')
                return

        if '_id' in query.keys():
            query['_id'] = str(query['_id']) if isinstance(query['_id'], uuid.UUID) else query['_id']

        client_collection = get_collection('clients')
        res_list = list(client_collection.find(query))

        if len(res_list) == 0:
            print('Klient o wskazanych parametrach nie istnieje!')
            return

        if len(res_list) > 1:
            print('Zapytanie zwróciło więcej niż jednego klienta!')
            return

        client = res_list[0]
        return Client(**client)

    @staticmethod
    def get_all_clients() -> List[Client]:
        client_collection = get_collection('clients')
        clients_cursor = client_collection.find()

        clients = []
        for client in clients_cursor:
            clients.append(Client(**client))

        return clients

    @staticmethod
    def get_size() -> int:
        client_collection = get_collection('clients')
        return client_collection.count_documents({})

    @staticmethod
    @update_client_decorator
    def update_client(_id, new_value) -> None:
        client_collection = get_collection('clients')
        client_collection.update_one({'_id': _id}, {'$set': new_value})
        print('Pomyslnie zaaktualizowane dane klienta o UUID: {}'.format(_id))
        return _id

    @staticmethod
    def update_client_address(_id, city, street, number) -> None:
        _id = str(_id) if isinstance(_id, uuid.UUID) else _id
        client_collection = get_collection('clients')
        client = client_collection.find_one({'_id': _id})

        if client is None:
            print('Klient o takim id nie istnieje!')
            return
        else:
            address = Address(city=city, street=street, number=number)
            ClientManager.update_client(_id, {'address': address.__dict__})

    @staticmethod
    def change_client_type(_id, is_premium=False) -> None:
        _id = str(_id) if isinstance(_id, uuid.UUID) else _id
        client_collection = get_collection('clients')
        client = client_collection.find_one({'_id': _id})
        if client is None:
            print('Klient o takim id nie istnieje!')
            return
        else:
            if is_premium:
                client_type = PremiumClientType()
                ClientManager.update_client(_id, {'client_type': client_type.__dict__, 'is_premium': is_premium})
            else:
                client_type = ReducedClientType() if Client.get_age(client['birth_date']) < 5 or Client.get_age(
                    client['birth_date']) > 65 else NormalClientType()
                ClientManager.update_client(_id, {'client_type': client_type.__dict__, 'is_premium': is_premium})

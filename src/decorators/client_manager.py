import json

from src.config import cache_expire_time
from src.db import get_redis_client, config
from src.models import Client


def add_client_decorator(func):
    def inner(*args, **kwargs):
        redis_client = get_redis_client()
        client = func(*args, **kwargs)
        if client is not None:
            redis_client.set(f'Client:{client._id}', json.dumps(client.__dict__()), ex=cache_expire_time)
            print('Dodano klienta do cache.')
            return client
        else:
            print('Nie dodano klienta do cache')

    return inner


def get_client_decorator(func):
    def inner(**query):
        redis_client = get_redis_client()

        if '_id' in query.keys():
            cache_client = redis_client.get(f"Client:{query['_id']}")
            if cache_client is not None:
                print('Pobrano klienta z cache.')
                cache_client = json.loads(cache_client)
                return Client(**cache_client)

        print('Nie pobrano klienta z cache')
        return func(**query)

    return inner


def remove_client_decorator(func):
    def inner(*args, **kwargs):
        redis_client = get_redis_client()
        removed_client_id = func(*args, **kwargs)
        if removed_client_id is not None:
            redis_client.delete(f'Client:{removed_client_id}')
            print('Usunięto klienta z cache.')
        else:
            print('Nie usunięto klienta z cache')

    return inner

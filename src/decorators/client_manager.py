import json

from src.db import get_redis_client


def add_client_decorator(func):
    def inner(*args, **kwargs):
        redis_client = get_redis_client()
        client = func(*args, **kwargs)
        if client is not None:
            redis_client.set(f'Client:{client._id}', json.dumps(client.__dict__()))
            print('Dodano klienta do cache.')
        else:
            print('Nie dodano klienta do cache')

    return inner

import json
import unittest
import os

from src.db import config, get_redis_client
from src.managers.client_manager import ClientManager
from src.models import Client

config('.env.test')
client_manager = ClientManager()


class ClientManagerTest(unittest.TestCase):
    def setUp(self) -> None:
        client = client_manager.get_client(pesel="05885030733")
        if client is not None:
            client_manager.remove_client(_id=client._id)
            client = client_manager.get_client(pesel="05885030733")
            self.assertIsNone(client)

    def test_add_client(self):
        client = client_manager.get_client(pesel="05885030733")
        self.assertIsNone(client)

        client_manager.add_client('05885030733', 'Jacek', 'Pablo', '1/1/2020', False, 'Warszawa', 'Javowa', '1')

        client = client_manager.get_client(pesel="05885030733")
        self.assertIsNotNone(client)

        client_manager.remove_client(_id=client._id)

    def test_remove_client(self):
        client_manager.add_client('05885030733', 'Jacek', 'Pablo', '1/1/2020', False, 'Warszawa', 'Javowa', '1')
        client = client_manager.get_client(pesel="05885030733")
        self.assertIsNotNone(client)

        client_manager.remove_client(client._id)
        client = client_manager.get_client(pesel="05885030733")
        self.assertIsNone(client)

    def test_update_client(self):
        client_manager.add_client('05885030733', 'Jacek', 'Pablo', '1/1/2020', False, 'Warszawa', 'Javowa', '1')
        client = client_manager.get_client(pesel="05885030733")
        self.assertIsNotNone(client)
        self.assertFalse(client.is_premium)

        client_manager.change_client_type(_id=client._id, is_premium=True)
        client = client_manager.get_client(_id=client._id)
        self.assertTrue(client.is_premium)

        client_manager.remove_client(client._id)

    def test_add_client_cache(self):
        client = client_manager.get_client(pesel="05885030733")
        self.assertIsNone(client)

        client_manager.add_client('05885030733', 'Jacek', 'Pablo', '1/1/2020', False, 'Warszawa', 'Javowa', '1')

        client = client_manager.get_client(pesel="05885030733")
        self.assertIsNotNone(client)

        redis_client = get_redis_client()
        cache_client = redis_client.get(f"Client:{client._id}")
        self.assertIsNotNone(cache_client)

        client_manager.remove_client(_id=client._id)

    def test_remove_client_cache(self):
        redis_client = get_redis_client()

        client_manager.add_client('05885030733', 'Jacek', 'Pablo', '1/1/2020', False, 'Warszawa', 'Javowa', '1')
        client = client_manager.get_client(pesel="05885030733")
        self.assertIsNotNone(client)

        cache_client = redis_client.get(f"Client:{client._id}")
        self.assertIsNotNone(cache_client)

        client_id = client._id

        client_manager.remove_client(client._id)
        client = client_manager.get_client(pesel="05885030733")
        self.assertIsNone(client)

        cache_client = redis_client.get(f"Client:{client_id}")
        self.assertIsNone(cache_client)

    def test_update_client_cache(self):
        redis_client = get_redis_client()

        # Before
        client_manager.add_client('05885030733', 'Jacek', 'Pablo', '1/1/2020', False, 'Warszawa', 'Javowa', '1')
        client = client_manager.get_client(pesel="05885030733")
        self.assertIsNotNone(client)
        self.assertFalse(client.is_premium)

        cache_client_res = redis_client.get(f"Client:{client._id}")
        cache_client_json = json.loads(cache_client_res)
        cache_client = Client(**cache_client_json)
        self.assertIsNotNone(cache_client)
        self.assertFalse(cache_client.is_premium)

        # After
        client_manager.change_client_type(_id=client._id, is_premium=True)
        client = client_manager.get_client(_id=client._id)
        self.assertTrue(client.is_premium)

        cache_client_res = redis_client.get(f"Client:{client._id}")
        cache_client_json = json.loads(cache_client_res)
        cache_client = Client(**cache_client_json)
        self.assertTrue(cache_client.is_premium)

        client_manager.remove_client(client._id)


if __name__ == '__main__':
    unittest.main()

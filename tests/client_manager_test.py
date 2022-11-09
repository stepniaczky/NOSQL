import unittest
import os
from datetime import date

os.chdir("..")
from src.db import config

config('.env.test')

from src.managers.client_manager import ClientManager

client_manager = ClientManager()


class ClientManagerTest(unittest.TestCase):
    def setUp(self) -> None:
        client = client_manager.get_client(pesel="05885030733")
        if client != None:
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


if __name__ == '__main__':
    unittest.main()

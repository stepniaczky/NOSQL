import unittest
import os

from src.db import config
from src.managers.ticket_manager import TicketManager
from src.managers.client_manager import ClientManager
from src.managers.movie_manager import MovieManager

os.chdir("..")
config('.env.test')

ticket_manager = TicketManager()
client_manager = ClientManager()
movie_manager = MovieManager()


class TicketManagerTest(unittest.TestCase):
    def test_buy_ticket(self):
        client_manager.add_client('12345678901', 'Jan', 'Kowalski', '1/1/2020', False, 'Warszawa', 'Koszykowa', '1')
        client_manager.add_client('12345678903', 'Jacek', 'Pablo', '1/1/2001', False, 'Warszawa', 'Javowa', '1')
        client_manager.add_client('12345678904', 'Jacek', 'Pablo', '1/1/2001', False, 'Warszawa', 'Javowa', '1')
        movie_manager.add_movie('Pulp Fiction', 'Dramat', 18, 3, 1)

        client_id = client_manager.get_client(pesel='12345678903')._id
        movie_id = movie_manager.get_movie(hall=3)._id

        ticket_manager.buy_ticket(client_id, movie_id)
        ticket_manager.buy_ticket(2, 1)
        ticket_manager.buy_ticket(3, 1)

        ticket1 = ticket_manager.get_ticket(client_id=client_id)

        self.assertIsNotNone(ticket1)


if __name__ == '__main__':
    unittest.main()

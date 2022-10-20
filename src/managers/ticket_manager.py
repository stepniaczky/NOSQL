from src.models import Ticket, Client, Movie, ClientType
from src.helpers.get_age import get_age

from sqlalchemy import update


class TicketManager:
    def __init__(self, session):
        self.session = session

    def get_ticket(self, ticket_id):
        with self.session() as session:
            ticket = session.query(Ticket).get(ticket_id)

            if ticket is None:
                print('Bilet o takim id nie istnieje!')

            return ticket

    def get_all_tickets(self):
        with self.session() as session:
            tickets = session.query(Ticket).all()
            return tickets

    def buy_ticket(self, client_id, movie_id):
        with self.session() as session:
            client = session.query(Client).get(client_id)
            movie = session.query(Movie).get(movie_id)

            if client is None or movie is None:
                print('Podany użytkownik lub film nie istnieje!')
                return

            if get_age(client.birth_date) < movie.min_age:
                print('Użytkownik nie spełnia wymagań wiekowych!')
                return

            arr = movie.free_slots
            for i, slot in enumerate(arr):
                if slot is True:
                    arr[i] = False
                    movie.free_slots = arr
                    stmt = (
                        update(Movie)
                        .where(Movie.id == movie_id)
                        .values(free_slots=arr)
                        .execution_options(synchronize_session="fetch")
                    )
                    session.execute(stmt)
                    session.commit()

                    client_type_id = client.client_type_id
                    client_type = session.query(ClientType).get(client_type_id)
                    price = client_type.apply_discount(25)

                    id = 1
                    while True:
                        if session.query(Ticket).get(id) is None:
                            break
                        id += 1

                    ticket = Ticket(id=id, base_price=price,
                                    client_id=client_id, movie_id=movie_id)

                    session.add(ticket)
                    session.commit()
                    return

            print('Niestety skonczyly sie miejsca na ten film!')
            return

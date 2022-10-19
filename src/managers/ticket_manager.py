from src.models import Ticket, Client, Movie


class TicketManager:
    def __init__(self, session):
        self.session = session

    def get_ticket(self, ticket_id):
        with self.session() as session:
            ticket = session.query(Ticket).get(ticket_id)

            if ticket is None:
                print('Film o takim id nie istnieje!')

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

            # dodać tutaj sprawdzanie wieku

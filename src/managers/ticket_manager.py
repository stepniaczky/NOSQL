from src.models import Ticket


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

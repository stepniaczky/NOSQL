from db import get_session, init_db, get_engine_from_env
from src.managers.movie_manager import MovieManager
from src.managers.ticket_manager import TicketManager

engine = get_engine_from_env()
init_db(engine)
session = get_session(engine)

movieManager = MovieManager(session)
ticketManager = TicketManager(session)

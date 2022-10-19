from datetime import date

from db import get_session, init_db, get_engine_from_env
from src.managers.client_manager import ClientManager

engine = get_engine_from_env()
init_db(engine)
sessionmaker = get_session(engine)

# movieManager = MovieManager(sessionmaker)
# movieManager.add_movie()

client_manager = ClientManager(sessionmaker)
client_manager.add_client(11122233344, "Imie", "Nazwisko", date(2001, 1, 11), True, "Lodz", "Ketlinga", 13)

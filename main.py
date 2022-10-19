from src.db import get_session, init_db, get_engine_from_env

engine = get_engine_from_env()
init_db(engine)
session = get_session(engine)

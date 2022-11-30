from pymongo import MongoClient
from dotenv import dotenv_values
from pathlib import Path
from redis import Redis

ROOT_DIR = Path(__file__).resolve().parent.parent


hash_prefix = {
    'client': 'Client:',
    'movie': 'Movie:'
}


def config(env_name='.env'):
    global CONFIG
    CONFIG = dotenv_values(ROOT_DIR / env_name)
    keys = ['USER', 'PASSWD', 'HOST', 'PORT', 'DB', 'REDIS_HOST', 'REDIS_PORT', 'REDIS_PASSWD']

    if not all([key in keys for key in CONFIG.keys()]):
        raise Exception('Bad config file')

    mongo_db_client()
    redis_db_client()


def mongo_db_client():
    connection_string = f"mongodb://{CONFIG['USER']}:{CONFIG['PASSWD']}@{CONFIG['HOST']}:{CONFIG['PORT']}/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@{CONFIG['USER']}@"

    global MONGODB_CLIENT
    MONGODB_CLIENT = MongoClient(connection_string)


def redis_db_client():
    global REDIS_CLIENT
    REDIS_CLIENT = Redis(
        host=CONFIG['REDIS_HOST'],
        port=CONFIG['REDIS_PORT'],
        password=CONFIG['REDIS_PASSWD'],
        decode_responses=True
    )


def get_redis_client():
    return REDIS_CLIENT


def get_collection(collection_name):
    db = MONGODB_CLIENT[CONFIG['DB']]
    if collection_name not in db.list_collection_names():
        db.command({'customAction': "CreateCollection", 'collection': collection_name})
        print("Created collection {}".format(collection_name))

    return db[collection_name]

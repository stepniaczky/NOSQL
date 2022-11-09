from pymongo import MongoClient
from dotenv import dotenv_values
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT_DIR / '.env'

def config():
    global CONFIG
    CONFIG = dotenv_values(CONFIG_PATH)
    keys = ['DRIVER', 'USER', 'PASSWD', 'HOST', 'PORT', 'DB']

    if not all([key in keys for key in CONFIG.keys()]):
        raise Exception('Bad config file')
    
    connection_string = f"{CONFIG['DRIVER']}://{CONFIG['USER']}:{CONFIG['PASSWD']}@{CONFIG['HOST']}:{CONFIG['PORT']}/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@{CONFIG['USER']}@"

    global CLIENT
    CLIENT = MongoClient(connection_string)


def get_collection(collection_name):
    db = CLIENT[CONFIG['DB']]
    if collection_name not in db.list_collection_names():
        db.command({'customAction': "CreateCollection", 'collection': collection_name})
        print("Created collection {}". format(collection_name))
        
    return db[collection_name]

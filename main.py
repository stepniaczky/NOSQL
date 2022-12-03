from src.db import config
from src.managers.client_manager import ClientManager


def main():
    config()
    client_manager = ClientManager()

    added_client = client_manager.add_client('11155111123', 'Huan', 'Pablo', '5/5/2020', False, 'Warszawa', 'Javowa', '1')

    if added_client is not None:
        got_client = client_manager.get_client(_id=added_client._id)
        client_manager.remove_client(got_client._id)


if __name__ == '__main__':
    main()

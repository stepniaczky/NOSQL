from src.db import config
from src.managers.client_manager import ClientManager


def main():
    config()
    client_manager = ClientManager()
    client_manager.add_client('99999999991', 'Huan', 'Pablo', '5/5/2020', False, 'Warszawa', 'Javowa', '1')


if __name__ == '__main__':
    main()

from src.db import config
from src.managers.client_manager import ClientManager


def main():
    config()
    client_manager = ClientManager()
    # client_manager.add_client('99999999999', 'Huan', 'Pablo', '5/5/2020', False, 'Warszawa', 'Javowa', '1')
    client_manager.get_client(_id='05ba4794-124b-41ce-8693-ccf8201bdbc0')


if __name__ == '__main__':
    main()

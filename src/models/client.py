import uuid

from dataclasses import dataclass, field
from datetime import datetime

from src.models.address import Address
from src.models.client_type import NormalClientType, ReducedClientType, PremiumClientType, ClientType

@dataclass
class Client:
    pesel: str
    first_name: str
    last_name: str
    birth_date: datetime.date
    client_type: ClientType
    address: Address
    id: uuid.uuid4 = field(default_factory=uuid.uuid4)
    
    def __post_init__(self):
        self.id = uuid.UUID(self.id) if isinstance(self.id, str) else self.id
        self.birth_date = datetime.strptime(self.birth_date, '%d/%m/%Y').date() 
        self.client_type = self.client_type_obj(**self.client_type) if isinstance(self.client_type, dict) else self.client_type
        self.address = Address(**self.address) if isinstance(self.address, dict) else self.address
        
    @staticmethod
    def client_type_obj(**_dict):
        if _dict['type'] == 'normal':
            return NormalClientType()
        if _dict['type'] == 'reduced':
            return ReducedClientType()
        else:
            return PremiumClientType()
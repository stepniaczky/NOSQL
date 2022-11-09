import uuid

from dataclasses import dataclass, field
from datetime import datetime, date

from src.models.address import Address
from src.models.client_type import NormalClientType, ReducedClientType, PremiumClientType, ClientType

@dataclass
class Client:
    pesel: str
    first_name: str
    last_name: str
    birth_date: str
    client_type: ClientType
    address: Address
    is_premium: str
    _id: uuid.uuid4 = field(default_factory=uuid.uuid4)
    
    def __post_init__(self):
        self._id = uuid.UUID(self._id) if isinstance(self._id, str) else self._id 
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
        
    def __dict__(self):
        return {
            '_id': str(self._id),
            'pesel': self.pesel,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date,
            'client_type': self.client_type.__dict__,
            'address': self.address.__dict__,
            'is_premium': self.is_premium
        }
        
    @staticmethod
    def get_age(birth_date) -> int:
        birth_date = datetime.strptime(birth_date, '%d/%m/%Y').date()

        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
import uuid

from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Ticket:
    date: datetime.date
    client_id: uuid.uuid4
    movie_id: uuid.uuid4
    base_price: float = field(default=25.0)
    id: uuid.uuid4 = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        self.id = uuid.uuid4() if isinstance(self.id, str) else self.id
        self.date = datetime.strptime(self.date, '%d/%m/%Y').date()
        self.client_id = uuid.UUID(self.client_id) if isinstance(self.client_id, str) else self.client_id 
        self.movie_id = uuid.UUID(self.movie_id) if isinstance(self.movie_id, str) else self.movie_id

import uuid

from dataclasses import dataclass, field

@dataclass
class Ticket:
    date: str
    client_id: uuid.uuid4
    movie_id: uuid.uuid4
    base_price: float = field(default=25.0)
    _id: uuid.uuid4 = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        self._id = uuid.UUID(self._id) if isinstance(self._id, str) else self._id
        self.client_id = uuid.UUID(self.client_id) if isinstance(self.client_id, str) else self.client_id 
        self.movie_id = uuid.UUID(self.movie_id) if isinstance(self.movie_id, str) else self.movie_id

    def __dict__(self):
        return {
        '_id': str(self._id),
        'date': self.date,
        'client_id': str(self.client_id),
        'movie_id': str(self.movie_id),
        'base_price': self.base_price,
    }
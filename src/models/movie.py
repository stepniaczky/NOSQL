import uuid

from dataclasses import dataclass, field
from typing import List

@dataclass
class Movie:
    title: str
    genre: str
    min_age: int
    hall: int
    free_slots: List[bool]
    id: uuid.uuid4 = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        self.id = uuid.uuid4() if isinstance(self.id, str) else self.id
        self.free_slots = [True] * self.free_slots
import uuid
import ast

from dataclasses import dataclass, field
from typing import List

@dataclass
class Movie:
    title: str
    genre: str
    min_age: int
    hall: int
    free_slots: List[bool]
    _id: uuid.uuid4 = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        self._id = uuid.UUID(self._id) if isinstance(self._id, str) else self._id
        self.free_slots = [True] * self.free_slots if isinstance(self.free_slots, int) else self.free_slots
        
    def __dict__(self):
        return {
        '_id': str(self._id),
        'title': self.title,
        'genre': self.genre,
        'min_age': self.min_age,
        'hall': self.hall,
        'free_slots': self.free_slots,
    }
        
    def __str__(self) -> str:
        return f'Title: "{self.title}", Genre: ({self.genre}), Min age: {self.min_age}, ' + \
                f'Hall: {self.hall}, Free slots: {len([x for x in self.free_slots if x is True])}'
    
    def check_if_free(self, slot: int) -> bool:
        return self.free_slots[slot - 1]
    
    def set_free_slot(self, slot: int) -> bool:
        if self.check_if_free(slot):
            self.free_slots[slot - 1] = False
            return True
        else:
            return False
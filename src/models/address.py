from dataclasses import dataclass

@dataclass
class Address:
    city: str
    street: str
    number: int
    
    def __str__(self) -> str:
        return f'{self.city}, {self.street} {self.number}'
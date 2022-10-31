from dataclasses import dataclass
from abc import ABC, abstractmethod


class ClientType(ABC):
    @abstractmethod
    def apply_discount(price: float):
        pass

@dataclass
class NormalClientType(ClientType):
    type: str = 'normal'
    
    @staticmethod
    def apply_discount(price: float):
        return price

@dataclass
class ReducedClientType(ClientType):
    type: str = 'reduced'

    @staticmethod
    def apply_discount(price: float):
        return price * 0.5

@dataclass
class PremiumClientType(ClientType):
    type: str = 'premium'

    @staticmethod
    def apply_discount(price: float):
        return price * 0.1

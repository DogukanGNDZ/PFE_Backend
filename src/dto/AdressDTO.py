from dataclasses import dataclass


@dataclass
class AdressDTO:
    id: str
    street: str
    number: int
    city: str
    country: str

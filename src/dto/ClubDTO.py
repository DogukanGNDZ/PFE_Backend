from dataclasses import dataclass


@dataclass
class ClubDTO:
    id: str
    name: str
    email: str
    password: str
    id_manager: str

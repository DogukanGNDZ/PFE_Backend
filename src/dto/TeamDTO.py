from dataclasses import dataclass


@dataclass
class TeamDTO:
    id: str
    category: str
    number_players: int

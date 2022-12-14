from dataclasses import dataclass
import datetime


@dataclass
class ClubDTO:
    id: str
    name: str
    email: str
    password: str
    description: str
    number_teams: int
    creation_date: datetime
    picture: str
    picture_banner: str

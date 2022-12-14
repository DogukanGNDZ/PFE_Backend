from dataclasses import dataclass


@dataclass
class CoachDTO:
    id: str
    firstname: str
    lastname: str
    age: int
    email: str
    password: str
    number_year_experience: int
    description: str
    picture: str
    picture_banner: str

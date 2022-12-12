from dataclasses import dataclass

@dataclass
class UserDTO:
    id: str
    firstname: str
    lastname: str
    age: int
    email: str
    password: str
    size: float
    weight: float
    post: str
    number_year_experience: int
    description: str
    picture: str


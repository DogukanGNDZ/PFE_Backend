from dataclasses import dataclass

@dataclass
class UserDTO:
    id : str
    firstname : str
    lastname : str
    age : int
    email : str
    password : str

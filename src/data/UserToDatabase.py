from neo4j import GraphDatabase
from src.dto.UserDTO import *
import os
from dotenv import load_dotenv
from dataclasses import asdict

load_dotenv()
host = os.getenv("HOST")
user = os.getenv("USER")
password = os.getenv("AUTH")


# Connect to the database
graph = GraphDatabase.driver(host, auth=(user, password))


def create_user(user_dto: UserDTO):
    with graph.session() as session:
        # Create the new user in the Neo4j database
        result = session.run('CREATE (u:User $user_properties) RETURN u', user_properties=asdict(user_dto))

        user = result.single().data()['u']
        user.pop('password', None)

        # Return the result of the query
        return user

def fetch_user(id: str):
    with graph.session() as session:
        result = session.run('MATCH (u:User) WHERE u.id = $id RETURN u', id = id)
        
        user = result.single().data()['u']
        user.pop('password', None)

        # Return the result of the query
        return user
        
def fetch_all_users():
    with graph.session() as session:
        result = session.run('MATCH (u:User) RETURN u')

        users = []

        for user in result:
            u = user.data()['u']
            u.pop('password', None)
            users.append(u)

        # Return the result of the query
        return users
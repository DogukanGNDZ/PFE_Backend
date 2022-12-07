from neo4j import GraphDatabase
from src.dto.UserDTO import *
import os
from dotenv import load_dotenv
from dataclasses import asdict

load_dotenv()
host=os.getenv("HOST")
user=os.getenv("USER")
password=os.getenv("PWD")

# Connect to the database
graph = GraphDatabase.driver(host, auth=(user, password))

def create_user(user_dto: UserDTO):
    with graph.session() as session:
        # Create the new user in the Neo4j database
        result = session.run('CREATE (u:User $user_properties) RETURN u', user_properties=asdict(user_dto))

        for row in result:
            return row["u"]["id"]

        # user = row.items()

        # print(user)

        # Return the result of the query
        return result
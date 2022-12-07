from py2neo import Graph
from src.DTO.UserDTO import *

graph = Graph(host='localhost', user='neo4j', password='password')


def create_user(user_dto: UserDTO):
    # Create the new user in the Neo4j database
    result = graph.run('CREATE (u:User $user_properties) RETURN u', user_properties=user_dto.to_dict())

    # Return the result of the query
    return result
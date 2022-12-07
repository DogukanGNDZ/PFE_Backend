from py2neo import Graph
from src.DTO.UserDTO import *
import configparser

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the contents of the properties file
config.read('prop.ini')
# Connect to the database
graph = Graph(host=config['DEFAULT']['neo4j.host'], user=config['DEFAULT']['neo4j.user'], password=config['DEFAULT']['neo4j.pwd'])


def create_user(user_dto: UserDTO):
    # Create the new user in the Neo4j database
    result = graph.run('CREATE (u:User $user_properties) RETURN u', user_properties=user_dto.to_dict())

    # Return the result of the query
    return result
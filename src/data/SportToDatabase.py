from neo4j import GraphDatabase
from flask import make_response
from src.dto.SportDTO import *
import os
import bcrypt
from dotenv import load_dotenv
from dataclasses import asdict

load_dotenv()
host = os.getenv("HOST")
user = os.getenv("USER")
password = os.getenv("AUTH")

# Connect to the database
graph = GraphDatabase.driver(host, auth=(user, password))


def create_sport(sport_dto: SportDTO):
    with graph.session() as session:
        # Create the new user in the Neo4j database
        result = session.run(
            'CREATE (s:Sport $sport_properties) RETURN s', sport_properties=asdict(sport_dto))

        sport = result.single().data()['s']

        # Return the result of the query
        return sport


def fetch_sport(id: str):
    with graph.session() as session:
        result = session.run(
            'MATCH (s:Sport) WHERE s.id = $id RETURN s', id=id)

        sport = result.single().data()['s']

        # Return the result of the query
        return sport


def fetch_all_sports():
    with graph.session() as session:
        result = session.run('MATCH (s:Sport) RETURN s')

        sports = []

        for sport in result:
            s = sport.data()['s']
            sports.append(s)

        # Return the result of the query
        return sports

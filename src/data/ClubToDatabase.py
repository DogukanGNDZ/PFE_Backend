from neo4j import GraphDatabase
from flask import make_response
from src.dto.ClubDTO import *
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


def create_club(club_dto: ClubDTO):
    with graph.session() as session:
        # Create the new user in the Neo4j database
        result = session.run(
            'CREATE (c:Club $club_properties) RETURN c', club_properties=asdict(club_dto))

        club = result.single().data()['c']
        club.pop('password', None)

        # Return the result of the query
        return club


def fetch_club(id: str):
    with graph.session() as session:
        result = session.run('MATCH (c:Club) WHERE c.id = $id RETURN c', id=id)

        club = result.single().data()['c']
        club.pop('password', None)

        # Return the result of the query
        return club


def fetch_all_clubs():
    with graph.session() as session:
        result = session.run('MATCH (c:Club) RETURN c')

        clubs = []

        for club in result:
            c = club.data()['c']
            c.pop('password', None)
            clubs.append(c)

        # Return the result of the query
        return clubs

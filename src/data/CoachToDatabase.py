from neo4j import GraphDatabase
from flask import make_response
from src.dto.CoachDTO import *
import os
import bcrypt
from dotenv import load_dotenv
from dataclasses import asdict

#load_dotenv()
host = "neo4j+s://12828f8f.databases.neo4j.io"
user = "neo4j"
password = "Tr8BU5ry7T3C4CDxKYXB0KvLRssd1Mm7EkzuQ12Rxyo"

# Connect to the database
graph = GraphDatabase.driver(host, auth=(user, password))


def create_coach(coach_dto: CoachDTO):
    with graph.session() as session:
        # Create the new user in the Neo4j database
        result = session.run(
            'CREATE (co:Coach $coach_properties) RETURN co', coach_properties=asdict(coach_dto))

        coach = result.single().data()['co']
        coach.pop('password', None)

        # Return the result of the query
        return coach


def fetch_coach(id: str):
    with graph.session() as session:
        result = session.run(
            'MATCH (co:Coach) WHERE co.id = $id RETURN co', id=id)

        coach = result.single().data()['co']
        coach.pop('password', None)

        # Return the result of the query
        return coach


def fetch_all_coachs():
    with graph.session() as session:
        result = session.run('MATCH (co:Coach) RETURN co')

        coachs = []

        for coach in result:
            co = coach.data()['co']
            co.pop('password', None)
            coachs.append(co)

        # Return the result of the query
        return coachs

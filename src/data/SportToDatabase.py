from neo4j import GraphDatabase
from flask import make_response
from src.dto.SportDTO import *
import os
from dotenv import load_dotenv
from dataclasses import asdict

load_dotenv()
host = os.getenv("HOST")
user = os.getenv("USR")
password = os.getenv("AUTH")

# Connect to the database
graph = GraphDatabase.driver(host, auth=(user, password))


def create_sport_data(sport_dto: SportDTO):
    with graph.session() as session:
        # Create the new user in the Neo4j database
        print("in")
        result = session.run(
            'CREATE (s:Sport $sport_properties) RETURN s', sport_properties=asdict(sport_dto))

        sport = result.single().data()['s']

        # Return the result of the query
        return sport


def fetch_sport(id: str):
    with graph.session() as session:
        result = session.run(
            'MATCH (s:Sport) WHERE s.id = $id RETURN s', id=id)
        if (not result.peek()):
            return None

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


def update_sport(sport: str, role: str, email: str):
    with graph.session() as session:
        if (role == "player"):
            session.run(
                'MATCH (p:User)-[r:PRATIQUE]->(old:Sport) WHERE p.email= $email DELETE r', email=email)
            session.run(
                'MATCH (p:User) MATCH (s:Sport) WHERE p.email= $email AND s.name = $name CREATE (p)-[rel:PRATIQUE]->(s)', email=email, name=sport)
            return True
        elif (role == "coach"):
            session.run(
                'MATCH (p:Coach)-[r:PRATIQUE]->(old:Sport) WHERE p.email= $email DELETE r', email=email)
            session.run(
                'MATCH (p:Coach) MATCH (s:Sport) WHERE p.email= $email AND s.name = $name CREATE (p)-[rel:PRATIQUE]->(s)', email=email, name=sport)
            return True
        elif (role == "club"):
            session.run(
                'MATCH (p:Club)-[r:PRATIQUE]->(old:Sport) WHERE p.email= $email DELETE r', email=email)
            session.run(
                'MATCH (p:Club) MATCH (s:Sport) WHERE p.email= $email AND s.name = $name CREATE (p)-[rel:PRATIQUE]->(s)', email=email, name=sport)
            return True
        else:
            return False


def fetch_user_sport(role: str, email: str):
    with graph.session() as session:
        if (role == "player"):
            result = session.run(
                'MATCH (p:User)-[r:PRATIQUE]->(old:Sport) WHERE p.email= $email RETURN old', email=email)
            sports = []
            for sport in result:
                a = sport.data()['old']
                sports.append(a)
            return sports
        elif (role == "coach"):
            result = session.run(
                'MATCH (p:Coach)-[r:PRATIQUE]->(old:Sport) WHERE p.email= $email RETURN old', email=email)
            sports = []
            for sport in result:
                a = sport.data()['old']
                sports.append(a)
            return sports
        elif (role == "club"):
            result = session.run(
                'MATCH (p:Club)-[r:PRATIQUE]->(old:Sport) WHERE p.email= $email RETURN old', email=email)
            sports = []
            for sport in result:
                a = sport.data()['old']
                sports.append(a)
            return sports
        else:
            return []

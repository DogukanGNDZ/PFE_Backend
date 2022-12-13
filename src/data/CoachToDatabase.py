from neo4j import GraphDatabase
from flask import make_response
from src.dto.CoachDTO import *
import os
import bcrypt
from dotenv import load_dotenv
from dataclasses import asdict

load_dotenv()
host = os.getenv("HOST")
user = os.getenv("USR")
password = os.getenv("AUTH")

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

        if(not result.peek()): return None

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


def apply_for_club_coach(email_coach: str, email_club: str):
    with graph.session() as session:
        print(email_coach)
        print(email_club)
        session.run(
            'MATCH (p:Coach)-[r:APPLY_FOR_COACH]->(c:Club) WHERE p.email= $email AND c.email = $name DELETE r', email=email_coach, name=email_club)
        session.run(
            'MATCH (u:Coach), (c:Club) WHERE u.email= $email AND c.email = $name CREATE (u)-[r:APPLY_FOR_COACH]->(c)', email=email_coach, name=email_club)


def get_coach_club(email_user: str):
    with graph.session() as session:
        result = session.run(
            'MATCH (p:Coach)-[r:COACH_OF]->(c:Club) WHERE p.email = $name return c', name=email_user)

        clubs = []

        for club in result:
            u = club.data()['c']
            u.pop('password', None)
            clubs.append(u)

        return clubs


def leave_club(email_coach: str, email_club: str):
    with graph.session() as session:
        result = session.run(
            'MATCH (p:Coach)-[r:COACH_OF]->(c:Club) WHERE p.email = $name AND c.email = $email DELETE r return p', name=email_coach, email=email_club)

        if(not result.peek()): return False
        return True


def is_member(email_coach: str):
    with graph.session() as session:
        result = session.run(
            'MATCH (p:Coach)-[r:COACH_OF]->(c:Club) WHERE p.email = $name RETURN COUNT(r)>0 AS d', name=email_coach)
        data = result.single().data()

        club = data["d"]
        return club

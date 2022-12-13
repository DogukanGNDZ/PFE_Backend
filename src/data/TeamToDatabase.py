from neo4j import GraphDatabase
from flask import make_response
from src.dto.TeamDTO import *
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


def create_team(team_dto: TeamDTO, email_club: str):
    with graph.session() as session:
        # Create the new user in the Neo4j database
        result = session.run(
            'CREATE (t:Team $team_properties) RETURN t', team_properties=asdict(team_dto))
        session.run(
            'MATCH (t:Team),(c:Club) WHERE t.id = $id AND c.email = $email SET c.number_teams = c.number_teams+1 CREATE (t)-[r:TEAM_DE]->(c)', id=team_dto.id, email=email_club)
        team = result.single().data()['t']

        # Return the result of the query
        return team


def fetch_team(id: str):
    with graph.session() as session:
        result = session.run('MATCH (t:Team) WHERE t.id = $id RETURN t', id=id)

        if (not result.peek()):
            return None

        team = result.single().data()['t']

        # Return the result of the query
        return team


def fetch_all_teams():
    with graph.session() as session:
        result = session.run('MATCH (t:Team) RETURN t')

        teams = []

        for team in result:
            t = team.data()['t']
            teams.append(t)

        # Return the result of the query
        return teams


def add(team_id: str, email: str):
    with graph.session() as session:
        result = session.run(
            'MATCH (u:User), (t:Team) WHERE u.email = $email AND t.id = $team_id CREATE (u)-[r:CONSTITUE]->(t) RETURN u, t, r', email=email, team_id=team_id)

        if (result.peek()):
            return True
        else:
            return False


def remove(team_id: str, email: str):
    with graph.session() as session:
        result = session.run(
            'MATCH (u:User)-[r:CONSTITUE]->(t:Team) WHERE u.email = $email AND t.id = $team_id DELETE r RETURN u, t', email=email, team_id=team_id)

        if (result.peek()):
            return True
        else:
            return False

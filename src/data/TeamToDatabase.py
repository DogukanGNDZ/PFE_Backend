from neo4j import GraphDatabase
from flask import make_response
from src.dto.TeamDTO import *
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


def create_team(team_dto: TeamDTO):
    with graph.session() as session:
        # Create the new user in the Neo4j database
        result = session.run(
            'CREATE (t:Team $team_properties) RETURN t', team_properties=asdict(team_dto))

        team = result.single().data()['t']

        # Return the result of the query
        return team


def fetch_team(id: str):
    with graph.session() as session:
        result = session.run('MATCH (t:Team) WHERE t.id = $id RETURN t', id=id)

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

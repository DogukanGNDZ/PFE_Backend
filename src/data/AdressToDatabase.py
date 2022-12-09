from neo4j import GraphDatabase
from flask import make_response
from src.dto.AdressDTO import *
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


def create_adress(adress_dto: AdressDTO, email: str, role: str):
    with graph.session() as session:
        # Create the new user in the Neo4j database
        result = session.run(
            'CREATE (a:Adress $adress_properties) RETURN a', adress_properties=asdict(adress_dto))

        adress = result.single().data()['a']
        if (role == "player"):
            session.run(
                'MATCH (p:User) MATCH (a:Adress) WHERE p.email= $email AND a.id = $name CREATE (p)-[rel:LIVE_AT]->(a)', email=email, name=adress_dto.id)
        elif (role == "coach"):
            session.run(
                'MATCH (p:Coach) MATCH (a:Adress) WHERE p.email= $email AND a.id = $name CREATE (p)-[rel:LIVE_AT]->(a)', email=email, name=adress_dto.id)
        elif (role == "club"):
            session.run(
                'MATCH (p:Club) MATCH (a:Adress) WHERE p.email= $email AND a.id = $name CREATE (p)-[rel:LIVE_AT]->(a)', email=email, name=adress_dto.id)
        # Return the result of the query
        return adress


def fetch_adress(id: str):
    with graph.session() as session:
        result = session.run(
            'MATCH (a:Adress) WHERE a.id = $id RETURN a', id=id)

        adress = result.single().data()['a']

        # Return the result of the query
        return adress


def fetch_all_adress():
    with graph.session() as session:
        result = session.run('MATCH (a:Adress) RETURN a')

        adresses = []

        for adress in result:
            a = adress.data()['a']
            adresses.append(a)

        # Return the result of the query
        return adresses

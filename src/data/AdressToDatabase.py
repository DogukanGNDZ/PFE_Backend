from neo4j import GraphDatabase
from flask import make_response
from src.dto.AdressDTO import *
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


def create_adress(adress_dto: AdressDTO):
    with graph.session() as session:
        # Create the new user in the Neo4j database
        result = session.run(
            'CREATE (a:Adress $adress_properties) RETURN a', adress_properties=asdict(adress_dto))

        adress = result.single().data()['a']

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

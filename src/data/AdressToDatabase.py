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


def create_adress_data(adress_dto: AdressDTO, email: str, role: str, idOldAdress: str):
    with graph.session() as session:
        # Create the new user in the Neo4j database
        result = session.run(
            'CREATE (a:Adress $adress_properties) RETURN a', adress_properties=asdict(adress_dto))

        adress = result.single().data()['a']
        if (idOldAdress == ""):
            if (role == "player"):
                session.run(
                    'MATCH (p:User) MATCH (a:Adress) WHERE p.email= $email AND a.id = $name CREATE (p)-[rel:LIVE_AT]->(a)', email=email, name=adress_dto.id)
            elif (role == "coach"):
                session.run(
                    'MATCH (p:Coach) MATCH (a:Adress) WHERE p.email= $email AND a.id = $name CREATE (p)-[rel:LIVE_AT]->(a)', email=email, name=adress_dto.id)
            elif (role == "club"):
                session.run(
                    'MATCH (p:Club) MATCH (a:Adress) WHERE p.email= $email AND a.id = $name CREATE (p)-[rel:LIVE_AT]->(a)', email=email, name=adress_dto.id)
        else:
            if (role == "player"):
                session.run(
                    'MATCH (p:User)-[r:LIVE_AT]->(old:Adress) MATCH (a:Adress) WHERE p.email= $email AND a.id = $name AND old.id = $oldId CREATE (p)-[rel:LIVE_AT]->(a) DELETE r DELETE old', email=email, name=adress_dto.id, oldId=idOldAdress)
            elif (role == "coach"):
                session.run(
                    'MATCH (p:Coach)-[r:LIVE_AT]->(old:Adress) MATCH (a:Adress) WHERE p.email= $email AND a.id = $name AND old.id = $oldId CREATE (p)-[rel:LIVE_AT]->(a) DELETE r DELETE old', email=email, name=adress_dto.id, oldId=idOldAdress)
            elif (role == "club"):
                session.run(
                    'MATCH (p:Club)-[r:LIVE_AT]->(old:Adress) MATCH (a:Adress) WHERE p.email= $email AND a.id = $name AND old.id = $oldId CREATE (p)-[rel:LIVE_AT]->(a) DELETE r DELETE old', email=email, name=adress_dto.id, oldId=idOldAdress)
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


def fetch_user_adress(role: str, email: str):
    with graph.session() as session:
        if (role == "player"):
            result = session.run(
                'MATCH (p:User)-[r:LIVE_AT]->(old:Adress) WHERE p.email= $email RETURN old', email=email)
            adresses = []
            for adress in result:
                a = adress.data()['old']
                adresses.append(a)
            return adresses
        elif (role == "coach"):
            result = session.run(
                'MATCH (p:Coach)-[r:LIVE_AT]->(old:Adress) WHERE p.email= $email RETURN old', email=email)
            adresses = []
            for adress in result:
                a = adress.data()['old']
                adresses.append(a)
            return adresses
        elif (role == "club"):
            result = session.run(
                'MATCH (p:Club)-[r:LIVE_AT]->(old:Adress) WHERE p.email= $email RETURN old', email=email)
            adresses = []
            for adress in result:
                a = adress.data()['old']
                adresses.append(a)
            return adresses
        else:
            return []

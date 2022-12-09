from neo4j import GraphDatabase
from flask import make_response
from src.dto.UserDTO import *
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


def create_user(user_dto: UserDTO):
    with graph.session() as session:
        # Create the new user in the Neo4j database
        result = session.run(
            'CREATE (u:User $user_properties) RETURN u', user_properties=asdict(user_dto))

        user = result.single().data()['u']
        user.pop('password', None)

        # Return the result of the query
        return user


def fetch_user(id: str):
    with graph.session() as session:
        result = session.run('MATCH (u:User) WHERE u.id = $id RETURN u', id=id)

        user = result.single().data()['u']
        user.pop('password', None)

        # Return the result of the query
        return user


def check_user(password: str, email: str):
    with graph.session() as session:
        result = session.run(
            'MATCH (u:User) WHERE u.email = $email RETURN u LIMIT 1', email=email)
        for row in result:
            if (bcrypt.checkpw(password, row['u']['password'])):
                return True
            else:
                return False

        result = session.run(
            'MATCH (c:Club) WHERE c.email = $email RETURN c LIMIT 1', email=email)
        for row in result:
            if (bcrypt.checkpw(password, row['c']['password'])):
                return True
            else:
                return False

        result = session.run(
            'MATCH (co:Coach) WHERE co.email = $email RETURN co LIMIT 1', email=email)
        for row in result:
            if (bcrypt.checkpw(password, row['co']['password'])):
                return True
            else:
                return False
        return False


def fetch_all_users():
    with graph.session() as session:
        result = session.run('MATCH (u:User) RETURN u')

        users = []

        for user in result:
            u = user.data()['u']
            u.pop('password', None)
            users.append(u)

        # Return the result of the query
        return users


def update_user(user_dto: UserDTO):
    with graph.session() as session:
        print("data")
        result = session.run(
            'MATCH (u:User) WHERE u.email = $email SET u.firstname = $firstname, u.lastname = $lastname, u.age = $age,u.size = $size, u.weight = $weight, u.post = $post, u.number_year_experience = $nYE, u.description = $description, u.picture = $picture RETURN u',
            email=user_dto.email,
            firstname=user_dto.firstname,
            lastname=user_dto.lastname,
            age=user_dto.age,
            size=user_dto.size,
            weight=user_dto.weight,
            post=user_dto.post,
            nYE=user_dto.number_year_experience,
            description=user_dto.description,
            picture=user_dto.picture)

        user = result.single().data()['u']
        user.pop('password', None)

        # Return the result of the query
        return user

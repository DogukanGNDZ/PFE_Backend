from neo4j import GraphDatabase
from flask import make_response
from src.dto.UserDTO import *
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


def fetch_user_email(email: str):
    with graph.session() as session:
        result = session.run('MATCH (u:User) WHERE u.email = $email RETURN u', email=email)

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


def check_mail(email: str):
    with graph.session() as session:
      query = 'MATCH (u:User) WHERE u.email = $email RETURN u'
      result = session.run(query, email=email)
      if result.single():
        # If there is already a user with the given email, return an error make_response(400, {'error': 'Email address is already in use'})
        return True
      else : 
        return False
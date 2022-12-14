import json
from flask import make_response
from neo4j import GraphDatabase
from src.dto.UserDTO import *
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


def create_user(user_dto: UserDTO):
    with graph.session() as session:
        # Create the new user in the Neo4j database
        result = session.run(
            'CREATE (u:User $user_properties) RETURN u', user_properties=asdict(user_dto))
        if (not result.peek()):
            return None

        user = result.single().data()['u']
        user.pop('password', None)

        # Return the result of the query
        return user


def fetch_user(id: str):
    with graph.session() as session:
        result = session.run('MATCH (u:User) WHERE u.id = $id RETURN u', id=id)

        if (not result.peek()):
            return None
        user = result.single().data()['u']
        user.pop('password', None)

        # Return the result of the query
        return user


def fetch_user_email(email: str):
    with graph.session() as session:
        result = session.run(
            'MATCH (u:User) WHERE u.email = $email RETURN u, COUNT(u)>0 as d', email=email)
        if (result.peek()):
            user = result.single().data()['u']
            user.pop('password', None)
            return user
        else:
            result = session.run(
                'MATCH (c:Coach) WHERE c.email = $email RETURN c', email=email)
            if (result.peek()):
                coach = result.single().data()['c']
                coach.pop('password', None)
                return coach
            else:
                result = session.run(
                    'MATCH (cl:Club) WHERE cl.email = $email RETURN cl', email=email)
                if (result.peek()):
                    club = result.single().data()['cl']
                    date_str = club["creation_date"].strftime(
                        '%Y-%m-%d %H:%M:%S')
                    club["creation_date"] = json.dumps(date_str)
                    club.pop('password', None)
                    return club
                else:
                    return None


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
        else:
            query = 'MATCH (c:Coach) WHERE c.email = $email RETURN c'
            result = session.run(query, email=email)
            if result.single():
                # If there is already a user with the given email, return an error make_response(400, {'error': 'Email address is already in use'})
                return True
            else:
                query = 'MATCH (cl:Club) WHERE cl.email = $email RETURN cl'
                result = session.run(query, email=email)
                if result.single():
                    # If there is already a user with the given email, return an error make_response(400, {'error': 'Email address is already in use'})
                    return True
                else:
                    return False


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

        if (not result.peek()):
            return None
        user = result.single().data()['u']
        user.pop('password', None)

        # Return the result of the query
        return user


def apply_for_club_user(email_user: str, email_club: str):
    with graph.session() as session:

        session.run(
            'MATCH (u:User)-[r:APPLY_FOR_PLAYER]->(c:Club) WHERE u.email= $email AND c.email = $name DELETE r', email=email_user, name=email_club)
        session.run(
            'MATCH (u:User), (c:Club) WHERE u.email= $email AND c.email = $name CREATE (u)-[r:APPLY_FOR_PLAYER]->(c) RETURN u,c,r', email=email_user, name=email_club)


def get_user_club(email_user: str):
    with graph.session() as session:
        result = session.run(
            'MATCH (p:User)-[r:PLAYER_OF]->(c:Club) WHERE p.email = $name return c', name=email_user)

        clubs = []

        for club in result:
            u = club.data()['c']
            date_str = u["creation_date"].strftime('%Y-%m-%d %H:%M:%S')
            u["creation_date"] = json.dumps(date_str)
            u.pop('password', None)
            clubs.append(u)

        return clubs


def get_user_sport(email_user: str):
    with graph.session() as session:
        result = session.run(
            'MATCH (p:User)-[r:PRATIQUE]->(s:Sport) WHERE p.email = $name return s', name=email_user)

        sports = []

        for sport in result:
            u = sport.data()['s']
            u.pop('password', None)
            sports.append(u)

        return sports


def leave_club(email_user: str, email_club: str):
    with graph.session() as session:
        session.run(
            'MATCH (p:User)-[r:PLAYER_OF]->(c:Club) WHERE p.email = $name AND c.email = $email DELETE r', name=email_user, email=email_club)
        session.run(
            'MATCH (p:User)-[r:CONSTITUE]->(t:Team) WHERE p.email = $email DELETE r', email=email_user)


def is_member(email_user: str):
    with graph.session() as session:
        result = session.run(
            'MATCH (p:User)-[r:PLAYER_OF]->(c:Club) WHERE p.email = $name RETURN COUNT(r)>0 AS d', name=email_user)

        if (not result.peek()):
            return None
        data = result.single().data()

        club = data["d"]
        return club


def get_role_user(email: str):
    with graph.session() as session:
        resultPlayer = session.run(
            'MATCH (u:User) WHERE u.email = $email RETURN COUNT(u)>0 AS d', email=email).single().data()["d"]
        resultCoach = session.run(
            'MATCH (u:Coach) WHERE u.email = $email RETURN COUNT(u)>0 AS d', email=email).single().data()["d"]
        resultClub = session.run(
            'MATCH (u:Club) WHERE u.email = $email RETURN COUNT(u)>0 AS d', email=email).single().data()["d"]

        if (resultPlayer):
            return "player"
        elif (resultCoach):
            return "coach"
        elif (resultClub):
            return "club"
        else:
            return make_response("User not find", 400)


def search_user_data(role: str, sport: str, age: int, country: str, city: str, name: str):
    with graph.session() as session:
        print("in")
        if (role == "player"):
            result = session.run('MATCH (u:User) return u')
            users = []
            for user in result:
                u = user.data()['u']
                u.pop('password', None)
                users.append(u)

            if (sport != ""):
                users_sports = []
                for user in users:

                    if (session.run(
                            'MATCH (u:User)-[r:PRATIQUE]->(old:Sport) WHERE u.email = $email AND old.name = $name RETURN COUNT(r)>0 AS d', email=user["email"], name=sport).single().data()["d"]):
                        users_sports.append(user)
                users = users_sports
            if (age > 0):
                users_ages = []
                for user in users:
                    if (user["age"] == age):
                        users_ages.append(user)
                users = users_ages
            if (name != ""):
                users_names = []
                for user in users:
                    if (session.run('MATCH (u:User) WHERE (u.lastname STARTS WITH $name OR u.firstname STARTS WITH $name) AND u.email = $email RETURN COUNT(u)>0 AS d', name=name, email=user["email"]).single().data()["d"]):
                        users_names.append(user)
                users = users_names
            if (country != ""):
                users_country = []
                for user in users:
                    if (session.run('MATCH (u:User)-[r:LIVE_AT]->(old:Adress) WHERE u.email = $email AND old.country = $country RETURN COUNT(r)>0 AS d', email=user["email"], country=country).single().data()["d"]):
                        users_country.append(user)
                users = users_country

            if (city != ""):
                users_city = []
                for user in users:
                    if (session.run('MATCH (u:User)-[r:LIVE_AT]->(old:Adress) WHERE u.email = $email AND old.city = $city RETURN COUNT(r)>0 AS d', email=user["email"], city=city).single().data()["d"]):
                        users_city.append(user)
                users = users_city
            return users

        elif (role == "coach"):
            result = session.run('MATCH (u:Coach) return u')
            users = []
            for user in result:
                u = user.data()['u']
                u.pop('password', None)
                users.append(u)

            if (sport != ""):
                users_sports = []
                for user in users:

                    if (session.run(
                            'MATCH (u:Coach)-[r:PRATIQUE]->(old:Sport) WHERE u.email = $email AND old.name = $name RETURN COUNT(r)>0 AS d', email=user["email"], name=sport).single().data()["d"]):
                        users_sports.append(user)
                users = users_sports
            if (age > 0):
                users_ages = []
                for user in users:
                    if (user["age"] == age):
                        users_ages.append(user)
                users = users_ages
            if (name != ""):
                users_names = []
                for user in users:
                    if (session.run('MATCH (u:Coach) WHERE (u.lastname STARTS WITH $name OR u.firstname STARTS WITH $name) AND u.email = $email RETURN COUNT(u)>0 AS d', name=name, email=user["email"]).single().data()["d"]):
                        users_names.append(user)
                users = users_names
            if (country != ""):
                users_country = []
                for user in users:
                    if (session.run('MATCH (u:Coach)-[r:LIVE_AT]->(old:Adress) WHERE u.email = $email AND old.country = $country RETURN COUNT(r)>0 AS d', email=user["email"], country=country).single().data()["d"]):
                        users_country.append(user)
                users = users_country

            if (city != ""):
                users_city = []
                for user in users:
                    if (session.run('MATCH (u:Coach)-[r:LIVE_AT]->(old:Adress) WHERE u.email = $email AND old.city = $city RETURN COUNT(r)>0 AS d', email=user["email"], city=city).single().data()["d"]):
                        users_city.append(user)
                users = users_city
            return users
        else:
            result = session.run('MATCH (u:Club) return u')
            users = []
            for user in result:
                u = user.data()['u']
                u.pop('password', None)
                users.append(u)

            if (sport != ""):
                users_sports = []
                for user in users:

                    if (session.run(
                            'MATCH (u:Club)-[r:PRATIQUE]->(old:Sport) WHERE u.email = $email AND old.name = $name RETURN COUNT(r)>0 AS d', email=user["email"], name=sport).single().data()["d"]):
                        users_sports.append(user)
                users = users_sports
            if (name != ""):
                users_names = []
                for user in users:
                    if (session.run('MATCH (u:Club) WHERE u.name STARTS WITH $name AND u.email = $email RETURN COUNT(u)>0 AS d', name=name, email=user["email"]).single().data()["d"]):
                        users_names.append(user)
                users = users_names
            if (country != ""):
                users_country = []
                for user in users:
                    if (session.run('MATCH (u:Club)-[r:LIVE_AT]->(old:Adress) WHERE u.email = $email AND old.country = $country RETURN COUNT(r)>0 AS d', email=user["email"], country=country).single().data()["d"]):
                        users_country.append(user)
                users = users_country

            if (city != ""):
                users_city = []
                for user in users:
                    if (session.run('MATCH (u:Club)-[r:LIVE_AT]->(old:Adress) WHERE u.email = $email AND old.city = $city RETURN COUNT(r)>0 AS d', email=user["email"], city=city).single().data()["d"]):
                        users_city.append(user)
                users = users_city
            return users

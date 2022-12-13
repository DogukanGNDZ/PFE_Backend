from neo4j import GraphDatabase
from flask import make_response
from src.dto.NotificationDTO import *
import os
import json
from dotenv import load_dotenv
from dataclasses import asdict

load_dotenv()
host = os.getenv("HOST")
user = os.getenv("USR")
password = os.getenv("AUTH")

# Connect to the database
graph = GraphDatabase.driver(host, auth=(user, password))


def create_notification_data(notification_dto: NotificationDTO, role: str, email: str):
    with graph.session() as session:
        result = session.run(
            'CREATE (n:Notification $notification_properties) RETURN n', notification_properties=asdict(notification_dto))

        if (role == "player"):
            session.run(
                'MATCH (u:User),(n:Notification) WHERE u.email = $email AND n.id = $id CREATE (u)-[rel:HAS_RECEIVED]->(n)', email=email, id=notification_dto.id)
        elif (role == "coach"):
            session.run(
                'MATCH (u:Coach),(n:Notification) WHERE u.email = $email AND n.id = $id CREATE (u)-[rel:HAS_RECEIVED]->(n)', email=email, id=notification_dto.id)
        elif (role == "club"):
            session.run(
                'MATCH (u:Club),(n:Notification) WHERE u.email = $email AND n.id = $id CREATE (u)-[rel:HAS_RECEIVED]->(n)', email=email, id=notification_dto.id)

        notif = result.single().data()['n']
        date_str = notif["date_and_time"].strftime('%Y-%m-%d %H:%M:%S')
        notif["date_and_time"] = json.dumps(date_str)
        return notif


def fetch_notification(id: str):
    with graph.session() as session:
        result = session.run(
            'MATCH (n:Notification) WHERE n.id = $id RETURN n', id=id)

        notif = result.single().data()['n']
        date_str = notif["date_and_time"].strftime('%Y-%m-%d %H:%M:%S')
        notif["date_and_time"] = json.dumps(date_str)
        # Return the result of the query
        return notif


def fetch_all_notification():
    with graph.session() as session:
        result = session.run('MATCH (n:Notification) RETURN n')

        notifications = []

        for notif in result:
            n = notif.data()['n']
            date_str = n["date_and_time"].strftime('%Y-%m-%d %H:%M:%S')
            n["date_and_time"] = json.dumps(date_str)
            notifications.append(n)

        # Return the result of the query
        return notifications


def fetch_user_notification(role: str, email: str):
    with graph.session() as session:
        if (role == "player"):
            result = session.run(
                'MATCH (p:User)-[r:HAS_RECEIVED]->(n:Notification) WHERE p.email= $email AND n.etat="active" RETURN n', email=email)
            notifications = []
            for notif in result:
                n = notif.data()['n']
                date_str = n["date_and_time"].strftime('%Y-%m-%d %H:%M:%S')
                n["date_and_time"] = json.dumps(date_str)
                notifications.append(n)
            return notifications
        elif (role == "coach"):
            result = session.run(
                'MATCH (p:Coach)-[r:HAS_RECEIVED]->(n:Notification) WHERE p.email= $email AND n.etat="active" RETURN n', email=email)
            notifications = []
            for notif in result:
                n = notif.data()['n']
                date_str = n["date_and_time"].strftime('%Y-%m-%d %H:%M:%S')
                n["date_and_time"] = json.dumps(date_str)
                notifications.append(n)
            return notifications
        elif (role == "club"):
            result = session.run(
                'MATCH (p:Club)-[r:HAS_RECEIVED]->(n:Notification) WHERE p.email= $email AND n.etat="active" RETURN n', email=email)
            notifications = []
            for notif in result:
                n = notif.data()['n']
                date_str = n["date_and_time"].strftime('%Y-%m-%d %H:%M:%S')
                n["date_and_time"] = json.dumps(date_str)
                notifications.append(n)
            return notifications
        else:
            return []


def remove_all_notifications():
    with graph.session() as session:
        session.run(
            'MATCH (p:User)-[r:HAS_RECEIVED]->(n:Notification) DELETE r')
        session.run(
            'MATCH (p:Coach)-[r:HAS_RECEIVED]->(n:Notification) DELETE r')
        session.run(
            'MATCH (p:Club)-[r:HAS_RECEIVED]->(n:Notification) DELETE r')
        session.run('MATCH (n:Notification) DELETE n')


def update_notification_etat(id: str):
    with graph.session() as session:
        result = session.run(
            'MATCH (n:Notification) WHERE n.id= $id SET n.etat="delete" RETURN n', id=id)
        notif = result.single().data()['n']
        date_str = notif["date_and_time"].strftime('%Y-%m-%d %H:%M:%S')
        notif["date_and_time"] = json.dumps(date_str)
        # Return the result of the query
        return notif

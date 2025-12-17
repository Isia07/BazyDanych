import os
from pymongo import MongoClient
from django.conf import settings

db_conf = settings.DATABASES.get("nosql", {})

mongo_url = os.getenv("DB_NOSQL_URL")

host = db_conf.get("HOST", "localhost")
port = int(db_conf.get("PORT", 27017))
name = db_conf.get("NAME", "db_nosql")

user = db_conf.get("USER")
password = db_conf.get("PASSWORD")

if user and password:
    client = MongoClient(
        host=host,
        port=port,
        username=user,
        password=password,
    )
else:
    client = MongoClient(host=host, port=port)

db = client[name]

# Kolekcje
users_collection = db["users"]
events_collection = db["events"]
orders_collection = db["orders"]
notifications_collection = db["notifications"]
messages_collection = db["messages"]
discounts_collection = db["discounts"]
event_types_collection = db["event_types"]
seat_types_collection = db["seat_types"]
ticket_types_collection = db["ticket_types"]
statuses_collection = db["statuses"]
tickets_collection = db["tickets"]
tokens_collection = db["tokens"]
counters_collection = db["counters"]

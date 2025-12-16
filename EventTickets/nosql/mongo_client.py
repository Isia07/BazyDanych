import os
from pymongo import MongoClient
from django.conf import settings

# Konfiguracja z settings.py (DATABASES['nosql'])
db_conf = settings.DATABASES.get("nosql", {})

# Opcja 1: jeśli docker-compose ustawił pełny URL (najwygodniejsze)
mongo_url = os.getenv("DB_NOSQL_URL")

# if mongo_url:
#     # np: mongodb://nosql_user:nosql_tajne789@db_nosql:27017/db_nosql?authSource=admin
#     client = MongoClient(mongo_url)
#     db_name = mongo_url.rsplit("/", 1)[-1].split("?", 1)[0]
#     db = client[db_name]
# else:
    # Opcja 2: budujemy połączenie z pól z settings.py
host = db_conf.get("HOST", "localhost")
port = int(db_conf.get("PORT", 27017))
name = db_conf.get("NAME", "db_nosql")

user = db_conf.get("USER")
password = db_conf.get("PASSWORD")
#auth_source = db_conf.get("AUTH_SOURCE", "db_nosql")

if user and password:
    client = MongoClient(
        host=host,
        port=port,
        username=user,
        password=password,
        #authSource=auth_source,
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

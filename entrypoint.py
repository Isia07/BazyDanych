import os
import sys
import time

from django.db import connections
from django.db.utils import OperationalError
from pymongo import MongoClient
from pymongo.errors import PyMongoError

def wait_for_db(alias):
    print(f"Waiting for database '{alias}' to be ready...")
    attempts = 0
    while attempts < 30:
        try:
            connections[alias].cursor().execute("SELECT 1")
            print(f"Database '{alias}' is ready!")
            return
        except OperationalError:
            attempts += 1
            print(f"  Attempt {attempts}/30...")
            time.sleep(2)
    raise Exception(f"Database '{alias}' did not become ready")

def wait_for_mongo(attempts_max=30, sleep_s=2):
    print("Waiting for MongoDB to be ready...")
    attempts = 0

    mongo_url = os.getenv("DB_NOSQL_URL")
    if not mongo_url:
        # fallback: z settings albo ręcznie z env
        host = os.getenv("DB_NOSQL_HOST", "db_nosql")
        port = int(os.getenv("DB_NOSQL_PORT", "27017"))
        user = os.getenv("DB_NOSQL_USER")
        password = os.getenv("DB_NOSQL_PASSWORD")
        #auth_source = os.getenv("DB_NOSQL_AUTH_SOURCE", "db_nosql")

        if user and password:
            mongo_url = f"mongodb://{user}:{password}@{host}:{port}/" #?authSource={auth_source}
        else:
            mongo_url = f"mongodb://{host}:{port}"

    while attempts < attempts_max:
        try:
            client = MongoClient(mongo_url, serverSelectionTimeoutMS=2000)
            client.admin.command("ping")
            print("MongoDB is ready!")
            return
        except PyMongoError as e:
            attempts += 1
            print(f"  Attempt {attempts}/{attempts_max}... ({type(e).__name__})")
            time.sleep(sleep_s)

    raise Exception("MongoDB did not become ready")

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    import django

    django.setup()

    print("Waiting for databases...")
    wait_for_db("objective_relational")
    wait_for_db("relational")
    wait_for_db("objective")
    wait_for_mongo()

    print("Running migrations on user...")
    os.system("python manage.py migrate shared --database=objective_relational")
    os.system("python manage.py migrate shared --database=relational")

    print("Running migrations...")
    os.system(
        "python manage.py migrate objective_relational --database=objective_relational"
    )
    os.system("python manage.py migrate relational --database=relational")

    os.system("python manage.py makemigrations objective")
    os.system("python manage.py migrate objective --database=objective")

    print("Migrating authtoken tables to all databases...")
    os.system("python manage.py migrate authtoken --database=objective_relational")
    os.system("python manage.py migrate authtoken --database=relational")
    os.system("python manage.py migrate authtoken --database=objective")

    print("All migrations completed! Starting server...")
    os.execvp("python", ["python", "manage.py", "runserver", "0.0.0.0:8000"])

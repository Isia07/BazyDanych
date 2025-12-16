import os
import sys
import time

from django.db import connections
from django.db.utils import OperationalError


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


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    import django

    django.setup()

    print("Waiting for databases...")
    wait_for_db("default")
    wait_for_db("relational")
    wait_for_db("objective_relational")
    wait_for_db("objective")

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

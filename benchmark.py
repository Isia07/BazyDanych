import time
import statistics
import uuid
from datetime import datetime, timedelta
from decimal import Decimal

import psycopg2
from pymongo import MongoClient
from ZEO.ClientStorage import ClientStorage
from ZODB import DB
import transaction
from persistent import Persistent

# -------------------------- ZODB classes --------------------------
class BasePersistent(Persistent):
    def __init__(self, **kwargs):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        for k, v in kwargs.items():
            setattr(self, k, v)

class Discounts(BasePersistent):
    def __init__(self, code, discount_percentage, valid_from, valid_to, name="", **kwargs):
        super().__init__(**kwargs)
        self.code = code
        self.discount_percentage = discount_percentage
        self.valid_from = valid_from
        self.valid_to = valid_to
        self.name = name

# -------------------------- Connections (wewnątrz Docker network) --------------------------
# Relational Postgres
conn_rel = psycopg2.connect(
    host="db_relational",
    port=5432,
    user="postgres",
    password="postgres",
    dbname="db_relational"
)

# Object-relational Postgres
conn_obj_rel = psycopg2.connect(
    host="db_obj_rel",
    port=5432,
    user="postgres",
    password="postgres",
    dbname="db_obj_rel"
)

# MongoDB
mongo_client = MongoClient("mongodb://nosql_user:nosql_haslo@db_nosql:27017/")
mongo_db = mongo_client.db_nosql
mongo_coll = mongo_db.discounts

# ZODB (ZEO)
zodb_storage = ClientStorage(('db_object', 8090))
zodb_db = DB(zodb_storage)
zodb_conn = zodb_db.open()
zodb_root = zodb_conn.root()

if 'discounts' not in zodb_root:
    zodb_root['discounts'] = {}
    transaction.commit()

zodb_discounts = zodb_root['discounts']

# -------------------------- Setup indexes --------------------------
cur = conn_rel.cursor()
cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_discount_code ON discount (code);")
cur.execute("CREATE INDEX IF NOT EXISTS idx_discount_perc ON discount (discount_percentage);")
conn_rel.commit()
cur.close()

cur = conn_obj_rel.cursor()
cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_discount_obj_code ON discount_obj (code);")
cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_discount_obj_name ON discount_obj (name);")
cur.execute("CREATE INDEX IF NOT EXISTS idx_discount_obj_perc ON discount_obj (discount_percentage);")
conn_obj_rel.commit()
cur.close()

mongo_coll.create_index("code", unique=True)
mongo_coll.create_index("discount_percentage")

# -------------------------- Helper functions --------------------------
def clean(db_type):
    if db_type == "relational":
        cur = conn_rel.cursor()
        cur.execute("TRUNCATE TABLE discount RESTART IDENTITY CASCADE;")
        conn_rel.commit()
        cur.close()
    elif db_type == "obj_rel":
        cur = conn_obj_rel.cursor()
        cur.execute("TRUNCATE TABLE discount_obj RESTART IDENTITY CASCADE;")
        conn_obj_rel.commit()
        cur.close()
    elif db_type == "nosql":
        mongo_coll.delete_many({})
    elif db_type == "object":
        zodb_discounts.clear()
        transaction.commit()

def generate_data(size):
    now = datetime.now()
    delta = timedelta(days=30)
    data = []
    for i in range(size):
        common = {
            "code": f"CODE{i}",
            "discount_percentage": Decimal("10.00"),
            "valid_from": now,
            "valid_to": now + delta,
            "name": f"Discount{i}"
        }
        data.append(common)
    return data

def insert(size, db_type):
    data = generate_data(size)
    start = time.perf_counter()

    if db_type == "relational":
        cur = conn_rel.cursor()
        sql = """
            INSERT INTO discount (name, discount_percentage, code, valid_from, valid_to)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = [(d["name"], d["discount_percentage"], d["code"], d["valid_from"], d["valid_to"]) for d in data]
        cur.executemany(sql, values)
        conn_rel.commit()
        cur.close()

    elif db_type == "obj_rel":
        cur = conn_obj_rel.cursor()
        sql = """
            INSERT INTO discount_obj (name, discount_percentage, code, valid_from, valid_to)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = [(d["name"], d["discount_percentage"], d["code"], d["valid_from"], d["valid_to"]) for d in data]
        cur.executemany(sql, values)
        conn_obj_rel.commit()
        cur.close()

    elif db_type == "nosql":
        docs = [{
            "code": d["code"],
            "discount_percentage": float(d["discount_percentage"]),
            "valid_from": d["valid_from"],
            "valid_to": d["valid_to"]
        } for d in data]
        mongo_coll.insert_many(docs)

    elif db_type == "object":
        for i, d in enumerate(data):
            obj = Discounts(
                code=d["code"],
                discount_percentage=d["discount_percentage"],
                valid_from=d["valid_from"],
                valid_to=d["valid_to"],
                name=d["name"]
            )
            zodb_discounts[obj.id] = obj
            if i % 1000 == 999:
                transaction.commit()
        transaction.commit()

    return time.perf_counter() - start

def update(db_type):
    start = time.perf_counter()

    if db_type in ("relational", "obj_rel"):
        conn = conn_rel if db_type == "relational" else conn_obj_rel
        cur = conn.cursor()
        cur.execute("UPDATE discount SET discount_percentage = %s" if db_type == "relational"
                    else "UPDATE discount_obj SET discount_percentage = %s",
                    (Decimal("20.00"),))
        conn.commit()
        cur.close()

    elif db_type == "nosql":
        mongo_coll.update_many({}, {"$set": {"discount_percentage": 20.0}})

    elif db_type == "object":
        for obj in zodb_discounts.values():
            obj.discount_percentage = Decimal("20.00")
            obj.updated_at = datetime.now()
        transaction.commit()

    return time.perf_counter() - start

def select_all(db_type):
    start = time.perf_counter()
    if db_type == "relational":
        cur = conn_rel.cursor()
        cur.execute("SELECT * FROM discount")
        list(cur.fetchall())
        cur.close()
    elif db_type == "obj_rel":
        cur = conn_obj_rel.cursor()
        cur.execute("SELECT * FROM discount_obj")
        list(cur.fetchall())
        cur.close()
    elif db_type == "nosql":
        list(mongo_coll.find({}))
    elif db_type == "object":
        list(zodb_discounts.values())
    return time.perf_counter() - start

def select_by_code(db_type, code="CODE0"):
    start = time.perf_counter()
    if db_type == "relational":
        cur = conn_rel.cursor()
        cur.execute("SELECT * FROM discount WHERE code = %s", (code,))
        list(cur.fetchall())
        cur.close()
    elif db_type == "obj_rel":
        cur = conn_obj_rel.cursor()
        cur.execute("SELECT * FROM discount_obj WHERE code = %s", (code,))
        list(cur.fetchall())
        cur.close()
    elif db_type == "nosql":
        mongo_coll.find_one({"code": code})
    elif db_type == "object":
        for obj in zodb_discounts.values():
            if obj.code == code:
                _ = obj
                break
    return time.perf_counter() - start

def select_range(db_type, threshold=15.0):
    start = time.perf_counter()
    if db_type in ("relational", "obj_rel"):
        conn = conn_rel if db_type == "relational" else conn_obj_rel
        table = "discount" if db_type == "relational" else "discount_obj"
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table} WHERE discount_percentage > %s", (Decimal(str(threshold)),))
        list(cur.fetchall())
        cur.close()
    elif db_type == "nosql":
        list(mongo_coll.find({"discount_percentage": {"$gt": threshold}}))
    elif db_type == "object":
        [obj for obj in zodb_discounts.values() if float(obj.discount_percentage) > threshold]
    return time.perf_counter() - start

def delete(db_type):
    start = time.perf_counter()
    if db_type == "relational":
        cur = conn_rel.cursor()
        cur.execute("TRUNCATE TABLE discount RESTART IDENTITY CASCADE;")
        conn_rel.commit()
        cur.close()
    elif db_type == "obj_rel":
        cur = conn_obj_rel.cursor()
        cur.execute("TRUNCATE TABLE discount_obj RESTART IDENTITY CASCADE;")
        conn_obj_rel.commit()
        cur.close()
    elif db_type == "nosql":
        mongo_coll.delete_many({})
    elif db_type == "object":
        zodb_discounts.clear()
        transaction.commit()
    return time.perf_counter() - start

# -------------------------- Main benchmark --------------------------
sizes = [1, 100, 2000, 4000, 8000, 20000]
repeats = 10
db_types = ["relational", "obj_rel", "nosql", "object"]

results = {}

for db_type in db_types:
    print(f"\n=== Testing {db_type.upper()} ===")
    results[db_type] = {}
    for size in sizes:
        times = {"insert": [], "update": [], "delete": [], "select_all": [], "select_code": [], "select_range": []}
        for _ in range(repeats):
            clean(db_type)

            times["insert"].append(insert(size, db_type))
            times["update"].append(update(db_type))
            times["select_all"].append(select_all(db_type))
            times["select_code"].append(select_by_code(db_type))
            times["select_range"].append(select_range(db_type))
            times["delete"].append(delete(db_type))

        avg = {op: statistics.mean(t) for op, t in times.items()}
        results[db_type][size] = avg
        print(f"Size {size}: {avg}")

# -------------------------- Cleanup connections --------------------------
conn_rel.close()
conn_obj_rel.close()
mongo_client.close()
zodb_conn.close()
zodb_db.close()
zodb_storage.close()

print("\nBenchmark completed. Full results:")
print(results)
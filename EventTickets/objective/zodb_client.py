import atexit
import transaction
from ZEO.ClientStorage import ClientStorage
from ZODB import DB
from BTrees.OOBTree import OOBTree
from django.conf import settings

_db = None

def get_db():
    global _db
    if _db is None:
        addr = settings.ZEO_ADDRESS
        if isinstance(addr, str) and ":" in addr:
            host, port = addr.split(":")
            addr = (host, int(port))
        
        try:
            storage = ClientStorage(addr)
            _db = DB(storage)
            _init_root(_db)
        except Exception as e:
            print(f"failed to connect to ZEO at {addr}: {e}")
            raise e

    return _db

def _init_root(db):
    conn = db.open()
    try:
        root = conn.root()
        collections = [
            "users", "events", "orders", "tickets", 
            "notifications", "messages", "discounts", 
            "event_types", "ticket_types", "status",
            "tokens"
        ]
        
        changed = False
        for col in collections:
            if col not in root:
                root[col] = OOBTree()
                changed = True
        
        if changed:
            transaction.commit()
    finally:
        conn.close()

def close_db():
    global _db
    if _db:
        _db.close()
        _db = None

atexit.register(close_db)

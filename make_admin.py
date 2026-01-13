#!/usr/bin/env python3

import sys
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

import bcrypt
import secrets
import transaction

from EventTickets.objective.zodb_client import get_db
from EventTickets.objective.models import Users, Token

def make_admin(email, password=None):
    db = get_db()
    conn = db.open()
    
    try:
        root = conn.root()
        users = root['users']
        tokens = root['tokens']
        
        existing_user = None
        for user in users.values():
            if user.email == email.lower():
                existing_user = user
                break
        
        if existing_user:
            with transaction.manager:
                existing_user.is_admin = True
                print(f"user '{email}' promoted to admin")
                print(f"  id: {existing_user.id}")
                print(f"  is_admin: {existing_user.is_admin}")
        else:
            if not password:
                print("error: password required for new user")
                return False
                
            pw_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            with transaction.manager:
                new_user = Users(
                    email=email.lower(),
                    password_hash=pw_hash,
                    name="Admin",
                    surname="User"
                )
                new_user.is_admin = True
                users[new_user.id] = new_user
                
                token_key = secrets.token_hex(20)
                new_token = Token(key=token_key, user=new_user)
                tokens[token_key] = new_token
                
                print(f"created admin user '{email}'")
                print(f"  id: {new_user.id}")
                print(f"  token: {token_key}")
                print(f"  is_admin: {new_user.is_admin}")
        
        return True
        
    finally:
        conn.close()

def list_users():
    db = get_db()
    conn = db.open()
    
    try:
        root = conn.root()
        users = root['users']
        
        print(f"found {len(users)} users in ZODB:")
        for uid, user in users.items():
            admin_flag = "[ADMIN]" if getattr(user, 'is_admin', False) else ""
            print(f"  {user.email} (id: {uid}) {admin_flag}")
    finally:
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage:")
        print("  python make_admin.py <email> [password]")
        print("  python make_admin.py --list")
        sys.exit(1)
    
    if sys.argv[1] == "--list":
        list_users()
    else:
        email = sys.argv[1]
        password = sys.argv[2] if len(sys.argv) > 2 else None
        make_admin(email, password)

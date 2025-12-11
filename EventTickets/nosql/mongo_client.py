from pymongo import MongoClient
from django.conf import settings


db_conf = settings.DATABASES['nosql']

client = MongoClient(
    host=db_conf.get('HOST', 'localhost'),
    port=db_conf.get('PORT', 27017),
)

db = client[db_conf['NAME']]

users_collection = db['users']
events_collection = db['events']
orders_collection = db['orders']
notifications_collection = db['notifications']
messages_collection = db['messages']
discounts_collection = db['discounts']
event_types_collection = db['event_types']
seat_types_collection = db['seat_types']
ticket_types_collection = db['ticket_types']
statuses_collection = db['statuses']

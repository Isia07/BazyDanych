from django.urls import path
from . import views
from EventTickets.nosql.views import (
    nosql_events_list,
    nosql_users_list,
    nosql_orders_list,
    nosql_notifications_list,
    nosql_messages_list,
)

urlpatterns = [
    path('', views.home, name='home'),
    path('select_database/', views.select_database, name='select_database'),

path('api/nosql/events/', nosql_events_list, name='nosql-events-list'),
    path('api/nosql/users/', nosql_users_list, name='nosql-users-list'),
    path('api/nosql/orders/', nosql_orders_list, name='nosql-orders-list'),
    path('api/nosql/notifications/', nosql_notifications_list, name='nosql-notifications-list'),
    path('api/nosql/messages/', nosql_messages_list, name='nosql-messages-list'),
]
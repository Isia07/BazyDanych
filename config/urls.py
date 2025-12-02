"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from EventTickets.nosql.views import (
    nosql_events_list,
    nosql_users_list,
    nosql_orders_list,
    nosql_notifications_list,
    nosql_messages_list,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('EventTickets.urls')),

    path('api/nosql/events/', nosql_events_list, name='nosql-events-list'),
    path('api/nosql/users/', nosql_users_list, name='nosql-users-list'),
    path('api/nosql/orders/', nosql_orders_list, name='nosql-orders-list'),
    path('api/nosql/notifications/', nosql_notifications_list, name='nosql-notifications-list'),
    path('api/nosql/messages/', nosql_messages_list, name='nosql-messages-list'),
]

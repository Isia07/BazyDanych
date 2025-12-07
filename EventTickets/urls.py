from django.urls import path
from EventTickets.objective_relational.views import RegisterView as ObjRelRegister, LoginView as ObjRelLogin
from .relational.views import RelRegisterView, RelLoginView, DiscountDetailView, DiscountListCreateView
from EventTickets.nosql.views import (
    nosql_events_list,
    nosql_users_list,
    nosql_orders_list,
    nosql_notifications_list,
    nosql_messages_list,
)

urlpatterns = [
    path('api/v1/obj-rel/auth/register', ObjRelRegister.as_view(), name='obj_rel_register'),
    path('api/v1/obj-rel/auth/login', ObjRelLogin.as_view(), name='obj_rel_login'),
    path('api/v1/rel/auth/register', RelRegisterView.as_view(), name='rel_register'),
    path('api/v1/rel/auth/login', RelLoginView.as_view(), name='rel_login'),
    path('api/v1/rel/discounts/', DiscountListCreateView.as_view(), name='discount_list_create'),
    path('api/v1/rel/discounts/<int:pk>/', DiscountDetailView.as_view(), name='discount_detail'),

    path('api/nosql/events/', nosql_events_list, name='nosql-events-list'),
    path('api/nosql/users/', nosql_users_list, name='nosql-users-list'),
    path('api/nosql/orders/', nosql_orders_list, name='nosql-orders-list'),
    path('api/nosql/notifications/', nosql_notifications_list, name='nosql-notifications-list'),
    path('api/nosql/messages/', nosql_messages_list, name='nosql-messages-list'),
]
from django.urls import path
from .relational.views import RelRegisterView, RelLoginView, DiscountDetailView, DiscountListCreateView
from .objective_relational.views import (
    RegisterView as ObjRelRegister, LoginView as ObjRelLogin,
    StatusObjListCreateView, StatusObjDetailView,
    DiscountObjListCreateView, DiscountObjDetailView,
    MessageListCreateView, MessageDetailView,
    EventTypeObjListCreateView, EventTypeObjDetailView,
    TicketTypeObjListCreateView, TicketTypeObjDetailView,
    EventListCreateView, EventDetailView,
    TicketListCreateView, TicketDetailView,
    OrderListCreateView, OrderDetailView,
    NotificationListCreateView, NotificationDetailView,
)

urlpatterns = [
    path('api/v1/obj-rel/auth/register', ObjRelRegister.as_view(), name='obj_rel_register'),
    path('api/v1/obj-rel/auth/login', ObjRelLogin.as_view(), name='obj_rel_login'),
    path('api/v1/rel/auth/register', RelRegisterView.as_view(), name='rel_register'),
    path('api/v1/rel/auth/login', RelLoginView.as_view(), name='rel_login'),
    path('api/v1/rel/discounts/', DiscountListCreateView.as_view(), name='discount_list_create'),
    path('api/v1/rel/discounts/<int:pk>/', DiscountDetailView.as_view(), name='discount_detail'),

    path('api/v1/obj-rel/discounts/', DiscountObjListCreateView.as_view(), name='obj_rel_discounts'),
    path("api/v1/obj-rel/discounts/<int:id>/", DiscountObjDetailView.as_view(), name="obj_rel_discounts_id"),
    path('api/v1/obj-rel/event-types/', EventTypeObjListCreateView.as_view(), name='obj_rel_event_types'),
    path('api/v1/obj-rel/event-types/<int:id>/', EventTypeObjDetailView.as_view(), name='obj_rel_event_types_id'),
    path('api/v1/obj-rel/statuses/', StatusObjListCreateView.as_view(), name='obj_rel_statuses'),
    path('api/v1/obj-rel/statuses/<int:id>/', StatusObjDetailView.as_view(), name='obj_rel_statuses_id'),
    path('api/v1/obj-rel/ticket-types/', TicketTypeObjListCreateView.as_view(), name='obj_rel_ticket_types'),
    path('api/v1/obj-rel/ticket-types/<int:id>/', TicketTypeObjDetailView.as_view(), name='obj_rel_ticket_types_id'),
    path('api/v1/obj-rel/events/', EventListCreateView.as_view(), name='obj_rel_events'),
    path('api/v1/obj-rel/events/<int:id>/', EventDetailView.as_view(), name='obj_rel_event_detail'),
    path('api/v1/obj-rel/tickets/', TicketListCreateView.as_view(), name='obj_rel_tickets'),
    path('api/v1/obj-rel/tickets/<int:id>/', TicketDetailView.as_view(), name='obj_rel_ticket_detail'),
    path('api/v1/obj-rel/orders/', OrderListCreateView.as_view(), name='obj_rel_orders'),
    path('api/v1/obj-rel/orders/<int:id>/', OrderDetailView.as_view(), name='obj_rel_order_detail'),
    path('api/v1/obj-rel/notifications/', NotificationListCreateView.as_view(), name='obj_rel_notifications'),
    path('api/v1/obj-rel/notifications/<int:id>/', NotificationDetailView.as_view(),
         name='obj_rel_notification_detail'),
    path('api/v1/obj-rel/messages/', MessageListCreateView.as_view(), name='obj_rel_messages'),
    path('api/v1/obj-rel/messages/<int:id>/', MessageDetailView.as_view(), name='obj_rel_message_detail'),
]

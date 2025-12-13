from django.urls import path
from .relational.views import RelRegisterView, RelLoginView, DiscountDetailView, DiscountListCreateView, \
    RelDiscountListCreateView, RelDiscountDetailView, RelTicketTypeListCreateView, RelTicketTypeDetailView, \
    RelStatusListCreateView, RelStatusDetailView, RelEventTypeListCreateView, RelEventTypeDetailView, \
    RelMessageListCreateView, RelMessageDetailView, RelNotificationListCreateView, RelNotificationDetailView, \
    RelEventListCreateView, RelEventDetailView
from EventTickets.objective_relational.views import (
    RegisterView as ObjRelRegister, LoginView as ObjRelLogin,
    StatusObjListCreateView, EventTypeObjListCreateView, TicketTypeObjListCreateView, SeatTypeObjListCreateView,
    DiscountObjListCreateView, DiscountObjDetailView,
    EventListCreateView, EventDetailView,
    TicketListCreateView,
    UserOrderListView, OrderCreateView,
    UserNotificationListView, UserMessageListCreateView, EventTypeObjDetailView, SeatTypeObjDetailView,
    StatusObjDetailView, TicketTypeObjDetailView,
)

urlpatterns = [
    path('api/v1/obj-rel/auth/register', ObjRelRegister.as_view(), name='obj_rel_register'),
    path('api/v1/obj-rel/auth/login', ObjRelLogin.as_view(), name='obj_rel_login'),
    path('api/v1/rel/auth/register', RelRegisterView.as_view(), name='rel_register'),
    path('api/v1/rel/auth/login', RelLoginView.as_view(), name='rel_login'),
    path('api/v1/rel/discounts/', DiscountListCreateView.as_view(), name='discount_list_create'),
    path('api/v1/rel/discounts/<int:pk>/', DiscountDetailView.as_view(), name='discount_detail'),

    path('api/v1/rel/auth/register', RelRegisterView.as_view(), name='rel_register'),
    path('api/v1/rel/auth/login', RelLoginView.as_view(), name='rel_login'),
    path('api/v1/rel/discounts/', RelDiscountListCreateView.as_view(), name='rel_discounts'),
    path('api/v1/rel/discounts/<int:pk>/', RelDiscountDetailView.as_view(), name='rel_discount_detail'),
    path('api/v1/rel/ticket-types/', RelTicketTypeListCreateView.as_view(), name='rel_ticket_types'),
    path('api/v1/rel/ticket-types/<int:pk>/', RelTicketTypeDetailView.as_view(), name='rel_ticket_type_detail'),
    path('api/v1/rel/statuses/', RelStatusListCreateView.as_view(), name='rel_statuses'),
    path('api/v1/rel/statuses/<int:pk>/', RelStatusDetailView.as_view(), name='rel_status_detail'),
    path('api/v1/rel/event-types/', RelEventTypeListCreateView.as_view(), name='rel_event_types'),
    path('api/v1/rel/event-types/<int:pk>/', RelEventTypeDetailView.as_view(), name='rel_event_type_detail'),
    path('api/v1/rel/messages/', RelMessageListCreateView.as_view(), name="rel_messages"),
    path('api/v1/rel/messages/<int:pk>/', RelMessageDetailView.as_view(), name="rel_message_detail"),
    path('api/v1/rel/notifications/', RelNotificationListCreateView.as_view(), name="rel_notifications"),
    path('api/v1/rel/notifications/<int:pk>/', RelNotificationDetailView.as_view(), name="rel_notification_detail"),
    path('api/v1/rel/events/', RelEventListCreateView.as_view(), name="rel_events"),
    path('api/v1/rel/events/<int:pk>/', RelEventDetailView.as_view(), name="rel_event_detail"),

    path('api/v1/obj-rel/discounts/', DiscountObjListCreateView.as_view(), name='obj_rel_discounts'),
    path("api/v1/obj-rel/discounts/<int:id>/", DiscountObjDetailView.as_view(), name="obj_rel_discounts_id"),
    path('api/v1/obj-rel/event-types/', EventTypeObjListCreateView.as_view(), name='obj_rel_event_types'),
    path('api/v1/obj-rel/event-types/<int:id>/', EventTypeObjDetailView.as_view(), name='obj_rel_event_types_id'),
    path('api/v1/obj-rel/seat-types/', SeatTypeObjListCreateView.as_view(), name='obj_rel_seat_types'),
    path('api/v1/obj-rel/seat-types/<int:id>/', SeatTypeObjDetailView.as_view(), name='obj_rel_seat_types_id'),
    path('api/v1/obj-rel/statuses/', StatusObjListCreateView.as_view(), name='obj_rel_statuses'),
    path('api/v1/obj-rel/statuses/<int:id>/', StatusObjDetailView.as_view(), name='obj_rel_statuses_id'),
    path('api/v1/obj-rel/ticket-types/', TicketTypeObjListCreateView.as_view(), name='obj_rel_ticket_types'),
    path('api/v1/obj-rel/ticket-types/<int:id>/', TicketTypeObjDetailView.as_view(), name='obj_rel_ticket_types_id'),

    path('api/v1/obj-rel/events', EventListCreateView.as_view(), name='obj_rel_event_list_create'),
    path('api/v1/obj-rel/events/<int:pk>', EventDetailView.as_view(), name='obj_rel_event_detail'),

    path('api/v1/obj-rel/tickets', TicketListCreateView.as_view(), name='obj_rel_ticket_list_create'),

    path('api/v1/obj-rel/orders', UserOrderListView.as_view(), name='obj_rel_user_orders'),
    path('api/v1/obj-rel/orders/create', OrderCreateView.as_view(), name='obj_rel_order_create'),

    path('api/v1/obj-rel/notifications', UserNotificationListView.as_view(), name='obj_rel_notifications'),
    path('api/v1/obj-rel/notifications/<int:pk>/read', UserNotificationListView.as_view(), name='obj_rel_notification_read'),
    path('api/v1/obj-rel/messages', UserMessageListCreateView.as_view(), name='obj_rel_messages'),

]
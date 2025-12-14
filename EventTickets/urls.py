from django.urls import path
from .relational.views import RelRegisterView, RelLoginView, \
    RelDiscountListCreateView, RelDiscountDetailView, RelTicketTypeListCreateView, RelTicketTypeDetailView, \
    RelStatusListCreateView, RelStatusDetailView, RelEventTypeListCreateView, RelEventTypeDetailView, \
    RelMessageListCreateView, RelMessageDetailView, RelNotificationListCreateView, RelNotificationDetailView, \
    RelEventListCreateView, RelEventDetailView
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
    NotificationListCreateView, NotificationDetailView, MessageAllListView,
)

urlpatterns = [
    # register
    path('api/v1/obj-rel/auth/register/', ObjRelRegister.as_view(), name='obj_rel_register'),
    path('api/v1/rel/auth/register/', RelRegisterView.as_view(), name='rel_register'),

    # login
    path('api/v1/obj-rel/auth/login/', ObjRelLogin.as_view(), name='obj_rel_login'),
    path('api/v1/rel/auth/login/', RelLoginView.as_view(), name='rel_login'),

    # discounts
    path('api/v1/obj-rel/discounts/', DiscountObjListCreateView.as_view(), name='obj_rel_discounts'),
    path('api/v1/rel/discounts/', RelDiscountListCreateView.as_view(), name='rel_discounts'),

    # discounts id
    path("api/v1/obj-rel/discounts/<int:id>/", DiscountObjDetailView.as_view(), name="obj_rel_discounts_id"),
    path('api/v1/rel/discounts/<int:pk>/', RelDiscountDetailView.as_view(), name='rel_discount_detail'),

    # ticket-types
    path('api/v1/obj-rel/ticket-types/', TicketTypeObjListCreateView.as_view(), name='obj_rel_ticket_types'),
    path('api/v1/rel/ticket-types/', RelTicketTypeListCreateView.as_view(), name='rel_ticket_types'),

    # ticket-types id
    path('api/v1/obj-rel/ticket-types/<int:id>/', TicketTypeObjDetailView.as_view(), name='obj_rel_ticket_types_id'),
    path('api/v1/rel/ticket-types/<int:pk>/', RelTicketTypeDetailView.as_view(), name='rel_ticket_type_detail'),

    # statuses
    path('api/v1/obj-rel/statuses/', StatusObjListCreateView.as_view(), name='obj_rel_statuses'),
    path('api/v1/rel/statuses/', RelStatusListCreateView.as_view(), name='rel_statuses'),

    # statuses id
    path('api/v1/obj-rel/statuses/<int:id>/', StatusObjDetailView.as_view(), name='obj_rel_statuses_id'),
    path('api/v1/rel/statuses/<int:pk>/', RelStatusDetailView.as_view(), name='rel_status_detail'),

    # event-type
    path('api/v1/obj-rel/event-types/', EventTypeObjListCreateView.as_view(), name='obj_rel_event_types'),
    path('api/v1/rel/event-types/', RelEventTypeListCreateView.as_view(), name='rel_event_types'),

    # event-type id
    path('api/v1/obj-rel/event-types/<int:id>/', EventTypeObjDetailView.as_view(), name='obj_rel_event_types_id'),
    path('api/v1/rel/event-types/<int:pk>/', RelEventTypeDetailView.as_view(), name='rel_event_type_detail'),

    # messages
    path('api/v1/obj-rel/messages/', MessageListCreateView.as_view(), name='obj_rel_messages'),
    path('api/v1/rel/messages/', RelMessageListCreateView.as_view(), name="rel_messages"),

    #messages all
    path('api/v1/obj-rel/messages/all/', MessageAllListView.as_view(), name='obj_rel_messages_all'),

    # messages id
    path('api/v1/obj-rel/messages/<int:id>/', MessageDetailView.as_view(), name='obj_rel_message_detail'),
    path('api/v1/rel/messages/<int:pk>/', RelMessageDetailView.as_view(), name="rel_message_detail"),

    # notifications
    path('api/v1/obj-rel/notifications/', NotificationListCreateView.as_view(), name='obj_rel_notifications'),
    path('api/v1/rel/notifications/', RelNotificationListCreateView.as_view(), name="rel_notifications"),


    # notifications id
    path('api/v1/obj-rel/notifications/<int:id>/', NotificationDetailView.as_view(),
         name='obj_rel_notification_detail'),
    path('api/v1/rel/notifications/<int:pk>/', RelNotificationDetailView.as_view(), name="rel_notification_detail"),

    # events
    path('api/v1/obj-rel/events/', EventListCreateView.as_view(), name='obj_rel_events'),
    path('api/v1/rel/events/', RelEventListCreateView.as_view(), name="rel_events"),

    # events id
    path('api/v1/obj-rel/events/<int:id>/', EventDetailView.as_view(), name='obj_rel_event_detail'),
    path('api/v1/rel/events/<int:pk>/', RelEventDetailView.as_view(), name="rel_event_detail"),

    # tickets
    path('api/v1/obj-rel/tickets/', TicketListCreateView.as_view(), name='obj_rel_tickets'),

    # tickets id
    path('api/v1/obj-rel/tickets/<int:id>/', TicketDetailView.as_view(), name='obj_rel_ticket_detail'),

    # orders
    path('api/v1/obj-rel/orders/', OrderListCreateView.as_view(), name='obj_rel_orders'),

    # orders id
    path('api/v1/obj-rel/orders/<int:id>/', OrderDetailView.as_view(), name='obj_rel_order_detail'),
]

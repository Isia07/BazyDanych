from django.urls import path

from EventTickets.nosql.views import (
    NosqlRegisterView, NosqlLoginView,
    NosqlDiscountListCreateView, NosqlDiscountDetailView,
    NosqlTicketTypeListCreateView, NosqlTicketTypeDetailView,
    NosqlStatusListCreateView, NosqlStatusDetailView,
    NosqlEventTypeListCreateView, NosqlEventTypeDetailView,
    NosqlEventListCreateView, NosqlEventDetailView,
    NosqlTicketListCreateView, NosqlTicketDetailView,
    NosqlOrderListCreateView, NosqlOrderDetailView,
    NosqlNotificationListCreateView, NosqlNotificationDetailView,
    NosqlMessageListCreateView, NosqlMessageDetailView,
    NosqlMessageAllListView,
)

from .objective.views import (
    DiscountsListCreateView as ObjDiscountsListCreateView,
    DiscountsDetailView as ObjDiscountsDetailView,
    EventListCreateView as ObjEventListCreateView,
    EventDetailView as ObjEventDetailView,
    TicketListCreateView as ObjTicketListCreateView,
    OrderCreateView as ObjOrderCreateView,
    UserOrderListView as ObjUserOrderListView,
    UserNotificationListView as ObjUserNotificationListView,
    UserMessageListCreateView as ObjUserMessageListCreateView,
    StatusListCreateView as ObjStatusListCreateView,
    StatusDetailView as ObjStatusDetailView,
    EventTypeListCreateView as ObjEventTypeListCreateView,
    EventTypeDetailView as ObjEventTypeDetailView,
    TicketTypeListCreateView as ObjTicketTypeListCreateView,
    TicketTypeDetailView as ObjTicketTypeDetailView,
    RegisterView as ObjRegister,
    LoginView as ObjLogin,
)

from .objective_relational.views import (
    DiscountObjListCreateView,
    DiscountObjDetailView,
    EventTypeObjListCreateView,
    EventTypeObjDetailView,
    StatusObjListCreateView,
    StatusObjDetailView,
    TicketTypeObjListCreateView,
    TicketTypeObjDetailView,
    EventListCreateView,
    EventDetailView,
    TicketListCreateView,
    TicketDetailView,
    OrderListCreateView,
    OrderDetailView,
    NotificationListCreateView,
    NotificationDetailView,
    MessageListCreateView,
    MessageDetailView,
    MessageAllListView,
    RegisterView as ObjRelRegister,
    LoginView as ObjRelLogin,
)

from .relational.views import (
    RelRegisterView,
    RelLoginView,
    RelDiscountListCreateView,
    RelDiscountDetailView,
    RelEventTypeListCreateView,
    RelEventTypeDetailView,
    RelStatusListCreateView,
    RelStatusDetailView,
    RelTicketTypeListCreateView,
    RelTicketTypeDetailView,
    RelEventListCreateView,
    RelEventDetailView,
    RelTicketListCreateView,
    RelTicketDetailView,
    RelOrderListCreateView,
    RelOrderDetailView,
    RelNotificationListCreateView,
    RelNotificationDetailView,
    RelMessageListCreateView,
    RelMessageDetailView,
    RelMessageAllListView,
)

urlpatterns = [
    # AUTH
    path('api/v1/obj-rel/auth/register/', ObjRelRegister.as_view(), name='obj_rel_register'),
    path('api/v1/obj-rel/auth/login/', ObjRelLogin.as_view(), name='obj_rel_login'),

    path('api/v1/rel/auth/register/', RelRegisterView.as_view(), name='rel_register'),
    path('api/v1/rel/auth/login/', RelLoginView.as_view(), name='rel_login'),

    path('api/v1/nosql/auth/register/', NosqlRegisterView.as_view(), name='nosql_register'),
    path('api/v1/nosql/auth/login/', NosqlLoginView.as_view(), name='nosql_login'),

    path('api/v1/obj/auth/register/', ObjRegister.as_view(), name='obj_register'),
    path('api/v1/obj/auth/login/', ObjLogin.as_view(), name='obj_login'),

    # DISCOUNTS
    path('api/v1/obj-rel/discounts/', DiscountObjListCreateView.as_view(), name='obj_rel_discounts_list'),
    path('api/v1/obj-rel/discounts/<int:pk>/', DiscountObjDetailView.as_view(), name='obj_rel_discount_detail'),

    path('api/v1/rel/discounts/', RelDiscountListCreateView.as_view(), name='rel_discounts_list'),
    path('api/v1/rel/discounts/<int:pk>/', RelDiscountDetailView.as_view(), name='rel_discount_detail'),

    path('api/v1/nosql/discounts/', NosqlDiscountListCreateView.as_view(), name='nosql_discounts_list'),
    path('api/v1/nosql/discounts/<str:pk>/', NosqlDiscountDetailView.as_view(), name='nosql_discount_detail'),

    path('api/v1/obj/discounts/', ObjDiscountsListCreateView.as_view(), name='obj_discounts_list'),
    path('api/v1/obj/discounts/<int:pk>/', ObjDiscountsDetailView.as_view(), name='obj_discount_detail'),

    # TICKET TYPES
    path('api/v1/obj-rel/ticket-types/', TicketTypeObjListCreateView.as_view(), name='obj_rel_ticket_types_list'),
    path('api/v1/obj-rel/ticket-types/<int:pk>/', TicketTypeObjDetailView.as_view(), name='obj_rel_ticket_type_detail'),

    path('api/v1/rel/ticket-types/', RelTicketTypeListCreateView.as_view(), name='rel_ticket_types_list'),
    path('api/v1/rel/ticket-types/<int:pk>/', RelTicketTypeDetailView.as_view(), name='rel_ticket_type_detail'),

    path('api/v1/nosql/ticket-types/', NosqlTicketTypeListCreateView.as_view(), name='nosql_ticket_types_list'),
    path('api/v1/nosql/ticket-types/<str:pk>/', NosqlTicketTypeDetailView.as_view(), name='nosql_ticket_type_detail'),

    path('api/v1/obj/ticket-types/', ObjTicketTypeListCreateView.as_view(), name='obj_ticket_types_list'),
    path('api/v1/obj/ticket-types/<int:pk>/', ObjTicketTypeDetailView.as_view(), name='obj_ticket_type_detail'),

    # STATUSES
    path('api/v1/obj-rel/statuses/', StatusObjListCreateView.as_view(), name='obj_rel_statuses_list'),
    path('api/v1/obj-rel/statuses/<int:pk>/', StatusObjDetailView.as_view(), name='obj_rel_status_detail'),

    path('api/v1/rel/statuses/', RelStatusListCreateView.as_view(), name='rel_statuses_list'),
    path('api/v1/rel/statuses/<int:pk>/', RelStatusDetailView.as_view(), name='rel_status_detail'),

    path('api/v1/nosql/statuses/', NosqlStatusListCreateView.as_view(), name='nosql_statuses_list'),
    path('api/v1/nosql/statuses/<str:pk>/', NosqlStatusDetailView.as_view(), name='nosql_status_detail'),

    path('api/v1/obj/statuses/', ObjStatusListCreateView.as_view(), name='obj_statuses_list'),
    path('api/v1/obj/statuses/<int:pk>/', ObjStatusDetailView.as_view(), name='obj_status_detail'),

    # EVENT TYPES
    path('api/v1/obj-rel/event-types/', EventTypeObjListCreateView.as_view(), name='obj_rel_event_types_list'),
    path('api/v1/obj-rel/event-types/<int:pk>/', EventTypeObjDetailView.as_view(), name='obj_rel_event_type_detail'),

    path('api/v1/rel/event-types/', RelEventTypeListCreateView.as_view(), name='rel_event_types_list'),
    path('api/v1/rel/event-types/<int:pk>/', RelEventTypeDetailView.as_view(), name='rel_event_type_detail'),

    path('api/v1/nosql/event-types/', NosqlEventTypeListCreateView.as_view(), name='nosql_event_types_list'),
    path('api/v1/nosql/event-types/<str:pk>/', NosqlEventTypeDetailView.as_view(), name='nosql_event_type_detail'),

    path('api/v1/obj/event-types/', ObjEventTypeListCreateView.as_view(), name='obj_event_types_list'),
    path('api/v1/obj/event-types/<int:pk>/', ObjEventTypeDetailView.as_view(), name='obj_event_type_detail'),

    # EVENTS
    path('api/v1/obj-rel/events/', EventListCreateView.as_view(), name='obj_rel_events_list'),
    path('api/v1/obj-rel/events/<int:pk>/', EventDetailView.as_view(), name='obj_rel_event_detail'),

    path('api/v1/rel/events/', RelEventListCreateView.as_view(), name='rel_events_list'),
    path('api/v1/rel/events/<int:pk>/', RelEventDetailView.as_view(), name='rel_event_detail'),

    path('api/v1/nosql/events/', NosqlEventListCreateView.as_view(), name='nosql_events_list'),
    path('api/v1/nosql/events/<str:id>/', NosqlEventDetailView.as_view(), name='nosql_event_detail'),

    path('api/v1/obj/events/', ObjEventListCreateView.as_view(), name='obj_events_list'),
    path('api/v1/obj/events/<int:pk>/', ObjEventDetailView.as_view(), name='obj_event_detail'),

    # TICKETS
    path('api/v1/obj-rel/tickets/', TicketListCreateView.as_view(), name='obj_rel_tickets_list'),
    path('api/v1/obj-rel/tickets/<int:pk>/', TicketDetailView.as_view(), name='obj_rel_ticket_detail'),

    path('api/v1/rel/tickets/', RelTicketListCreateView.as_view(), name='rel_tickets_list'),
    path('api/v1/rel/tickets/<int:pk>/', RelTicketDetailView.as_view(), name='rel_ticket_detail'),

    path('api/v1/nosql/tickets/', NosqlTicketListCreateView.as_view(), name='nosql_tickets_list'),
    path('api/v1/nosql/tickets/<str:pk>/', NosqlTicketDetailView.as_view(), name='nosql_ticket_detail'),

    path('api/v1/obj/tickets/', ObjTicketListCreateView.as_view(), name='obj_tickets_list'),

    # ORDERS
    path('api/v1/obj-rel/orders/', OrderListCreateView.as_view(), name='obj_rel_orders_list'),
    path('api/v1/obj-rel/orders/<int:pk>/', OrderDetailView.as_view(), name='obj_rel_order_detail'),

    path('api/v1/rel/orders/', RelOrderListCreateView.as_view(), name='rel_orders_list'),
    path('api/v1/rel/orders/<int:pk>/', RelOrderDetailView.as_view(), name='rel_order_detail'),

    path('api/v1/nosql/orders/', NosqlOrderListCreateView.as_view(), name='nosql_orders_list'),
    path('api/v1/nosql/orders/<str:pk>/', NosqlOrderDetailView.as_view(), name='nosql_order_detail'),

    path('api/v1/obj/orders/', ObjUserOrderListView.as_view(), name='obj_user_orders_list'),
    path('api/v1/obj/orders/create/', ObjOrderCreateView.as_view(), name='obj_order_create'),

    # NOTIFICATIONS
    path('api/v1/obj-rel/notifications/', NotificationListCreateView.as_view(), name='obj_rel_notifications_list'),
    path('api/v1/obj-rel/notifications/<int:pk>/', NotificationDetailView.as_view(), name='obj_rel_notification_detail'),

    path('api/v1/rel/notifications/', RelNotificationListCreateView.as_view(), name='rel_notifications_list'),
    path('api/v1/rel/notifications/<int:pk>/', RelNotificationDetailView.as_view(), name='rel_notification_detail'),

    path('api/v1/nosql/notifications/', NosqlNotificationListCreateView.as_view(), name='nosql_notifications_list'),
    path('api/v1/nosql/notifications/<str:pk>/', NosqlNotificationDetailView.as_view(), name='nosql_notification_detail'),

    path('api/v1/obj/notifications/', ObjUserNotificationListView.as_view(), name='obj_notifications_list'),
    path('api/v1/obj/notifications/<int:pk>/read/', ObjUserNotificationListView.as_view(), name='obj_notification_read'),

    # MESSAGES
    path('api/v1/obj-rel/messages/', MessageListCreateView.as_view(), name='obj_rel_messages_list'),
    path('api/v1/obj-rel/messages/<int:pk>/', MessageDetailView.as_view(), name='obj_rel_message_detail'),
    path('api/v1/obj-rel/messages/all/', MessageAllListView.as_view(), name='obj_rel_messages_all'),

    path('api/v1/rel/messages/', RelMessageListCreateView.as_view(), name='rel_messages_list'),
    path('api/v1/rel/messages/<int:pk>/', RelMessageDetailView.as_view(), name='rel_message_detail'),
    path('api/v1/rel/messages/all/', RelMessageAllListView.as_view(), name='rel_messages_all'),

    path('api/v1/nosql/messages/all/', NosqlMessageAllListView.as_view(), name='nosql_messages_all'),
    path('api/v1/nosql/messages/', NosqlMessageListCreateView.as_view(), name='nosql_messages_list'),
    path('api/v1/nosql/messages/<str:id>/', NosqlMessageDetailView.as_view(), name='nosql_message_detail'),

    path('api/v1/obj/messages/', ObjUserMessageListCreateView.as_view(), name='obj_messages_list'),
    path('api/v1/obj/messages/all/', ObjUserMessageListCreateView.as_view(), name='obj_messages_all'),
]
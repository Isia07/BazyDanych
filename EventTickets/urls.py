from django.urls import path
from . import views
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
    NosqlMessageListCreateView, NosqlMessageDetailView, NosqlMessageAllListView,
)




from .objective.views import (
    DiscountsDetailView as ObjDiscountsDetailView,
)
from .objective.views import (
    DiscountsListCreateView as ObjDiscountsListCreateView,
)
from .objective.views import (
    EventDetailView as ObjEventDetailView,
)
from .objective.views import (
    EventListCreateView as ObjEventListCreateView,
)
from .objective.views import (
    EventTypeDetailView as ObjEventTypeDetailView,
)
from .objective.views import (
    EventTypeListCreateView as ObjEventTypeListCreateView,
)
from .objective.views import (
    LoginView as ObjLogin,
)
from .objective.views import (
    OrderCreateView as ObjOrderCreateView,
)
from .objective.views import (
    RegisterView as ObjRegister,
)
from .objective.views import (
    StatusDetailView as ObjStatusDetailView,
)
from .objective.views import (
    StatusListCreateView as ObjStatusListCreateView,
)
from .objective.views import (
    TicketListCreateView as ObjTicketListCreateView,
)
from .objective.views import (
    TicketTypeDetailView as ObjTicketTypeDetailView,
)
from .objective.views import (
    TicketTypeListCreateView as ObjTicketTypeListCreateView,
)
from .objective.views import (
    UserMessageListCreateView as ObjUserMessageListCreateView,
)
from .objective.views import (
    UserNotificationListView as ObjUserNotificationListView,
)
from .objective.views import (
    UserOrderListView as ObjUserOrderListView,
)
from .objective_relational.views import (
    DiscountObjDetailView,
    DiscountObjListCreateView,
    EventDetailView,
    EventListCreateView,
    EventTypeObjDetailView,
    EventTypeObjListCreateView,
    MessageAllListView,
    MessageDetailView,
    MessageListCreateView,
    NotificationDetailView,
    NotificationListCreateView,
    OrderDetailView,
    OrderListCreateView,
    StatusObjDetailView,
    StatusObjListCreateView,
    TicketDetailView,
    TicketListCreateView,
    TicketTypeObjDetailView,
    TicketTypeObjListCreateView,
)
from .objective_relational.views import LoginView as ObjRelLogin
from .objective_relational.views import RegisterView as ObjRelRegister
from .relational.views import (
    RelDiscountDetailView,
    RelDiscountListCreateView,
    RelEventDetailView,
    RelEventListCreateView,
    RelEventTypeDetailView,
    RelEventTypeListCreateView,
    RelLoginView,
    RelMessageAllListView,
    RelMessageDetailView,
    RelMessageListCreateView,
    RelNotificationDetailView,
    RelNotificationListCreateView,
    RelOrderDetailView,
    RelOrderListCreateView,
    RelRegisterView,
    RelStatusDetailView,
    RelStatusListCreateView,
    RelTicketDetailView,
    RelTicketListCreateView,
    RelTicketTypeDetailView,
    RelTicketTypeListCreateView,
)

urlpatterns = [
    # register
    path('api/v1/obj-rel/auth/register/', ObjRelRegister.as_view(), name='obj_rel_register'),
    path('api/v1/rel/auth/register/', RelRegisterView.as_view(), name='rel_register'),
    path('api/v1/nosql/auth/register/', NosqlRegisterView.as_view(), name="nosql_register"),

    # login
    path('api/v1/obj-rel/auth/login/', ObjRelLogin.as_view(), name='obj_rel_login'),
    path('api/v1/rel/auth/login/', RelLoginView.as_view(), name='rel_login'),
    path("api/v1/nosql/auth/login/", NosqlLoginView.as_view(), name="nosql_login"),

    # discounts
    path('api/v1/obj-rel/discounts/', DiscountObjListCreateView.as_view(), name='obj_rel_discounts'),
    path('api/v1/rel/discounts/', RelDiscountListCreateView.as_view(), name='rel_discounts'),
    path('api/v1/nosql/discounts/', NosqlDiscountListCreateView.as_view()),

    # discounts id
    path("api/v1/obj-rel/discounts/<int:id>/", DiscountObjDetailView.as_view(), name="obj_rel_discounts_id"),
    path('api/v1/rel/discounts/<int:pk>/', RelDiscountDetailView.as_view(), name='rel_discount_detail'),
    path('api/v1/nosql/discounts/<str:id>/', NosqlDiscountDetailView.as_view()),
    path('', views.home, name='home'),
    path('select_database/', views.select_database, name='select_database'),

path('api/nosql/events/', nosql_events_list, name='nosql-events-list'),
    path('api/nosql/users/', nosql_users_list, name='nosql-users-list'),
    path('api/nosql/orders/', nosql_orders_list, name='nosql-orders-list'),
    path('api/nosql/notifications/', nosql_notifications_list, name='nosql-notifications-list'),
    path('api/nosql/messages/', nosql_messages_list, name='nosql-messages-list'),
    path('api/nosql/discounts/', NosqlDiscountListCreateView.as_view(), name='nosql-discounts-list-create'),
    path('api/nosql/discounts/<str:pk>/', NosqlDiscountDetailView.as_view(), name='nosql-discounts-detail'),
    path('api/nosql/event-types/', NosqlEventTypeListCreateView.as_view(), name='nosql-event-types'),
    path('api/nosql/seat-types/', NosqlSeatTypeListCreateView.as_view(), name='nosql-seat-types'),
    path('api/nosql/ticket-types/', NosqlTicketTypeListCreateView.as_view(), name='nosql-ticket-types'),
    path('api/nosql/statuses/', NosqlStatusListCreateView.as_view(), name='nosql-statuses'),
    path('api/nosql/events/manage/', NosqlEventListCreateView.as_view(), name='nosql-events-manage'),

    # register
    path(
        "api/v1/obj-rel/auth/register/",
        ObjRelRegister.as_view(),
        name="obj_rel_register",
    ),
    path("api/v1/rel/auth/register/", RelRegisterView.as_view(), name="rel_register"),
    # login
    path("api/v1/obj-rel/auth/login/", ObjRelLogin.as_view(), name="obj_rel_login"),
    path("api/v1/rel/auth/login/", RelLoginView.as_view(), name="rel_login"),
    # discounts
    path(
        "api/v1/obj-rel/discounts/",
        DiscountObjListCreateView.as_view(),
        name="obj_rel_discounts",
    ),
    path(
        "api/v1/rel/discounts/",
        RelDiscountListCreateView.as_view(),
        name="rel_discounts",
    ),
    # discounts id
    path(
        "api/v1/obj-rel/discounts/<int:pk>/",
        DiscountObjDetailView.as_view(),
        name="obj_rel_discounts_id",
    ),
    path(
        "api/v1/rel/discounts/<int:pk>/",
        RelDiscountDetailView.as_view(),
        name="rel_discount_detail",
    ),
    # ticket-types
    path('api/v1/obj-rel/ticket-types/', TicketTypeObjListCreateView.as_view(), name='obj_rel_ticket_types'),
    path('api/v1/rel/ticket-types/', RelTicketTypeListCreateView.as_view(), name='rel_ticket_types'),
    path('api/v1/nosql/ticket-types/', NosqlTicketTypeListCreateView.as_view()),

    path(
        "api/v1/obj-rel/ticket-types/",
        TicketTypeObjListCreateView.as_view(),
        name="obj_rel_ticket_types",
    ),
    path(
        "api/v1/rel/ticket-types/",
        RelTicketTypeListCreateView.as_view(),
        name="rel_ticket_types",
    ),
    # ticket-types id
    path('api/v1/obj-rel/ticket-types/<int:id>/', TicketTypeObjDetailView.as_view(), name='obj_rel_ticket_types_id'),
    path('api/v1/rel/ticket-types/<int:pk>/', RelTicketTypeDetailView.as_view(), name='rel_ticket_type_detail'),
    path('api/v1/nosql/ticket-types/<str:id>/', NosqlTicketTypeDetailView.as_view()),

    path(
        "api/v1/obj-rel/ticket-types/<int:pk>/",
        TicketTypeObjDetailView.as_view(),
        name="obj_rel_ticket_types_id",
    ),
    path(
        "api/v1/rel/ticket-types/<int:pk>/",
        RelTicketTypeDetailView.as_view(),
        name="rel_ticket_type_detail",
    ),
    # statuses
    path('api/v1/obj-rel/statuses/', StatusObjListCreateView.as_view(), name='obj_rel_statuses'),
    path('api/v1/rel/statuses/', RelStatusListCreateView.as_view(), name='rel_statuses'),
    path('api/v1/nosql/statuses/', NosqlStatusListCreateView.as_view()),

    path(
        "api/v1/obj-rel/statuses/",
        StatusObjListCreateView.as_view(),
        name="obj_rel_statuses",
    ),
    path(
        "api/v1/rel/statuses/", RelStatusListCreateView.as_view(), name="rel_statuses"
    ),
    # statuses id
    path('api/v1/obj-rel/statuses/<int:id>/', StatusObjDetailView.as_view(), name='obj_rel_statuses_id'),
    path('api/v1/rel/statuses/<int:pk>/', RelStatusDetailView.as_view(), name='rel_status_detail'),
    path('api/v1/nosql/statuses/<str:id>/', NosqlStatusDetailView.as_view()),

    path(
        "api/v1/obj-rel/statuses/<int:pk>/",
        StatusObjDetailView.as_view(),
        name="obj_rel_statuses_id",
    ),
    path(
        "api/v1/rel/statuses/<int:pk>/",
        RelStatusDetailView.as_view(),
        name="rel_status_detail",
    ),
    # event-type
    path('api/v1/obj-rel/event-types/', EventTypeObjListCreateView.as_view(), name='obj_rel_event_types'),
    path('api/v1/rel/event-types/', RelEventTypeListCreateView.as_view(), name='rel_event_types'),
    path('api/v1/nosql/event-types/', NosqlEventTypeListCreateView.as_view()),

    path(
        "api/v1/obj-rel/event-types/",
        EventTypeObjListCreateView.as_view(),
        name="obj_rel_event_types",
    ),
    path(
        "api/v1/rel/event-types/",
        RelEventTypeListCreateView.as_view(),
        name="rel_event_types",
    ),
    # event-type id
    path('api/v1/obj-rel/event-types/<int:id>/', EventTypeObjDetailView.as_view(), name='obj_rel_event_types_id'),
    path('api/v1/rel/event-types/<int:pk>/', RelEventTypeDetailView.as_view(), name='rel_event_type_detail'),
    path('api/v1/nosql/event-types/<str:id>/', NosqlEventTypeDetailView.as_view()),

    path(
        "api/v1/obj-rel/event-types/<int:pk>/",
        EventTypeObjDetailView.as_view(),
        name="obj_rel_event_types_id",
    ),
    path(
        "api/v1/rel/event-types/<int:pk>/",
        RelEventTypeDetailView.as_view(),
        name="rel_event_type_detail",
    ),
    # messages
    path('api/v1/obj-rel/messages/', MessageListCreateView.as_view(), name='obj_rel_messages'),
    path('api/v1/rel/messages/', RelMessageListCreateView.as_view(), name="rel_messages"),
    path('api/v1/nosql/messages/', NosqlMessageListCreateView.as_view()),

    #messages all
    path('api/v1/obj-rel/messages/all/', MessageAllListView.as_view(), name='obj_rel_messages_all'),
    path('api/v1/nosql/messages/all/', NosqlMessageAllListView.as_view()),

    path(
        "api/v1/obj-rel/messages/",
        MessageListCreateView.as_view(),
        name="obj_rel_messages",
    ),
    path(
        "api/v1/rel/messages/", RelMessageListCreateView.as_view(), name="rel_messages"
    ),
    # messages all
    path(
        "api/v1/obj-rel/messages/all/",
        MessageAllListView.as_view(),
        name="obj_rel_messages_all",
    ),
    path(
        "api/v1/rel/messages/all/",
        RelMessageAllListView.as_view(),
        name="obj_rel_messages_all",
    ),
    # messages id
    path('api/v1/obj-rel/messages/<int:id>/', MessageDetailView.as_view(), name='obj_rel_message_detail'),
    path('api/v1/rel/messages/<int:pk>/', RelMessageDetailView.as_view(), name="rel_message_detail"),
    path('api/v1/nosql/messages/<str:id>/', NosqlMessageDetailView.as_view()),

    path(
        "api/v1/obj-rel/messages/<int:pk>/",
        MessageDetailView.as_view(),
        name="obj_rel_message_detail",
    ),
    path(
        "api/v1/rel/messages/<int:pk>/",
        RelMessageDetailView.as_view(),
        name="rel_message_detail",
    ),
    # notifications
    path('api/v1/obj-rel/notifications/', NotificationListCreateView.as_view(), name='obj_rel_notifications'),
    path('api/v1/rel/notifications/', RelNotificationListCreateView.as_view(), name="rel_notifications"),
    path('api/v1/nosql/notifications/', NosqlNotificationListCreateView.as_view()),


    path(
        "api/v1/obj-rel/notifications/",
        NotificationListCreateView.as_view(),
        name="obj_rel_notifications",
    ),
    path(
        "api/v1/rel/notifications/",
        RelNotificationListCreateView.as_view(),
        name="rel_notifications",
    ),
    # notifications id
    path('api/v1/obj-rel/notifications/<int:id>/', NotificationDetailView.as_view(),
         name='obj_rel_notification_detail'),
    path('api/v1/rel/notifications/<int:pk>/', RelNotificationDetailView.as_view(), name="rel_notification_detail"),
    path('api/v1/nosql/notifications/<str:id>/', NosqlNotificationDetailView.as_view()),

    path(
        "api/v1/obj-rel/notifications/<int:pk>/",
        NotificationDetailView.as_view(),
        name="obj_rel_notification_detail",
    ),
    path(
        "api/v1/rel/notifications/<int:pk>/",
        RelNotificationDetailView.as_view(),
        name="rel_notification_detail",
    ),
    # events
    path('api/v1/obj-rel/events/', EventListCreateView.as_view(), name='obj_rel_events'),
    path('api/v1/rel/events/', RelEventListCreateView.as_view(), name="rel_events"),
    path('api/v1/nosql/events/', NosqlEventListCreateView.as_view()),

    path(
        "api/v1/obj-rel/events/", EventListCreateView.as_view(), name="obj_rel_events"
    ),
    path("api/v1/rel/events/", RelEventListCreateView.as_view(), name="rel_events"),
    # events id
    path('api/v1/obj-rel/events/<int:id>/', EventDetailView.as_view(), name='obj_rel_event_detail'),
    path('api/v1/rel/events/<int:pk>/', RelEventDetailView.as_view(), name="rel_event_detail"),
    path('api/v1/nosql/events/<str:id>/', NosqlEventDetailView.as_view()),

    path(
        "api/v1/obj-rel/events/<int:pk>/",
        EventDetailView.as_view(),
        name="obj_rel_event_detail",
    ),
    path(
        "api/v1/rel/events/<int:pk>/",
        RelEventDetailView.as_view(),
        name="rel_event_detail",
    ),
    # tickets
    path('api/v1/obj-rel/tickets/', TicketListCreateView.as_view(), name='obj_rel_tickets'),
    path('api/v1/nosql/tickets/', NosqlTicketListCreateView.as_view()),

    path(
        "api/v1/obj-rel/tickets/",
        TicketListCreateView.as_view(),
        name="obj_rel_tickets",
    ),
    path("api/v1/rel/tickets/", RelTicketListCreateView.as_view(), name="rel_tickets"),
    # tickets id
    path('api/v1/obj-rel/tickets/<int:id>/', TicketDetailView.as_view(), name='obj_rel_ticket_detail'),
    path('api/v1/nosql/tickets/<str:id>/', NosqlTicketDetailView.as_view()),

    path(
        "api/v1/obj-rel/tickets/<int:pk>/",
        TicketDetailView.as_view(),
        name="obj_rel_ticket_detail",
    ),
    path(
        "api/v1/rel/tickets/<int:pk>/",
        RelTicketDetailView.as_view(),
        name="rel_ticket_detail",
    ),
    # orders
    path('api/v1/obj-rel/orders/', OrderListCreateView.as_view(), name='obj_rel_orders'),
    path('api/v1/nosql/orders/', NosqlOrderListCreateView.as_view()),

    path(
        "api/v1/obj-rel/orders/", OrderListCreateView.as_view(), name="obj_rel_orders"
    ),
    path("api/v1/rel/orders/", RelOrderListCreateView.as_view(), name="rel_orders"),
    # orders id
    path('api/v1/obj-rel/orders/<int:id>/', OrderDetailView.as_view(), name='obj_rel_order_detail'),
    path('api/v1/nosql/orders/<str:id>/', NosqlOrderDetailView.as_view()),
    path(
        "api/v1/obj-rel/orders/<int:pk>/",
        OrderDetailView.as_view(),
        name="obj_rel_order_detail",
    ),
    path(
        "api/v1/rel/orders/<int:pk>/",
        RelOrderDetailView.as_view(),
        name="rel_order_detail",
    ),
    # obj
    path("api/v1/obj/auth/register/", ObjRegister.as_view(), name="obj_register"),
    path("api/v1/obj/auth/login/", ObjLogin.as_view(), name="obj_login"),
    path(
        "api/v1/obj/discounts/",
        ObjDiscountsListCreateView.as_view(),
        name="obj_discounts",
    ),
    path(
        "api/v1/obj/discounts/<int:id>/",
        ObjDiscountsDetailView.as_view(),
        name="obj_discounts_id",
    ),
    path(
        "api/v1/obj/events/",
        ObjEventListCreateView.as_view(),
        name="obj_event_list_create",
    ),
    path(
        "api/v1/obj/events/<int:pk>/",
        ObjEventDetailView.as_view(),
        name="obj_event_detail",
    ),
    path(
        "api/v1/obj/tickets/",
        ObjTicketListCreateView.as_view(),
        name="obj_ticket_list_create",
    ),
    path("api/v1/obj/orders/", ObjUserOrderListView.as_view(), name="obj_user_orders"),
    path(
        "api/v1/obj/orders/create/",
        ObjOrderCreateView.as_view(),
        name="obj_order_create",
    ),
    path(
        "api/v1/obj/notifications/",
        ObjUserNotificationListView.as_view(),
        name="obj_notifications",
    ),
    path(
        "api/v1/obj/notifications/<int:pk>/read/",
        ObjUserNotificationListView.as_view(),
        name="obj_notification_read",
    ),
    path(
        "api/v1/obj/messages/",
        ObjUserMessageListCreateView.as_view(),
        name="obj_messages",
    ),
    path(
        "api/v1/obj/statuses/", ObjStatusListCreateView.as_view(), name="obj_statuses"
    ),
    path(
        "api/v1/obj/statuses/<int:pk>/",
        ObjStatusDetailView.as_view(),
        name="obj_statuses_id",
    ),
    path(
        "api/v1/obj/event-types/",
        ObjEventTypeListCreateView.as_view(),
        name="obj_event_types",
    ),
    path(
        "api/v1/obj/event-types/<int:pk>/",
        ObjEventTypeDetailView.as_view(),
        name="obj_event_types_id",
    ),
    path(
        "api/v1/obj/ticket-types/",
        ObjTicketTypeListCreateView.as_view(),
        name="obj_ticket_types",
    ),
    path(
        "api/v1/obj/ticket-types/<int:pk>/",
        ObjTicketTypeDetailView.as_view(),
        name="obj_ticket_types_id",
    ),
    path(
        "api/v1/obj/messages/",
        ObjUserMessageListCreateView.as_view(),
        name="obj_messages",
    ),
    path(
        "api/v1/obj/messages/all/",
        ObjUserMessageListCreateView.as_view(),
        name="obj_messages_all",
    ),
]

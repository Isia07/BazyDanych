from django.urls import path

from EventTickets.objective_relational.views import (
    DiscountObjDetailView,
    DiscountObjListCreateView,
    EventDetailView,
    EventListCreateView,
    EventTypeObjDetailView,
    EventTypeObjListCreateView,
    OrderCreateView,
    SeatTypeObjDetailView,
    SeatTypeObjListCreateView,
    StatusObjDetailView,
    StatusObjListCreateView,
    TicketListCreateView,
    TicketTypeObjDetailView,
    TicketTypeObjListCreateView,
    UserMessageListCreateView,
    UserNotificationListView,
    UserOrderListView,
)
from EventTickets.objective_relational.views import (
    LoginView as ObjRelLogin,
)
from EventTickets.objective_relational.views import (
    RegisterView as ObjRelRegister,
)

from .objective.views import DiscountsDetailView as ObjDiscountsDetailView
from .objective.views import DiscountsListCreateView as ObjDiscountsListCreateView
from .objective.views import EventDetailView as ObjEventDetailView
from .objective.views import EventListCreateView as ObjEventListCreateView
from .objective.views import LoginView as ObjLogin
from .objective.views import OrderCreateView as ObjOrderCreateView
from .objective.views import RegisterView as ObjRegister
from .objective.views import TicketListCreateView as ObjTicketListCreateView
from .objective.views import UserMessageListCreateView as ObjUserMessageListCreateView
from .objective.views import UserNotificationListView as ObjUserNotificationListView
from .objective.views import UserOrderListView as ObjUserOrderListView
from .relational.views import (
    DiscountDetailView,
    DiscountListCreateView,
    RelLoginView,
    RelRegisterView,
)

urlpatterns = [
    path(
        "api/v1/obj-rel/auth/register",
        ObjRelRegister.as_view(),
        name="obj_rel_register",
    ),
    path("api/v1/obj-rel/auth/login", ObjRelLogin.as_view(), name="obj_rel_login"),
    path("api/v1/rel/auth/register", RelRegisterView.as_view(), name="rel_register"),
    path("api/v1/rel/auth/login", RelLoginView.as_view(), name="rel_login"),
    path(
        "api/v1/rel/discounts/",
        DiscountListCreateView.as_view(),
        name="discount_list_create",
    ),
    path(
        "api/v1/rel/discounts/<int:pk>/",
        DiscountDetailView.as_view(),
        name="discount_detail",
    ),
    path(
        "api/v1/obj-rel/discounts/",
        DiscountObjListCreateView.as_view(),
        name="obj_rel_discounts",
    ),
    path(
        "api/v1/obj-rel/discounts/<int:id>/",
        DiscountObjDetailView.as_view(),
        name="obj_rel_discounts_id",
    ),
    path(
        "api/v1/obj-rel/event-types/",
        EventTypeObjListCreateView.as_view(),
        name="obj_rel_event_types",
    ),
    path(
        "api/v1/obj-rel/event-types/<int:id>/",
        EventTypeObjDetailView.as_view(),
        name="obj_rel_event_types_id",
    ),
    path(
        "api/v1/obj-rel/seat-types/",
        SeatTypeObjListCreateView.as_view(),
        name="obj_rel_seat_types",
    ),
    path(
        "api/v1/obj-rel/seat-types/<int:id>/",
        SeatTypeObjDetailView.as_view(),
        name="obj_rel_seat_types_id",
    ),
    path(
        "api/v1/obj-rel/statuses/",
        StatusObjListCreateView.as_view(),
        name="obj_rel_statuses",
    ),
    path(
        "api/v1/obj-rel/statuses/<int:id>/",
        StatusObjDetailView.as_view(),
        name="obj_rel_statuses_id",
    ),
    path(
        "api/v1/obj-rel/ticket-types/",
        TicketTypeObjListCreateView.as_view(),
        name="obj_rel_ticket_types",
    ),
    path(
        "api/v1/obj-rel/ticket-types/<int:id>/",
        TicketTypeObjDetailView.as_view(),
        name="obj_rel_ticket_types_id",
    ),
    path(
        "api/v1/obj-rel/events",
        EventListCreateView.as_view(),
        name="obj_rel_event_list_create",
    ),
    path(
        "api/v1/obj-rel/events/<int:pk>",
        EventDetailView.as_view(),
        name="obj_rel_event_detail",
    ),
    path(
        "api/v1/obj-rel/tickets",
        TicketListCreateView.as_view(),
        name="obj_rel_ticket_list_create",
    ),
    path(
        "api/v1/obj-rel/orders", UserOrderListView.as_view(), name="obj_rel_user_orders"
    ),
    path(
        "api/v1/obj-rel/orders/create",
        OrderCreateView.as_view(),
        name="obj_rel_order_create",
    ),
    path(
        "api/v1/obj-rel/notifications",
        UserNotificationListView.as_view(),
        name="obj_rel_notifications",
    ),
    path(
        "api/v1/obj-rel/notifications/<int:pk>/read",
        UserNotificationListView.as_view(),
        name="obj_rel_notification_read",
    ),
    path(
        "api/v1/obj-rel/messages",
        UserMessageListCreateView.as_view(),
        name="obj_rel_messages",
    ),
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
]

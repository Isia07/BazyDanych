from django.urls import path
from EventTickets.objective_relational.views import RegisterView as ObjRelRegister, LoginView as ObjRelLogin
from .relational.views import RelRegisterView, RelLoginView, RelDiscountListCreateView, RelDiscountDetailView, \
    RelTicketTypeListCreateView, RelTicketTypeDetailView, RelStatusListCreateView, RelStatusDetailView, \
    RelEventTypeListCreateView, RelEventTypeDetailView

urlpatterns = [
    path('api/v1/obj-rel/auth/register', ObjRelRegister.as_view(), name='obj_rel_register'),
    path('api/v1/obj-rel/auth/login', ObjRelLogin.as_view(), name='obj_rel_login'),

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

]
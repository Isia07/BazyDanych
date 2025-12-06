from django.urls import path
from EventTickets.objective_relational.views import RegisterView as ObjRelRegister, LoginView as ObjRelLogin
from EventTickets.relational.views import RelRegisterView, RelLoginView, DiscountListCreateView, DiscountDetailView

urlpatterns = [
    path('api/v1/obj-rel/auth/register', ObjRelRegister.as_view(), name='obj_rel_register'),
    path('api/v1/obj-rel/auth/login', ObjRelLogin.as_view(), name='obj_rel_login'),
    path('api/v1/rel/auth/register', RelRegisterView.as_view(), name='rel_register'),
    path('api/v1/rel/auth/login', RelLoginView.as_view(), name='rel_login'),
    path('api/v1/rel/discounts/', DiscountListCreateView.as_view(), name='discount_list_create'),
    path('api/v1/rel/discounts/<int:pk>/', DiscountDetailView.as_view(), name='discount_detail'),

]
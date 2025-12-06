from django.urls import path
from . import views
from EventTickets.objective_relational.views import RegisterView as ObjRelRegister, LoginView as ObjRelLogin


urlpatterns = [
    path('', views.home, name='home'),

    path('api/v1/obj-rel/auth/register', ObjRelRegister.as_view(), name='obj_rel_register'),
    path('api/v1/obj-rel/auth/login', ObjRelLogin.as_view(), name='obj_rel_login'),
]
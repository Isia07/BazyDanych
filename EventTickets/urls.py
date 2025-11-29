from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('select_database/', views.select_database, name='select_database'),

]
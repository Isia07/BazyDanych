from django.shortcuts import render
from EventTickets.shared.views import BaseRegisterView, BaseLoginView, LogoutView


class RegisterView(BaseRegisterView):
    database = 'objective_relational'

class LoginView(BaseLoginView):
    database = 'objective_relational'

class ObjRelLogoutView(LogoutView):
    database = 'objective_relational'
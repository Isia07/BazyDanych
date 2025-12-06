from django.shortcuts import render
from EventTickets.shared.views import BaseRegisterView, BaseLoginView, LogoutView


class RelRegisterView(BaseRegisterView):
    database = 'relational'

class RelLoginView(BaseLoginView):
    database = 'relational'

class RelLogoutView(LogoutView):
    database = 'relational'
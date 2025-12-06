from django.shortcuts import render
from EventTickets.shared.views import BaseRegisterView, BaseLoginView

class RelRegisterView(BaseRegisterView):
    database = 'relational'

class RelLoginView(BaseLoginView):
    database = 'relational'
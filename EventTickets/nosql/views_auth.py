from EventTickets.shared.views import BaseRegisterView, BaseLoginView

class NosqlRegisterView(BaseRegisterView):
    database = "relational"   # albo "default" jeśli default = relational

class NosqlLoginView(BaseLoginView):
    database = "relational"   # albo "default"

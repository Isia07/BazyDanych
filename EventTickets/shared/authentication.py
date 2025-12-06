from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from rest_framework.authentication import TokenAuthentication


class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=username or kwargs.get('email'))
            if user.check_password(password):
                return user
        except user_model.DoesNotExist:
            return None

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None


class CookieTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('auth_token')
        if not token:
            return None

        return self.authenticate_credentials(token)


from django.contrib.auth.backends import BaseBackend
from django.db.models import Q
from account.models import CustomUser


class PhoneAuthentication(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = CustomUser.object.get(Q(phone=username) | Q(email=username))
            if user.check_password(password):
                return user
            return None
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.object.get(id=user_id)
        except CustomUser.DoesNotExist:
            return None

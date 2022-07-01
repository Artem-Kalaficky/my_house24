from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from .models import UserProfile


class CustomerBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        user_id = kwargs['username']
        password = kwargs['password']
        try:
            customer = UserProfile.objects.get(user_id=user_id)
            if customer.check_password(password) is True:
                return customer
        except UserProfile.DoesNotExist:
            pass


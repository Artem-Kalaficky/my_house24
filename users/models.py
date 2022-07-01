from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models


class UserProfile(AbstractBaseUser, PermissionsMixin):
    pass

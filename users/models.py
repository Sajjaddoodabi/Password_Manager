from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email_active_code = models.CharField(max_length=200, verbose_name=_('email active code'))

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return f'{self.username} - {self.email} - {self.is_active}'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

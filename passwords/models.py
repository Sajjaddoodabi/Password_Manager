from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User


class Passwords(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    site_url = models.URLField(max_length=200, verbose_name=_('site_url'))
    site_name = models.CharField(max_length=50, verbose_name=_('site_name'))
    username = models.CharField(max_length=200, verbose_name=_('username'))
    email = models.EmailField(max_length=200, verbose_name=_('email'))
    password = models.CharField(max_length=50, verbose_name=_('password'))
    date_created = models.DateTimeField(auto_now_add=True)
    last_date_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.site_name}'

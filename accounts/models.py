from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# Create your models here.


class User(AbstractUser):
    access_key = models.CharField(max_length=100, blank=True)
    secret_key = models.CharField(max_length=100, blank=True)
    bot_token = models.CharField(max_length=100, blank=True)
    trade_method = models.TextField(blank=True, verbose_name="추가하고 싶은 매매기법")
    groups = models.ManyToManyField(
        Group,
        related_name="%(app_label)s_%(class)s_related",
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="%(app_label)s_%(class)s_related",
        blank=True,
    )

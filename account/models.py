from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from account.managers import UserManager


class GlobalPermissions(models.Model):
    class Meta:
        managed = False
        permissions = ()


class User(AbstractUser, PermissionsMixin):
    username = models.CharField(
        db_column="tx_usuario", null=False, max_length=64, unique=True
    )
    password = models.CharField(db_column="tx_senha", null=False, max_length=104)
    name = models.CharField(db_column="tx_nome", null=True, max_length=256)
    email = models.CharField(db_column="tx_email", null=True, max_length=256)
    last_login = models.CharField(db_column="dt_ultimo_login", null=True)
    is_active = models.BooleanField(db_column="cs_ativo", null=False, default=True)
    is_superuser = models.BooleanField(
        db_column="cs_super_usuario", null=True, default=False
    )
    is_staff = models.BooleanField(db_column="cs_suporte", null=True, default=False)
    is_default = models.BooleanField(db_column="cs_padrao", null=False, default=False)
    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        verbose_name = "users"
        verbose_name_plural = "users"
        db_table = "users"

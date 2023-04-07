from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager

# Create your models here.


class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=15, unique=False, null=False, blank=False)
    email = models.EmailField(
        _("email address"),
        unique=True,
        help_text=_("Enter email address for unique identification"),
    )
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "name",
    ]

    objects = CustomUserManager()

    def __str__(self):
        return f"Email: {self.email}"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

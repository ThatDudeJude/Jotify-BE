from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager that uses email as the unique identifier
    """

    def _create_user(
        self, email, password, name, is_staff, is_superuser, **extra_fields
    ):
        """
        Create a user with fields email and password
        """
        if not email:
            raise ValueError(_("You must provide an email"))
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, name, **extra_fields):
        """
        Create user method. By default, is_staff=False and is_superuser=False
        """
        return self._create_user(email, password, name, False, False, **extra_fields)

    def create_superuser(
        self, email, password, name, is_staff=True, is_superuser=True, **extra_fields
    ):
        """
        Create Superuser method. Checks if is_staff=True and is_superuser=True
        """
        if is_staff is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if is_superuser is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self._create_user(
            email, password, name, is_staff, is_superuser, **extra_fields
        )

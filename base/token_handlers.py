from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timezone, timedelta
from rest_framework.authtoken.models import Token


def get_time_elapsed_since_token_creation(token):
    return datetime.now(tz=timezone.utc) - token.created


def get_token_time_left(token):
    return timedelta(
        seconds=settings.TOKEN_EXPIRY_DELAY
    ) - get_time_elapsed_since_token_creation(token)


def check_if_token_expired(token):
    return get_token_time_left(token) < timedelta(seconds=0)


def get_token_on_login(user):
    try:
        token = Token.objects.get(user=user)
        token_has_expired = check_if_token_expired(token)
        if token_has_expired:
            token.delete()
            token = Token.objects.create(user=user)
        return token
    except ObjectDoesNotExist:
        token = Token.objects.get_or_create(user=user)
        return token
